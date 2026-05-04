---
name: ppt-implement
description: PPT生成实现、PPTX文件创建、学术PPT制作、PowerPoint自动化、大纲转PPT、python-pptx生成幻灯片、学术汇报PPT文件输出
---

# 🎬 PPT 实现器 — 从蓝图到真实 .pptx

## 角色定义
您是**专业的 PPT 工程师**。您的任务是将 `@PPT架构师` 生成的逐页视觉蓝图，通过 `python-pptx` 库渲染为**可直接使用的 .pptx 文件**。

## 核心使命
**不要只给用户一个文字大纲 —— 给他们一个打开就能用的 PowerPoint 文件。**

---

## 技术栈

| 组件 | 用途 |
|------|------|
| **python-pptx** | PPTX 文件生成（核心引擎） |
| **Python 3.x** | 脚本执行环境 |

### 环境准备

每次执行前，先检测 Python 环境：
```bash
where python >nul 2>nul && python --version
```

检查/安装依赖：
```bash
pip install python-pptx -q
```

---

## 输入规范

接收来自 **@PPT架构师 (ppt-architect)** 的输出，格式为：

```markdown
### 第 X 页：「结论式标题」
- **视觉元素**：[具体说明放什么图/表/代码]
- **核心要点**（不超过3个bullet）：
  - [要点1]
  - [要点2]
  - [要点3]
- **演讲提示**：[这一页要强调什么]
```

---

## PPT 设计规范

### 全局样式（浙大蓝实测值）

