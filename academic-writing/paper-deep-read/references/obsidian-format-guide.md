# Obsidian格式参考 — v4.0

---

## 一、YAML Frontmatter

必填: title, year, journal, paper_type, domains, read_date, tags, source_pdf
可选: authors, doi, keywords, methods, tools, databases, aliases

自检: frontmatter中的tools/methods/databases必须在正文有对应提及

---

## 二、图像引用

- 必须包含扩展名: `![[fig1.png|w800]]`
- 图不可孤立堆放，必须在叙述中嵌入
- 排版流程：叙述 → 图片 → caption(斜体) → Panel解读 → 继续叙述
- caption格式：*图N {{标题}}。(a) {{Panel A子标题}}；(b) {{Panel B子标题}}。*

---

## 三、Callout类型(4+1)

| 类型 | 语义 | 折叠 | 默认用途 |
|------|------|------|----------|
| `[!abstract]-` | 快读路径+Abstract | 折叠 | 层1入口 |
| `[!figure]-` | 仅Supplementary/表格型Figure | 折叠 | 例外场景 |
| `[!critique]-` | 方法论硬伤（仅真正硬伤） | 折叠 | 层2补充 |
| `[!tip]-` | 方法Protocol/实践要点 | 折叠 | 层2补充 |
| `[!question]-` | 思考题/研究裂变 | 折叠 | 层2补充 |

核心Figure解读方式：叙述段落嵌入（非Callout折叠）
→ **Panel X — {{子标题}}** 加粗标签 + 2-3句解读
→ 图片就在叙述流中，读到哪里图就在哪里

禁止使用: warning, info, important, attack, example, caution, note, code

---

## 四、视觉层级规则

| 类型 | 格式 | 语义 | 示例 |
|------|------|------|------|
| **结构标签** | `**标签：**`冒号结尾 | 告诉读者"接下来是什么内容" | **实验目的：** **核心发现：** **逻辑衔接：** |
| **Panel标签** | `**Panel X — 子标题**`破折号连接 | 告诉读者"这是图中哪个面板的解读" | **Panel A — MEME motif logo** |
| **斜体caption** | `*图N 标题。(a)...(b)...*` | 图片标题，在Panel解读之前 | *图1 DdaA结合motif鉴定。(a)...；* |

---

## 五、批判标注规则

**通用方法局限** → 🧪引用块（醒目且含[[4.X]]链接）：
```markdown
> 🧪 方法局限：DNA pulldown在非交联条件下进行，可能遗漏间接结合位点。交联验证参见[[4.1 DNA pulldown Protocol]]。
```

**真正方法论硬伤** → `[!critique]-` Callout（仅硬伤才有）：
```markdown
> [!critique]- 方法论硬伤
> 3.5 RNA-seq仅分析了单一时间点（15 min），无法判断DDR基因上调的时序动态。
> 单时间点设计无法区分"立即响应"和"延迟响应"。
```

---

## 六、分隔规则

- ★转折点/★双重节点 → 上方有一条`---`
- （确认点） → 上方无`---`
- Section级别 → 保留`---`
- 规则：全文只有3-4条分隔线（只标记论证阶段转换），而不是每段都有

---

## 七、标签体系

#type/ #domain/ #method/ #tool/ #database/ #year/

---

## 八、Mermaid图规范

节点数>15时使用subgraph分组。布局:
- 流水线: LR
- 架构/概念图: TD