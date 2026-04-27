---
name: paper-deep-read
version: 3.0.0
description: "深度解读科学文献，生成Obsidian笔记。支持生物信息学+生物学+AI/ML跨域解读，PDF全图像提取（Figure+Table+公式），渐进式内容分层，批量分析与知识图谱构建，全套质检体系。"
allowed-tools: Read Write Edit Bash Glob Grep Agent AskUserQuestion
tags: [论文解读, 学术阅读, Obsidian, 生物信息学, AI/ML, 知识图谱, PDF提取, 中文]
metadata:
  skill-author: "Claude Code Custom Skill"
  skill-version: "3.0.0"
  trigger-keywords: ["解读文献", "阅读论文", "分析文章", "拆解文献", "文献解读",
                      "read paper", "analyze paper", "deconstruct paper",
                      "深度解读", "论文分析", "批量解读", "知识图谱"]
---

# Paper Deep Read v3.0 — 论文深度解读技能

将科学文献拆解为**初学者看完也能直接学会和复现**的 Obsidian 笔记，构建跨论文知识图谱。

## 商业差异化

| 维度 | 本技能 | 竞品 |
|------|--------|------|
| 解读深度 | 复现级：初学者可独立复现实验 | 概要级：仅理解论文大意 |
| 图文对照 | 全可视化提取（Figure+Table+公式截图） | 仅文字描述或无图 |
| 领域适配 | 生信/生物学/AI-ML跨域专用模块 | 通用模板无领域深度 |
| 知识管理 | Obsidian双链+标签+Dataview，自动构建知识库 | 孤立文档无关联 |
| 质量保障 | 5阶段检查点+3轮自我批评+4维评分 | 无系统质检 |

---

## 触发条件

当用户请求中包含以下意图时自动激活：
- "解读这篇文献"、"阅读这个论文"、"分析这篇文章"
- "拆解这个PDF"、"帮我理解这篇paper"
- 提供PDF文件路径并要求解读/分析/总结
- "批量解读"、"对比这些论文"、"构建知识图谱"
- 任何涉及文献深度理解的需求

---

## 快速参考

| 文件 | 用途 |
|------|------|
| `config.json` | 运行配置：vault路径、默认深度、质检参数 |
| **代理 (agents/)** | |
| `agents/extractor.md` | PDF提取代理：文本+图像+表格+公式 |
| `agents/analyzer.md` | 深度分析代理：类型识别+结构分析+领域适配 |
| `agents/qa-reviewer.md` | QA审阅代理：检查点+自我批评+评分 |
| `agents/knowledge-builder.md` | 知识库代理：批量+对比+图谱 |
| **脚本 (scripts/)** | |
| `scripts/pdf_extract.py` | 核心PDF提取引擎 |
| `scripts/pdf_extract_tables.py` | 表格区域检测+裁剪 |
| `scripts/pdf_extract_formulas.py` | 公式区域识别+裁剪 |
| `scripts/obsidian_note_builder.py` | Obsidian笔记组装+验证 |
| `scripts/vault_organizer.py` | PaperVault目录管理 |
| `scripts/knowledge_graph.py` | Mermaid概念图生成 |
| **参考 (references/)** | |
| `references/bioinformatics-specials.md` | 生信专用：命令重现+流程图+数据库+统计 |
| `references/ai-ml-specials.md` | AI/ML专用：模型架构+训练流程+Benchmark |
| `references/obsidian-format-guide.md` | Obsidian格式完整参考 |
| `references/paper-type-adaptation.md` | 6种论文类型适配矩阵 |
| `references/quality-standards.md` | 完整QA系统+评分标准 |
| `references/multi-paper-operations.md` | 批量+对比+知识图谱+自动追踪 |
| **模板 (templates/)** | |
| `templates/single-paper/note-template.md` | 单论文完整笔记模板 |
| `templates/single-paper/images-readme.md` | 图像命名约定 |
| `templates/comparison/comparison-template.md` | 多论文对比模板 |
| `templates/knowledge-base/vault-scaffold.md` | PaperVault目录结构 |
| `templates/knowledge-base/moc-template.md` | Map of Content模板 |
| `templates/knowledge-base/dataview-queries.md` | Dataview查询集 |
| `templates/bioinformatics/pipeline-template.md` | 分析流水线Mermaid模板 |
| `templates/bioinformatics/database-summary.md` | 数据库资源摘要模板 |

---

## 执行流程

### 总览

