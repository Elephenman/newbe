"""
配置管理模块 - 应用设置与状态持久化
"""

import os
import yaml
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# 默认配置文件路径
DEFAULT_CONFIG_DIR = Path.home() / ".md2ipynb_sync"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.yaml"


@dataclass
class AppConfig:
    """应用配置"""
    # 路径配置
    source_dir: str = ""             # Obsidian 源目录
    output_dir: str = ""             # ipynb 输出目录

    # Jupytext 配置
    format: str = "myst"             # md 格式：myst 或 markdown

    # 同步配置
    auto_sync: bool = True           # 是否自动同步
    skip_paired: bool = True         # 批量操作时跳过已配对文件
    debounce_interval: float = 1.5   # 防抖间隔（秒）

    # JupyterLab 配置
    auto_open_jupyterlab: bool = False  # 配对后自动打开 JupyterLab

    # 冲突处理
    conflict_default: str = "ask"    # 冲突默认处理: "ask" | "md" | "ipynb"

    # 界面配置
    window_width: int = 1100
    window_height: int = 750
    show_hidden_files: bool = False
    log_level: str = "INFO"

    # 最近使用的目录
    recent_source_dirs: list = field(default_factory=list)
    recent_output_dirs: list = field(default_factory=list)

    def save(self, path: Optional[Path] = None):
        """保存配置到文件"""
        config_path = path or DEFAULT_CONFIG_FILE
        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, "w", encoding="utf-8") as f:
                yaml.dump(asdict(self), f, default_flow_style=False, allow_unicode=True)
            logger.info(f"配置已保存: {config_path}")
        except Exception as e:
            logger.error(f"保存配置失败: {e}")

    @classmethod
    def load(cls, path: Optional[Path] = None) -> "AppConfig":
        """从文件加载配置"""
        config_path = path or DEFAULT_CONFIG_FILE
        if not config_path.exists():
            logger.info("配置文件不存在，使用默认配置")
            return cls()

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            config = cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
            logger.info(f"配置已加载: {config_path}")
            return config
        except Exception as e:
            logger.error(f"加载配置失败: {e}")
            return cls()

    def add_recent_source(self, dir_path: str):
        """添加最近使用的源目录"""
        self._add_recent(dir_path, self.recent_source_dirs)

    def add_recent_output(self, dir_path: str):
        """添加最近使用的输出目录"""
        self._add_recent(dir_path, self.recent_output_dirs)

    def _add_recent(self, dir_path: str, recent_list: list):
        """添加到最近使用列表"""
        if dir_path in recent_list:
            recent_list.remove(dir_path)
        recent_list.insert(0, dir_path)
        # 最多保留 10 个
        del recent_list[10:]

    def validate(self) -> list:
        """
        验证配置有效性

        Returns:
            错误消息列表，空列表表示配置有效
        """
        errors = []

        if self.source_dir and not Path(self.source_dir).exists():
            errors.append(f"源目录不存在: {self.source_dir}")

        if self.output_dir:
            # 输出目录不存在不报错，会自动创建
            pass

        if self.source_dir and self.output_dir:
            src = Path(self.source_dir).resolve()
            out = Path(self.output_dir).resolve()
            # 检查输出目录是否在源目录内（避免递归）
            try:
                out.relative_to(src)
                errors.append("输出目录不能在源目录内，会导致递归监控")
            except ValueError:
                pass

        if self.format not in ("myst", "markdown"):
            errors.append(f"不支持的格式: {self.format}，请使用 myst 或 markdown")

        return errors
