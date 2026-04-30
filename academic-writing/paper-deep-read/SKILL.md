---
name: paper-deep-read-v3
version: 4.1.0
description: "深度解读科学文献，生成详尽Obsidian笔记。复现者+审稿人双视角，叙述流嵌入式Figure解读（⚠️原文caption对照），逻辑衔接5步闭环，★转折/双重节点标记，🧪方法局限醒目标注，[[4.X]]跨Section链接。"
allowed-tools: Read Write Edit Bash Glob Grep Agent
tags: [论文解读, 学术阅读, Obsidian, 生物信息学, PDF提取, 批判性评价, 中文, 叙述流嵌入, 逻辑衔接]
metadata:
  skill-author: "Claude Code Custom Skill"
  skill-version: "4.1.0"
  trigger-keywords: ["深度解读文献", "批判性阅读", "审稿人视角解读", "论文深度拆解",
                      "deep read paper", "critical analysis paper",
                      "深度解读", "论文分析", "论文笔记"]
---

# Paper Deep Read v4.1 — 双视角论文深度解读

将科学文献拆解为**解读视角(70%) + 批判视角(30%)**的双透镜 Obsidian 笔记。

**核心定位**：解读笔记 = 学习材料。让小白读懂 → 学会思路 → 学会写作 → 实现复现。

## 执行流程

```
Phase 1: PDF提取 → Phase 2: 类型识别(★确认) → Phase 3: 大纲(★确认)
→ Phase 4: 深度解读 → Phase 5: QA → Phase 6: Obsidian输出
```

---

### Phase 1: PDF提取

1. 确认PDF路径存在
2. 确认pymupdf可用，失败则 `pip install pymupdf`
3. 文本提取: `python scripts/pdf_extract.py --pdf "路径" --output-dir "目录" --mode text`
4. 图像提取(内嵌原图直接提取): `python scripts/pdf_extract.py --pdf "路径" --output-dir "目录" --mode figures`
   - Caption定位Figure编号 → 匹配同页嵌入图 → 直接提取原始字节 → PNG统一输出
5. 结构识别: 从提取文本识别章节边界

---

### Phase 2: 类型识别 ★确认★

1. 分类: 方法学 / 发现型 / 综述 / 数据库 / 计算生信 / 结构生物学
2. 领域标签: `bioinformatics` / `biology` / `ai-ml`
3. 用户确认类型和重点方向

---

### Phase 3: 大纲生成 ★确认★

1. 按类型生成定制大纲（参照 `templates/single-paper/note-template.md`）
2. 用户确认

---

### Phase 4: 深度解读生成

**核心原则**: 解读为主，批判为辅；叙述流中嵌入Figure解读。

1. **术语**: 中文主体，专业术语首次: 中文(English)，后续用中文或缩写

2. **Figure解读方式（微信式排版：叙述流嵌入）**:
   默认：叙述段落嵌入（不用Callout折叠）

   **⚠️ 最高优先级：原文caption对照**（v4.1新增）
   → 生成Figure解读前，必须从论文原文Results或Figure legends中定位该Figure的完整caption
   → 提取caption中所有Panel编号(A/B/C/...)和描述 → 列出完整Panel清单
   → Panel编号和子标题严格按原文caption，绝不允许凭想象编造
   → 如果论文Figure 1有7个Panel(A-G)，解读必须包含全部7个Panel，不能遗漏
   → 斜体caption引用原文Figure caption（可精简但保留Panel编号和核心描述）
   → 图片文件名(figN.png)必须对应论文Figure编号，不同Section可引用同一张图片
   → 绝不允许引用不存在的图片文件

   排版流程：
   → 图片直接放在叙述流中
   → 图片下方放斜体caption（引用原文Figure caption）：*图N {{原文标题}}。(A) {{原文Panel A描述}}；(B) {{原文Panel B描述}}。*
   → caption之后用**Panel A — {{原文子标题}}**加粗标签引导解读
   → 每Panel 2-3句解读直接写在标签后
   → 最后一句"**图的整体逻辑：**"概括各Panel关系

   **视觉层级区分**：
   | 类型 | 格式 | 语义 | 示例 |
   |------|------|------|------|
   | **结构标签** | `**标签：**`冒号结尾 | 告诉读者"接下来是什么内容" | **实验目的：** **核心发现：** **逻辑衔接：** |
   | **Panel标签** | `**Panel X — 子标题**` 破折号连接 | 告诉读者"这是图中哪个面板的解读" | **Panel A — MEME motif logo** |
   | **斜体caption** | `*图N 标题。(a)...(b)...*` | 图片标题，在Panel解读之前 | *图1 DdaA结合motif鉴定。(a)...；*

   排版流程：叙述 → 图片 → caption(斜体) → Panel解读 → 继续叙述
   → 像微信式解读笔记和论文本身一样自然流畅

   例外（使用`[!figure]-` Callout折叠）：
   → Supplementary Figure（非核心补充图）
   → 数据表格型Figure（不是面板型复合图）
   → 用户明确要求折叠的Figure

3. **叙述节奏**:
   | 标记 | 语义 | 叙述量 | 逻辑衔接格式 |
   |------|------|--------|-------------|
   | ★转折点 | 实验结论推翻前假设或揭示新方向 | ≥8句 | 5步闭环 |
   | （确认点） | 实验仅验证已知结论 | 4-6句 | 3步简洁 |
   | ★双重节点 | 既验证已知又揭示新方向 | ≥8句 | 5步闭环+双预期 |

