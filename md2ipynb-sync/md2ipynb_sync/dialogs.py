"""
对话框模块 - 冲突解决、设置面板等
"""

import logging
from pathlib import Path

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QGroupBox, QFormLayout, QComboBox, QCheckBox,
    QSpinBox, QDoubleSpinBox, QLineEdit, QDialogButtonBox,
    QFileDialog, QMessageBox, QSplitter, QWidget,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QTextCharFormat

from .config import AppConfig
from .engine import PairStatus, MDFileInfo

logger = logging.getLogger(__name__)


class ConflictResolutionDialog(QDialog):
    """冲突解决对话框"""

    resolved = pyqtSignal(str, str)  # rel_path, winner ("md" | "ipynb")

    def __init__(self, info: MDFileInfo, parent=None):
        super().__init__(parent)
        self.info = info
        self.winner = None
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("⚠️ 同步冲突")
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)

        layout = QVBoxLayout(self)

        # 标题
        title_label = QLabel(f"文件冲突: {self.info.rel_path}")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #e74c3c;")
        layout.addWidget(title_label)

        # 说明
        desc = QLabel(
            "MD 文件和 Notebook 文件都有改动，请选择以哪个版本为准：\n"
            "选择后，另一个文件将被覆盖为所选版本的内容。"
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # 文件信息
        info_group = QGroupBox("文件信息")
        info_layout = QFormLayout()
        info_layout.addRow("MD 修改时间:", QLabel(self._format_time(self.info.md_mtime)))
        info_layout.addRow("Notebook 修改时间:", QLabel(self._format_time(self.info.ipynb_mtime)))
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # 预览区域
        splitter = QSplitter(Qt.Horizontal)

        # MD 预览
        md_group = QGroupBox("MD 文件内容")
        md_layout = QVBoxLayout()
        self.md_preview = QTextEdit()
        self.md_preview.setReadOnly(True)
        self.md_preview.setFont(QFont("Consolas", 10))
        md_layout.addWidget(self.md_preview)
        md_btn = QPushButton("📄 以 MD 为准")
        md_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                padding: 8px; font-size: 13px; font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        md_btn.clicked.connect(lambda: self._choose("md"))
        md_layout.addWidget(md_btn)
        md_group.setLayout(md_layout)

        # IPYNB 预览
        ipynb_group = QGroupBox("Notebook 内容")
        ipynb_layout = QVBoxLayout()
        self.ipynb_preview = QTextEdit()
        self.ipynb_preview.setReadOnly(True)
        self.ipynb_preview.setFont(QFont("Consolas", 10))
        ipynb_layout.addWidget(self.ipynb_preview)
        ipynb_btn = QPushButton("📓 以 Notebook 为准")
        ipynb_btn.setStyleSheet("""
            QPushButton {
                background-color: #2980b9; color: white;
                padding: 8px; font-size: 13px; font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #3498db; }
        """)
        ipynb_btn.clicked.connect(lambda: self._choose("ipynb"))
        ipynb_layout.addWidget(ipynb_btn)
        ipynb_group.setLayout(ipynb_layout)

        splitter.addWidget(md_group)
        splitter.addWidget(ipynb_group)
        layout.addWidget(splitter)

        # 底部按钮
        btn_layout = QHBoxLayout()
        skip_btn = QPushButton("跳过（暂不处理）")
        skip_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(skip_btn)
        layout.addLayout(btn_layout)

        # 加载预览内容
        self._load_previews()

    def _load_previews(self):
        """加载文件预览"""
        try:
            with open(self.info.md_path, "r", encoding="utf-8") as f:
                md_content = f.read()
            self.md_preview.setPlainText(md_content[:5000])
            if len(md_content) > 5000:
                self.md_preview.append("\n\n... (内容已截断)")
        except Exception as e:
            self.md_preview.setPlainText(f"无法读取: {e}")

        try:
            import json
            with open(self.info.ipynb_path, "r", encoding="utf-8") as f:
                nb_data = json.load(f)
            # 提取 notebook 中的文本内容用于预览
            cells_text = []
            for cell in nb_data.get("cells", []):
                cell_type = cell.get("cell_type", "")
                source = "".join(cell.get("source", []))
                if cell_type == "markdown":
                    cells_text.append(f"[Markdown]\n{source}")
                elif cell_type == "code":
                    cells_text.append(f"[Code]\n{source}")
            preview = "\n\n---\n\n".join(cells_text)
            self.ipynb_preview.setPlainText(preview[:5000])
            if len(preview) > 5000:
                self.ipynb_preview.append("\n\n... (内容已截断)")
        except Exception as e:
            self.ipynb_preview.setPlainText(f"无法读取: {e}")

    def _choose(self, winner: str):
        """选择以哪个版本为准"""
        self.winner = winner
        self.resolved.emit(self.info.rel_path, winner)
        self.accept()

    @staticmethod
    def _format_time(timestamp: float) -> str:
        """格式化时间戳"""
        if timestamp == 0:
            return "不存在"
        from datetime import datetime
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


class SettingsDialog(QDialog):
    """设置对话框"""

    settings_changed = pyqtSignal(dict)

    def __init__(self, config: AppConfig, parent=None):
        super().__init__(parent)
        self.config = config
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("⚙️ 设置")
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)

        # Jupytext 设置
        jupytext_group = QGroupBox("Jupytext 配置")
        jupytext_layout = QFormLayout()

        self.format_combo = QComboBox()
        self.format_combo.addItems(["myst", "markdown"])
        self.format_combo.setCurrentText(self.config.format)
        jupytext_layout.addRow("MD 格式:", self.format_combo)

        jupytext_group.setLayout(jupytext_layout)
        layout.addWidget(jupytext_group)

        # 同步设置
        sync_group = QGroupBox("同步配置")
        sync_layout = QFormLayout()

        self.auto_sync_check = QCheckBox("启用自动同步（实时监控）")
        self.auto_sync_check.setChecked(self.config.auto_sync)
        sync_layout.addRow(self.auto_sync_check)

        self.skip_paired_check = QCheckBox("批量操作时跳过已配对文件")
        self.skip_paired_check.setChecked(self.config.skip_paired)
        sync_layout.addRow(self.skip_paired_check)

        self.debounce_spin = QDoubleSpinBox()
        self.debounce_spin.setRange(0.5, 10.0)
        self.debounce_spin.setSingleStep(0.5)
        self.debounce_spin.setValue(self.config.debounce_interval)
        self.debounce_spin.setSuffix(" 秒")
        sync_layout.addRow("防抖间隔:", self.debounce_spin)

        self.conflict_combo = QComboBox()
        self.conflict_combo.addItems(["每次询问", "以 MD 为准", "以 Notebook 为准"])
        conflict_map = {"ask": 0, "md": 1, "ipynb": 2}
        self.conflict_combo.setCurrentIndex(conflict_map.get(self.config.conflict_default, 0))
        sync_layout.addRow("冲突默认处理:", self.conflict_combo)

        sync_group.setLayout(sync_layout)
        layout.addWidget(sync_group)

        # JupyterLab 设置
        jupyter_group = QGroupBox("JupyterLab 配置")
        jupyter_layout = QFormLayout()

        self.auto_open_check = QCheckBox("配对完成后自动打开 JupyterLab")
        self.auto_open_check.setChecked(self.config.auto_open_jupyterlab)
        jupyter_layout.addRow(self.auto_open_check)

        jupyter_group.setLayout(jupyter_layout)
        layout.addWidget(jupyter_group)

        # 日志设置
        log_group = QGroupBox("日志配置")
        log_layout = QFormLayout()

        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        self.log_level_combo.setCurrentText(self.config.log_level)
        log_layout.addRow("日志级别:", self.log_level_combo)

        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        # 按钮
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self._accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def _accept(self):
        """确认设置"""
        conflict_map = {0: "ask", 1: "md", 2: "ipynb"}
        settings = {
            "format": self.format_combo.currentText(),
            "auto_sync": self.auto_sync_check.isChecked(),
            "skip_paired": self.skip_paired_check.isChecked(),
            "debounce_interval": self.debounce_spin.value(),
            "conflict_default": conflict_map.get(self.conflict_combo.currentIndex(), "ask"),
            "auto_open_jupyterlab": self.auto_open_check.isChecked(),
            "log_level": self.log_level_combo.currentText(),
        }
        self.settings_changed.emit(settings)
        self.accept()


