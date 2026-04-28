<div align="center">

# 🛠️ Newbe

**面向生信研究者的开源工具箱 — 160+ 交互式小工具，开箱即用**

[![GitHub](https://img.shields.io/badge/GitHub-Elephenman/newbe-blue?logo=github)](https://github.com/Elephenman/newbe)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-4.0+-276DC3?logo=r&logoColor=white)](https://cran.r-project.org/)
[![Tools](https://img.shields.io/badge/Tools-160+-orange)](https://github.com/Elephenman/newbe)

</div>

---

## 🌟 Newbe 是什么？

**Newbe** 是一个面向生物信息学研究者的开源工具集合，涵盖从测序数据质控、转录组分析、单细胞处理、基因组变异注释，到文献管理、学术写作、科研可视化的 **160+ 个交互式小工具**。

每个工具都是**独立可运行**的——无需安装复杂依赖，无需配置环境文件，直接运行脚本，按提示输入参数即可。所有参数均提供合理默认值，回车即可使用。

### 💡 Newbe 能做什么？

| 场景 | 工具举例 |
|------|---------|
| 测序数据拿到手，先看看质量行不行 | `fastq-qc-checker` → 3秒出Q20/Q30/GC/Adapter报告 |
| FASTQ需要过滤低质量reads | `fastq-filter` → 按质量/长度/GC一键过滤 |
| DESeq2跑完了，结果怎么出图 | `deseq2-result-formatter` → 发表级火山图+统计表 |
| 做了单细胞，质控+注释一头雾水 | `seurat-qc-pipeline` + `cell-type-annotator` → 一条龙 |
| 文献太多管不过来 | `pubmed-batch-searcher` + `obsidian-paper-note-generator` → 检索+笔记 |
| 论文配图配色丑 | `sci-color-palette` → Nature/Cell配色一键生成 |
| ……还有 150+ 个场景 | 往下看 👇 |

### ✨ 核心特性

- 🎯 **交互式输入** — 每个参数都有提示和默认值，回车即用，零配置启动
- 📦 **独立运行** — 每个工具自包含，不依赖项目内其他工具
- 🐍 **双语言覆盖** — Python 工具 120+ 个，R 工具 40+ 个
- 🧬 **全流程覆盖** — 从原始测序数据到发表级图表，一站式解决
- 🔓 **完全开源** — MIT 协议，随意使用、修改、分享

---

## 🚀 如何使用？

### 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/Elephenman/newbe.git
cd newbe

# 2. 进入任意工具目录
cd fastq-qc-checker

# 3. 运行（Python 工具）
python fastq_qc_checker.py

# 3. 运行（R 工具）
Rscript seurat_qc_pipeline.R
```

### 交互式输入模式

所有工具采用统一的交互式输入范式：

```
============================================================
  🧬 FASTQ质量一键体检报告
============================================================

输入FASTQ文件路径 [默认: sample.fastq.gz]: /data/sample_R1.fastq
是否生成报告文件 [默认: yes]: 
报告格式(txt/html) [默认: txt]: html
```

- 每个参数都有**中文提示**和**合理默认值**
- 直接回车使用默认值
- 输入完成后自动执行，结果立等可取

### 依赖说明

- **Python 工具**：大部分仅依赖标准库（`os`, `sys`, `collections`），少数需要 `matplotlib`/`plotly`/`pandas` 等第三方包
- **R 工具**：需要对应的 CRAN/Bioconductor 包（如 `Seurat`, `ggplot2`, `DESeq2` 等），脚本启动时会自动检测并提示安装

---

## 📋 工具目录

### 🧬 测序数据处理 (1-10)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
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

### 🧬 测序数据处理扩展 (51-60)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
| 51 | [sam-to-fastq-converter](./sam-to-fastq-converter/) | Python | SAM/BAM转FASTQ+可选拆分paired-end |
| 52 | [read-duplication-calculator](./read-duplication-calculator/) | Python | 测序reads重复率统计+分布可视化 |
| 53 | [adapter-trimmer-wrapper](./adapter-trimmer-wrapper/) | Python | FASTQ adapter序列检测+修剪报告 |
| 54 | [contig-length-plotter](./contig-length-plotter/) | Python | 组装contig/N50统计+长度分布图 |
| 55 | [coverage-depth-calculator](./coverage-depth-calculator/) | Python | BAM覆盖深度统计+区间分布 |
| 56 | [paired-end-sync-checker](./paired-end-sync-checker/) | Python | paired-end FASTQ配对一致性检查 |
| 57 | [base-quality-plotter](./base-quality-plotter/) | Python | 碱基质量值逐位置分布图 |
| 58 | [genome-size-estimator](./genome-size-estimator/) | Python | K-mer频率估算基因组大小+杂合度 |
| 59 | [fastq-duplicate-remover](./fastq-duplicate-remover/) | Python | FASTQ精确重复reads去重+统计 |
| 60 | [gff3-to-gtf-converter](./gff3-to-gtf-converter/) | Python | GFF3→GTF格式转换+属性保留 |

### 📊 转录组/表达分析 (11-20)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
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

### 📊 转录组/表达分析扩展 (61-70)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
| 61 | [volcano-plot-enhancer](./volcano-plot-enhancer/) | Python | 火山图增强版（标注+配色+阈值线） |
| 62 | [pathway-heatmap-builder](./pathway-heatmap-builder/) | R | 通路基因集表达热图+分层聚类 |
| 63 | [gene-length-normalizer](./gene-length-normalizer/) | Python | 基因长度偏差校正（RPKM/TPM/GC） |
| 64 | [expression-boxplot-maker](./expression-boxplot-maker/) | R | 基因表达箱线图批量生成+统计检验 |
| 65 | [deg-volcano-interactive](./deg-volcano-interactive/) | Python | 交互式火山图（Plotly点击查看基因） |
| 66 | [rna-seq-count-merger](./rna-seq-count-merger/) | Python | 多样本count矩阵合并+一致性检查 |
| 67 | [transcript-id-mapper](./transcript-id-mapper/) | Python | 转录本ID↔基因ID↔基因名批量映射 |
| 68 | [alternative-splicing-detector](./alternative-splicing-detector/) | R | 可变剪接事件检测+可视化 |
| 69 | [gene-set-enrichment-visualizer](./gene-set-enrichment-visualizer/) | R | 富集结果多维度可视化（气泡/条形/网络） |
| 70 | [expression-correlation-matrix](./expression-correlation-matrix/) | Python | 基因表达相关性矩阵+热图 |

### 🔬 单细胞/空间组学 (21-28)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
| 21 | [seurat-qc-pipeline](./seurat-qc-pipeline/) | R | Seurat质控一键流水线 |
| 22 | [cell-type-annotator](./cell-type-annotator/) | R | 单细胞自动注释辅助（marker匹配） |
| 23 | [umap-batch-plotter](./umap-batch-plotter/) | R | UMAP按多维度批量分色绘图 |
| 24 | [pseudotime-setup](./pseudotime-setup/) | R | 拟时序分析启动器（Monocle3/Slingshot） |
| 25 | [cellchat-interaction-parser](./cellchat-interaction-parser/) | R | CellChat细胞通讯一键分析 |
| 26 | [doublet-detector-wrapper](./doublet-detector-wrapper/) | R | 单细胞doublet检测+过滤 |
| 27 | [spatial-spot-annotator](./spatial-spot-annotator/) | R | 空间转录组spot自动注释 |
| 28 | [sc-marker-finder](./sc-marker-finder/) | R | 单细胞marker基因批量查找 |

### 🔬 单细胞/空间组学扩展 (71-80)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
| 71 | [seurat-integration-helper](./seurat-integration-helper/) | R | Seurat多样本整合辅助+批次校正评估 |
| 72 | [sc-trajectory-comparer](./sc-trajectory-comparer/) | R | 多拟时序方法结果对比+一致性评估 |
| 73 | [cell-proportion-analyzer](./cell-proportion-analyzer/) | R | 细胞类型比例变化分析+堆叠条形图 |
| 74 | [sc-cluster-stability-checker](./sc-cluster-stability-checker/) | R | 单细胞聚类稳定性评估+分辨率优化 |
| 75 | [spatial-deg-finder](./spatial-deg-finder/) | R | 空间转录组差异表达基因发现 |
| 76 | [sc-gene-module-extractor](./sc-gene-module-extractor/) | R | 单细胞基因模块提取+活性评分 |
| 77 | [neighborhood-enrichment-calculator](./neighborhood-enrichment-calculator/) | R | 细胞邻域富集分析（空间邻近偏好） |
| 78 | [sc-vega-pathway-plotter](./sc-vega-pathway-plotter/) | R | 单细胞通路活性小提琴图+统计 |
| 79 | [spatial-variability-mapper](./spatial-variability-mapper/) | R | 空间基因表达变异度可视化 |
| 80 | [cell-cycle-scorer](./cell-cycle-scorer/) | R | 单细胞周期评分+G1/S/G2M分类 |

### 🧪 基因组/变异/调控 (29-35)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
| 29 | [snp-stats-reporter](./snp-stats-reporter/) | Python | SNP/InDel变异统计报告+MAF分布 |
| 30 | [motif-scanner](./motif-scanner/) | Python | DNA序列motif扫描（JASPAR库） |
| 31 | [genome-density-plotter](./genome-density-plotter/) | Python | 染色体密度图（circos/线性） |
| 32 | [ld-decay-calculator](./ld-decay-calculator/) | Python | LD衰减曲线计算与绘图 |
| 33 | [promoter-extractor](./promoter-extractor/) | Python | 批量提取启动子序列+TSS注释 |
| 34 | [cnv-segment-plotter](./cnv-segment-plotter/) | Python | CNV分段结果可视化 |
| 35 | [dna-damage-gene-collector](./dna-damage-gene-collector/) | Python | 🔥DNA损伤修复基因集（对口陆慧智课题组） |

### 🧪 基因组/变异/调控扩展 (81-90)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
| 81 | [somatic-mutation-filter](./somatic-mutation-filter/) | Python | 体细胞变异过滤（肿瘤/正常配对） |
| 82 | [structural-variant-summarizer](./structural-variant-summarizer/) | Python | 结构变异(SV)类型统计+环形图 |
| 83 | [hi-c-contact-mapper](./hi-c-contact-mapper/) | Python | Hi-C接触矩阵可视化+TAD标注 |
| 84 | [atac-peak-annotator](./atac-peak-annotator/) | Python | ATAC-seq peak最近基因+调控元件注释 |
| 85 | [chip-seq-peak-merger](./chip-seq-peak-merger/) | Python | ChIP-seq peak合并+共有peak提取 |
| 86 | [repeat-region-masker](./repeat-region-masker/) | Python | 基因组重复序列标注+mask文件生成 |
| 87 | [codon-usage-analyzer](./codon-usage-analyzer/) | Python | 密码子使用偏性分析+RSCU/CAI计算 |
| 88 | [protein-domain-mapper](./protein-domain-mapper/) | Python | 蛋白质结构域注释+可视化分布 |
| 89 | [gene-ortholog-finder](./gene-ortholog-finder/) | Python | 跨物种同源基因查找+进化树构建 |
| 90 | [variant-effect-predictor-wrapper](./variant-effect-predictor-wrapper/) | Python | VEP/SnpEff结果解析+报告生成 |

### 📖 文献/学术工具 (36-43)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
| 36 | [pubmed-batch-searcher](./pubmed-batch-searcher/) | Python | PubMed批量检索+结果导出 |
| 37 | [doi-to-citation](./doi-to-citation/) | Python | DOI→APA/MLA/GB-T/BibTeX引用 |
| 38 | [paper-pdf-meta-extractor](./paper-pdf-meta-extractor/) | Python | PDF论文元数据自动提取 |
| 39 | [keyword-network-builder](./keyword-network-builder/) | Python | 文献关键词共现网络构建 |
| 40 | [literature-review-matrix](./literature-review-matrix/) | Python | 文献综述矩阵自动生成 |
| 41 | [citation-tracker](./citation-tracker/) | Python | 论文被引追踪+趋势图 |
| 42 | [reference-cleaner](./reference-cleaner/) | Python | 参考文献格式统一清洗+DOI验证 |
| 43 | [obsidian-paper-note-generator](./obsidian-paper-note-generator/) | Python | 论文→Obsidian笔记模板（精简/详细/组会） |

### 📖 文献/学术工具扩展 (91-100)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
| 91 | [manuscript-word-counter](./manuscript-word-counter/) | Python | 论文逐章节字数统计+合规检查 |
| 92 | [figure-caption-extractor](./figure-caption-extractor/) | Python | 论文图表标题批量提取+编号校验 |
| 93 | [supplementary-file-organizer](./supplementary-file-organizer/) | Python | 附件材料整理+编号重排+目录生成 |
| 94 | [grant-budget-calculator](./grant-budget-calculator/) | Python | 基金预算自动计算+分项汇总 |
| 95 | [experiment-timer-tracker](./experiment-timer-tracker/) | Python | 实验时间记录+耗时统计+效率报告 |
| 96 | [lab-reagent-inventory](./lab-reagent-inventory/) | Python | 实验室试剂库存管理+过期预警 |
| 97 | [conference-abstract-formatter](./conference-abstract-formatter/) | Python | 会议摘要格式化+字数合规检查 |
| 98 | [research-diary-generator](./research-diary-generator/) | Python | 科研日记模板生成+Markdown格式 |
| 99 | [thesis-chapter-outline](./thesis-chapter-outline/) | Python | 学位论文章节大纲生成+进度追踪 |
| 100 | [lab-meeting-minute-generator](./lab-meeting-minute-generator/) | Python | 组会纪要模板生成+待办追踪 |

### 🎨 绘图/数据/流程工具 (44-50)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
| 44 | [sci-color-palette](./sci-color-palette/) | Python | 科研配色方案生成器（Nature/Cell配色库） |
| 45 | [figure-size-checker](./figure-size-checker/) | Python | 论文图片合规检查（DPI/尺寸/格式） |
| 46 | [multi-panel-composer](./multi-panel-composer/) | Python | 多子图组合排版（ABCD标签） |
| 47 | [project-dir-initializer](./project-dir-initializer/) | Python | 科研项目目录一键初始化+git init |
| 48 | [sample-sheet-validator](./sample-sheet-validator/) | Python | 实验样本表格式校验 |
| 49 | [conda-env-checker](./conda-env-checker/) | Python | 项目环境依赖一致性检查 |
| 50 | [pipeline-log-parser](./pipeline-log-parser/) | Python | 分析流程日志解析+耗时统计 |

### 🎨 绘图/数据/流程工具扩展 (101-110)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
| 101 | [circos-plot-builder](./circos-plot-builder/) | Python | Circos环形图数据准备+配置生成 |
| 102 | [sankey-flow-visualizer](./sankey-flow-visualizer/) | Python | Sankey流向图（数据通路/样本流转） |
| 103 | [ridgeline-plot-maker](./ridgeline-plot-maker/) | R | Ridgeline山脊图（多组分布对比） |
| 104 | [correlation-scatter-matrix](./correlation-scatter-matrix/) | Python | 相关性散点矩阵图+回归线 |
| 105 | [timeline-gantt-plotter](./timeline-gantt-plotter/) | Python | 项目时间线甘特图+里程碑标注 |
| 106 | [stats-summary-table-maker](./stats-summary-table-maker/) | Python | 统计摘要表一键生成（均值/SD/检验） |
| 107 | [data-type-converter](./data-type-converter/) | Python | CSV↔TSV↔JSON↔Excel格式互转 |
| 108 | [markdown-to-slides-converter](./markdown-to-slides-converter/) | Python | Markdown→reveal.js幻灯片转换 |
| 109 | [notebook-cell-extractor](./notebook-cell-extractor/) | Python | Jupyter notebook指定cell提取+导出 |
| 110 | [result-file-aggregator](./result-file-aggregator/) | Python | 分析结果文件自动汇总+索引生成 |

### 🧬 测序数据处理进阶 (111-120)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
| 111 | [fastq-quality-trimmer](./fastq-quality-trimmer/) | Python | 根据质量值对FASTQ reads进行3'/5'端截尾修剪 |
| 112 | [bam-coverage-plotter](./bam-coverage-plotter/) | Python | 从BAM文件计算并绘制基因组覆盖度分布图 |
| 113 | [vcf-concordance-checker](./vcf-concordance-checker/) | Python | 比较两个VCF文件的变异一致性 |
| 114 | [fasta-stats-reporter](./fasta-stats-reporter/) | Python | 统计FASTA文件长度/GC/N含量等 |
| 115 | [sequencing-depth-calculator](./sequencing-depth-calculator/) | Python | 根据FASTQ和基因组大小计算测序深度 |
| 116 | [fastq-subset-sampler](./fastq-subset-sampler/) | Python | 从FASTQ中随机采样指定数量或比例的reads |
| 117 | [bam-filter-by-flag](./bam-filter-by-flag/) | Python | 根据SAM flag过滤BAM reads |
| 118 | [vcf-genotype-extractor](./vcf-genotype-extractor/) | Python | 从VCF提取指定样本的基因型矩阵 |
| 119 | [bed-fasta-extractor](./bed-fasta-extractor/) | Python | 根据BED坐标从FASTA中提取序列 |
| 120 | [multi-fasta-concatenator](./multi-fasta-concatenator/) | Python | 多FASTA合并+文件名前缀避免ID冲突 |

### 📊 转录组/表达分析进阶 (121-130)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
| 121 | [deg-pathway-annotator](./deg-pathway-annotator/) | R | DEG结果自动注释到KEGG/GO通路 |
| 122 | [wgcna-module-extractor](./wgcna-module-extractor/) | R | WGCNA共表达网络模块识别 |
| 123 | [rna-seq-normalizer](./rna-seq-normalizer/) | Python | RNA-seq计数TPM/FPKM/RPKM/CPM标准化 |
| 124 | [gene-fusion-detector](./gene-fusion-detector/) | Python | STAR-Fusion/Arriba融合事件筛选 |
| 125 | [isoform-expression-comparer](./isoform-expression-comparer/) | R | 同一基因不同亚型表达差异可视化 |
| 126 | [deg-venn-plotter](./deg-venn-plotter/) | Python | 多组DEG韦恩图绘制 |
| 127 | [expression-violin-plotter](./expression-violin-plotter/) | R | 多基因/多样本表达小提琴图 |
| 128 | [rna-editing-site-finder](./rna-editing-site-finder/) | Python | RNA-seq VCF中候选RNA编辑位点筛选 |
| 129 | [splice-junction-counter](./splice-junction-counter/) | Python | STAR SJ.out.tab剪接junction统计 |
| 130 | [gene-id-version-normalizer](./gene-id-version-normalizer/) | Python | 基因ID格式统一(去版本号等) |

### 🔬 单细胞/空间组学进阶 (131-140)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
| 131 | [sc-mitochondria-filter](./sc-mitochondria-filter/) | R | 线粒体基因比例过滤低质量细胞 |
| 132 | [sc-doublet-visualizer](./sc-doublet-visualizer/) | R | 双细胞检测结果UMAP可视化 |
| 133 | [spatial-niche-detector](./spatial-niche-detector/) | R | 空间转录组生态位检测 |
| 134 | [sc-rna-velocity-runner](./sc-rna-velocity-runner/) | R | RNA velocity分析流程包装 |
| 135 | [spatial-deconvolution-wrapper](./spatial-deconvolution-wrapper/) | R | 空间反卷积(SPOTlight) |
| 136 | [sc-subset-extractor](./sc-subset-extractor/) | R | 按条件提取单细胞子集 |
| 137 | [sc-differential-abundance](./sc-differential-abundance/) | R | 单细胞差异丰度分析 |
| 138 | [spatial-moran-plotter](./spatial-moran-plotter/) | R | 空间Moran's I自相关统计 |
| 139 | [sc-gene-trend-plotter](./sc-gene-trend-plotter/) | R | 基因沿伪时间趋势图 |
| 140 | [spatial-neighbor-graph](./spatial-neighbor-graph/) | R | 空间邻域图构建与可视化 |

### 🧪 基因组/变异/调控进阶 (141-150)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
| 141 | [germline-variant-filter](./germline-variant-filter/) | Python | 胚系变异过滤与分类 |
| 142 | [mutational-signature-extractor](./mutational-signature-extractor/) | Python | 突变特征SBS96谱提取与可视化 |
| 143 | [enhancer-target-linker](./enhancer-target-linker/) | Python | 基于Hi-C数据关联增强子与靶基因 |
| 144 | [replication-timing-plotter](./replication-timing-plotter/) | Python | 复制时序Repli-seq可视化 |
| 145 | [dna-damage-hotspot-finder](./dna-damage-hotspot-finder/) | Python | 🔥DNA损伤修复热点区域识别 |
| 146 | [copy-number-segment-annotator](./copy-number-segment-annotator/) | Python | CNV片段基因注释 |
| 147 | [methylation-beta-calculator](./methylation-beta-calculator/) | Python | 甲基化β值计算与统计 |
| 148 | [tf-binding-site-comparer](./tf-binding-site-comparer/) | Python | 两条件TF结合位点差异比较 |
| 149 | [snp-ld-block-extractor](./snp-ld-block-extractor/) | Python | LD block提取与tag SNP识别 |
| 150 | [chromatin-state-annotator](./chromatin-state-annotator/) | Python | ChromHMM染色质状态注释 |

### 🎨 文献/学术/绘图/流程进阶 (151-160)

| # | 工具 | 语言 | 说明 |
|---|------|------|------|
| 151 | [paper-figure-organizer](./paper-figure-organizer/) | Python | 论文图片按Figure编号自动整理 |
| 152 | [experiment-design-checker](./experiment-design-checker/) | Python | 实验设计检查(重复/对照/平衡) |
| 153 | [bioinformatics-pipeline-doc](./bioinformatics-pipeline-doc/) | Python | 生信流程文档自动生成 |
| 154 | [genomic-coordinate-converter](./genomic-coordinate-converter/) | Python | 基因组坐标系统转换(hg19↔hg38) |
| 155 | [heatmap-annotation-builder](./heatmap-annotation-builder/) | Python | 热图行列注释文件构建 |
| 156 | [volcano-label-editor](./volcano-label-editor/) | Python | 火山图标签编辑器(添加/修改基因标签) |
| 157 | [colorblind-safe-palette-generator](./colorblind-safe-palette-generator/) | Python | 色盲友好科研配色方案生成 |
| 158 | [boxplot-outlier-detector](./boxplot-outlier-detector/) | Python | 箱线图异常值检测与报告 |
| 159 | [multi-omics-integration-helper](./multi-omics-integration-helper/) | Python | 多组学数据整合辅助 |
| 160 | [benchmark-result-comparator](./benchmark-result-comparator/) | Python | 基准测试结果比较与排名 |

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

## 📌 更新日志

| 日期 | 更新内容 |
|------|---------|
| 2026-04-28 | Batch 3: 50 new bioinformatics tools added (#111-#160, 36 Python + 14 R, DNA damage hotspot finder for LU lab) |
| 2026-04-28 | Batch 2: 60 new bioinformatics tools added (#51-#110, interactive input, 45 Python + 15 R) |
| 2026-04-28 | Batch 1: 50 bioinformatics tools added (all complete, interactive input) |
| 2026-04-27 | Initial release: 5 original sub-projects |

---

## 🗺️ Roadmap

- [x] 50 bioinformatics tools (complete with interactive input)
- [x] 60 new bioinformatics tools (#51-#110, all interactive)
- [x] 50 new bioinformatics tools (#111-#160, 36 Python + 14 R)
- [x] FASTQ/BAM/VCF/GTF/BED processing tools
- [x] DESeq2/enrichment/WGCNA/survival analysis pipelines
- [x] Seurat/CellChat/pseudotime/single-cell QC
- [x] DNA damage gene collector (for LU lab)
- [x] PubMed/DOI/citation/reference literature tools
- [x] Color palette/figure check/panel compose workflow tools
- [x] Hi-C/ATAC-seq/ChIP-seq/variant analysis tools
- [x] Circos/Sankey/Ridgeline/Gantt visualization tools
- [x] WGCNA/Pathway/Violin/Venn/RNA-editing analysis
- [x] Spatial niche/Moran/velocity/deconvolution tools
- [x] SBS96/CNV/Enhancer/Methylation/ChromHMM tools
- [x] Colorblind-safe palette/benchmark/outlier detection tools
- [ ] Auto-expand: more tools every 3 hours via automation

---

## 📄 License

[MIT License](./LICENSE) — use freely, modify freely, share freely.
