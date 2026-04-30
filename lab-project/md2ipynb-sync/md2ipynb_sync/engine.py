"""
核心同步引擎 - 基于 Jupytext 的 MD↔IPYNB 双向同步逻辑
"""

import os
import json
import time
import shutil
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from enum import Enum
from typing import List, Optional, Dict, Tuple, Callable

import jupytext
from nbformat import validate
from nbformat.v4 import new_notebook, nbformat_minor

logger = logging.getLogger(__name__)


class PairStatus(Enum):
    """配对状态"""
    UNPAIRED = "unpaired"        # md 存在，ipynb 不存在
    PAIRED = "paired"            # 已配对，无冲突
    MD_NEWER = "md_newer"        # md 更新（需同步到 ipynb）
    IPYNB_NEWER = "ipynb_newer"  # ipynb 更新（需同步到 md）
    CONFLICT = "conflict"        # 双方都有改动，需手动解决
    ERROR = "error"              # 同步出错


@dataclass
class MDFileInfo:
    """MD 文件信息"""
    md_path: str                   # md 绝对路径
    ipynb_path: str                # 对应 ipynb 绝对路径
    rel_path: str                  # 相对于源目录的路径
    status: PairStatus = PairStatus.UNPAIRED
    md_mtime: float = 0.0          # md 修改时间
    ipynb_mtime: float = 0.0       # ipynb 修改时间
    last_sync_time: float = 0.0    # 上次同步时间
    error_msg: str = ""            # 错误信息

    @property
    def status_display(self) -> str:
        """状态显示文本"""
        mapping = {
            PairStatus.UNPAIRED: "未配对",
            PairStatus.PAIRED: "已配对",
            PairStatus.MD_NEWER: "MD 已更新",
            PairStatus.IPYNB_NEWER: "Notebook 已更新",
            PairStatus.CONFLICT: "⚠️ 冲突",
            PairStatus.ERROR: "❌ 错误",
        }
        return mapping.get(self.status, str(self.status))

    @property
    def status_icon(self) -> str:
        """状态图标"""
        mapping = {
            PairStatus.UNPAIRED: "⬜",
            PairStatus.PAIRED: "✅",
            PairStatus.MD_NEWER: "🟡",
            PairStatus.IPYNB_NEWER: "🔵",
            PairStatus.CONFLICT: "🔴",
            PairStatus.ERROR: "❌",
        }
        return mapping.get(self.status, "❓")


@dataclass
class SyncResult:
    """同步操作结果"""
    success: bool
    md_path: str
    ipynb_path: str
    direction: str = ""       # "md→ipynb" 或 "ipynb→md"
    message: str = ""
    duration: float = 0.0


@dataclass
class BatchResult:
    """批量操作结果"""
    total: int = 0
    success: int = 0
    skipped: int = 0
    failed: int = 0
    conflicted: int = 0
    results: List[SyncResult] = field(default_factory=list)

    @property
    def summary(self) -> str:
        return (
            f"总计 {self.total} 个文件 | "
            f"成功 {self.success} | "
            f"跳过 {self.skipped} | "
            f"冲突 {self.conflicted} | "
            f"失败 {self.failed}"
        )


