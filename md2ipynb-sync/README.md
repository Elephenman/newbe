# MD↔IPYNB 同步管理器

基于 [Jupytext](https://jupytext.readthedocs.io/) 的 **Obsidian Markdown ↔ Jupyter Notebook 双向同步工具**。

让你在 Obsidian 中写笔记，在 JupyterLab 中跑代码，两边改动自动同步。

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 🔄 双向同步 | MD ↔ IPYNB 改动自动同步 |
| 👁 实时监控 | 文件保存即触发同步（watchdog） |
| 🖱️ 手动同步 | 一键批量同步，也可单文件操作 |
| 📋 批量配对 | 扫描目录后一键为所有 MD 文件创建 Notebook |
| ⏭️ 增量同步 | 跳过已配对的文件，只处理有改动的 |
| ⚠️ 冲突解决 | 双方都改动时弹窗让你选择以哪个为准 |
| 🚀 启动 JupyterLab | 配对完成后一键打开 JupyterLab |
| 📊 状态面板 | 实时查看已配对/冲突/待同步文件数量 |
| 📝 Obsidian 兼容 | 保留 `[[双链]]`、`#标签`、Callout 等语法原样 |

## 📦 安装

### 前置条件

- Python 3.9+
- Conda（推荐）

### 安装步骤

```bash
# 1. 创建 conda 环境
conda create -n md2ipynb python=3.10 -y
conda activate md2ipynb

# 2. 克隆或下载项目
cd /path/to/md2ipynb-sync

# 3. 安装依赖
pip install -e .

# 4. 安装 JupyterLab 和 Jupytext 扩展
conda install jupyterlab -y
```

### 验证安装

```bash
python -c "import jupytext; print(jupytext.__version__)"
python -c "from md2ipynb_sync.engine import SyncEngine; print('OK')"
```

## 🚀 使用方法

### GUI 模式（推荐）

```bash
conda activate md2ipynb
python -m md2ipynb_sync.main
```

或安装后直接：

```bash
md2ipynb
```

**操作流程：**

1. 选择 **Obsidian 源目录**（包含 .md 文件的 vault 目录）
2. 选择 **Notebook 输出目录**（ipynb 统一存放位置）
3. 点击 **初始化引擎**
4. 点击 **扫描** 查看文件状态
5. 点击 **全部配对** 为 MD 文件创建 Notebook
6. 点击 **启动监控** 开启实时同步
7. 点击 **打开 JupyterLab** 开始使用

### 命令行模式

```bash
# 扫描目录
python -m md2ipynb_sync.main --no-gui -s /path/to/vault -o /path/to/output --scan

# 指定格式
python -m md2ipynb_sync.main -s /path/to/vault -o /path/to/output --format myst
```

### 带参数启动 GUI

```bash
# 预填目录
python -m md2ipynb_sync.main -s "D:\Obsidian\Vault" -o "D:\Notebooks"

# 启动后自动监控
python -m md2ipynb_sync.main -s "D:\Obsidian\Vault" -o "D:\Notebooks" --watch
```

## 📂 目录结构

```
源目录 (Obsidian Vault)          输出目录 (Notebooks)
├── 01-笔记/                     ├── 01-笔记/
│   └── note1.md        ←→       │   └── note1.ipynb
├── 02-R绘图模板/                ├── 02-R绘图模板/
│   ├── ggplot2/                 │   ├── ggplot2/
│   │   └── template1.md ←→     │   │   └── template1.ipynb
│   └── base-R/                  │   └── base-R/
│       └── template2.md ←→      │       └── template2.ipynb
└── 03-SCI图表/                  └── 03-SCI图表/
    └── chart1.md       ←→          └── chart1.ipynb
```

输出目录会**镜像源目录的结构**，方便你在 JupyterLab 中保持相同的目录组织。

## 🔧 同步机制

### 状态流转

```
⬜ 未配对 ──创建配对──→ ✅ 已配对
                        ↕ 改动
                   🟡 MD已更新 ──同步──→ ✅ 已配对
                   🔵 NB已更新 ──同步──→ ✅ 已配对
                   🔴 冲突   ──手动选择──→ ✅ 已配对
```

### 自动同步逻辑

| 触发条件 | 动作 |
|----------|------|
| 在 Obsidian 中保存 MD | 自动同步到 ipynb |
| 在 JupyterLab 中保存 Notebook | 自动同步到 MD |
| 两边都改了 | 标记冲突，等待手动解决 |

### 防抖机制

文件保存可能在短时间内触发多个事件，使用 1.5 秒防抖间隔合并重复事件。

同时内置**循环同步防护**：同步操作触发的文件变更不会被再次同步。

## ⚙️ 设置

点击 GUI 中的 **⚙️ 设置** 按钮可配置：

| 设置项 | 默认值 | 说明 |
|--------|--------|------|
| MD 格式 | myst | MyST 支持代码块标记，推荐 |
| 自动同步 | 开启 | 实时监控模式 |
| 跳过已配对 | 开启 | 批量操作时跳过 |
| 防抖间隔 | 1.5 秒 | 文件变更检测间隔 |
| 冲突处理 | 每次询问 | ask / md / ipynb |
| 自动打开 JupyterLab | 关闭 | 配对后是否自动启动 |

配置文件保存在 `~/.md2ipynb_sync/config.yaml`。

## 🔗 JupyterLab 集成

本工具创建的 ipynb 文件包含 Jupytext 元数据，在 JupyterLab 中安装 Jupytext 扩展后可直接识别：

```bash
# 安装 Jupytext 的 JupyterLab 扩展
pip install jupytext
```

在 JupyterLab 中打开 ipynb 文件时，Jupytext 会自动识别与 MD 文件的配对关系。

## 🛠️ 常见问题

### Q: MD 文件中的 Obsidian 特殊语法会被转换吗？

不会。MyST 格式会将 Obsidian 的 `[[双链]]`、`#标签`、Callout 语法等作为文本原样保留在 Notebook 的 Markdown 单元格中。

### Q: 输出目录可以放在源目录内吗？

不可以。这会导致 watchdog 递归监控，工具会自动检测并提示错误。

### Q: 冲突了怎么办？

双击冲突文件行或右键选择「解决冲突」，会弹出对比窗口，让你选择以 MD 还是 Notebook 为准。

### Q: 支持其他 Markdown 格式吗？

支持 `myst`（推荐）和 `markdown` 两种格式。MyST 能精确标记代码单元格边界，是 Jupytext 官方推荐的格式。

## 📄 许可证

MIT License