| 属性 | 值 | 来源 |
|------|-----|------|
| 幻灯片尺寸 | 960pt × 540pt (16:9) | tokens.json |
| 字体 | 中文：微软雅黑 / 英文：Calibri | tokens.json |
| 主标题字号 | 44pt, 加粗, 浙大蓝 (#003F88) | tokens.json |
| 内容标题字号 | 24pt, 加粗, 浙大蓝 (#003F88) | tokens.json |
| 内容正文字号 | 16pt, 常规, 深灰蓝 (#44546A) | tokens.json |
| 标题栏高度 | ≈49pt | tokens.json |
| 页码footer | y=500.5pt, 右侧706pt | tokens.json |
| 网格基准 | 36pt | tokens.json |
| 浙大蓝 | #003F88 (SCHEME主色) | tokens.json |
| 警示橙 | #ED7D31 | tokens.json |
| 辅助蓝 | #5B9BD5 | tokens.json |
| 高光金 | #FFC000 | tokens.json |
| 正向绿 | #70AD47 | tokens.json |
| 批判红 | #C00000 | tokens.json |
| 深灰蓝 | #44546A | tokens.json |

### 页面类型模板（8种Layout变体）

> 所有layout变体基于 `ppt-architect/references/zju-blue-tokens.json` 实测数据，坐标精确到pt。

| 变体ID | 名称 | 描述 |
|--------|------|------|
| F1-cover | 封面页 | 白底+校徽+大标题+文献标签+底部栏(汇报人+时间) |
| F2-toc | 目录页 | 右上"目录"区+编号圆角矩形+论文标题列表 |
| F3-section-separator | 章节分隔页 | 右上大字编号+PART标签+编号列表 |
| F4-ending | 结尾致谢页 | 类似封面，大字"谢谢聆听" |
| C1-info | 文献基本信息页 | 标题栏+左图+右表+关键词+底部内容 |
| C2-image-text | 左图右文页 | 标题栏+左大图+右双栏(背景+意义) |
| C3-flowchart | 流程图页 | 标题栏+椭圆节点+箭头+标签条 |
| C4-general | 通用内容页 | 标题栏+灵活内容区(图表/结果/讨论) |

---

## 执行流程

### Step 1：解析与验证输入
- 接收来自 @ppt-architect 的 `slides_data.json`
- 调用 `validate_slides_data()` 验证JSON schema（P2-9）
- 若提供 `layout_selection.json`，合并到 `slides_data.json` 的对应slide

### Step 2：确定路线
- **路线A（模板克隆）**：若 `--template` 参数指向有效模板文件 → 打开模板，按layout变体克隆slide
- **路线B（纯绘制）**：无模板时 → 用 `LAYOUT_COORDS` 实测坐标从空白slide创建所有元素

### Step 3：执行生成
```bash
# 路线B（纯绘制，默认）
python references/build_pptx.py --output "论文标题_组会汇报.pptx" --data slides_data.json --images-dir images/

# 路线A（模板克隆，需提供模板）
python references/build_pptx.py --output "论文标题_组会汇报.pptx" --data slides_data.json --template "浙大蓝-多篇版.pptx" --images-dir images/
```

### Step 4：验证交付
- 确认 .pptx 文件已生成
- 报告文件路径和大小
- 列出每页标题供用户快速预览

---

## 完整 Python 脚本模板

以下脚本位于 `references/build_pptx.py`，完整代码请查看该文件。

> **⚠️ 修复记录**：
> - P0-1: 所有create_*_slide函数现在接受`coords`参数并使用`LAYOUT_COORDS`（而非硬编码Inches值）
> - P0-2: `LAYOUT_COORDS`坐标全部来自`tokens.json`实测值（如F1标题left=105.43而非36）
> - P0-3: `create_cover_slide`改为浙大蓝F1样式（白底+校徽+大标题+文献标签+底部栏）
> - P1-4: `--template`参数现在有实际功能（模板克隆路线A，XML深拷贝）
> - P1-5: `slides_data.json`支持`image_path`字段，`--images-dir`指定基目录，实际嵌入论文图片
> - P2-9: 增加`validate_slides_data()` schema验证
> - P2-10: F1 `LAYOUT_COORDS`包含完整元素（分隔线/文献标签/底部栏/竖线等）
> - P2-13: `pt_to_emu()`被`add_textbox_at_coords`等函数广泛使用，不再是死代码

```python
# 核心架构示意（完整代码见 references/build_pptx.py）

from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# LAYOUT_COORDS: 8种变体×实测坐标(pt->EMU×12700)
# COLORS: 浙大蓝配色(来自tokens.json)
# 双路线: 路线A(模板克隆) vs 路线B(纯绘制)

def create_cover_slide(prs, title, subtitle="", presenter="", date_str="", coords=None):
    """F1-cover: 白底+校徽+大标题+文献标签+底部栏"""
    # 使用coords中的实测坐标放置每个元素
    ...

def create_info_slide(prs, section_num, section_title, image_path=None, ...):
    """C1-info: 标题栏+左图+右表+关键词+底部内容"""
    # image_path有图则嵌入，无图则占位框
    ...

def main():
    # --data: slides_data.json
    # --template: 浙大蓝模板.pptx(可选)
    # --images-dir: 论文图片目录(可选)
    # Schema验证 -> 合并layout -> 按layout_id路由到对应create_*函数
    ...
```

---

## 数据接口格式

`@PPT架构师` 在输出蓝图的同时，需要额外输出一份 `slides_data.json`，格式如下：

```json
{
  "meta": {
    "paper_title": "[论文名]",
    "presenter": "[汇报人]",
    "date": "2026-04-17",
    "total_pages": 10
  },
  "slides": [
    {
      "type": "cover",
      "layout": "F1-cover",
      "title": "「结论式封面标题」",
      "subtitle": "文献一标题|文献二标题|文献三标题",
      "presenter": "汇报人：XXX",
      "date_str": "2026-05-01"
    },
    {
      "type": "toc",
      "layout": "F2-toc",
      "title": "「目录」",
      "items": ["章节1", "章节2", "章节3", "章节4"]
    },
    {
      "type": "section_separator",
      "layout": "F3-section-separator",
      "section_num": "1",
      "section_label": "PART ONE",
      "items": ["文献1标题", "文献2标题", "文献3标题"]
    },
    {
      "type": "content",
      "layout": "C1-info",
      "section_num": "1.1",
      "title": "「文献基本信息」",
      "image_path": "images/fig1.png",
      "table_data": "期刊: Nature | 年份: 2025 | ...",
      "keywords": ["关键词1", "关键词2", "关键词3", "关键词4"],
      "bottom_text": "主要研究内容描述..."
    },
    {
      "type": "content",
      "layout": "C2-image-text",
      "section_num": "1.2",
      "title": "「结论式标题」",
      "image_path": "images/fig2.png",
      "right_col1_title": "研究背景",
      "right_col1_text": "背景描述...",
      "right_col2_title": "研究意义",
      "right_col2_text": "意义描述...",
      "caption": "图1 实验设计示意图"
    },
    {
      "type": "content",
      "layout": "C3-flowchart",
      "section_num": "1.3",
      "title": "「方法流程」",
      "flow_items": ["数据收集", "预处理", "模型训练", "验证"]
    },
    {
      "type": "critique",
      "layout": "C4-general",
      "section_num": "2.1",
      "title": "方法论批判与局限",
      "critiques": [
        {"title": "样本偏差", "detail": "287份访谈全部来自一线城市，外推效度存疑"},
        {"title": "理论未饱和", "detail": "仅两轮编码即声称饱和"}
      ],
      "fix_suggestions": "未来研究可扩展至多城市样本"
    },
    {
      "type": "content",
      "layout": "C4-general",
      "section_num": "2.2",
      "title": "「结论式标题」",
      "content_text": "▸ 要点1\n▸ 要点2\n▸ 要点3",
      "image_path": "images/fig3.png"
    },
    {
      "type": "summary",
      "layout": "C4-general",
      "section_num": "3",
      "title": "总结与下一步",
      "takeaway": "一句话总结核心发现",
      "inspirations": ["启发点1", "启发点2"],
      "next_steps": ["行动项1", "行动项2"]
    },
    {
      "type": "ending",
      "layout": "F4-ending"
    }
  ]
}
```

> **字段说明**：
> - **必须字段**：每页必须有 `type` 和 `layout` 字段
> - `type`：cover / toc / section_separator / content / critique / summary / ending
> - `layout`：取值为8种变体ID（如 `F1-cover`, `C2-image-text`），由 @ppt-architect 在生成蓝图时指定
> - `image_path`：P1-5 FIX 支持论文图片嵌入，路径相对于 `--images-dir` 参数指定的基目录
> - `section_num`/`section_title`：浙大蓝标题栏的编号和标题（如 "1.1" 和 "文献基本信息"）
> - 合并规则：若单独存在 `layout_selection.json`，构建时将其合并到 `slides_data.json` 的对应slide中
> - C1引擎通过此字段确定每页使用哪种浙大蓝layout变体的坐标映射
> - 合并规则：若单独存在 `layout_selection.json`，构建时将其合并到 `slides_data.json` 的对应slide中

---

## 与其他 Skill 的协作关系

### 上游
- **@PPT架构师 (`ppt-architect`)**：提供逐页蓝图 → 本 Skill 将其转化为 `.pptx` 文件
- **@方法论刺客 (`methodology-critic`)**：提供批判内容 → 填入批判页卡片

### 数据流
```
@PPT架构师 输出:
  ├── 02_PPT视觉架构蓝图.md  (人类阅读版)
  └── slides_data.json        (机器消费版) ← 本 Skill 使用此文件
         ↓
    @paper-deep-read 提取的论文图片:
  └── images/                  ← --images-dir 参数
         ↓
@ppt-implement 接收 slides_data.json + images/ → 生成 xxx_组会汇报.pptx
```

### 下游
- 直接向用户交付 `.pptx` 文件（最终产物）

### 架构选择
- **路线A（模板克隆）**：`--template` 指向浙大蓝模板 → XML深拷贝 → 替换文字 → 保留所有模板样式
- **路线B（纯绘制）**：无模板 → `LAYOUT_COORDS` 实测坐标 → 白底slide上绘制所有元素 → 浙大蓝配色

---

## 使用方式

### 触发词
- "生成 PPT 文件"
- "把大纲变成 PPT"
- "导出 .pptx"
- "实现 PPT"

### 单独调用
```
用户: "帮我生成这篇论文的组会汇报PPT"
→ 系统自动调用完整流水线 → 最终由本 Skill 输出 .pptx
```

### 作为流水线的一部分
本 Skill 通常作为 **Stage 2.5**（在 @PPT架构师 之后）被主控流水线自动调用。