```
Phase 1: PDF提取 → CP1(提取完整性) →
Phase 2: 论文类型识别 ★用户确认★ → CP2(类型确认) →
Phase 3: 大纲生成 ★用户确认★ → CP3(大纲确认) →
Phase 4: 深度解读生成 → CP4(内容质量) →
Phase 5: QA审阅(3轮自我批评) → CP5(输出质量≥3.5分) →
Phase 6: Obsidian输出(PaperVault放置)
```

---

### Phase 1: PDF提取

**目标**: 从PDF中提取所有可用内容（文本+图像+表格+公式），识别论文结构。

**步骤**:

1. **确认输入**: 获取PDF路径，检查文件存在性和可读性
2. **环境验证**: 确认pymupdf可用
   ```bash
   python -c "import fitz; print(f'pymupdf {fitz.version}')"
   ```
   若失败: `pip install pymupdf`
3. **文本提取**（调用 `scripts/pdf_extract.py`）:
   ```bash
   python scripts/pdf_extract.py --pdf "PDF路径" --output-dir "输出目录" --mode text --batch-size 8
   ```
   - 长论文(>20页)分批提取，每批5-8页
   - Windows环境自动处理UTF-8编码
4. **图像提取**:
   ```bash
   python scripts/pdf_extract.py --pdf "PDF路径" --output-dir "输出目录" --mode images
   ```
5. **表格提取**（调用 `scripts/pdf_extract_tables.py`）:
   ```bash
   python scripts/pdf_extract_tables.py --pdf "PDF路径" --output-dir "输出目录"
   ```
6. **公式提取**（调用 `scripts/pdf_extract_formulas.py`）:
   ```bash
   python scripts/pdf_extract_formulas.py --pdf "PDF路径" --output-dir "输出目录"
   ```
7. **结构识别**: 从提取文本中识别章节边界

**检查点 CP1: 提取完整性**
- [ ] 所有页面文本已提取
- [ ] 0个乱码页面（扫描版需OCR则标注）
- [ ] 所有嵌入图像已提取到 images/
- [ ] 表格区域已检测并裁剪
- [ ] 公式区域已检测并裁剪
- [ ] 论文结构（章节边界）已识别

**失败操作**: 重新提取失败页面；扫描版PDF提示用户需要OCR

---

### Phase 2: 论文类型识别 ★关键确认节点★

**目标**: 识别论文类型和领域，与用户确认解读方向。

**步骤**:

1. **类型分类**: 使用决策树分类（参照 `references/paper-type-adaptation.md`）
   - 方法学论文 (Methodological)
   - 发现型论文 (Discovery)
   - 综述论文 (Review)
   - 数据库/资源论文 (Database/Resource)
   - 计算/生信论文 (Computational/Bioinformatics)
   - 结构生物学论文 (Structural Biology)

2. **领域标签识别**:
   - `bioinformatics`: 含GEO/SRA/命令行/流水线/数据库
   - `biology`: 含实验操作/试剂/细胞系/动物模型
   - `ai-ml`: 含模型/训练/基准/损失函数/架构

3. **用户确认**（使用AskUserQuestion）:
   - "识别为 **[类型]** 论文，重点将放在 **[模块]**。是否正确？"
   - 同时确认:
     - 解读深度: 概览级 vs 复现级（默认复现级）
     - 重点方向（默认: 方法+结论）
     - 受众: 初学者 vs 研究者（默认初学者）

**检查点 CP2: 类型确认**
- [ ] 论文类型已分类且有依据
- [ ] 用户已确认类型

---

### Phase 3: 大纲生成 ★关键确认节点★

**目标**: 基于论文类型生成定制大纲，与用户确认。

**步骤**:

1. **从模板生成大纲**: 基于 `templates/single-paper/note-template.md`
2. **按类型调整模块权重**: 参照 `references/paper-type-adaptation.md`
3. **预填充已识别的节标题**
4. **标注每个模块的预计长度和内容范围**
5. **用户确认**（使用AskUserQuestion）:
   - 展示大纲结构
   - "是否需要调整重点或增删模块？"

**检查点 CP3: 大纲确认**
- [ ] 大纲覆盖论文所有章节
- [ ] 模块权重与论文类型匹配
- [ ] 用户已确认大纲

---

### Phase 4: 深度解读生成

**目标**: 按大纲逐模块生成解读内容。

**生成规则**:

