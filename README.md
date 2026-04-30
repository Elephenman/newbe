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

| 分类 | 工具数 | 说明 |
|------|:------:|------|
| [🧬 测序数据质控](./sequencing-qc/) | 18 | FASTQ/BAM质控、过滤、修剪、去重、采样等原始测序数据处理工具 |
| [🔗 比对/BAM处理](./alignment-bam/) | 8 | BAM/SAM统计、过滤、覆盖度、插入片段等比对结果处理工具 |
| [🧪 变异/基因组分析](./variant-analysis/) | 28 | VCF/SNP/Indel/CNV/SV/GWAS/单体型/突变特征等变异分析工具 |
| [📊 转录组/表达分析](./rna-expression/) | 34 | DESeq2/DEG/标准化/火山图/热图/WGCNA等转录组表达分析工具 |
| [🔬 单细胞分析](./single-cell/) | 36 | Seurat质控/注释/聚类/整合/拟时序/CellChat/双重细胞等单细胞工具 |
| [🗺️ 空间转录组](./spatial-transcriptomics/) | 13 | 空间spot注释/差异分析/反卷积/Moran/生态位/邻域图等空间组学工具 |
| [🧫 表观遗传学](./epigenomics/) | 14 | ChIP-seq/ATAC-seq/甲基化/Hi-C/TF motif/增强子/染色质状态等表观遗传工具 |
| [📖 基因组注释](./genome-annotation/) | 14 | GTF/BED/坐标转换/启动子/内含子/Circos/基因组密度等注释工具 |
| [🧬 序列分析](./sequence-analysis/) | 15 | FASTA统计/比对/kmer/密码子/基因组N50/同线性等序列分析工具 |
| [🌐 基因功能/通路](./gene-function/) | 21 | 富集分析/GSEA/通路网络/DDR/共表达/WGCNA模块等基因功能注释工具 |
| [🎨 可视化/绘图](./visualization/) | 18 | 配色/热图/Venn/Forest/Ridgeline/点图/通用绘图等可视化工具 |
| [🔄 数据格式转换](./data-format/) | 7 | 格式互转/ID映射/FASTQ转FASTA等数据格式处理工具 |
| [📋 实验室/项目管理](./lab-project/) | 20 | 环境检查/项目初始化/日志/甘特图/试剂/Protocol等管理工具 |
| [📝 学术写作/文献](./academic-writing/) | 29 | PubMed/DOI/引用/笔记/论文/会议/基金等学术写作工具 |

| **合计** | **275** | **14个分类，覆盖生信全流程** |

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

## 📌 更新日志

| 日期 | 更新内容 |
|------|---------|
| 2026-04-30 | 工具分类整理：275个工具按领域归入14个子文件夹 |
| 2026-04-28 | Batch 5: 50 new tools (#211-#260, DDR scores, arXiv, manuscript) |
| 2026-04-28 | Batch 4: 50 new tools (#161-#210, DDR pathway, Forest, Harmony) |
| 2026-04-28 | Batch 3: 50 new tools (#111-#160, DNA damage hotspot) |
| 2026-04-28 | Batch 2: 60 new tools (#51-#110, 45 Python + 15 R) |
| 2026-04-28 | Batch 1: 50 bioinformatics tools (interactive input) |
| 2026-04-27 | Initial release: 5 original sub-projects |

---

## 🗺️ Roadmap

- [x] 275 bioinformatics tools across 14 categories
- [x] Sequencing QC / BAM / VCF / GTF / BED processing
- [x] DESeq2 / enrichment / WGCNA / survival analysis
- [x] Seurat / CellChat / pseudotime / single-cell QC
- [x] Spatial transcriptomics (Moran / deconvolution / niche)
- [x] Epigenomics (ChIP / ATAC / methylation / Hi-C / TF)
- [x] DNA damage repair (DDR pathway / hotspot / gene sets)
- [x] Academic writing (PubMed / DOI / manuscript / thesis)
- [x] Scientific visualization (palette / Venn / Forest / Circos)
- [ ] Auto-expand: more tools via automation

---

## 📄 License

[MIT License](./LICENSE) — use freely, modify freely, share freely.