4. **结果小节结构（叙述流嵌入）**:
   ```
   **实验目的：** {{1-2句}}

   {{主干叙述：展开关键发现前的铺垫}}

   ![[fig1.png|w800]]

   *图1 {{标题}}。(a)...(b)...*

   **Panel A — {{子标题}}** {{2-3句}}
   **Panel B — {{子标题}}** {{2-3句}}

   **图的整体逻辑：** {{1句}}

   **核心发现：** {{2-3句，含具体数据}}

   **逻辑衔接：** {{发现→追问→设计→预期→验证，转折点5步/确认点3步}}

   > 🧪 方法局限：{{一句话+[[4.X]]链接}}（仅存在时才写）
   ```

5. **逻辑衔接（替代推导语+策略解释）**:
   - **转折点★**: 完整5步闭环：发现→追问→设计→预期→验证
   ```
   **逻辑衔接：** 3.X的pulldown在非交联条件下捕获了DdaA，但无法排除间接结合。
   → 追问：DdaA是否直接结合motif DNA？
   → 设计：EMSA是回答这个问题的最直接方法（[[4.2 EMSA Protocol]])——纯化蛋白+纯化DNA，无中介因子。
   → 预期：如果DdaA直接结合，EMSA中应出现阻滞带；如果不结合（间接结合），则无阻滞。
   → 验证：3.2的EMSA结果确认了前者——DdaA与motif DNA的结合呈浓度依赖性阻滞带。
   ```
   - **确认点**: 简洁3步：追问→设计→验证（不含预期展开）
   ```
   **逻辑衔接：** 进化分析确认DdaA在402个Moraxellaceae基因组中普遍存在 → 下一步验证DdaA的DDR调控功能（3.5）。
   ```
   - **★双重节点**: 5步闭环+双预期
   ```
   **逻辑衔接：** ChAP-seq验证了DdaA对DDR基因的调控（确认3.1-3.2结论），但发现了DdaA也结合CRISPR-Cas和RM系统启动子 →
   追问DdaA是否同时调控抗噬菌体防御 →
   预期1（如果DdaA调控抗噬菌体）：敲除株应噬菌体敏感；预期2（如果不调控）：噬菌体抵抗力不变 →
   验证见3.5-3.8。
   ```

6. **批判定位 → 补充视角**:
   - **正文解读句数 ≥ 2× 批判句数**
   - 通用方法局限 → `> 🧪 方法局限：{{一句话+[[4.X Protocol]]链接}}`（醒目引用块）
   - 真正方法论硬伤 → `[!critique]-` Callout（仅硬伤才有）
   - Section 6保留批判汇总，但正文解读量必须≥2×批判量

7. **长文档分隔规则**:
   - ★转折点/★双重节点 → 上方有一条`---`
   - （确认点） → 上方无`---`
   - Section级别 → 保留`---`

8. **Section 1.2 已知范式概览**: 2-3段概述领域在本文发表前的主流认知

9. **Section 5 Discussion解读**: 提取作者核心论点 + 自述局限 + 与Skill批判对照

10. **Section 4 方法学详解**: 复现级参数+对照设计。逻辑衔接段中的`[[4.X Protocol]]`是Obsidian wikilink，初学者可按需跳转

11. **Callout类型(4+1)**:
   - `[!abstract]-` 快读路径+Abstract
   - `[!figure]-` 仅Supplementary/表格型Figure
   - `[!critique]-` 方法论硬伤（仅真正硬伤）
   - `[!tip]-` 方法Protocol/复现要点
   - `[!question]-` 思考题/研究裂变

12. **Wikilink / YAML / 标签**: 自动生成，`source_pdf`字段，frontmatter自检

13. **快读路径**: `[!abstract]-`，3发现+论证链速览+阅读建议

14. **文件命名**: `{年}-{期刊}-{关键词}.md`

---

### Phase 5: QA审阅

3轮自我批评:

| 轮次 | 维度 | 重点 |
|------|------|------|
| 1 | 逻辑一致性 | 结论有数据支撑？逻辑衔接5步闭环完整？★双重节点标记正确？ |
| 2 | 初学者可达性 | 可理解？可复现？Figure嵌入叙述流？🧪标注醒目？ |
| 3 | 域专家深度 | 嵌入式批判到位？Discussion解读准确？[[4.X]]链接有效？ |

4维评分(各1-5分，均分>=3.5及格): 可复现性 / 清晰度 / 完整性 / 深度

---

### Phase 6: Obsidian输出

1. 组装笔记(模板填充 + source_pdf + PDF wikilink)
2. 放置到PaperVault(域分类 → 命名 → images/目录 → 复制PDF → 更新MOC)
3. 输出报告

---

## 配置 (config.json)

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `defaults.read_depth` | "reproduction" | 解读深度 |
| `defaults.audience` | "beginner" | 目标受众 |
| `quality.min_score` | 3.5 | QA及格线 |
| `quality.self_criticism_rounds` | 3 | 自我批评轮数 |
| `extraction.batch_size` | 8 | 长论文分批大小 |
| `extraction.extract_embedded_images` | true | 直接提取PDF内嵌原图 |
| `vault.root` | "" | PaperVault路径 |
| `naming.note_format` | "{year}-{journal}-{keyword}" | 笔记命名格式 |

---

## 错误处理

| 问题 | 解决方案 |
|------|---------|
| PDF提取乱码 | 尝试不同编码；扫描版需OCR |
| pymupdf未安装 | 自动 `pip install pymupdf` |
| 论文非英文 | 仍用中文解读，术语附原文 |
| 超长论文(>30页) | 分批提取，重点详细 |
| QA评分不达标 | 修复薄弱模块，重跑自我批评 |

---

## 使用示例

```
"解读这篇文献 A:/papers/nature12345.pdf"
  → Phase 1-6完整流程 → 生成Obsidian笔记到PaperVault

"解读这个PDF，重点看方法，要能复现的那种"
  → 侧重方法学模块，复现级深度

"帮我解读这两篇论文并对比"
  → 各自解读 + 横向对比笔记
```