1. **术语处理**: 中文主体，专业术语首次出现时: 中文(English Term)，后续使用中文或缩写
2. **图文融合**: 图像**不可孤立堆放**，必须在叙述逻辑节点处嵌入，遵循"前导句→图→解读→后续叙述"四步节奏。每张图必须包含:
   - **前导句**（1句话）: 预告图将展示什么关键数据
   - **图片嵌入**: `![[图像文件名.png|w800]]`（**必须包含文件扩展名**，如`.png`）
   - **解读Callout**: `[!figure]-` 块，7个必含字段：
     - 图的目的（这张图要回答什么问题，在论证链中扮演什么角色）
     - 坐标轴/分区（X轴、Y轴含义，各panel展示内容）
     - 关键趋势（主要数据趋势方向和转折点）
     - 统计显著性（p值、效应量、置信区间）
     - 对照组差异（与对照组/基准方法的差异有多大）
     - 异常点（偏离趋势的数据点或边界情况）
     - 支撑结论（图中哪个特征支撑论文哪个结论——**最后一句必须写明**）
   - **后续叙述**（1-2句话）: 基于图数据继续推进论述
   不同类型图的解读重点：
   - **数据图(Figure)**: 趋势+统计显著性+对照组差异
   - **表格图(Table)**: 关键数值对比+排名+异常行+文字数据复述（便于搜索索引）
   - **公式截图(formula)**: 含义+各符号定义+与其他公式的关联
   - **流程图/示意图**: 流程逻辑+关键决策节点+与前文方法的对应
3. **Wikilink**: 识别的专业概念创建 `[[概念]]` 双链
4. **Callout块**: 按7种类型分层:
   - `[!abstract]-` 一句话概括（笔记顶部）
   - `[!figure]-` 图解读（7字段：目的/坐标轴/趋势/统计/对照/异常/支撑结论）
   - `[!info]-` 进阶概念（高级读者深入）
   - `[!tip]-` 实践要点（可操作建议）
   - `[!warning]-` 常见误区（初学者陷阱）
   - `[!example]-` 代码复现（命令行/代码）
   - `[!question]-` 思考题（延伸思考）
   - 所有Callout默认折叠（渐进式分层）

5. **领域专用模块**:
   - 生信论文（参照 `references/bioinformatics-specials.md`）:
     - 命令重现: 提取命令行+版本+参数表
     - 分析流水线: Mermaid DAG可视化
     - 数据库资源汇总: 所有数据库ID列表
     - 统计方法解读: 原理+适用场景+结果解读
   - AI/ML论文（参照 `references/ai-ml-specials.md`）:
     - 模型架构: Mermaid图可视化
     - 训练流程: 数据流+超参数表
     - Benchmark对比: 与SOTA性能比较

6. **YAML frontmatter**: 生成完整元数据，包含 `source_pdf` 字段记录原始PDF路径（参照 `references/obsidian-format-guide.md`）
7. **标签系统**: 自动生成层级标签（#type/ #domain/ #method/ #tool/ #database/ #year/）
8. **文件命名**: `{年}-{期刊}-{关键词}.md`（参照config.json缩写表）

**检查点 CP4: 内容质量**
- [ ] 所有方法都有参数表
- [ ] 所有结果都有数据支撑
- [ ] 所有概念都有wikilink
- [ ] 域专用部分已完成
- [ ] 每张图都在叙述逻辑节点处嵌入（非集中堆放）
- [ ] 每张图有前导句预告展示内容
- [ ] 每张图有 `[!figure]-` 解读块且7个必含字段完整
- [ ] 数据图解读含趋势+统计+对照组
- [ ] 表格图解读含关键数值对比+异常行
- [ ] 公式截图解读含含义+符号定义
- [ ] 流程图解读含逻辑+决策节点
- [ ] 每张图解读最后一句说明"图中哪个特征支撑论文哪个结论"

---

### Phase 5: QA审阅

**目标**: 通过3轮自我批评确保输出质量达到商业级标准。

**详细规范**: 参照 `references/quality-standards.md`

**自我批评循环**:

| 轮次 | 检查维度 | 重点 |
|------|----------|------|
| 第1轮 | 逻辑一致性 | 结论是否有数据支撑？方法是否匹配声明？证据链有无断裂？ |
| 第2轮 | 初学者可达性 | 能否不查外部资料理解？能否按描述复现？Callout使用正确？ |
| 第3轮 | 域专家深度 | 边界情况考虑？局限性坦诚？比较公平？域专用功能完整？ |

每轮产生修订项，必须修复后才能进入下一轮。

**4维评分**（各1-5分）:

| 维度 | 及格线 |
|------|--------|
| 可复现性 | ≥3 |
| 清晰度 | ≥3 |
| 完整性 | ≥3 |
| 深度 | ≥3 |
| **综合均分** | **≥3.5** |

**检查点 CP5: 输出质量**
- [ ] YAML frontmatter格式有效
- [ ] 所有wikilink语法正确
- [ ] 所有Callout块格式正确
- [ ] 所有Mermaid块语法正确
- [ ] 所有图像引用指向存在的文件
- [ ] 综合评分 ≥ 3.5/5

