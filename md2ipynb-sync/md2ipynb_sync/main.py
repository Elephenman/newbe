"""
MD↔IPYNB 同步管理器 - 入口点
"""

import sys
import argparse
import logging


def setup_logging(level: str = "INFO"):
    """配置日志"""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="MD↔IPYNB 同步管理器 - 基于 Jupytext 的 Obsidian Markdown 与 Jupyter Notebook 双向同步工具"
    )
    parser.add_argument(
        "--source", "-s",
        help="Obsidian MD 文件源目录",
    )
    parser.add_argument(
        "--output", "-o",
        help="Notebook 输出目录",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["myst", "markdown"],
        default="myst",
        help="Jupytext 格式 (默认: myst)",
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="启动后自动扫描",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="启动后自动开启文件监控",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="日志级别",
    )
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="无界面模式（仅命令行）",
    )

    args = parser.parse_args()
    setup_logging(args.log_level)

    if args.no_gui:
        # 命令行模式
        _cli_mode(args)
    else:
        # GUI 模式
        _gui_mode(args)


def _gui_mode(args):
    """GUI 模式"""
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt

    # 高 DPI 支持
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("MD↔IPYNB 同步管理器")
    app.setStyle("Fusion")

    from .config import AppConfig
    from .gui import MainWindow

    # 加载配置
    config = AppConfig.load()
    if args.source:
        config.source_dir = args.source
    if args.output:
        config.output_dir = args.output
    config.format = args.format

    # 创建主窗口
    window = MainWindow(config)
    window.show()

    # 自动操作
    if args.watch and config.source_dir and config.output_dir:
        import QTimer
        # 延迟启动监控
        QTimer.singleShot(2000, window._toggle_watch)

    sys.exit(app.exec_())


def _cli_mode(args):
    """命令行模式"""
    from .config import AppConfig
    from .engine import SyncEngine

    if not args.source or not args.output:
        print("❌ 命令行模式需要指定 --source 和 --output")
        return

    config = AppConfig(source_dir=args.source, output_dir=args.output, format=args.format)
    errors = config.validate()
    if errors:
        for err in errors:
            print(f"❌ {err}")
        return

    engine = SyncEngine(args.source, args.output, fmt=args.format)

    if args.scan:
        files = engine.scan()
        print(f"\n📁 扫描结果: 共 {len(files)} 个 MD 文件\n")
        print(f"{'状态':<12} {'文件路径'}")
        print("-" * 60)
        for info in files:
            print(f"{info.status_display:<12} {info.rel_path}")

        # 统计
        summary = engine.get_status_summary()
        print(f"\n📊 统计:")
        for key, count in summary.items():
            print(f"  {key}: {count}")
    else:
        print("使用 --scan 扫描文件，或使用 --help 查看所有选项")


if __name__ == "__main__":
    main()
