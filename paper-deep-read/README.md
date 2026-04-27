# Paper Deep Read v4.1

**论文深度解读技能** — 面向生物信息学、生物学、AI/ML的学术论文Obsidian笔记生成器

将科学文献拆解为**初学者看完也能直接学会和复现**的 Obsidian 笔记，构建跨论文知识图谱。

## 核心特性

| 特性 | 说明 |
|------|------|
| **⚠️原文caption对照** | Panel编号和子标题严格按论文原文Figure caption，绝不允许凭想象编造(v4.1最高优先级) |
| **全可视化提取** | 从PDF提取Figure + Table + 公式截图，图文对照解读 |
| **叙述流嵌入式解读** | Figure解读直接嵌入正文叙述流，像论文本身一样自然流畅，不需要展开/折叠 |
| **逻辑衔接5步闭环** | 发现→追问→设计→预期→验证，替代简单预告式推导语 |
| **★双重节点标记** | 既验证已知又揭示新方向的实验，含双预期逻辑衔接 |
| **🧪方法局限醒目标注** | 引用块格式+[[4.X]]跨Section链接，醒目且不打断阅读流 |
| **视觉层级清晰** | 结构标签冒号结尾 vs Panel标签破折号连接 vs 斜体caption |
| **解读70%/批判30%** | 正文解读句数 ≥ 2×批判句数，批判定位为补充视角 |
| **Obsidian原生输出** | YAML frontmatter / 双链 / 标签 / Callout折叠块 / Dataview查询 |
| **生信专用模块** | 命令重现 / 分析流程Mermaid图 / 数据库资源汇总 / 统计方法解读 |
| **AI/ML专用模块** | 模型架构Mermaid可视化 / 训练流程 / Benchmark对比 |
| **全套质检体系** | 5阶段检查点 + 3轮自我批评 + 4维评分 |
| **知识库构建** | PaperVault目录 + MOC + 概念图谱 + 方法演进追踪 |

## 架构

```
paper-deep-read-v3/
├── SKILL.md                          # 主入口：6阶段执行流程+生成规则
├── config.json                       # 运行配置(v4.0)
├── agents/                           # 子代理定义
│   ├── extractor.md                  # PDF提取代理
│   ├── analyzer.md                   # 深度分析代理(70/30权重+叙述流嵌入)
│   ├── qa-reviewer.md               # QA审阅代理(逻辑衔接5步闭环检查)
│   └── knowledge-builder.md         # 知识库代理
├── scripts/                          # Python脚本
│   ├── pdf_extract.py               # 核心PDF提取引擎
│   ├── pdf_extract_tables.py        # 表格区域检测+裁剪
│   ├── pdf_extract_formulas.py      # 公式区域识别+裁剪
│   ├── obsidian_note_builder.py     # Obsidian笔记组装+验证
│   ├── vault_organizer.py           # PaperVault目录管理
│   └── knowledge_graph.py           # Mermaid概念图生成
├── references/                       # 深度参考文档
│   ├── reading-guide.md             # ★新增：解读写作规范
│   ├── figure-interpretation-guide.md # ★新增：Figure解读规范
│   ├── critical-analysis-guide.md   # 批判性分析指南(补充视角定位)
│   ├── obsidian-format-guide.md     # Obsidian格式规范(v4.0)
│   ├── paper-type-adaptation.md     # 6种论文类型适配矩阵(Callout统一4+1)
│   ├── quality-standards.md         # 完整QA体系
│   ├── bioinformatics-specials.md   # 生信专用功能
│   ├── ai-ml-specials.md            # AI/ML专用功能
│   └── multi-paper-operations.md    # 多论文操作规范
└── templates/                        # Obsidian笔记模板
    ├── single-paper/                 # 单论文笔记+图像命名
    ├── comparison/                   # 多论文对比
    ├── knowledge-base/               # PaperVault+MOC+Dataview
    └── bioinformatics/               # 流水线+数据库模板
```

## 执行流程

```
Phase 1: PDF提取 → CP1(提取完整性) →
Phase 2: 论文类型识别 ★用户确认★ → CP2 →
Phase 3: 大纲生成 ★用户确认★ → CP3 →
Phase 4: 深度解读生成 → CP4(内容质量) →
Phase 5: QA审阅(3轮自我批评) → CP5(评分≥3.5) →
Phase 6: Obsidian输出(PaperVault放置)
```