---

### Phase 6: Obsidian输出

**目标**: 组装最终Obsidian笔记，放置到PaperVault知识库。

**步骤**:

1. **组装笔记**（调用 `scripts/obsidian_note_builder.py`）:
   - 填充模板，替换占位符
   - 在YAML frontmatter中添加 `source_pdf` 字段（原始PDF绝对路径）
   - 在标题行添加原文PDF的wikilink：`# 笔记标题[[原始PDF文件名.pdf]]`
   - 验证YAML/Wikilink/Callout/Mermaid语法
2. **放置到PaperVault**（调用 `scripts/vault_organizer.py`）:
   - 域分类 → 确定目标文件夹
   - 文件命名 → `{年}-{期刊}-{关键词}.md`
   - 创建images/同级目录
   - **复制原始PDF到笔记同目录**（使PDF wikilink可在Obsidian中直接打开）
   - 更新域MOC文件
3. **输出报告**:
   ```
   ✅ 论文解读完成
   - 笔记路径: PaperVault/01-Bioinformatics/.../2024-Nature-AlphaFold3.md
   - 图像数量: 12张
   - QA评分: 4.2/5
   - Wikilink数量: 23个
   - 建议关联: [[2023-Science-蛋白质折叠]], [[2024-Nat-Methods-结构预测]]
   ```

---

## 多论文支持

### 单篇深度解读（默认）

上述6阶段完整流程。

### 批量解读

输入多个PDF路径 → 并行提取 → 顺序分析 → 各自独立笔记 + 批量摘要
→ 参照 `references/multi-paper-operations.md`

### 横向对比

输入多个PDF + 对比焦点 → 使用 `templates/comparison/comparison-template.md`
→ 方法对比矩阵 + 结果对比 + 时间线视图 + 综合结论

### 知识图谱构建

输入主题 + 已有笔记目录 → 概念关联图 + 方法演进图 + 工具生态图
→ 调用 `scripts/knowledge_graph.py` → 嵌入MOC笔记

→ 详细规范参照 `references/multi-paper-operations.md`

---

## 配置

运行配置在 `config.json` 中，关键字段：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `defaults.read_depth` | "reproduction" | 解读深度: overview/reproduction |
| `defaults.audience` | "beginner" | 目标受众 |
| `quality.min_score` | 3.5 | QA及格线 |
| `quality.self_criticism_rounds` | 3 | 自我批评轮数 |
| `extraction.batch_size` | 8 | 长论文分批大小 |
| `extraction.extract_tables` | true | 是否提取表格 |
| `extraction.extract_formulas` | true | 是否提取公式 |
| `vault.root` | "" | PaperVault路径（空=与PDF同目录） |
| `naming.note_format` | "{year}-{journal}-{keyword}" | 笔记命名格式 |

---

## 错误处理

| 问题 | 解决方案 |
|------|---------|
| PDF提取乱码 | 尝试不同编码；扫描版PDF提示需要OCR |
| pymupdf未安装 | 自动执行 `pip install pymupdf` |
| 论文非英文 | 仍用中文解读，专业术语附原文 |
| 超长论文(>30页) | 分批提取，重点部分详细，补充材料简述 |
| 补充材料无法获取 | 标注 "[补充材料未获取，待补充]" |
| PDF路径含空格 | 路径用双引号包裹 |
| Windows编码错误 | 脚本自动设置 `sys.stdout.reconfigure(encoding='utf-8')` |
| QA评分不达标 | 修复薄弱模块，重新运行自我批评循环 |
| Wikilink目标不存在 | 创建占位笔记或标注为待创建 |

---

## 使用示例

```
用户: "解读这篇文献 A:/papers/nature12345.pdf"
      → Phase 1-6完整流程 → 生成Obsidian笔记到PaperVault

用户: "解读这个PDF，重点看方法，要能复现的那种"
      → 侧重方法学模块，复现级深度，[!example]代码复现Callout优先

用户: "帮我解读这两篇论文并对比"
      → 各自解读 + 横向对比笔记（comparison-template）

用户: "构建CRISPR领域的知识图谱"
      → 扫描已有CRISPR相关笔记 → 生成概念关联图+方法演进图

用户: "这篇论文是生信方向的，帮我把命令都提取出来"
      → 激活生信专用模块 → 命令重现+流程图+数据库汇总+统计解读

用户: "这篇AI论文的模型架构帮我画出来"
      → 激活AI/ML专用模块 → Mermaid模型架构图+超参数表+Benchmark对比
```
