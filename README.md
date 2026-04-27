# 🛠️ Newbe Toolbox

叶泳峰（Elephenman）的个人小工具合集——生信脚本、论文解读、组会PPT，开箱即用。

> "newbe" = 新手的工具，但工具不新手。

---

## 📦 工具一览

| 工具 | 简介 | 语言/依赖 | 状态 |
|------|------|-----------|------|
| [phylo-tools](./phylo-tools/) | 进化树枝名批量处理（解析FASTA→补全CSV→重命名树） | Python + BioPython | ✅ 可用 |
| [paper-deep-read](./paper-deep-read/) | 论文深度解读 Skill v3.0（Obsidian笔记+知识图谱+质检体系） | Skill / Python | ✅ 可用 |
| [academic-group-meeting-pipeline](./academic-group-meeting-pipeline/) | 组会汇报全流水线（7个AI Skill：PPT架构→逐字稿→答辩防御） | Skill / PPTX | ✅ 可用 |

---

## 🔬 phylo-tools — 进化树批量处理工具集

三个 Python 脚本，用于进化树构建后的枝名批量处理。

**典型工作流：**
```
NCBI下载FASTA → parse_fasta_headers.py 提取CSV
CSV不完整     → fill_csv_from_ncbi.py 从NCBI补全
替换树枝名    → rename_tree_tips.py 生成美化树文件
```

| 脚本 | 功能 |
|------|------|
| `parse_fasta_headers.py` | 解析NCBI FASTA头→提取序列号+物种名→生成CSV |
| `fill_csv_from_ncbi.py` | 自动识别CSV缺列→NCBI抓取填补 |
| `rename_tree_tips.py` | 用CSV映射表批量替换树文件枝名 |

**依赖：** `pip install biopython`（脚本1只需标准库）

👉 [详细文档](./phylo-tools/README.md)

---

## 📖 paper-deep-read — 论文深度解读 v3.0

复现者+审稿人双视角的论文解读 Skill，生成详尽 Obsidian 笔记。

**核心特性：**
- 叙述流嵌入式 Figure 解读（⚠️原文caption对照）
- 逻辑衔接5步闭环，★转折/双重节点标记
- 🧪方法局限醒目标注，[[4.X]]跨Section链接
- PDF全图像提取（Figure+Table+公式）
- 生信+AI/ML跨域解读支持

**结构：**
- `agents/` — 4个Agent定义（分析器、提取器、知识构建器、QA审核）
- `references/` — 6个参考指南（生信/AI特殊处理、格式规范、质检标准）
- `scripts/` — 6个Python脚本（PDF提取、Obsidian笔记构建、知识图谱）
- `templates/` — 4类笔记模板（单篇/对比/生信/知识库）

👉 [详细文档](./paper-deep-read/README.md)

---

## 🎤 academic-group-meeting-pipeline — 组会汇报全流水线

从论文分析到答辩防御的7个AI Skill，学术组会一键搞定。

| Skill | 功能 |
|-------|------|
| `group-meeting-pipeline` | 组会汇报全流水线总控 |
| `methodology-critic` | 论文方法论批判、研究设计漏洞挖掘 |
| `paper-logic-deconstructor` | 论文逻辑解构、底层骨架提取 |
| `ppt-architect` | 学术PPT架构设计、视觉层级规划 |
| `ppt-implement-custom` | PPT生成实现、PPTX文件输出 |
| `qa-defense-system` | 导师提问预测、答辩防御话术 |
| `speech-writer` | 学术汇报逐字稿、口语化演讲稿 |

👉 [详细文档](./academic-group-meeting-pipeline/README.md)

---

## 🚀 快速开始

每个子目录都是独立可用的，直接进对应目录看 README 即可。

```bash
# 克隆整个工具箱
git clone https://github.com/Elephenman/newbe.git

# 或者只下载你需要的工具（稀疏检出）
git clone --filter=blob:none --sparse https://github.com/Elephenman/newbe.git
cd newbe
git sparse-checkout set phylo-tools  # 只检出phylo-tools
```

---

## 📌 更新日志

| 日期 | 更新内容 |
|------|----------|
| 2026-04-27 | 初始整合：phylo-tools + paper-deep-read + academic-group-meeting-pipeline |

---

## 👤 作者

**叶泳峰 / Elephenman**
- 浙大生物信息学研究生
- GitHub: [Elephenman](https://github.com/Elephenman)
- 专注生信+AI交叉方向

---

## 📄 License

各子工具保留各自原有的 License（见子目录），未特别声明的部分默认 MIT License。