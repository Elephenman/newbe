# 🛠️ Newbe Toolbox

> 叶泳峰（Elephenman）的个人开源工具箱——生信脚本、R绘图模板、论文解读、组会PPT，开箱即用。
>
> "newbe" = 新手的工具，但工具不新手。

---

## 📦 工具索引

| # | 工具 | 简介 | 语言/依赖 | 文件数 |
|---|------|------|-----------|--------|
| 1 | [phylo-tools](./phylo-tools/) | 进化树枝名批量处理（解析FASTA→补全CSV→重命名树） | Python + BioPython | 4 |
| 2 | [r-plot-templates](./r-plot-templates/) | R语言科研绘图模板库（106个绑图模板 + 51个SCI图表代码 + Seurat + 生信工具） | R / ggplot2 | 180+ |
| 3 | [paper-deep-read](./paper-deep-read/) | 论文深度解读 Skill v3.0（Obsidian笔记+知识图谱+复现者/审稿人双视角） | Skill / Python | 30+ |
| 4 | [academic-group-meeting-pipeline](./academic-group-meeting-pipeline/) | 组会汇报全流水线（7个AI Skill：PPT架构→逐字稿→答辩防御） | Skill / PPTX | 8 |

---

## 🔬 1. phylo-tools — 进化树批量处理工具集

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

**依赖：** `pip install biopython`（rename_tree_tips.py 只需标准库）

👉 [详细文档](./phylo-tools/README.md)

---

## 🎨 2. r-plot-templates — R语言科研绘图模板库

> 106个绑图模板 + 51个SCI图表代码 + Seurat单细胞分析 + 生信工具代码

### 目录结构

```
r-plot-templates/
├── 01_绘图模板代码/        ← 106个R绑图模板（按图表类型命名）
├── 02_SCI图表代码/         ← 51个SCI标准图表代码（bioR系列）
├── 05_Seurat单细胞分析/    ← Seurat完全手册 + 章节学习笔记
├── 06_生信工具代码库/      ← clusterProfiler/DESeq2/tidyverse/pandas实战代码
└── R绘图代码全集_Obsidian学习笔记.md  ← 106个模板的完整学习笔记
```

### 01_绘图模板代码（106个）

按图表类型分类，每个文件名即功能描述：

| 类别 | 示例 |
|------|------|
| **柱状/条形图** | 柱状图、柱状堆积图、双向柱状图、环形柱状图、嵌套柱状图 |
| **箱线/小提琴图** | 分组箱线图、小提琴图、云雨图、豆荚图、半小提琴图 |
| **散点/回归图** | 散点+回归曲线、散点+拟合+分面、散点密度图、ECDF图 |
| **热图** | 环形热图、双层环形热图、单列热图、三角形热图 |
| **火山图** | 火山图、多组火山图 |
| **进化树** | 半圆进化树、tree+分支颜色+注释、tree+柱状堆积图 |
| **地图** | 世界地图+采样点、中国地图+散点 |
| **网络/相关** | 网络图、弦图、mantel test、线性相关性 |
| **其他** | 桑基图、雷达图、曼哈顿图、南丁格尔图、词云图、花瓣图、Venn图 |

### 02_SCI图表代码（51个bioR系列）

编号从 bioR02 到 bioR51，覆盖科研论文常见图表：

| 范围 | 类型 |
|------|------|
| bioR02-06 | 柱状图（统计/P值/百分比/分组） |
| bioR07-10 | 箱线图（排序/差异/临床/分面） |
| bioR11-13 | 小提琴图 |
| bioR14-16 | 配对差异/气球图/偏差图 |
| bioR17-18 | 热图（pheatmap/临床热图） |
| bioR19-21 | 火山图/Venn/UpSetR |
| bioR22-25 | 相关性（散点/circos/网络） |
| bioR26-30 | 雷达/桑基/饼图/气泡/棒棒糖 |
| bioR31-33 | GO/KEGG circos/GSEA |
| bioR34-38 | 生存分析（离散/连续/截断/双变量/森林图） |
| bioR39-44 | 列线图/ROC/多变量ROC/timeROC |
| bioR45-51 | PCA/3dPCA/circos/基因组/ggtree/maftools/解剖图 |

**依赖：** R 4.0+、ggplot2、dplyr、pheatmap、survival、survminer、timeROC 等（各脚本头部有说明）

---

## 📖 3. paper-deep-read — 论文深度解读 v3.0

> 复现者+审稿人双视角的论文解读 Skill，生成详尽 Obsidian 笔记。

### 核心特性

- 🔄 叙述流嵌入式 Figure 解读（⚠️原文caption对照）
- 🔗 逻辑衔接5步闭环，★转折/双重节点标记
- 🧪 方法局限醒目标注，[[4.X]]跨Section链接
- 📊 PDF全图像提取（Figure+Table+公式）
- 🧬 生信+AI/ML跨域解读支持

### 目录结构

```
paper-deep-read/
├── agents/          ← 4个Agent（分析器/提取器/知识构建器/QA审核）
├── references/      ← 9个参考指南（生信/AI特殊处理/批判分析/图表解读/格式规范/质检标准）
├── scripts/         ← 6个Python脚本（PDF提取/公式提取/表格提取/Obsidian笔记/知识图谱/Vault组织）
├── templates/       ← 4类笔记模板（单篇/对比/生信/知识库）
├── config.json      ← Skill配置
├── SKILL.md         ← Skill主入口
└── README.md        ← 详细说明
```

👉 [详细文档](./paper-deep-read/README.md)

---

## 🎤 4. academic-group-meeting-pipeline — 组会汇报全流水线

> 从论文分析到答辩防御的7个AI Skill，学术组会一键搞定。

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

每个子目录独立可用，直接进对应目录看 README 即可。

```bash
# 克隆整个工具箱
git clone https://github.com/Elephenman/newbe.git

# 稀疏检出——只要某个工具
git clone --filter=blob:none --sparse https://github.com/Elephenman/newbe.git
cd newbe
git sparse-checkout set r-plot-templates  # 只要R绘图模板
```

---

## 📌 更新日志

| 日期 | 更新内容 |
|------|----------|
| 2026-04-27 | 🎉 初始整合：phylo-tools + paper-deep-read-v3 + academic-group-meeting-pipeline + r-plot-templates |
| 2026-04-27 | 📖 paper-deep-read 升级到 v3.0（本地最新版同步） |
| 2026-04-27 | 🎨 新增 r-plot-templates：106个绑图模板 + 51个SCI图表 + Seurat + 生信工具代码 |

---

## 🗺️ 路线图

- [ ] 更多生信小工具持续整合
- [ ] R绘图模板在线预览（HTML gallery）
- [ ] paper-deep-read 多语言论文支持
- [ ] 组会流水线视频输出支持


---

## 📄 License

各子工具保留各自原有的 License（见子目录），未特别声明的部分默认 [MIT License](./LICENSE)。