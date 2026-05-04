# 🚀 Academic Group Meeting Pipeline (学术组会汇报流水线)

> 一句话启动 → 7 个 AI Agent 协作 → 完整组会汇报材料包（含 PPT）

[English](#english) | [中文](#简介)

---

## 简介

这是一套专为**学术文献组会汇报**设计的 **WorkBuddy AI Skill 流水线** v2.0。灵感来自「全息学术」公众号的方法论，经过工程化改造，将论文从 PDF 到完整汇报材料的全流程自动化。

### 核心能力

```
📄 论文 PDF
    │
    ├── Phase 1: 论文深读引擎（防信息幻觉）
    │   PDF全文提取 → 结构化解读（文本+图表+表格+公式）
    │
    ├── Phase 2: 逻辑解构师
    │   提取 4 大核心支柱：理论盲区 / 方法论创新 / 核心机制 / 致命缺陷
    │
    ├── Phase 3: 并行处理
    │   ├─ PPT架构师 → 10页视觉蓝图 + slides_data.json
    │   └─ 方法论刺客 → 2条原创致命批判
    │
    ├── Phase 4: 逐字稿大牛
    │   融合蓝图+批判 → 自然口语化逐字稿（含丝滑转场词）
    │
    ├── Phase 5: Q&A防御系统
    │   预测3个刁钻导师问题 + 完美防御话术 + 紧急预案
    │
    └── Phase 6: PPT实现（三引擎可选）
        ├─ C3: 学术工坊 ⭐推荐（.pptx + 逐字稿 + Q&A 一站式）
        ├─ C1: .pptx 浙大蓝模板（python-pptx，可编辑可分发）
        └─ C2: 网页PPT（Vite前端引擎，视觉精美有动画）
```

### 最终交付物

| # | 文件 | 内容 |
|---|------|------|
| 1 | `00_论文深度解读.md` | 完整的结构化解读报告 |
| 2 | `01_逻辑骨架解构报告.md` | 4大核心支柱 |
| 3 | `02_PPT视觉架构蓝图.md` | 10页逐页大纲 |
| 4 | `03_方法论刺客报告.md` | 2条致命批判 |
| 5 | `04_汇报逐字稿(完整版).md` | 口语化讲稿 |
| 6 | `05_Q&A防御作弊条.md` | 答辩备忘录 |
| **7** | **`xxx_组会汇报.pptx`** | **真实PPT文件(C1/C3)** |
| **8** | **`frontend/`** | **网页版PPT项目(C2)** |

---

## 📦 包含的 Skills

| # | Skill 名称 | 文件夹 | 定位 |
|---|-----------|--------|------|
| A | [paper-deep-read](#) *(依赖)* | _(需单独安装)_ | PDF 深度解读引擎 |
| B1 | **paper-logic-deconstructor** | `skills/paper-logic-deconstructor/` | 🧬 论文底层逻辑解构师 |
| B2 | **ppt-architect** | `skills/ppt-architect/` | 🎨 PPT 视觉架构师（含浙大蓝layout骨架+设计令牌） |
| B3 | **methodology-critic** | `skills/methodology-critic/` | 🗡️ 方法论刺客 |
| B4 | **speech-writer** | `skills/speech-writer/` | 🎙️ 逐字稿大牛 |
| B5 | **qa-defense-system** | `skills/qa-defense-system/` | 🛡️ 防御系统 |
| C1 | **ppt-implement** | `skills/ppt-implement/` | 🎬 .pptx 文件生成器（含build_pptx.py模板） |
| **主控** | **group-meeting-pipeline** | `skills/group-meeting-pipeline/` | 🚀 一键总控流水线 v2.0 |

---

## ⚡ 使用方式

### 触发命令

在 WorkBuddy 中输入任意一句：

```
"帮我用组会流水线做这篇论文的汇报材料和PPT"
"跑一下组会流水线"
"我要汇报这篇论文"
"一键组会模式"
```

然后提供论文 PDF 路径即可。

### 启动配置选项

| 项目 | 默认值 | 可选值 |
|------|-------|--------|
| 汇报时长 | 15-20分钟 | 10 / 25 / 30 分钟 |
| 听众类型 | 导师+同门 | 仅同门 / 开题答辩 / 学术会议 |
| 演讲风格 | 专业稳重型 | 轻松亲和 / 犀利自信 / 谦虚学习 |
| **PPT输出格式** | **学术工坊(.pptx+逐字稿+Q&A)** | **浙大蓝模板(.pptx)** / **网页PPT** / **两个都要** |
| 输出范围 | 全套材料 | 只要PPT / 只要逐字稿 / 全要 |
| 解读深度 | 复现级 | 概览级 |

---

## 🔧 安装

### 方式一：安装到 WorkBuddy Skills 目录

```bash
# 复制 skills/ 下所有文件夹到你的 WorkBuddy skills 目录
cp -r skills/* ~/.workbuddy/skills/
```

每个子文件夹包含一个 `SKILL.md`，即该 Skill 的完整指令定义。`ppt-architect` 和 `ppt-implement` 还包含 `references/` 目录下的设计令牌和模板脚本。

### 方式二：仅使用主控流水线

只需安装 `group-meeting-pipeline/SKILL.md` 即可一键启动全部流程（其他 Skill 作为依赖被自动调用）。

### 前置依赖

| 依赖 | 说明 |
|------|------|
| **@paper-deep-read** | 必须已安装（用于 Phase 1 PDF 深读） |
| **@academic-workshop** | 可选（用于 C3 学术工坊格式输出，默认推荐） |
| **@ppt-implement (插件原版)** | 可选（用于网页 PPT 格式输出） |
| Python 3.x + python-pptx | 用于 .pptx 文件格式输出 |

---

## 🏗️ 架构设计

### 三大子系统

```
┌──────────────────────────────────────────────┐
│         🚀 学术组会汇报全自动流水线 v2.0       │
│                                              │
│  Sub-A: 论文深读引擎 (@paper-deep-read)       │
│     PDF → 文本+图像+表格+公式 → 结构化解读     │
│                                              │
│  Sub-B: 组会汇报5件套引擎                     │
│     解构 → 蓝图+批判(并行) → 逐字稿 → Q&A     │
│                                              │
│  Sub-C: PPT实现引擎（三引擎可选）              │
│     C3: 学术工坊 → .pptx + 逐字稿 + Q&A ⭐   │
│     C1: python-pptx → .pptx                  │
│     C2: Vite前端引擎 → 网页PPT                │
└──────────────────────────────────────────────┘
```

### 核心设计原则

1. **绝不直接丢PDF给AI** — 先通过深读引擎提取和结构化，防止信息幻觉
2. **并行处理优化** — PPT蓝图和方法论批判无依赖关系，并行执行
3. **三引擎PPT输出** — 学术工坊(默认推荐)、浙大蓝模板(.pptx)、网页PPT
4. **图片自动嵌入** — 论文原图可自动嵌入PPT，支持python-pptx的add_picture()
5. **渐进式信息密度** — 从骨架→蓝图→逐字稿→Q&A，层层细化

---

## 💡 设计理念来源

本流水线的核心理念和方法论框架来源于：

> **全息学术 @学术AI大模型**
> "许多人在学术生涯中都体验过效率低下的文献组会...当汇报突然被导师打断，
> 并被质问'这项研究对我们课题组的下一步工作有何实质性启发'时，
> 我们往往会陷入语塞。"

在此基础上进行了以下工程增强：
- ✅ 新增 **Phase 0** 启动配置（时长/风格/格式选择）
- ✅ 接入 **@paper-deep-read** 解决 PDF 信息幻觉问题
- ✅ 增加 **Phase 6** 三引擎 PPT 输出（新增C3学术工坊）
- ✅ **ppt-architect** 新增浙大蓝layout骨架HTML + 设计令牌JSON
- ✅ **ppt-implement** 新增完整build_pptx.py脚本模板（支持图片嵌入）
- ✅ 完善各 Skill 间的数据接口协议
- ✅ 加入质量保障 Checkpoints 和异常预案

---

## 📁 项目结构

```
academic-group-meeting-pipeline/
│
├── README.md                    ← 本文件
├── LICENSE                      ← MIT 协议
│
└── skills/                      ← 所有 AI Skill 定义
    │
    ├── group-meeting-pipeline/  ← 🚀 主控：一键总控流水线 v2.0
    │   └── SKILL.md
    │
    ├── paper-logic-deconstructor/ ← B1: 论文逻辑解构
    │   └── SKILL.md
    │
    ├── ppt-architect/             ← B2: PPT视觉架构
    │   ├── SKILL.md
    │   └── references/            ← 浙大蓝设计资产
    │       ├── zju-blue-tokens.json      ← 设计令牌（颜色/字号/8种layout坐标）
    │       ├── zju-blue-measured-data.json ← 实测数据
    │       ├── zju-blue-image-spec.md     ← 图片处理规范
    │       └── zju-blue-layouts/          ← 8种layout的HTML骨架
    │           ├── F1-cover.html
    │           ├── F2-toc.html
    │           ├── F3-section-separator.html
    │           ├── F4-closing.html
    │           ├── C1-info.html
    │           ├── C2-image-text.html
    │           ├── C3-flowchart.html
    │           ├── C4-general.html
    │           └── index.md
    │
    ├── methodology-critic/        ← B3: 方法论批判
    │   └── SKILL.md
    │
    ├── speech-writer/             ← B4: 口语化逐字稿
    │   └── SKILL.md
    │
    ├── qa-defense-system/         ← B5: Q&A答辩防御
    │   └── SKILL.md
    │
    └── ppt-implement/             ← C1: .pptx文件生成器
        ├── SKILL.md
        └── references/
            └── build_pptx.py      ← 完整python-pptx生成脚本模板
```

---

## 🤝 贡献

欢迎 Issue 和 PR！特别是：
- 更多学科领域的适配模板
- PPT 视觉模板扩展
- 多语言支持

## License

MIT License © 2026

---

## English

### What is this?

A complete **AI-powered pipeline for academic group meeting presentations**, built as a collection of WorkBuddy Skills. It takes a research paper PDF and produces:

1. **Deep reading report** with extracted figures, tables, formulas
2. **Logic deconstruction** (4 core pillars)
3. **10-slide PPT blueprint** with takeaway headers
4. **Methodology critique** (2 original fatal flaws)
5. **Natural speech script** with smooth transitions
6. **Q&A defense cheat sheet** (3 predicted tough questions)
7. **Real PPT file** (.pptx or web-based, your choice)

### One Command to Run All

> "Help me prepare my group meeting presentation for this paper"

That's it. 7 AI agents collaborate behind the scenes.
