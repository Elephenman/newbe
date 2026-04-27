<div align="center">

# 🛠️ Newbe

**Bioinformatics Toolbox · Open Source · Ready to Use**

进化树处理 · R绘图模板 · 论文深度解读 · 组会汇报流水线 · Obsidian↔Jupyter同步 · 50个生信小工具

[![GitHub](https://img.shields.io/badge/GitHub-Elephenman/newbe-blue?logo=github)](https://github.com/Elephenman/newbe)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-4.0+-276DC3?logo=r&logoColor=white)](https://cran.r-project.org/)
[![Tools](https://img.shields.io/badge/Tools-55+-orange)](https://github.com/Elephenman/newbe)

</div>

---

## 📋 目录索引

### 🧬 测序数据处理

| # | 工具 | 语言 | 一句话说明 |
|---|------|------|-----------|
| 1 | [fastq-qc-checker](./fastq-qc-checker/) | Python | FASTQ质量一键体检报告（Q20/Q30/GC/Adapter） |
| 2 | [fastq-filter](./fastq-filter/) | Python | FASTQ按质量/长度/GC含量过滤 |
| 3 | [fastq-to-fasta](./fastq-to-fasta/) | Python | FASTQ转FASTA+可选去冗余 |
| 4 | [bam-stats-reporter](./bam-stats-reporter/) | Python | BAM/SAM关键指标速查（mapped率/覆盖度/MAPQ） |
| 5 | [vcf-filter-annotate](./vcf-filter-annotate/) | Python | VCF变异过滤+注释格式化（QUAL/DP/缺失率） |
| 6 | [gtf-feature-extractor](./gtf-feature-extractor/) | Python | 从GTF/GFF提取指定特征到表格 |
| 7 | [genome-fasta-slicer](./genome-fasta-slicer/) | Python | 参考基因组按坐标切片提取序列+flank |
| 8 | [sequence-stat-visualizer](./sequence-stat-visualizer/) | Python | 多序列统计+可视化（长度/GC/氨基酸） |
| 9 | [kmer-counter](./kmer-counter/) | Python | K-mer频次统计与差异比较 |
| 10 | [bed-merge-annotate](./bed-merge-annotate/) | Python | BED文件合并+GTF基因注释 |

### 📊 转录组/表达分析

| # | 工具 | 语言 | 一句话说明 |
|---|------|------|-----------|
| 11 | [deseq2-result-formatter](./deseq2-result-formatter/) | R | DESeq2结果→发表级表格+火山图 |
| 12 | [expression-heatmap-cluster](./expression-heatmap-cluster/) | R | 表达矩阵→聚类热图（Nature配色） |
| 13 | [enrichment-auto-pipeline](./enrichment-auto-pipeline/) | R | GO/KEGG富集分析一键流水线 |
| 14 | [gsea-runner](./gsea-runner/) | R | GSEA分析一键运行 |
| 15 | [tpm-fpkm-calculator](./tpm-fpkm-calculator/) | Python | raw counts→TPM/FPKM/CPM转换 |
| 16 | [pca-tsne-umap-plotter](./pca-tsne-umap-plotter/) | Python | 降维可视化三合一 |
| 17 | [deg-compare-tool](./deg-compare-tool/) | Python | 多组DEG结果交叉对比（Venn/UpSet） |
| 18 | [co-expression-network](./co-expression-network/) | R | WGCNA简化版一键网络构建 |
| 19 | [survival-expression-correlator](./survival-expression-correlator/) | R | 基因表达与生存关联分析+KM曲线 |
| 20 | [batch-effect-inspector](./batch-effect-inspector/) | Python | 批次效应检测+PCA可视化 |

### 🔬 单细胞/空间组学

| # | 工具 | 语言 | 一句话说明 |
|---|------|------|-----------|
| 21 | [seurat-qc-pipeline](./seurat-qc-pipeline/) | R | Seurat质控一键流水线 |
| 22 | [cell-type-annotator](./cell-type-annotator/) | R | 单细胞自动注释辅助（marker匹配） |
| 23 | [umap-batch-plotter](./umap-batch-plotter/) | R | UMAP按多维度批量分色绘图 |
| 24 | [pseudotime-setup](./pseudotime-setup/) | R | 拟时序分析启动器（Monocle3/Slingshot） |
| 25 | [cellchat-interaction-parser](./cellchat-interaction-parser/) | R | CellChat细胞通讯一键分析 |
| 26 | [doublet-detector-wrapper](./doublet-detector-wrapper/) | R | 单细胞doublet检测+过滤 |
| 27 | [spatial-spot-annotator](./spatial-spot-annotator/) | R | 空间转录组spot自动注释 |
| 28 | [sc-marker-finder](./sc-marker-finder/) | R | 单细胞marker基因批量查找 |

### 🧪 基因组/变异/调控

| # | 工具 | 语言 | 一句话说明 |
|---|------|------|-----------|
| 29 | [snp-stats-reporter](./snp-stats-reporter/) | Python | SNP/InDel变异统计报告+MAF分布 |
| 30 | [motif-scanner](./motif-scanner/) | Python | DNA序列motif扫描（JASPAR库） |
| 31 | [genome-density-plotter](./genome-density-plotter/) | Python | 染色体密度图（circos/线性） |
| 32 | [ld-decay-calculator](./ld-decay-calculator/) | Python | LD衰减曲线计算与绘图 |
| 33 | [promoter-extractor](./promoter-extractor/) | Python | 批量提取启动子序列+TSS注释 |
| 34 | [cnv-segment-plotter](./cnv-segment-plotter/) | Python | CNV分段结果可视化 |
| 35 | [dna-damage-gene-collector](./dna-damage-gene-collector/) | Python | 🔥DNA损伤修复基因集（对口陆慧智课题组） |

### 📖 文献/学术工具

| # | 工具 | 语言 | 一句话说明 |
|---|------|------|-----------|
| 36 | [pubmed-batch-searcher](./pubmed-batch-searcher/) | Python | PubMed批量检索+结果导出 |
| 37 | [doi-to-citation](./doi-to-citation/) | Python | DOI→APA/MLA/GB-T/BibTeX引用 |
| 38 | [paper-pdf-meta-extractor](./paper-pdf-meta-extractor/) | Python | PDF论文元数据自动提取 |
| 39 | [keyword-network-builder](./keyword-network-builder/) | Python | 文献关键词共现网络构建 |
| 40 | [literature-review-matrix](./literature-review-matrix/) | Python | 文献综述矩阵自动生成 |
| 41 | [citation-tracker](./citation-tracker/) | Python | 论文被引追踪+趋势图 |
| 42 | [reference-cleaner](./reference-cleaner/) | Python | 参考文献格式统一清洗+DOI验证 |
| 43 | [obsidian-paper-note-generator](./obsidian-paper-note-generator/) | Python | 论文→Obsidian笔记模板（精简/详细/组会） |

### 🎨 绘图/数据/流程工具

| # | 工具 | 语言 | 一句话说明 |
|---|------|------|-----------|
| 44 | [sci-color-palette](./sci-color-palette/) | Python | 科研配色方案生成器（Nature/Cell配色库） |
| 45 | [figure-size-checker](./figure-size-checker/) | Python | 论文图片合规检查（DPI/尺寸/格式） |
| 46 | [multi-panel-composer](./multi-panel-composer/) | Python | 多子图组合排版（ABCD标签） |
| 47 | [project-dir-initializer](./project-dir-initializer/) | Python | 科研项目目录一键初始化+git init |
| 48 | [sample-sheet-validator](./sample-sheet-validator/) | Python | 实验样本表格式校验 |
| 49 | [conda-env-checker](./conda-env-checker/) | Python | 项目环境依赖一致性检查 |
| 50 | [pipeline-log-parser](./pipeline-log-parser/) | Python | 分析流程日志解析+耗时统计 |

---

## 🧬 5个原始子项目

<table>
<tr>
<td width="20%" align="center"><a href="./phylo-tools/"><img src="https://img.shields.io/badge/🧬-phylo_tools-6B8E23?style=for-the-badge"/></a><br><br>进化树批量处理<br><sub>3 Python脚本</sub></td>
<td width="20%" align="center"><a href="./r-plot-templates/"><img src="https://img.shields.io/badge/🎨-r_plot_templates-E91E63?style=for-the-badge"/></a><br><br>R科研绘图模板库<br><sub>106绑图+51SCI</sub></td>
<td width="20%" align="center"><a href="./paper-deep-read/"><img src="https://img.shields.io/badge/📖-paper_deep_read_v3-1565C0?style=for-the-badge"/></a><br><br>论文深度解读<br><sub>复现者+审稿人双视角</sub></td>
<td width="20%" align="center"><a href="./academic-group-meeting-pipeline/"><img src="https://img.shields.io/badge/🎤-group_meeting-7B1FA2?style=for-the-badge"/></a><br><br>组会汇报流水线<br><sub>论文→PPT→答辩</sub></td>
<td width="20%" align="center"><a href="./md2ipynb-sync/"><img src="https://img.shields.io/badge/📝-md2ipynb_sync-FF6F00?style=for-the-badge"/></a><br><br>Obsidian↔Jupyter同步<br><sub>MD↔IPYNB双向</sub></td>
</tr>
</table>

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/Elephenman/newbe.git

# Use any tool
cd fastq-qc-checker
python fastq_qc_checker.py
```

Each tool is self-contained — all parameters via interactive `input()` with defaults.

---

## 📌 Recent Updates

> **2026-04-28** — 50 bioinformatics tools added (all complete, interactive input)
> **2026-04-27** — Initial release: 5 original sub-projects

---

## 🗺️ Roadmap

- [x] 50 bioinformatics tools (complete with interactive input)
- [x] FASTQ/BAM/VCF/GTF/BED processing tools
- [x] DESeq2/enrichment/WGCNA/survival analysis pipelines
- [x] Seurat/CellChat/pseudotime/single-cell QC
- [x] DNA damage gene collector (for LU lab)
- [x] PubMed/DOI/citation/reference literature tools
- [x] Color palette/figure check/panel compose workflow tools
- [ ] Auto-expand: 50 new tools every 3 hours via automation

---

## 📄 License

[MIT License](./LICENSE) — use freely, modify freely, share freely.