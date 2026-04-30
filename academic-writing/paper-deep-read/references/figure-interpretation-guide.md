# Figure解读规范 — v4.1

## 默认方式：叙述段落嵌入

每张复合图直接在叙述流中解读，不使用Callout折叠。

排版流程：

```
一段叙述（策略解释/背景铺垫）
→ 图片
→ 图片caption（斜体，图下方）
→ Panel A解读 → Panel B解读 → ... → 图的整体逻辑
→ 核心发现
→ 逻辑衔接
→ 🧪标注（仅存在时）
```

格式：

```markdown
![[figN.png|w800]]

*图N {{整体标题}}。(a) {{Panel A子标题}}；(b) {{Panel B子标题}}；(c) {{Panel C子标题}}；(d) {{Panel D子标题}}。*

**Panel A — {{子标题}}** {{2-3句解读：具体数据、形态、与预期对比}}

**Panel B — {{子标题}}** {{2-3句解读}}

**Panel C — {{子标题}}** {{2-3句解读}}

**Panel D — {{子标题}}** {{2-3句解读}}

**图的整体逻辑：** {{1句概括各Panel间递进关系}}
```

## 视觉层级

| 类型 | 格式 | 语义 |
|------|------|------|
| **Panel标签** | `**Panel X — {{子标题}}**` 破折号连接 | Figure解读锚点 |
| **结构标签** | `**标签：**` 冒号结尾 | 叙述定位标记（实验目的/核心发现/逻辑衔接） |
| **斜体caption** | `*图N {{标题}}。(a)...(b)...*` 斜体 | 图片标题 |

**关键**：Panel标签用破折号（`—`），结构标签用冒号（`：`），caption用斜体。速览型读者一眼区分"这是Panel解读"还是"正文定位标记"。

## 例外：[!figure]- Callout折叠

仅用于：
- Supplementary Figure（非核心补充图）
- 数据表格型Figure（不是面板型复合图）
- 用户明确要求折叠的Figure

```markdown
> [!figure]- Figure SX: {{标题}}
> 
> **Panel A — {{子标题}}**
> {{2-3句解读}}
> 
> **图的整体逻辑：** {{1句}}
```

## 解读深度要求

每个Panel的解读必须包含：
1. 该Panel展示了什么数据/图像
2. 关键数值或形态特征（不要只说"有趋势"，要给具体数字）
3. 该Panel与论文结论的关系

## ⚠️ 最高优先级：原文caption对照（v4.1新增）

**这是Figure解读最核心的规则，违反此规则会导致解读与论文图片完全不对应——这是不可接受的硬伤。**

### 规则
1. **Panel编号必须严格对应论文原文Figure caption中的Panel编号**：
   - 论文写"(A) Schematic bioinformatic workflow；(B) Binding motif；(C) DNA pull-down assay" → 解读必须写`**Panel A — Schematic bioinformatic workflow**`、`**Panel B — Binding motif**`、`**Panel C — DNA pull-down assay**`
   - **绝不允许**凭想象编造Panel编号或内容——如论文有7个Panel(A-G)，解读必须包含全部7个Panel，不能只写4个(A-D)
   - **绝不允许**把论文的Panel B说成Panel A，或把Panel E的ChAP-seq说成Panel D

2. **斜体caption必须逐字引用论文原文Figure caption**：
   - 格式：`*图N {{原文Figure caption的完整标题}}。(A) {{原文Panel A描述}}；(B) {{原文Panel B描述}}。*`
   - 不是用自己的话概括，而是**从论文原文中提取Figure caption原文**，包含所有Panel描述
   - 如果原文caption过长，可以适当精简但**Panel编号和子标题必须保留原文措辞**

3. **Figure-Section映射必须准确**：
   - 论文Figure 1可能包含多个Section的内容（如3.1+3.2+3.3共享Figure 1）
   - 解读时，每个Section引用自己相关的Panel，而不是虚构独立的图片
   - 例：如果3.1讨论Figure 1的A-C，3.2讨论Figure 1的D，3.3讨论Figure 1的E → 3.1展示完整Figure 1并解读A-C，3.2仅解读D（引用同一张fig1.png），3.3仅解读E

4. **图片文件名映射必须正确**：
   - PDF提取的图片文件名(fig1.png, fig2.png等)必须对应论文的Figure编号(Figure 1, Figure 2等)
   - 不同Section可能引用同一张图片文件
   - **绝不允许**引用不存在的图片文件（如fig5.png当论文只有4个Figure）

### 为什么这很重要

论文Figure是科学论证的核心视觉证据。如果解读的Panel编号和内容与论文图片不对应：
- 读者无法将解读文字与图片上的具体面板对照理解
- 解读的"核心发现"可能指向错误的Panel
- 逻辑衔接中引用的数据可能来自完全不同的实验
- **本质上，解读失去了与论文原文的锚定关系，变成了一篇"凭想象编造"的虚构文本**

### 对照流程

生成Figure解读时，必须执行以下对照步骤：
```
Step 1: 从论文原文中定位该Figure的完整caption（在Results或Figure legends中）
Step 2: 提取caption中所有Panel编号和描述 → 列出完整Panel清单
Step 3: 确认PDF提取的图片文件名(figN.png)对应论文的Figure编号
Step 4: 每个Panel解读严格按原文caption的Panel编号和子标题
Step 5: 斜体caption引用原文Figure caption（可精简但保留Panel编号和核心描述）
```

## 禁止

- ❌ 用1行"关键趋势"概括整张4面板复合图
- ❌ 只说"XXX组有差异"不给具体倍数/p值
- ❌ 略过Panel不解读（每个Panel都必须解读）
- ❌ 把核心Figure解读塞进折叠Callout打断阅读流
- ❌ 用表格格式概括复合图（改用叙述段落Panel解读）
- ❌ **凭想象编造Panel编号或内容——必须严格对照论文原文Figure caption**（v4.1新增）
- ❌ **遗漏Panel——论文有7个Panel只解读4个**（v4.1新增）
- ❌ **引用不存在的图片文件——论文只有Figure 1-4不能写fig5.png**（v4.1新增）
- ❌ **不同Section使用同一Figure但各写独立图片——应引用同一figN.png**（v4.1新增）