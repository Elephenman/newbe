[English](./README.md) · [中文](./README_CN.md)

<div align="center">

# 🛠️ Newbe

**面向生信研究者的开源工具箱 — 275+ 交互式小工具，开箱即用**

[![GitHub](https://img.shields.io/badge/GitHub-Elephenman/newbe-blue?logo=github)](https://github.com/Elephenman/newbe)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-4.0+-276DC3?logo=r&logoColor=white)](https://cran.r-project.org/)
[![Tools](https://img.shields.io/badge/Tools-275+-orange)](https://github.com/Elephenman/newbe)

</div>

---

## 🌟 Newbe 是什么？

**Newbe** 是面向生物信息学研究者的开源工具集合，涵盖从测序质控到发表级图表的 **275+ 个交互式小工具**。

每个工具**独立可运行**——无需复杂依赖，直接运行脚本按提示输入即可。所有参数均有合理默认值，回车即用。

### ✨ 核心特性

- 🎯 **交互式输入** — 每个参数都有提示和默认值，回车即用，零配置启动
- 📦 **独立运行** — 每个工具自包含，不依赖项目内其他工具
- 🐍 **双语言覆盖** — Python 工具 190+ 个，R 工具 80+ 个
- 🧬 **全流程覆盖** — 从原始测序数据到发表级图表，一站式解决
- 🔓 **完全开源** — MIT 协议，随意使用、修改、分享

---

## 🚀 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/Elephenman/newbe.git
cd newbe

# 2. 进入工具目录（例如测序质控）
cd sequencing-qc/fastq-qc-checker

# 3. 运行
python fastq_qc_checker.py      # Python 工具
Rscript seurat_qc_pipeline.R    # R 工具
```

所有工具采用统一的交互式输入范式——每个参数有**中文提示**和**合理默认值**，直接回车即可使用默认值。

---

## 📋 工具目录

> 点击分类名称查看该分类下所有工具的详细说明。

<table>
<tr>
<td width="50%">

### 🧬 [测序数据质控](./sequencing-qc/) <sup>18</sup>

FASTQ/BAM 质控、过滤、修剪、去重、采样

- Adapter检测修剪 · 碱基质量分布 · Barcode拆分
- 重复reads去除 · 质量过滤 · 配对一致性检查
- 长度过滤 · Strand方向检测 · UMI去重统计
- QC报告汇总 · 测序深度计算 · 样本表校验

</td>
<td width="50%">

### 🔗 [比对 / BAM处理](./alignment-bam/) <sup>8</sup>

BAM/SAM 统计、过滤、覆盖度、插入片段

- 染色体信息提取 · 覆盖度分布图 · Flag过滤
- 插入片段统计 · Mate-pair修复 · Readcount汇总
- BAM关键指标速查 · 覆盖深度统计

</td>
</tr>

<tr>
<td width="50%">

### 🧪 [变异 / 基因组分析](./variant-analysis/) <sup>28</sup>

VCF · SNP · CNV · SV · GWAS · 单体型 · 突变特征

- Manhattan/QQ图 · LD衰减 · 单体型定相
- SBS96突变特征 · CNV分段注释 · SV断点可视化
- 胚系/体细胞变异过滤 · 临床注释 · 祖源推断
- VCF过滤/解析/一致性 · MAF分布 · 缺失率检查

</td>
<td width="50%">

### 📊 [转录组 / 表达分析](./rna-expression/) <sup>34</sup>

DESeq2 · DEG · 标准化 · 火山图 · 热图 · WGCNA

- DESeq2结果格式化 · 多组DEG对比(Venn/UpSet)
- 火山图(交互式/增强版/标签编辑) · 聚类热图
- TPM/FPKM/RPKM标准化 · ERCC spike-in · Z-score
- DEG效应量/FDR校正/元分析 · 批次效应检测
- 表达箱线图/小提琴图/百分位排名 · 剪接junction

</td>
</tr>

<tr>
<td width="50%">

### 🔬 [单细胞分析](./single-cell/) <sup>36</sup>

Seurat · 注释 · 聚类 · 整合 · 拟时序 · CellChat

- Seurat质控/整合 · 自动注释 · Marker发现
- PCA/t-SNE/UMAP · Harmony批次校正 · UMAP批量绘图
- 拟时序(Monocle3) · RNA velocity · Doublet检测
- 细胞周期评分/回归 · 高变基因选择 · JackStraw
- 细胞比例分析 · 邻域富集 · 基因模块/趋势图

</td>
<td width="50%">

### 🗺️ [空间转录组](./spatial-transcriptomics/) <sup>13</sup>

Spot注释 · DEG · 反卷积 · Moran · 生态位 · 邻域图

- Spot自动注释/质量过滤 · 空间DEG发现
- 反卷积(SPOTlight) · Moran's I自相关 · Geary检验
- 生态位检测 · 邻域图构建 · 区域边界分割
- 共表达地图 · 距离衰减 · 变异度映射

</td>
</tr>

<tr>
<td width="50%">

### 🧫 [表观遗传学](./epigenomics/) <sup>14</sup>

ChIP-seq · ATAC-seq · 甲基化 · Hi-C · TF · 增强子

- ATAC peak注释 · ChIP peak合并 · 染色质状态
- 甲基化β值 · TF足迹检测 · Motif扫描/富集
- 增强子信号定量/靶基因关联 · Hi-C接触矩阵
- CTCF绝缘子 · 复制起始点/时序 · TF结合位点比较

</td>
<td width="50%">

### 📖 [基因组注释](./genome-annotation/) <sup>14</sup>

GTF · BED · 坐标转换 · 启动子 · 内含子 · Circos

- GTF exon/intron/feature提取 · BED交集/合并/注释
- 基因组坐标转换(hg19↔hg38) · 启动子提取
- Circos环形图 · 基因组密度图 · 多轨道叠加
- 重复序列mask · 基因组bin统计 · 覆盖度插值

</td>
</tr>

<tr>
<td width="50%">

### 🧬 [序列分析](./sequence-analysis/) <sup>15</sup>

FASTA · 比对 · k-mer · 密码子 · N50 · 同线性 · 进化树

- FASTA统计/反转/切片 · Needleman-Wunsch比对
- k-mer频次 · 密码子使用偏性(RSCU/CAI) · N50计算
- 基因组大小估算 · GC滑动窗口 · 同线性区块
- 多FASTA合并 · 进化树批量处理 · 组装contig统计

</td>
<td width="50%">

### 🌐 [基因功能 / 通路](./gene-function/) <sup>21</sup>

富集 · GSEA · 通路网络 · DDR · 共表达 · WGCNA

- GO/KEGG富集流水线 · GSEA运行/rank文件生成
- WGCNA模块提取 · 共表达网络 · 通路交叉对话
- DDR通路映射/突变评分/损伤热点/信号关联
- 基因荒漠 · 同源基因 · 蛋白结构域 · 生存关联
- Sankey流向图 · 通路热图/网络 · 多组学整合

</td>
</tr>

<tr>
<td width="50%">

### 🎨 [可视化 / 绘图](./visualization/) <sup>18</sup>

配色 · 热图 · Venn · Forest · Ridgeline · 点图

- Nature/Cell配色方案 · 色盲友好配色 · R绘图模板库
- Venn图(2-5组) · Forest图 · Ridgeline山脊图
- 热图注释/排序 · 增强点图 · 堆叠条形图
- 相关性矩阵 · 统计摘要表 · 箱线图异常值 · 比较表

</td>
<td width="50%">

### 🔄 [数据格式转换](./data-format/) <sup>7</sup>

CSV↔TSV↔JSON↔Excel · ID映射 · FASTQ↔FASTA · SAM↔FASTQ

- 通用格式互转 · DPI转换(300/600) · FASTQ→FASTA
- GFF3→GTF · SAM/BAM→FASTQ · 基因ID版本统一
- 转录本↔基因ID↔基因名映射

</td>
</tr>

<tr>
<td width="50%">

### 📋 [实验室 / 项目管理](./lab-project/) <sup>20</sup>

环境 · 初始化 · 日志 · 甘特图 · 试剂 · Protocol

- Conda环境检查/导出 · 项目目录初始化 · 流程文档生成
- Pipeline日志解析 · 甘特图+里程碑 · Protocol版本管理
- 试剂库存+过期预警 · 实验计时器 · 组会纪要
- 基金预算 · 实验设计检查 · 结果文件汇总 · R模板

</td>
<td width="50%">

### 📝 [学术写作 / 文献](./academic-writing/) <sup>29</sup>

PubMed · DOI · 引用 · 笔记 · 论文 · 会议 · 基金

- PubMed批量检索 · DOI→引用格式 · 被引追踪+趋势
- Obsidian笔记模板 · arXiv下载 · BibTeX网络
- 论文深度解读 · 可读性评分 · 字数/章节统计
- 图片合规检查/排版/标签 · 参考文献清洗 · 会议摘要
- 学位论文大纲 · 基金预算 · 关键词提取 · 相似度检测

</td>
</tr>
</table>

---

## 🧬 5个原始子项目

<table>
<tr>
<td width="20%" align="center"><a href="./sequence-analysis/phylo-tools/"><img src="https://img.shields.io/badge/🧬-phylo_tools-6B8E23?style=for-the-badge"/></a><br><br>进化树批量处理<br><sub>3 Python脚本</sub></td>
<td width="20%" align="center"><a href="./visualization/r-plot-templates/"><img src="https://img.shields.io/badge/🎨-r_plot_templates-E91E63?style=for-the-badge"/></a><br><br>R科研绘图模板库<br><sub>106绑图+51SCI</sub></td>
<td width="20%" align="center"><a href="./academic-writing/paper-deep-read/"><img src="https://img.shields.io/badge/📖-paper_deep_read-1565C0?style=for-the-badge"/></a><br><br>论文深度解读<br><sub>复现者+审稿人双视角</sub></td>
<td width="20%" align="center"><a href="./lab-project/academic-group-meeting-pipeline/"><img src="https://img.shields.io/badge/🎤-group_meeting-7B1FA2?style=for-the-badge"/></a><br><br>组会汇报流水线<br><sub>论文→PPT→答辩</sub></td>
<td width="20%" align="center"><a href="./lab-project/md2ipynb-sync/"><img src="https://img.shields.io/badge/📝-md2ipynb-FF6F00?style=for-the-badge"/></a><br><br>Obsidian↔Jupyter同步<br><sub>MD↔IPYNB双向</sub></td>
</tr>
</table>

---

## 📄 License

[MIT License](./LICENSE) — 随意使用、修改、分享。