class BatchConflictDialog(QDialog):
    """批量冲突解决对话框"""

    all_resolved = pyqtSignal(dict)  # {rel_path: winner}

    def __init__(self, conflicted_files: list, parent=None):
        """
        Args:
            conflicted_files: MDFileInfo 列表（都是冲突状态）
        """
        super().__init__(parent)
        self.conflicted_files = conflicted_files
        self.resolutions = {}
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle(f"⚠️ 批量冲突解决 ({len(self.conflicted_files)} 个冲突)")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)

        layout = QVBoxLayout(self)

        # 说明
        desc = QLabel(
            f"发现 {len(self.conflicted_files)} 个冲突文件。\n"
            "可以为每个文件选择以哪个版本为准，也可以使用底部按钮批量处理。"
        )
        layout.addWidget(desc)

        # 文件列表
        from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
        self.table = QTableWidget(len(self.conflicted_files), 4)
        self.table.setHorizontalHeaderLabels(["文件", "MD 修改时间", "Notebook 修改时间", "选择"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        for row, info in enumerate(self.conflicted_files):
            self.table.setItem(row, 0, QTableWidgetItem(info.rel_path))
            self.table.setItem(row, 1, QTableWidgetItem(self._format_time(info.md_mtime)))
            self.table.setItem(row, 2, QTableWidgetItem(self._format_time(info.ipynb_mtime)))

            combo = QComboBox()
            combo.addItems(["未决定", "以 MD 为准", "以 Notebook 为准", "跳过"])
            self.table.setCellWidget(row, 3, combo)

        layout.addWidget(self.table)

        # 批量操作按钮
        batch_layout = QHBoxLayout()
        all_md_btn = QPushButton("全部以 MD 为准")
        all_md_btn.clicked.connect(lambda: self._batch_select("md"))
        all_ipynb_btn = QPushButton("全部以 Notebook 为准")
        all_ipynb_btn.clicked.connect(lambda: self._batch_select("ipynb"))
        all_skip_btn = QPushButton("全部跳过")
        all_skip_btn.clicked.connect(lambda: self._batch_select("skip"))
        batch_layout.addWidget(all_md_btn)
        batch_layout.addWidget(all_ipynb_btn)
        batch_layout.addWidget(all_skip_btn)
        layout.addLayout(batch_layout)

        # 确认按钮
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self._accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def _batch_select(self, winner: str):
        """批量选择"""
        choice_map = {"md": 1, "ipynb": 2, "skip": 3}
        idx = choice_map.get(winner, 0)
        for row in range(self.table.rowCount()):
            combo = self.table.cellWidget(row, 3)
            if combo:
                combo.setCurrentIndex(idx)

    def _accept(self):
        """确认选择"""
        winner_map = {1: "md", 2: "ipynb"}
        for row in range(self.table.rowCount()):
            combo = self.table.cellWidget(row, 3)
            rel_path = self.table.item(row, 0).text()
            choice = combo.currentIndex()
            if choice in winner_map:
                self.resolutions[rel_path] = winner_map[choice]

        if self.resolutions:
            self.all_resolved.emit(self.resolutions)
        self.accept()

    @staticmethod
    def _format_time(timestamp: float) -> str:
        if timestamp == 0:
            return "不存在"
        from datetime import datetime
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