## 6种论文类型适配

| 类型 | 重点模块 | 弱化模块 |
|------|----------|----------|
| 方法学论文 | 方法学详解、参数优化 | 背景和结论 |
| 发现型论文 | 结果详解、证据链分析 | 方法学细节 |
| 综述论文 | 领域全景、发展脉络 | 单一方法 |
| 数据库/资源论文 | 数据来源、使用方法 | 实验验证 |
| 计算/生信论文 | 命令重现、流程图、数据库 | 湿实验 |
| 结构生物学论文 | 结构解析流程、结构分析 | 功能验证 |

## 核心改进亮点(v4.0)

### 叙述流嵌入式Figure解读
- Figure解读直接嵌入正文叙述流（非Callout折叠）
- 排版：叙述 → 图片 → caption(斜体) → Panel解读 → 继续叙述
- 像论文本身一样自然流畅，不需要"展开→阅读→折叠→继续"

### 视觉层级清晰化
- 结构标签：`**实验目的：**` / `**核心发现：**` / `**逻辑衔接：**`（冒号结尾）
- Panel标签：`**Panel A — MEME motif logo**`（破折号连接）
- 斜体caption：`*图1 标题。(a)...(b)...*`
- 速览型读者一眼区分"正文定位"和"Figure解读"

### 逻辑衔接5步闭环
- ★转折点：完整5步（发现→追问→设计→预期→验证）
- （确认点）：简洁3步（追问→设计→验证）
- ★双重节点：5步+双预期（既确认又揭示）
- 替代简单预告式推导语——解释"为什么必须做下一个实验"

### 🧪方法局限醒目标注
- 通用局限：`> 🧪 方法局限：{{一句话+[[4.X Protocol]]链接}}`
- 真正硬伤：`[!critique]-` Callout（仅真正硬伤才有）
- 醒目引用块格式+跨Section链接

## Obsidian输出

正文使用5种Callout块实现渐进式分层：

- `[!abstract]-` 快读路径+Abstract
- `[!figure]-` 仅Supplementary/表格型Figure（核心Figure叙述流嵌入）
- `[!critique]-` 方法论硬伤（仅真正硬伤）
- `[!tip]-` 实践要点/方法Protocol
- `[!question]-` 思考题/研究裂变

通用方法局限用🧪引用块标注（醒目引用块格式+[[4.X]]链接）。

## 质检体系

**5阶段检查点**: 每个Phase转换时必须通过门条件

**3轮自我批评**:
1. 逻辑一致性 — 结论有数据支撑？逻辑衔接5步闭环完整？★双重节点标记正确？
2. 初学者可达性 — Figure嵌入叙述流？🧪标注醒目？视觉层级清晰？
3. 域专家深度 — 嵌入式批判到位？Discussion解读准确？[[4.X]]链接有效？

**4维评分**（各1-5分，及格线3.5）: 可复现性 / 清晰度 / 完整性 / 深度

## 使用示例

```
"解读这篇文献 A:/papers/nature12345.pdf"
      → 6阶段完整流程 → Obsidian笔记到PaperVault

"解读这个PDF，重点看方法，要能复现的那种"
      → 侧重方法学模块，复现级深度

"帮我解读这两篇论文并对比"
      → 各自解读 + 横向对比笔记

"构建CRISPR领域的知识图谱"
      → 概念关联图 + 方法演进图 + 工具生态图
```

## 依赖

- **Python**: pymupdf（PDF提取，自动安装）
- **Obsidian**: 推荐安装 Dataview 插件（查询支持）
- **输出目录**: PaperVault知识库（自动创建）

## 配置

编辑 `config.json` 自定义：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `defaults.read_depth` | "reproduction" | overview / reproduction |
| `defaults.figure_embed_mode` | "narrative-paragraph" | 叙述流嵌入 / Callout折叠 |
| `defaults.logical_transition_format` | "5-step-closure" | 逻辑衔接5步闭环 |
| `defaults.critique_mode` | "supplementary-perspective" | 批判补充视角 |
| `quality.min_score` | 3.5 | QA及格线 |
| `extraction.batch_size` | 8 | 长论文分批大小 |
| `vault.root` | "" | PaperVault路径 |

## 许可

MIT