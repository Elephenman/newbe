# Paper Deep Read v3.0

**论文深度解读技能** — 面向生物信息学、生物学、AI/ML的学术论文Obsidian笔记生成器

将科学文献拆解为**初学者看完也能直接学会和复现**的 Obsidian 笔记，构建跨论文知识图谱。

## 核心特性

| 特性 | 说明 |
|------|------|
| **全可视化提取** | 从PDF提取Figure + Table + 公式截图，图文对照解读 |
| **Obsidian原生输出** | YAML frontmatter / 双链 / 标签 / Callout折叠块 / Dataview查询 |
| **渐进式分层** | 主体面向初学者，高级概念用Callout折叠块按需展开 |
| **生信专用模块** | 命令重现 / 分析流程Mermaid图 / 数据库资源汇总 / 统计方法解读 |
| **AI/ML专用模块** | 模型架构Mermaid可视化 / 训练流程 / Benchmark对比 |
| **全套质检体系** | 5阶段检查点 + 3轮自我批评 + 4维评分 |
| **知识库构建** | PaperVault目录 + MOC + 概念图谱 + 方法演进追踪 |

## 架构

```
paper-deep-read/
├── SKILL.md                          # 主入口：6阶段执行流程
├── config.json                       # 运行配置
├── agents/                           # 子代理定义
│   ├── extractor.md                  # PDF提取代理
│   ├── analyzer.md                   # 深度分析代理
│   ├── qa-reviewer.md               # QA审阅代理
│   └── knowledge-builder.md         # 知识库代理
├── scripts/                          # Python脚本
│   ├── pdf_extract.py               # 核心PDF提取引擎
│   ├── pdf_extract_tables.py        # 表格区域检测+裁剪
│   ├── pdf_extract_formulas.py      # 公式区域识别+裁剪
│   ├── obsidian_note_builder.py     # Obsidian笔记组装+验证
│   ├── vault_organizer.py           # PaperVault目录管理
│   └── knowledge_graph.py           # Mermaid概念图生成
├── references/                       # 深度参考文档
│   ├── bioinformatics-specials.md   # 生信专用功能
│   ├── ai-ml-specials.md            # AI/ML专用功能
│   ├── obsidian-format-guide.md     # Obsidian格式规范
│   ├── paper-type-adaptation.md     # 6种论文类型适配矩阵
│   ├── quality-standards.md         # 完整QA体系
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

## Obsidian输出示例

每篇论文笔记自动生成：

```yaml
---
title: "AlphaFold3: Accurate structure prediction..."
year: 2024
journal: "Nature"
paper_type: "computational"
domains: [bioinformatics, ai-ml, structural-biology]
methods: [diffusion model, attention mechanism]
tools: [AlphaFold3, HHblits]
tags: [type/computational, domain/bioinformatics, year/2024]
---
```

正文使用6种Callout块实现渐进式分层：

- `[!abstract]-` 一句话概括
- `[!info]-` 进阶概念（高级读者深入）
- `[!tip]-` 实践要点（可操作建议）
- `[!warning]-` 常见误区（初学者陷阱）
- `[!example]-` 代码复现（命令行/代码）
- `[!question]-` 思考题（延伸思考）

## 质检体系

**5阶段检查点**: 每个Phase转换时必须通过门条件

**3轮自我批评**:
1. 逻辑一致性 — 结论是否有数据支撑？证据链有无断裂？
2. 初学者可达性 — 能否不查外部资料理解？能否按描述复现？
3. 域专家深度 — 边界情况？局限性坦诚？比较公平？

**4维评分**（各1-5分，及格线3.5）: 可复现性 / 清晰度 / 完整性 / 深度

## 使用示例

```
"解读这篇文献 A:/papers/nature12345.pdf"
      → 6阶段完整流程 → Obsidian笔记到PaperVault

"解读这个PDF，重点看方法，要能复现的那种"
      → 侧重方法学模块，[!example]代码复现优先

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
| `quality.min_score` | 3.5 | QA及格线 |
| `extraction.batch_size` | 8 | 长论文分批大小 |
| `extraction.extract_formulas` | true | 是否提取公式截图 |
| `vault.root` | "" | PaperVault路径 |

## 许可

MIT
