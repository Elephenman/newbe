"""
文件监控模块 - 使用 watchdog 实现实时文件变更检测与自动同步
"""

import time
import logging
from pathlib import Path
from typing import Optional, Callable, Dict, Set

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent

logger = logging.getLogger(__name__)


class DebouncedHandler(FileSystemEventHandler):
    """
    防抖文件事件处理器

    同一次保存操作可能触发多个事件（Created + Modified），
    使用防抖机制合并短时间内的重复事件。
    """

    def __init__(
        self,
        callback: Callable[[str, str], None],
        debounce_interval: float = 1.0,
        extensions: Optional[Set[str]] = None,
    ):
        """
        Args:
            callback: 回调函数 callback(path, event_type)
            debounce_interval: 防抖间隔（秒）
            extensions: 监控的文件扩展名集合（如 {'.md', '.ipynb'}）
        """
        super().__init__()
        self.callback = callback
        self.debounce_interval = debounce_interval
        self.extensions = extensions or {".md", ".ipynb"}
        self._pending: Dict[str, float] = {}  # path -> last_event_time
        self._last_synced: Dict[str, float] = {}  # path -> last_sync_time（避免循环同步）

    def on_modified(self, event):
        if event.is_directory:
            return
        self._handle_event(event.src_path, "modified")

    def on_created(self, event):
        if event.is_directory:
            return
        self._handle_event(event.src_path, "created")

    def on_deleted(self, event):
        if event.is_directory:
            return
        self._handle_event(event.src_path, "deleted")

    def _handle_event(self, path: str, event_type: str):
        """处理文件事件"""
        file_path = Path(path)

        # 过滤扩展名
        if file_path.suffix not in self.extensions:
            return

        # 过滤临时文件（如 .~xxx、xxx.tmp）
        if file_path.name.startswith(".") or file_path.name.startswith("~") or file_path.suffix == ".tmp":
            return

        # 过滤元数据文件
        if file_path.name == ".md2ipynb_meta.json":
            return

        now = time.time()

        # 防抖：如果距离上次事件太近，忽略
        if path in self._pending and now - self._pending[path] < self.debounce_interval:
            return

        # 避免循环同步：如果刚同步过，忽略
        if path in self._last_synced and now - self._last_synced[path] < 2.0:
            return

        self._pending[path] = now
        logger.debug(f"文件事件: {event_type} - {path}")

        try:
            self.callback(path, event_type)
        except Exception as e:
            logger.error(f"处理文件事件失败 {path}: {e}")

    def mark_synced(self, path: str):
        """标记文件刚被同步过，用于避免循环同步"""
        self._last_synced[path] = time.time()


class SyncWatcher:
    """
    文件同步监控器

    监控源目录和输出目录的文件变更，触发自动同步。
    """

    def __init__(
        self,
        engine,  # SyncEngine 实例
        on_md_changed: Optional[Callable] = None,
        on_ipynb_changed: Optional[Callable] = None,
        on_sync_complete: Optional[Callable] = None,
        on_error: Optional[Callable] = None,
        debounce_interval: float = 1.5,
    ):
        """
        Args:
            engine: SyncEngine 实例
            on_md_changed: md 文件变更回调 callback(rel_path, event_type)
            on_ipynb_changed: ipynb 文件变更回调 callback(rel_path, event_type)
            on_sync_complete: 同步完成回调 callback(rel_path, direction, success)
            on_error: 错误回调 callback(rel_path, error_msg)
            debounce_interval: 防抖间隔
        """
        self.engine = engine
        self.on_md_changed = on_md_changed
        self.on_ipynb_changed = on_ipynb_changed
        self.on_sync_complete = on_sync_complete
        self.on_error = on_error

        self._observer: Optional[Observer] = None
        self._running = False

        # 创建事件处理器
        self._md_handler = DebouncedHandler(
            callback=self._handle_md_event,
            debounce_interval=debounce_interval,
            extensions={".md"},
        )
        self._ipynb_handler = DebouncedHandler(
            callback=self._handle_ipynb_event,
            debounce_interval=debounce_interval,
            extensions={".ipynb"},
        )

    @property
    def is_running(self) -> bool:
        return self._running

    def start(self):
        """启动文件监控"""
        if self._running:
            logger.warning("监控器已在运行")
            return

        self._observer = Observer()
        source_dir = str(self.engine.source_dir)
        output_dir = str(self.engine.output_dir)

        # 监控源目录（md 文件）
        if Path(source_dir).exists():
            self._observer.schedule(self._md_handler, source_dir, recursive=True)
            logger.info(f"开始监控源目录: {source_dir}")

        # 监控输出目录（ipynb 文件）
        if Path(output_dir).exists():
            self._observer.schedule(self._ipynb_handler, output_dir, recursive=True)
            logger.info(f"开始监控输出目录: {output_dir}")

        self._observer.start()
        self._running = True
        logger.info("文件监控已启动")

    def stop(self):
        """停止文件监控"""
        if not self._running or self._observer is None:
            return

        self._observer.stop()
        self._observer.join(timeout=5.0)
        self._running = False
        logger.info("文件监控已停止")

    def _handle_md_event(self, path: str, event_type: str):
        """处理 md 文件变更事件"""
        try:
            md_path = Path(path)
            rel_path = str(md_path.relative_to(self.engine.source_dir))

            logger.info(f"检测到 MD 文件变更: {rel_path} ({event_type})")

            # 通知 GUI
            if self.on_md_changed:
                self.on_md_changed(rel_path, event_type)

            # 自动同步到 ipynb
            if event_type != "deleted":
                self.engine.refresh_file_status(rel_path)
                info = self.engine.get_file_info(rel_path)

                if info and info.status.value in ("md_newer", "unpaired"):
                    result = self.engine.sync_to_ipynb(rel_path)
                    self._md_handler.mark_synced(path)
                    self._ipynb_handler.mark_synced(info.ipynb_path)

                    if self.on_sync_complete:
                        self.on_sync_complete(rel_path, "md→ipynb", result.success)

                    if not result.success and self.on_error:
                        self.on_error(rel_path, result.message)

        except Exception as e:
            logger.error(f"处理 MD 事件失败 {path}: {e}")
            if self.on_error:
                self.on_error(path, str(e))

    def _handle_ipynb_event(self, path: str, event_type: str):
        """处理 ipynb 文件变更事件"""
        try:
            ipynb_path = Path(path)
            # 通过 ipynb 路径反查 md 路径
            rel_ipynb = str(ipynb_path.relative_to(self.engine.output_dir))
            rel_path = str(Path(rel_ipynb).with_suffix(".md"))

            logger.info(f"检测到 Notebook 文件变更: {rel_ipynb} ({event_type})")

            # 通知 GUI
            if self.on_ipynb_changed:
                self.on_ipynb_changed(rel_path, event_type)

            # 自动同步回 md
            if event_type != "deleted":
                self.engine.refresh_file_status(rel_path)
                info = self.engine.get_file_info(rel_path)

                if info and info.status.value == "ipynb_newer":
                    result = self.engine.sync_to_md(rel_path)
                    self._ipynb_handler.mark_synced(path)
                    self._md_handler.mark_synced(info.md_path)

                    if self.on_sync_complete:
                        self.on_sync_complete(rel_path, "ipynb→md", result.success)

                    if not result.success and self.on_error:
                        self.on_error(rel_path, result.message)

        except Exception as e:
            logger.error(f"处理 Notebook 事件失败 {path}: {e}")
            if self.on_error:
                self.on_error(path, str(e))