class SyncEngine:
    """核心同步引擎"""

    META_FILE = ".md2ipynb_meta.json"  # 同步元数据文件名

    def __init__(self, source_dir: str, output_dir: str, fmt: str = "myst"):
        """
        初始化同步引擎

        Args:
            source_dir: Obsidian md 文件源目录
            output_dir: ipynb 统一输出目录
            fmt: Jupytext 格式，默认 myst
        """
        self.source_dir = Path(source_dir).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.fmt = fmt
        self._meta: Dict[str, dict] = {}  # rel_path -> metadata
        self._file_cache: Dict[str, MDFileInfo] = {}  # rel_path -> info
        self._load_meta()

    # ==================== 扫描与状态 ====================

    def scan(self) -> List[MDFileInfo]:
        """
        扫描源目录，返回所有 md 文件的状态信息

        Returns:
            文件信息列表
        """
        files = []
        self._file_cache.clear()

        for md_path in self._walk_md_files():
            rel_path = md_path.relative_to(self.source_dir)
            ipynb_path = self.output_dir / rel_path.with_suffix(".ipynb")

            info = MDFileInfo(
                md_path=str(md_path),
                ipynb_path=str(ipynb_path),
                rel_path=str(rel_path),
            )

            # 获取修改时间
            if md_path.exists():
                info.md_mtime = md_path.stat().st_mtime
            if ipynb_path.exists():
                info.ipynb_mtime = ipynb_path.stat().st_mtime

            # 判断状态
            info.status = self._compute_status(info)
            info.last_sync_time = self._meta.get(str(rel_path), {}).get("last_sync", 0.0)

            self._file_cache[str(rel_path)] = info
            files.append(info)

        return files

    def get_file_info(self, rel_path: str) -> Optional[MDFileInfo]:
        """获取单个文件信息"""
        return self._file_cache.get(rel_path)

    def get_status_summary(self) -> Dict[str, int]:
        """获取状态统计"""
        summary = {}
        for info in self._file_cache.values():
            key = info.status.value
            summary[key] = summary.get(key, 0) + 1
        return summary

    def _compute_status(self, info: MDFileInfo) -> PairStatus:
        """计算配对状态"""
        md_exists = Path(info.md_path).exists()
        ipynb_exists = Path(info.ipynb_path).exists()

        if not md_exists:
            return PairStatus.ERROR

        if not ipynb_exists:
            return PairStatus.UNPAIRED

        # 双方都存在，检查是否有改动
        last_sync = self._meta.get(info.rel_path, {}).get("last_sync", 0.0)

        if last_sync == 0.0:
            # 从未同步过但文件都存在 - 视为冲突
            return PairStatus.PAIRED  # 首次视为已配对

        md_changed = info.md_mtime > last_sync
        ipynb_changed = info.ipynb_mtime > last_sync

        if md_changed and ipynb_changed:
            return PairStatus.CONFLICT
        elif md_changed:
            return PairStatus.MD_NEWER
        elif ipynb_changed:
            return PairStatus.IPYNB_NEWER
        else:
            return PairStatus.PAIRED

    def _walk_md_files(self) -> List[Path]:
        """遍历源目录下所有 md 文件"""
        md_files = []
        for root, dirs, files in os.walk(self.source_dir):
            # 跳过隐藏目录和 Obsidian 特殊目录
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for f in files:
                if f.endswith(".md") and not f.startswith("."):
                    md_files.append(Path(root) / f)
        return sorted(md_files)

    # ==================== 配对与同步 ====================

    def create_pair(self, rel_path: str) -> SyncResult:
        """
        为单个 md 文件创建配对的 ipynb

        Args:
            rel_path: 相对于源目录的路径

        Returns:
            同步结果
        """
        start_time = time.time()
        info = self._file_cache.get(rel_path)

        if info is None:
            return SyncResult(
                success=False,
                md_path="",
                ipynb_path="",
                message=f"文件信息未找到: {rel_path}",
            )

        try:
            md_path = Path(info.md_path)
            ipynb_path = Path(info.ipynb_path)

            # 确保输出目录存在
            ipynb_path.parent.mkdir(parents=True, exist_ok=True)

            # 使用 jupytext 读取 md 文件
            nb = jupytext.read(str(md_path), fmt={"extension": ".md", "format_name": self.fmt})

            # 添加 jupytext 配对元数据
            self._set_pair_metadata(nb, md_path)

            # 写入 ipynb
            jupytext.write(nb, str(ipynb_path))

            # 更新元数据
            now = time.time()
            self._meta[rel_path] = {
                "last_sync": now,
                "md_mtime": md_path.stat().st_mtime,
                "ipynb_mtime": ipynb_path.stat().st_mtime,
            }
            self._save_meta()

            # 更新缓存
            info.status = PairStatus.PAIRED
            info.last_sync_time = now
            info.ipynb_mtime = ipynb_path.stat().st_mtime

            duration = time.time() - start_time
            return SyncResult(
                success=True,
                md_path=str(md_path),
                ipynb_path=str(ipynb_path),
                direction="md→ipynb",
                message=f"配对创建成功 ({duration:.2f}s)",
                duration=duration,
            )

        except Exception as e:
            logger.error(f"创建配对失败 {rel_path}: {e}")
            info.status = PairStatus.ERROR
            info.error_msg = str(e)
            return SyncResult(
                success=False,
                md_path=info.md_path,
                ipynb_path=info.ipynb_path,
                direction="md→ipynb",
                message=f"创建配对失败: {e}",
            )

    def sync_to_ipynb(self, rel_path: str, force: bool = False) -> SyncResult:
        """
        将 md 的改动同步到 ipynb

        Args:
            rel_path: 相对路径
            force: 是否强制同步（忽略冲突检查）
        """
        start_time = time.time()
        info = self._file_cache.get(rel_path)

        if info is None:
            return SyncResult(False, "", "", message=f"文件信息未找到: {rel_path}")

        if not force and info.status == PairStatus.CONFLICT:
            return SyncResult(
                False, info.md_path, info.ipynb_path,
                message="存在冲突，请先解决冲突或使用强制同步",
            )

        try:
            md_path = Path(info.md_path)
            ipynb_path = Path(info.ipynb_path)

            # 读取 md 并转换为 notebook
            nb = jupytext.read(str(md_path), fmt={"extension": ".md", "format_name": self.fmt})
            self._set_pair_metadata(nb, md_path)
            jupytext.write(nb, str(ipynb_path))

            # 更新元数据
            now = time.time()
            self._meta[rel_path] = {
                "last_sync": now,
                "md_mtime": md_path.stat().st_mtime,
                "ipynb_mtime": ipynb_path.stat().st_mtime,
            }
            self._save_meta()

            info.status = PairStatus.PAIRED
            info.last_sync_time = now
            info.md_mtime = md_path.stat().st_mtime
            info.ipynb_mtime = ipynb_path.stat().st_mtime

            duration = time.time() - start_time
            return SyncResult(
                True, str(md_path), str(ipynb_path),
                direction="md→ipynb",
                message=f"同步成功 ({duration:.2f}s)",
                duration=duration,
            )

        except Exception as e:
            logger.error(f"同步失败 md→ipynb {rel_path}: {e}")
            return SyncResult(
                False, info.md_path, info.ipynb_path,
                direction="md→ipynb",
                message=f"同步失败: {e}",
            )

    def sync_to_md(self, rel_path: str, force: bool = False) -> SyncResult:
        """
        将 ipynb 的改动同步回 md

        Args:
            rel_path: 相对路径
            force: 是否强制同步
        """
        start_time = time.time()
        info = self._file_cache.get(rel_path)

        if info is None:
            return SyncResult(False, "", "", message=f"文件信息未找到: {rel_path}")

        if not force and info.status == PairStatus.CONFLICT:
            return SyncResult(
                False, info.md_path, info.ipynb_path,
                message="存在冲突，请先解决冲突或使用强制同步",
            )

        try:
            md_path = Path(info.md_path)
            ipynb_path = Path(info.ipynb_path)

            # 读取 ipynb 并转换为 md
            nb = jupytext.read(str(ipynb_path))
            jupytext.write(nb, str(md_path), fmt={"extension": ".md", "format_name": self.fmt})

            # 更新元数据
            now = time.time()
            self._meta[rel_path] = {
                "last_sync": now,
                "md_mtime": md_path.stat().st_mtime,
                "ipynb_mtime": ipynb_path.stat().st_mtime,
            }
            self._save_meta()

            info.status = PairStatus.PAIRED
            info.last_sync_time = now
            info.md_mtime = md_path.stat().st_mtime
            info.ipynb_mtime = ipynb_path.stat().st_mtime

            duration = time.time() - start_time
            return SyncResult(
                True, str(md_path), str(ipynb_path),
                direction="ipynb→md",
                message=f"同步成功 ({duration:.2f}s)",
                duration=duration,
            )

        except Exception as e:
            logger.error(f"同步失败 ipynb→md {rel_path}: {e}")
            return SyncResult(
                False, info.md_path, info.ipynb_path,
                direction="ipynb→md",
                message=f"同步失败: {e}",
            )

    def resolve_conflict(self, rel_path: str, winner: str) -> SyncResult:
        """
        解决冲突

        Args:
            rel_path: 相对路径
            winner: "md" 或 "ipynb"，以哪个为准
        """
        if winner == "md":
            return self.sync_to_ipynb(rel_path, force=True)
        elif winner == "ipynb":
            return self.sync_to_md(rel_path, force=True)
        else:
            return SyncResult(False, "", "", message=f"无效的 winner: {winner}")

    # ==================== 批量操作 ====================

    def batch_create(self, skip_paired: bool = True) -> BatchResult:
        """
        批量创建配对

        Args:
            skip_paired: 是否跳过已配对的文件
        """
        result = BatchResult()
        files = self.scan()
        result.total = len(files)

        for info in files:
            if skip_paired and info.status not in (PairStatus.UNPAIRED,):
                result.skipped += 1
                continue

            sync_result = self.create_pair(info.rel_path)
            result.results.append(sync_result)

            if sync_result.success:
                result.success += 1
            else:
                result.failed += 1

        return result

    def batch_sync(self, directions: Optional[Dict[str, str]] = None) -> BatchResult:
        """
        批量同步

        Args:
            directions: 指定每个文件的同步方向 {rel_path: "md" | "ipynb"}
                       如果为 None，自动判断方向
        """
        result = BatchResult()
        files = self.scan()
        result.total = len(files)

        for info in files:
            if info.status == PairStatus.PAIRED:
                result.skipped += 1
                continue

            if info.status == PairStatus.CONFLICT:
                if directions and info.rel_path in directions:
                    sync_result = self.resolve_conflict(info.rel_path, directions[info.rel_path])
                    result.results.append(sync_result)
                    if sync_result.success:
                        result.success += 1
                    else:
                        result.failed += 1
                else:
                    result.conflicted += 1
                continue

            if info.status == PairStatus.UNPAIRED:
                sync_result = self.create_pair(info.rel_path)
            elif info.status == PairStatus.MD_NEWER:
                sync_result = self.sync_to_ipynb(info.rel_path)
            elif info.status == PairStatus.IPYNB_NEWER:
                sync_result = self.sync_to_md(info.rel_path)
            elif info.status == PairStatus.ERROR:
                result.failed += 1
                continue
            else:
                result.skipped += 1
                continue

            result.results.append(sync_result)
            if sync_result.success:
                result.success += 1
            else:
                result.failed += 1

        return result

    # ==================== 工具方法 ====================

    def _set_pair_metadata(self, nb, md_path: Path):
        """为 notebook 设置 jupytext 配对元数据"""
        if "jupytext" not in nb.metadata:
            nb.metadata["jupytext"] = {}

        nb.metadata["jupytext"].update({
            "formats": "md:myst,ipynb",
            "text_representation": {
                "extension": ".md",
                "format_name": self.fmt,
                "format_version": "0.13",
            },
        })

        # 设置内核信息（如果不存在）
        if "kernelspec" not in nb.metadata:
            nb.metadata["kernelspec"] = {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            }

        # 规范化 notebook（确保 cell id 等字段完整）
        try:
            validate(nb)
        except Exception:
            pass

    def _get_meta_path(self) -> Path:
        """获取元数据文件路径"""
        return self.output_dir / self.META_FILE

    def _load_meta(self):
        """加载同步元数据"""
        meta_path = self._get_meta_path()
        if meta_path.exists():
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    self._meta = json.load(f)
                logger.info(f"已加载元数据: {len(self._meta)} 条记录")
            except Exception as e:
                logger.warning(f"加载元数据失败: {e}")
                self._meta = {}
        else:
            self._meta = {}

    def _save_meta(self):
        """保存同步元数据"""
        meta_path = self._get_meta_path()
        try:
            meta_path.parent.mkdir(parents=True, exist_ok=True)
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(self._meta, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"保存元数据失败: {e}")

    def refresh_file_status(self, rel_path: str) -> MDFileInfo:
        """刷新单个文件的状态"""
        md_path = Path(self.source_dir) / rel_path
        ipynb_path = self.output_dir / Path(rel_path).with_suffix(".ipynb")

        info = self._file_cache.get(rel_path)
        if info is None:
            info = MDFileInfo(
                md_path=str(md_path),
                ipynb_path=str(ipynb_path),
                rel_path=rel_path,
            )
            self._file_cache[rel_path] = info

        if md_path.exists():
            info.md_mtime = md_path.stat().st_mtime
        if ipynb_path.exists():
            info.ipynb_mtime = ipynb_path.stat().st_mtime

        info.status = self._compute_status(info)
        info.last_sync_time = self._meta.get(rel_path, {}).get("last_sync", 0.0)
        return info

    def get_ipynb_path_for_md(self, md_path: str) -> str:
        """根据 md 路径计算对应的 ipynb 路径"""
        md = Path(md_path)
        try:
            rel = md.relative_to(self.source_dir)
        except ValueError:
            # 不在源目录下，直接替换后缀
            rel = md.name
        return str(self.output_dir / rel.with_suffix(".ipynb"))

    def get_md_path_for_ipynb(self, ipynb_path: str) -> Optional[str]:
        """根据 ipynb 路径查找对应的 md 路径"""
        ipynb = Path(ipynb_path)
        try:
            rel = ipynb.relative_to(self.output_dir)
        except ValueError:
            return None
        md_path = self.source_dir / rel.with_suffix(".md")
        return str(md_path) if md_path.exists() else None

    def open_jupyterlab(self, directory: Optional[str] = None):
        """启动 JupyterLab"""
        import subprocess
        target = directory or str(self.output_dir)
        try:
            subprocess.Popen(
                ["jupyter", "lab", target],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            logger.info(f"已启动 JupyterLab: {target}")
        except FileNotFoundError:
            logger.error("未找到 jupyter 命令，请确认已安装 JupyterLab")
            raise
