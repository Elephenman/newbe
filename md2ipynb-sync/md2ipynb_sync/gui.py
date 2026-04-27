"""
MD↔IPYNB 同步管理器 - PyQt5 主界面

基于 Jupytext 的 Obsidian Markdown 与 Jupyter Notebook 双向同步工具
"""

import sys
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFileDialog, QGroupBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit,
    QProgressBar, QStatusBar, QSplitter, QComboBox,
    QCheckBox, QMessageBox, QMenu, QAction, QAbstractItemView,
    QToolBar, QStyle, QTabWidget,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QFont, QColor, QIcon, QBrush

from .engine import SyncEngine, PairStatus, MDFileInfo, BatchResult
from .watcher import SyncWatcher
from .config import AppConfig
from .dialogs import ConflictResolutionDialog, SettingsDialog, BatchConflictDialog

logger = logging.getLogger(__name__)

# 状态颜色映射
STATUS_COLORS = {
    PairStatus.UNPAIRED: QColor("#95a5a6"),     # 灰色
    PairStatus.PAIRED: QColor("#27ae60"),        # 绿色
    PairStatus.MD_NEWER: QColor("#f39c12"),      # 橙色
    PairStatus.IPYNB_NEWER: QColor("#3498db"),   # 蓝色
    PairStatus.CONFLICT: QColor("#e74c3c"),      # 红色
    PairStatus.ERROR: QColor("#c0392b"),         # 深红色
}


class ScanWorker(QThread):
    """扫描工作线程"""
    finished = pyqtSignal(list)  # List[MDFileInfo]

    def __init__(self, engine: SyncEngine):
        super().__init__()
        self.engine = engine

    def run(self):
        files = self.engine.scan()
        self.finished.emit(files)


