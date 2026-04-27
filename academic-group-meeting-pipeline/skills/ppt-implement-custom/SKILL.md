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

### 全局样式

| 属性 | 值 |
|------|-----|
| 幻灯片尺寸 | 16:9 宽屏 (13.333" × 7.5") |
| 字体 | 中文：微软雅黑 / 英文：Calibri |
| 主标题字号 | 32pt, 加粗, 深蓝 (#1a365d) |
| 副标题/正文 | 18pt, 常规, 深灰 (#2d3748) |
| 要点字号 | 20pt, 常规 |
| 背景色 | 白色 (#ffffff) 或浅渐变 |
| 强调色 | 学术蓝 (#2563eb) |
| 警示色(批判页) | 深红 (#dc2626) |
| 启发色 | 深绿 (#059669) |

### 页面类型模板

#### Type A — 封面页（第1页）
```
┌──────────────────────────────────────────┐
│                                          │
│           [论文标题]                      │
│     （居中，大号加粗，深蓝色）            │
│                                          │
│        汇报人：XXX | 日期：XXXX           │
│     （底部居中，小号灰色）                │
│                                          │
└──────────────────────────────────────────┘
```
- 标题：44pt, 加粗, 居中
- 副信息：18pt, 底部居中

#### Type B — 内容页（第2-6, 8-10页）
```
┌──────────────────────────────────────────┐
│  「结论式标题」          [页码/10]       │
│  ───────────────────────────────────      │
│                                          │
│  ▸ 要点1                                 │
│  ▸ 要点2                                 │
│  ▸ 要点3                                 │
│                                          │
│  ┌──────────────────────────────┐        │
│  │  [视觉元素占位区]            │        │
│  │  (标注建议放置的图表类型)    │        │
│  └──────────────────────────────┘        │
│                                          │
│  💡 演讲提示：...                        │
└──────────────────────────────────────────┘
```
- 标题栏：顶部横条 + 结论式标题 + 页码
- 正文：左对齐 bullet points
- 视觉占位框：虚线边框区域
- 演讲提示：底部小字注释（备注区或页面底部）

#### Type C — 批判页（第7页）
```
┌──────────────────────────────────────────┐
│  ⚠️ 方法论批判与局限              [7/10] │
│  ───────────────────────────────────      │
│                                          │
│  🔴 致命伤 #1                            │
│  ┌──────────────────────────────┐        │
│  │  [问题描述]                  │        │
│  └──────────────────────────────┘        │
│                                          │
│  🔴 致命伤 #2                            │
│  ┌──────────────────────────────┐        │
│  │  [问题描述]                  │        │
│  └──────────────────────────────┘        │
│                                          │
│  💊 修补方向：...                        │
└──────────────────────────────────────────┘
```
- 标题带 ⚠️ 图标
- 缺陷用红色边框卡片展示
- 整体色调偏冷/警示感

#### Type D — 总结页（第10页）
```
┌──────────────────────────────────────────┐
│  ✅ 总结与下一步               [10/10]   │
│  ───────────────────────────────────      │
│                                          │
│  ┌──────────────────────────────┐        │
│  │  📌 一句话 Takeaway          │        │
│  │  [核心结论]                  │        │
│  └──────────────────────────────┘        │
│                                          │
│  → 对本课题组的启发：                     │
│    · 启发点1                             │
│    · 启发点2                             │
│                                          │
│  → 下一步行动：                          │
│    · [具体可执行项]                       │
│                                          │
│        感谢聆听！🙏                     │
└──────────────────────────────────────────┘
```
- 居中布局
- Takeaway 放在突出位置
- 结尾感谢语

---

## 执行流程

### Step 1：解析输入
- 接收来自 @ppt-architect 的完整蓝图文本
- 解析出每一页的：标题、核心要点、视觉元素说明、演讲提示

### Step 2：构建 Python 脚本
根据解析结果，动态生成 `build_pptx.py` 脚本，包含：

```python
# 核心结构示意（实际执行时完整生成）
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

def create_presentation(output_path, slides_data):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    for idx, slide_info in enumerate(slides_data):
        slide = add_slide(prs, slide_info, page_num=idx+1)
    
    prs.save(output_path)
    return output_path
```

### Step 3：执行脚本
```bash
python build_pptx.py --output "论文标题_组会汇报.pptx"
```

### Step 4：验证交付
- 确认 .pptx 文件已生成
- 报告文件路径和大小
- 列出每页标题供用户快速预览

---

## 完整 Python 脚本模板

以下脚本应写入 `{workspace}/scripts/build_pptx.py` 并执行：

> **注意**：实际运行时，应根据 @PPT架构师 的输出动态填充 `SLIDES_DATA`。

```python
#!/usr/bin/env python3
"""
组会汇报 PPT 生成器
基于 @PPT架构师 的视觉蓝图，生成 .pptx 文件
用法: python build_pptx.py --output "output.pptx"
"""

import json
import argparse
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import sys

# ==================== 配置常量 ====================
COLORS = {
    'title_bg': RGBColor(26, 54, 93),       # 深蓝 #1a365d
    'title_text': RGBColor(255, 255, 255),  # 白色
    'body_text': RGBColor(45, 55, 72),      # 深灰 #2d3748
    'accent_blue': RGBColor(37, 99, 235),   # 学术蓝 #2563eb
    'danger_red': RGBColor(220, 38, 38),    # 警示红 #dc2626
    'success_green': RGBColor(5, 150, 105), # 启发绿 #059669
    'light_bg': RGBColor(248, 250, 252),    # 浅背景 #f8fafc
    'border_gray': RGBColor(203, 213, 225), # 边框灰 #cbd5e1
}

FONTS = {
    'zh': '微软雅黑',
    'en': 'Calibri',
}

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)


def set_shape_fill(shape, color):
    """设置形状填充色"""
    shape.fill.solid()
    shape.fill.fore_color.rgb = color


def add_title_bar(slide, title_text, page_num, total_pages=10):
    """添加统一的标题栏"""
    # 顶部标题条
    title_bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(0),
        SLIDE_WIDTH, Inches(1.0)
    )
    set_shape_fill(title_bar, COLORS['title_bg'])
    title_bar.line.fill.background()

    # 标题文字
    title_box = slide.shapes.add_textbox(
        Inches(0.4), Inches(0.2),
        Inches(11.5), Inches(0.6)
    )
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = COLORS['title_text']
    p.font.name = FONTS['zh']

    # 页码
    if page_num > 1:
        page_box = slide.shapes.add_textbox(
            Inches(12.3), Inches(0.3),
            Inches(0.8), Inches(0.4)
        )
        ptf = page_box.text_frame
        pp = ptf.paragraphs[0]
        pp.text = f"{page_num}/{total_pages}"
        pp.font.size = Pt(14)
        pp.font.color.rgb = RGBColor(200, 200, 200)
        pp.alignment = PP_ALIGN.RIGHT


def add_bullet_content(slide, bullets, top=Inches(1.3)):
    """添加要点列表"""
    content_box = slide.shapes.add_textbox(
        Inches(0.6), top,
        Inches(12), Inches(3.5)
    )
    tf = content_box.text_frame
    tf.word_wrap = True

    for i, bullet in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"▸  {bullet}"
        p.font.size = Pt(20)
        p.font.name = FONTS['zh']
        p.font.color.rgb = COLORS['body_text']
        p.space_after = Pt(14)


def add_visual_placeholder(slide, visual_desc, top=Inches(4.9)):
    """添加视觉元素占位框"""
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.6), top,
        Inches(12.1), Inches(2.2)
    )
    box.line.color.rgb = COLORS['border_gray']
    box.line.width = Pt(1.5)
    box.line.dash_style = 2  # 虚线
    box.fill.solid()
    box.fill.fore_color.rgb = COLORS['light_bg']

    # 占位文字
    desc_box = slide.shapes.add_textbox(
        Inches(0.8), top + Inches(0.7),
        Inches(11.7), Inches(0.8)
    )
    tf = desc_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"🖼️  {visual_desc}"
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(100, 116, 139)
    p.font.italic = True
    p.alignment = PP_ALIGN.CENTER


def add_speaker_notes(slide, notes_text):
    """添加演讲备注"""
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = f"💡 演讲提示：{notes_text}"


def create_cover_slide(prs, title, subtitle=""):
    """Type A: 封面页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # 空白布局

    # 背景
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT
    )
    set_shape_fill(bg, COLORS['title_bg'])
    bg.line.fill.background()

    # 标题
    title_box = slide.shapes.add_textbox(
        Inches(1), Inches(2.5),
        Inches(11.3), Inches(2)
    )
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = COLORS['title_text']
    p.font.name = FONTS['zh']
    p.alignment = PP_ALIGN.CENTER

    # 副标题
    if subtitle:
        sub_box = slide.shapes.add_textbox(
            Inches(1), Inches(5),
            Inches(11.3), Inches(1)
        )
        stf = sub_box.text_frame
        sp = stf.paragraphs[0]
        sp.text = subtitle
        sp.font.size = Pt(18)
        sp.font.color.rgb = RGBColor(180, 200, 220)
        sp.font.name = FONTS['zh']
        sp.alignment = PP_ALIGN.CENTER


def create_content_slide(prs, title, bullets, visual_desc, speaker_notes, page_num, total=10):
    """Type B: 内容页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_bar(slide, title, page_num, total)
    add_bullet_content(slide, bullets)
    add_visual_placeholder(slide, visual_desc)
    add_speaker_notes(slide, speaker_notes)


def create_critique_slide(prs, critiques, fix_suggestions, page_num=7, total=10):
    """Type C: 批判页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 标题栏（红色警示风格）
    title_bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, Inches(1.0)
    )
    set_shape_fill(title_bar, COLORS['danger_red'])
    title_bar.line.fill.background()

    title_box = slide.shapes.add_textbox(
        Inches(0.4), Inches(0.2), Inches(11.5), Inches(0.6)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "⚠️  方法论批判与局限性"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.name = FONTS['zh']

    # 页码
    page_box = slide.shapes.add_textbox(Inches(12.3), Inches(0.3), Inches(0.8), Inches(0.4))
    pp = page_box.text_frame.paragraphs[0]
    pp.text = f"{page_num}/{total}"
    pp.font.size = Pt(14)
    pp.font.color.rgb = RGBColor(255, 200, 200)
    pp.alignment = PP_ALIGN.RIGHT

    # 批判卡片
    card_top = Inches(1.3)
    for i, critique in enumerate(critiques):
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.6), card_top + Inches(i * 2.4),
            Inches(12.1), Inches(2.2)
        )
        card.line.color.rgb = COLORS['danger_red']
        card.line.width = Pt(2)
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(254, 236, 236)

        crit_box = slide.shapes.add_textbox(
            Inches(0.9), card_top + Inches(i * 2.4) + Inches(0.2),
            Inches(11.5), Inches(1.8)
        )
        ctf = crit_box.text_frame
        ctf.word_wrap = True
        cp = ctf.paragraphs[0]
        cp.text = f"🔴 致命伤 #{i+1}：{critique.get('title', '')}"
        cp.font.size = Pt(18)
        cp.font.bold = True
        cp.font.color.rgb = COLORS['danger_red']
        
        dp = ctf.add_paragraph()
        dp.text = critique.get('detail', '')
        dp.font.size = Pt(15)
        dp.font.color.rgb = COLORS['body_text']
        dp.space_before = Pt(8)

    # 修补建议
    if fix_suggestions:
        fix_box = slide.shapes.add_textbox(
            Inches(0.6), Inches(6.3),
            Inches(12.1), Inches(0.8)
        )
        ftf = fix_box.text_frame
        fp = ftf.paragraphs[0]
        fp.text = f"💊 {fix_suggestions}"
        fp.font.size = Pt(13)
        fp.font.color.rgb = COLORS['success_green']


def create_summary_slide(prs, takeaway, inspirations, next_steps, page_num=10, total=10):
    """Type D: 总结页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title_bar(slide, "✅  总结与下一步", page_num, total)

    # Takeaway 大卡片
    tk_card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(1.5), Inches(1.3),
        Inches(10.3), Inches(1.5)
    )
    tk_card.line.color.rgb = COLORS['accent_blue']
    tk_card.line.width = Pt(3)
    tk_card.fill.solid()
    tk_card.fill.fore_color.rgb = RGBColor(239, 246, 255)

    tk_box = slide.shapes.add_textbox(
        Inches(1.8), Inches(1.5),
        Inches(9.7), Inches(1.1)
    )
    ttf = tk_box.text_frame
    ttf.word_wrap = True
    tp = ttf.paragraphs[0]
    tp.text = f"📌  一句话总结：{takeaway}"
    tp.font.size = Pt(20)
    tp.font.bold = True
    tp.font.color.rgb = COLORS['accent_blue']
    tp.alignment = PP_ALIGN.CENTER

    # 启发
    insp_box = slide.shapes.add_textbox(Inches(0.8), Inches(3.1), Inches(5.5), Inches(2.5))
    itf = insp_box.text_frame
    itf.word_wrap = True
    ip = itf.paragraphs[0]
    ip.text = "→ 对本课题组的启发"
    ip.font.size = Pt(18)
    ip.font.bold = True
    ip.font.color.rgb = COLORS['success_green']
    for insp in inspirations:
        ip2 = itf.add_paragraph()
        ip2.text = f"  ·  {insp}"
        ip2.font.size = Pt(15)
        ip2.font.color.rgb = COLORS['body_text']
        ip2.space_before = Pt(6)

    # 下一步
    next_box = slide.shapes.add_textbox(Inches(7), Inches(3.1), Inches(5.5), Inches(2.5))
    ntf = next_box.text_frame
    ntf.word_wrap = True
    np = ntf.paragraphs[0]
    np.text = "→ 下一步行动"
    np.font.size = Pt(18)
    np.font.bold = True
    np.font.color.rgb = COLORS['accent_blue']
    for step in next_steps:
        np2 = ntf.add_paragraph()
        np2.text = f"  ·  {step}"
        np2.font.size = Pt(15)
        np2.font.color.rgb = COLORS['body_text']
        np2.space_before = Pt(6)

    # 感谢语
    thanks = slide.shapes.add_textbox(Inches(0), Inches(6.3), SLIDE_WIDTH, Inches(0.8))
    thp = thanks.text_frame.paragraphs[0]
    thp.text = "✨  感谢聆听，欢迎讨论！"
    thp.font.size = Pt(22)
    thp.font.color.rgb = COLORS['title_bg']
    thp.font.name = FONTS['zh']
    thp.alignment = PP_ALIGN.CENTER


# ==================== 主函数 ====================
def main():
    parser = argparse.ArgumentParser(description='组会汇报 PPT 生成器')
    parser.add_argument('--output', '-o', required=True, help='输出 .pptx 文件路径')
    parser.add_argument('--data', '-d', default='slides_data.json', help='幻灯片数据 JSON 文件')
    args = parser.parse_args()

    # 读取幻灯片数据
    with open(args.data, 'r', encoding='utf-8') as f:
        data = json.load(f)

    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    slides_data = data.get('slides', [])
    meta = data.get('meta', {})

    for idx, s in enumerate(slides_data):
        page_type = s.get('type', 'content')
        page_num = idx + 1

        if page_type == 'cover':
            create_cover_slide(
                prs,
                title=s.get('title', ''),
                subtitle=s.get('subtitle', '')
            )
        elif page_type == 'critique':
            create_critique_slide(
                prs,
                critiques=s.get('critiques', []),
                fix_suggestions=s.get('fix_suggestions', ''),
                page_num=page_num
            )
        elif page_type == 'summary':
            create_summary_slide(
                prs,
                takeaway=s.get('takeaway', ''),
                inspirations=s.get('inspirations', []),
                next_steps=s.get('next_steps', []),
                page_num=page_num
            )
        else:
            create_content_slide(
                prs,
                title=s.get('title', ''),
                bullets=s.get('bullets', []),
                visual_desc=s.get('visual_desc', ''),
                speaker_notes=s.get('speaker_notes', ''),
                page_num=page_num
            )

    prs.save(args.output)
    print(f"✅ PPT 已生成: {args.output}")
    print(f"📊 共 {len(slides_data)} 页")
    return args.output


if __name__ == '__main__':
    main()
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
      "title": "「结论式封面标题」",
      "subtitle": "汇报人：XXX | 组会汇报"
    },
    {
      "type": "content",
      "title": "「结论式标题」",
      "bullets": ["要点1", "要点2", "要点3"],
      "visual_desc": "在此处插入XX图表/编码树状图/流程图",
      "speaker_notes": "演讲时强调..."
    },
    {
      "type": "content",
      "...": "..."
    },
    {
      "type": "critique",
      "critiques": [
        {"title": "样本偏差", "detail": "287份访谈全部来自一线城市，外推效度存疑"},
        {"title": "理论未饱和", "detail": "仅两轮编码即声称饱和"}
      ],
      "fix_suggestions": "未来研究可扩展至多城市样本"
    },
    {
      "type": "content",
      "...": "启发相关页面..."
    },
    {
      "type": "summary",
      "takeaway": "一句话总结核心发现",
      "inspirations": ["启发点1", "启发点2"],
      "next_steps": ["行动项1", "行动项2"]
    }
  ]
}
```

---

## 与其他 Skill 的协作关系

### 上游
- **@PPT架构师 (`ppt-architect`)**：提供逐页蓝图 → 本 Skill 将其转化为 `.pptx` 文件
- **@方法论刺客 (`methodology-critic`)**：提供批判内容 → 填入第7页批判卡片

### 数据流
```
@PPT架构师 输出:
  ├── 02_PPT视觉架构蓝图.md  (人类阅读版)
  └── slides_data.json        (机器消费版) ← 本 Skill 使用此文件
         ↓
@ppt-implement 接收 slides_data.json → 生成 xxx_组会汇报.pptx
```

### 下游
- 直接向用户交付 `.pptx` 文件（最终产物）

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