class BatchWorker(QThread):
    """批量操作工作线程"""
    progress = pyqtSignal(int, int, str)  # current, total, message
    finished = pyqtSignal(object)  # BatchResult

    def __init__(self, engine: SyncEngine, operation: str, skip_paired: bool = True,
                 resolutions: Optional[Dict[str, str]] = None):
        super().__init__()
        self.engine = engine
        self.operation = operation
        self.skip_paired = skip_paired
        self.resolutions = resolutions or {}

    def run(self):
        if self.operation == "create":
            result = self.engine.batch_create(skip_paired=self.skip_paired)
        elif self.operation == "sync":
            result = self.engine.batch_sync(directions=self.resolutions or None)
        else:
            result = BatchResult()
        self.finished.emit(result)


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self, config: Optional[AppConfig] = None):
        super().__init__()
        self.config = config or AppConfig()
        self.engine: Optional[SyncEngine] = None
        self.watcher: Optional[SyncWatcher] = None
        self._file_infos: Dict[str, MDFileInfo] = {}

        self._init_ui()
        self._load_config_to_ui()

        # 如果配置中有路径，自动初始化
        if self.config.source_dir and self.config.output_dir:
            QTimer.singleShot(500, self._init_engine)

    def _init_ui(self):
        """初始化界面"""
        self.setWindowTitle("MD↔IPYNB 同步管理器")
        self.setMinimumSize(self.config.window_width, self.config.window_height)
        self.resize(self.config.window_width, self.config.window_height)

        # 中央部件
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(8)

        # ======== 顶部：目录选择 ========
        dir_group = QGroupBox("📁 目录配置")
        dir_layout = QVBoxLayout(dir_group)

        # 源目录
        src_layout = QHBoxLayout()
        src_layout.addWidget(QLabel("Obsidian 源目录:"))
        self.source_edit = QLineEdit()
        self.source_edit.setPlaceholderText("选择包含 .md 文件的 Obsidian vault 目录...")
        src_layout.addWidget(self.source_edit, 1)
        self.source_browse_btn = QPushButton("浏览")
        self.source_browse_btn.clicked.connect(self._browse_source)
        src_layout.addWidget(self.source_browse_btn)
        dir_layout.addLayout(src_layout)

        # 输出目录
        out_layout = QHBoxLayout()
        out_layout.addWidget(QLabel("Notebook 输出目录:"))
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("选择 ipynb 文件的统一输出目录...")
        out_layout.addWidget(self.output_edit, 1)
        self.output_browse_btn = QPushButton("浏览")
        self.output_browse_btn.clicked.connect(self._browse_output)
        out_layout.addWidget(self.output_browse_btn)
        dir_layout.addLayout(out_layout)

        # 初始化按钮
        self.init_btn = QPushButton("🔗 初始化引擎")
        self.init_btn.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50; color: white;
                padding: 6px 16px; font-weight: bold; border-radius: 4px;
            }
            QPushButton:hover { background-color: #34495e; }
            QPushButton:disabled { background-color: #bdc3c7; }
        """)
        self.init_btn.clicked.connect(self._init_engine)
        dir_layout.addWidget(self.init_btn, alignment=Qt.AlignRight)

        main_layout.addWidget(dir_group)

        # ======== 中部：操作工具栏 + 文件列表 + 日志 ========
        splitter = QSplitter(Qt.Vertical)

        # 操作工具栏
        toolbar_layout = QHBoxLayout()

        self.scan_btn = QPushButton("🔍 扫描")
        self.scan_btn.setEnabled(False)
        self.scan_btn.clicked.connect(self._scan)
        toolbar_layout.addWidget(self.scan_btn)

        self.pair_all_btn = QPushButton("📋 全部配对")
        self.pair_all_btn.setEnabled(False)
        self.pair_all_btn.clicked.connect(self._pair_all)
        toolbar_layout.addWidget(self.pair_all_btn)

        self.sync_btn = QPushButton("🔄 手动同步")
        self.sync_btn.setEnabled(False)
        self.sync_btn.clicked.connect(self._manual_sync)
        toolbar_layout.addWidget(self.sync_btn)

        self.watch_btn = QPushButton("👁 启动监控")
        self.watch_btn.setEnabled(False)
        self.watch_btn.setCheckable(True)
        self.watch_btn.clicked.connect(self._toggle_watch)
        toolbar_layout.addWidget(self.watch_btn)

        self.jupyter_btn = QPushButton("🚀 打开 JupyterLab")
        self.jupyter_btn.setEnabled(False)
        self.jupyter_btn.clicked.connect(self._open_jupyterlab)
        toolbar_layout.addWidget(self.jupyter_btn)

        toolbar_layout.addStretch()

        self.settings_btn = QPushButton("⚙️ 设置")
        self.settings_btn.clicked.connect(self._show_settings)
        toolbar_layout.addWidget(self.settings_btn)

        # 状态统计
        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        toolbar_layout.addWidget(self.stats_label)

        main_layout.addLayout(toolbar_layout)

        # 文件列表
        self.file_table = QTableWidget()
        self.file_table.setColumnCount(5)
        self.file_table.setHorizontalHeaderLabels(["状态", "文件路径", "MD 修改时间", "Notebook 修改时间", "上次同步"])
        self.file_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.file_table.horizontalHeader().resizeSection(0, 80)
        self.file_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.file_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.file_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.file_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.file_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.file_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_table.customContextMenuRequested.connect(self._show_context_menu)
        self.file_table.doubleClicked.connect(self._on_double_click)
        splitter.addWidget(self.file_table)

        # 日志面板
        log_group = QGroupBox("📝 操作日志")
        log_layout = QVBoxLayout(log_group)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        self.log_text.setMaximumHeight(150)
        log_layout.addWidget(self.log_text)

        log_btn_layout = QHBoxLayout()
        clear_log_btn = QPushButton("清空日志")
        clear_log_btn.clicked.connect(self.log_text.clear)
        log_btn_layout.addStretch()
        log_btn_layout.addWidget(clear_log_btn)
        log_layout.addLayout(log_btn_layout)

        splitter.addWidget(log_group)
        splitter.setSizes([500, 150])
        main_layout.addWidget(splitter, 1)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # 状态栏
        self.statusBar().showMessage("就绪 - 请选择源目录和输出目录后初始化引擎")

        # ======== 样式 ========
        self.setStyleSheet("""
            QMainWindow { background-color: #fafafa; }
            QGroupBox {
                font-weight: bold; border: 1px solid #ddd;
                border-radius: 6px; margin-top: 8px; padding-top: 16px;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; }
            QPushButton {
                padding: 6px 12px; border-radius: 4px;
                border: 1px solid #bdc3c7; background-color: #ecf0f1;
            }
            QPushButton:hover { background-color: #d5dbdb; }
            QPushButton:pressed { background-color: #bdc3c7; }
            QPushButton:disabled { color: #bdc3c7; }
            QTableWidget { border: 1px solid #ddd; border-radius: 4px; }
        """)

    # ==================== 目录选择 ====================

    def _browse_source(self):
        """选择源目录"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择 Obsidian 源目录", self.source_edit.text()
        )
        if dir_path:
            self.source_edit.setText(dir_path)
            self.config.source_dir = dir_path
            self.config.add_recent_source(dir_path)

    def _browse_output(self):
        """选择输出目录"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择 Notebook 输出目录", self.output_edit.text()
        )
        if dir_path:
            self.output_edit.setText(dir_path)
            self.config.output_dir = dir_path
            self.config.add_recent_output(dir_path)

    # ==================== 引擎初始化 ====================

    def _init_engine(self):
        """初始化同步引擎"""
        source_dir = self.source_edit.text().strip()
        output_dir = self.output_edit.text().strip()

        if not source_dir:
            QMessageBox.warning(self, "提示", "请先选择 Obsidian 源目录")
            return
        if not output_dir:
            QMessageBox.warning(self, "提示", "请先选择 Notebook 输出目录")
            return

        # 验证配置
        self.config.source_dir = source_dir
        self.config.output_dir = output_dir
        errors = self.config.validate()
        if errors:
            QMessageBox.critical(self, "配置错误", "\n".join(errors))
            return

        try:
            # 创建输出目录（如果不存在）
            Path(output_dir).mkdir(parents=True, exist_ok=True)

            self.engine = SyncEngine(source_dir, output_dir, fmt=self.config.format)
            self._log(f"✅ 引擎初始化成功")
            self._log(f"   源目录: {source_dir}")
            self._log(f"   输出目录: {output_dir}")
            self._log(f"   格式: {self.config.format}")

            # 启用按钮
            self.scan_btn.setEnabled(True)
            self.pair_all_btn.setEnabled(True)
            self.sync_btn.setEnabled(True)
            self.watch_btn.setEnabled(True)
            self.jupyter_btn.setEnabled(True)
            self.init_btn.setEnabled(False)
            self.source_edit.setEnabled(False)
            self.output_edit.setEnabled(False)
            self.source_browse_btn.setEnabled(False)
            self.output_browse_btn.setEnabled(False)

            self.statusBar().showMessage("引擎已就绪 - 点击「扫描」查看文件状态")

            # 保存配置
            self.config.save()

            # 自动扫描
            QTimer.singleShot(300, self._scan)

        except Exception as e:
            QMessageBox.critical(self, "初始化失败", f"引擎初始化失败:\n{e}")
            self._log(f"❌ 引擎初始化失败: {e}")

    # ==================== 文件扫描 ====================

    def _scan(self):
        """扫描文件"""
        if not self.engine:
            return

        self._log("🔍 开始扫描...")
        self.statusBar().showMessage("正在扫描文件...")
        self.scan_btn.setEnabled(False)

        # 在线程中扫描
        self._scan_worker = ScanWorker(self.engine)
        self._scan_worker.finished.connect(self._on_scan_complete)
        self._scan_worker.start()

    def _on_scan_complete(self, files: list):
        """扫描完成"""
        self.scan_btn.setEnabled(True)

        # 更新文件缓存
        self._file_infos.clear()
        for info in files:
            self._file_infos[info.rel_path] = info

        # 更新表格
        self._update_table(files)

        # 更新统计
        self._update_stats()

        self._log(f"✅ 扫描完成: 共 {len(files)} 个 MD 文件")
        self.statusBar().showMessage(f"扫描完成: {len(files)} 个文件")

    def _update_table(self, files: list):
        """更新文件表格"""
        self.file_table.setRowCount(len(files))

        for row, info in enumerate(files):
            # 状态
            status_item = QTableWidgetItem(f"{info.status_icon} {info.status_display}")
            status_item.setForeground(QBrush(STATUS_COLORS.get(info.status, QColor("#000"))))
            self.file_table.setItem(row, 0, status_item)

            # 文件路径
            path_item = QTableWidgetItem(info.rel_path)
            path_item.setData(Qt.UserRole, info.rel_path)  # 存储相对路径
            self.file_table.setItem(row, 1, path_item)

            # MD 修改时间
            self.file_table.setItem(row, 2, QTableWidgetItem(self._format_time(info.md_mtime)))

            # IPYNB 修改时间
            ipynb_time = self._format_time(info.ipynb_mtime) if info.ipynb_mtime > 0 else "-"
            self.file_table.setItem(row, 3, QTableWidgetItem(ipynb_time))

            # 上次同步
            sync_time = self._format_time(info.last_sync_time) if info.last_sync_time > 0 else "-"
            self.file_table.setItem(row, 4, QTableWidgetItem(sync_time))

    def _update_stats(self):
        """更新状态统计"""
        if not self.engine:
            return
        summary = self.engine.get_status_summary()
        parts = []
        label_map = {
            "paired": ("✅ 已配对", "#27ae60"),
            "unpaired": ("⬜ 未配对", "#95a5a6"),
            "md_newer": ("🟡 MD已更新", "#f39c12"),
            "ipynb_newer": ("🔵 NB已更新", "#3498db"),
            "conflict": ("🔴 冲突", "#e74c3c"),
            "error": ("❌ 错误", "#c0392b"),
        }
        for key, count in summary.items():
            label, color = label_map.get(key, (key, "#000"))
            parts.append(f'<span style="color:{color}">{label}: {count}</span>')

        self.stats_label.setText("&nbsp;&nbsp;|&nbsp;&nbsp;".join(parts))

    # ==================== 批量操作 ====================

    def _pair_all(self):
        """全部配对"""
        if not self.engine:
            return

        reply = QMessageBox.question(
            self, "确认", "确定要为所有未配对的 MD 文件创建 Notebook 配对吗？",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        self._log("📋 开始批量配对...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 不确定进度
        self.pair_all_btn.setEnabled(False)

        self._batch_worker = BatchWorker(
            self.engine, "create", skip_paired=self.config.skip_paired
        )
        self._batch_worker.finished.connect(self._on_batch_complete)
        self._batch_worker.start()

    def _manual_sync(self):
        """手动同步"""
        if not self.engine:
            return

        # 先检查冲突
        files = self.engine.scan()
        conflicted = [f for f in files if f.status == PairStatus.CONFLICT]

        resolutions = {}
        if conflicted:
            # 显示批量冲突解决对话框
            dialog = BatchConflictDialog(conflicted, self)
            dialog.all_resolved.connect(lambda r: resolutions.update(r))
            if dialog.exec_() != BatchConflictDialog.Accepted:
                return

        self._log("🔄 开始手动同步...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.sync_btn.setEnabled(False)

        self._batch_worker = BatchWorker(
            self.engine, "sync", resolutions=resolutions if resolutions else None
        )
        self._batch_worker.finished.connect(self._on_batch_complete)
        self._batch_worker.start()

    def _on_batch_complete(self, result: BatchResult):
        """批量操作完成"""
        self.progress_bar.setVisible(False)
        self.pair_all_btn.setEnabled(True)
        self.sync_btn.setEnabled(True)

        self._log(f"✅ 批量操作完成: {result.summary}")

        # 显示失败信息
        for r in result.results:
            if not r.success:
                self._log(f"   ❌ {r.md_path}: {r.message}")

        # 刷新文件列表
        self._scan()

    # ==================== 文件监控 ====================

    def _toggle_watch(self, checked: bool):
        """切换文件监控"""
        if checked:
            self._start_watch()
        else:
            self._stop_watch()

    def _start_watch(self):
        """启动文件监控"""
        if not self.engine:
            return

        self.watcher = SyncWatcher(
            engine=self.engine,
            on_md_changed=self._on_md_changed,
            on_ipynb_changed=self._on_ipynb_changed,
            on_sync_complete=self._on_sync_complete,
            on_error=self._on_sync_error,
            debounce_interval=self.config.debounce_interval,
        )
        self.watcher.start()
        self.watch_btn.setText("👁 停止监控")
        self._log("👁 文件监控已启动")
        self.statusBar().showMessage("文件监控运行中...")

    def _stop_watch(self):
        """停止文件监控"""
        if self.watcher:
            self.watcher.stop()
            self.watcher = None
        self.watch_btn.setText("👁 启动监控")
        self._log("👁 文件监控已停止")
        self.statusBar().showMessage("文件监控已停止")

    def _on_md_changed(self, rel_path: str, event_type: str):
        """MD 文件变更回调"""
        self._log(f"📝 MD 变更: {rel_path} ({event_type})")
        # 刷新该行的状态
        QTimer.singleShot(100, self._refresh_table_row)

    def _on_ipynb_changed(self, rel_path: str, event_type: str):
        """IPYNB 文件变更回调"""
        self._log(f"📓 Notebook 变更: {rel_path} ({event_type})")
        QTimer.singleShot(100, self._refresh_table_row)

    def _on_sync_complete(self, rel_path: str, direction: str, success: bool):
        """同步完成回调"""
        icon = "✅" if success else "❌"
        self._log(f"{icon} 自动同步 {direction}: {rel_path}")
        QTimer.singleShot(100, self._refresh_table_row)

    def _on_sync_error(self, rel_path: str, error_msg: str):
        """同步错误回调"""
        self._log(f"❌ 同步错误 {rel_path}: {error_msg}")

    def _refresh_table_row(self):
        """刷新表格显示"""
        if not self.engine:
            return
        files = self.engine.scan()
        self._update_table(files)
        self._update_stats()

    # ==================== 右键菜单与双击 ====================

    def _show_context_menu(self, pos):
        """显示右键菜单"""
        row = self.file_table.rowAt(pos.y())
        if row < 0:
            return

        item = self.file_table.item(row, 1)
        if not item:
            return
        rel_path = item.data(Qt.UserRole)
        info = self._file_infos.get(rel_path)
        if not info:
            return

        menu = QMenu(self)

        # 根据状态添加操作
        if info.status == PairStatus.UNPAIRED:
            action = menu.addAction("📋 创建配对")
            action.triggered.connect(lambda: self._single_pair(rel_path))
        elif info.status == PairStatus.MD_NEWER:
            action = menu.addAction("→ 同步到 Notebook")
            action.triggered.connect(lambda: self._single_sync_to_ipynb(rel_path))
        elif info.status == PairStatus.IPYNB_NEWER:
            action = menu.addAction("← 同步到 MD")
            action.triggered.connect(lambda: self._single_sync_to_md(rel_path))
        elif info.status == PairStatus.CONFLICT:
            action = menu.addAction("⚠️ 解决冲突...")
            action.triggered.connect(lambda: self._resolve_conflict(rel_path))
        elif info.status == PairStatus.PAIRED:
            action = menu.addAction("→ 强制同步到 Notebook")
            action.triggered.connect(lambda: self._single_sync_to_ipynb(rel_path, force=True))
            action = menu.addAction("← 强制同步到 MD")
            action.triggered.connect(lambda: self._single_sync_to_md(rel_path, force=True))

        menu.addSeparator()

        # 通用操作
        action = menu.addAction("🔄 刷新状态")
        action.triggered.connect(lambda: self._refresh_single(rel_path))

        action = menu.addAction("📂 打开 MD 文件位置")
        action.triggered.connect(lambda: self._open_file_location(info.md_path))

        if info.ipynb_mtime > 0:
            action = menu.addAction("📂 打开 Notebook 文件位置")
            action.triggered.connect(lambda: self._open_file_location(info.ipynb_path))

        menu.exec_(self.file_table.viewport().mapToGlobal(pos))

    def _on_double_click(self, index):
        """双击文件行"""
        row = index.row()
        item = self.file_table.item(row, 1)
        if not item:
            return
        rel_path = item.data(Qt.UserRole)
        info = self._file_infos.get(rel_path)
        if not info:
            return

        if info.status == PairStatus.UNPAIRED:
            self._single_pair(rel_path)
        elif info.status == PairStatus.MD_NEWER:
            self._single_sync_to_ipynb(rel_path)
        elif info.status == PairStatus.IPYNB_NEWER:
            self._single_sync_to_md(rel_path)
        elif info.status == PairStatus.CONFLICT:
            self._resolve_conflict(rel_path)

    # ==================== 单文件操作 ====================

    def _single_pair(self, rel_path: str):
        """创建单个配对"""
        if not self.engine:
            return
        result = self.engine.create_pair(rel_path)
        if result.success:
            self._log(f"✅ 配对成功: {rel_path}")
        else:
            self._log(f"❌ 配对失败: {rel_path} - {result.message}")
            QMessageBox.warning(self, "配对失败", result.message)
        self._refresh_table_row()

    def _single_sync_to_ipynb(self, rel_path: str, force: bool = False):
        """同步单个文件 md → ipynb"""
        if not self.engine:
            return
        result = self.engine.sync_to_ipynb(rel_path, force=force)
        if result.success:
            self._log(f"✅ 同步成功 md→ipynb: {rel_path}")
        else:
            self._log(f"❌ 同步失败: {rel_path} - {result.message}")
            QMessageBox.warning(self, "同步失败", result.message)
        self._refresh_table_row()

    def _single_sync_to_md(self, rel_path: str, force: bool = False):
        """同步单个文件 ipynb → md"""
        if not self.engine:
            return
        result = self.engine.sync_to_md(rel_path, force=force)
        if result.success:
            self._log(f"✅ 同步成功 ipynb→md: {rel_path}")
        else:
            self._log(f"❌ 同步失败: {rel_path} - {result.message}")
            QMessageBox.warning(self, "同步失败", result.message)
        self._refresh_table_row()

    def _resolve_conflict(self, rel_path: str):
        """解决冲突"""
        info = self._file_infos.get(rel_path)
        if not info:
            return

        dialog = ConflictResolutionDialog(info, self)
        dialog.resolved.connect(self._on_conflict_resolved)
        dialog.exec_()

    def _on_conflict_resolved(self, rel_path: str, winner: str):
        """冲突解决回调"""
        if not self.engine:
            return
        result = self.engine.resolve_conflict(rel_path, winner)
        if result.success:
            self._log(f"✅ 冲突已解决 ({winner} 为准): {rel_path}")
        else:
            self._log(f"❌ 冲突解决失败: {rel_path} - {result.message}")
        self._refresh_table_row()

    def _refresh_single(self, rel_path: str):
        """刷新单个文件状态"""
        if not self.engine:
            return
        self.engine.refresh_file_status(rel_path)
        self._refresh_table_row()

    def _open_file_location(self, file_path: str):
        """在文件管理器中打开文件位置"""
        import subprocess
        try:
            if sys.platform == "win32":
                subprocess.Popen(f'explorer /select,"{file_path}"')
            elif sys.platform == "darwin":
                subprocess.Popen(["open", "-R", file_path])
            else:
                subprocess.Popen(["xdg-open", str(Path(file_path).parent)])
        except Exception as e:
            self._log(f"❌ 无法打开文件位置: {e}")

    # ==================== JupyterLab ====================

    def _open_jupyterlab(self):
        """打开 JupyterLab"""
        if not self.engine:
            return
        try:
            self.engine.open_jupyterlab()
            self._log("🚀 JupyterLab 已启动")
        except FileNotFoundError:
            QMessageBox.critical(
                self, "启动失败",
                "未找到 jupyter 命令。\n请确认已安装 JupyterLab:\n  conda install jupyterlab"
            )

    # ==================== 设置 ====================

    def _show_settings(self):
        """显示设置对话框"""
        dialog = SettingsDialog(self.config, self)
        dialog.settings_changed.connect(self._apply_settings)
        dialog.exec_()

    def _apply_settings(self, settings: dict):
        """应用设置"""
        for key, value in settings.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)

        # 更新日志级别
        logging.getLogger("md2ipynb_sync").setLevel(getattr(logging, self.config.log_level, logging.INFO))

        self.config.save()
        self._log("⚙️ 设置已更新并保存")

        # 如果引擎已初始化，需要更新格式
        if self.engine and self.config.format != self.engine.fmt:
            self._log(f"📝 Jupytext 格式已更新为: {self.config.format}")
            self.engine.fmt = self.config.format

    def _load_config_to_ui(self):
        """加载配置到界面"""
        self.source_edit.setText(self.config.source_dir)
        self.output_edit.setText(self.config.output_dir)

    # ==================== 工具方法 ====================

    def _log(self, message: str):
        """添加日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        # 自动滚动到底部
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    @staticmethod
    def _format_time(timestamp: float) -> str:
        """格式化时间戳"""
        if timestamp == 0:
            return "-"
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")

    def closeEvent(self, event):
        """窗口关闭事件"""
        # 停止监控
        if self.watcher:
            self._stop_watch()

        # 保存窗口大小
        self.config.window_width = self.width()
        self.config.window_height = self.height()
        self.config.save()

        event.accept()
