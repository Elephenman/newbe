[English](./README.md) · [中文](./README_CN.md)

<div align="center">

# 🛠️ Newbe

**Open-source bioinformatics toolbox for researchers — 275+ interactive tools, ready to use**

[![GitHub](https://img.shields.io/badge/GitHub-Elephenman/newbe-blue?logo=github)](https://github.com/Elephenman/newbe)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-4.0+-276DC3?logo=r&logoColor=white)](https://cran.r-project.org/)
[![Tools](https://img.shields.io/badge/Tools-275+-orange)](https://github.com/Elephenman/newbe)

</div>

---

## 🌟 What is Newbe?

**Newbe** is an open-source toolkit for bioinformatics researchers, providing **275+ interactive micro-tools** covering everything from sequencing QC to publication-grade figures.

Each tool is **standalone** — no complex dependencies, just run the script and follow the prompts. All parameters have sensible defaults, press Enter to use them.

### ✨ Key Features

- 🎯 **Interactive Input** — Every parameter has prompts and defaults, press Enter to use defaults
- 📦 **Standalone** — Each tool is self-contained, no cross-tool dependencies
- 🐍 **Dual Language** — 190+ Python tools, 80+ R tools
- 🧬 **Full Pipeline** — From raw sequencing data to publication-grade figures
- 🔓 **Open Source** — MIT license, use/modify/share freely

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Elephenman/newbe.git
cd newbe

# 2. Navigate to a tool (e.g. sequencing QC)
cd sequencing-qc/fastq-qc-checker

# 3. Run
python fastq_qc_checker.py      # Python tool
Rscript seurat_qc_pipeline.R    # R tool
```

All tools use unified interactive input — each parameter has **prompts** and **sensible defaults**, press Enter to accept.

---

## 📋 Tool Directory

> Click a category to see detailed tool descriptions within that category.

<table>
<tr>
<td width="50%">

### 🧬 [Sequencing QC](./sequencing-qc/) <sup>18</sup>

FASTQ/BAM quality control, filtering, trimming, deduplication, sampling

- Adapter detection & trimming · Base quality distribution · Barcode splitting
- Duplicate read removal · Quality/length/GC filtering · Paired-end sync check
- Read length filtering · Strand orientation detection · UMI dedup statistics
- QC report aggregation · Sequencing depth calculation · Sample sheet validation

</td>
<td width="50%">

### 🔗 [Alignment & BAM](./alignment-bam/) <sup>8</sup>

BAM/SAM statistics, filtering, coverage, insert size

- Chromosome info extraction · Coverage distribution plot · SAM flag filtering
- Insert size statistics · Mate-pair resolution · Read count summarization
- BAM key metrics report · Coverage depth statistics

</td>
</tr>

<tr>
<td width="50%">

### 🧪 [Variant & Genomic Analysis](./variant-analysis/) <sup>28</sup>

VCF · SNP · CNV · SV · GWAS · Haplotype · Mutational Signature

- Manhattan & QQ plots · LD decay curve · Haplotype phasing (PS/HP tags)
- SBS96 signature extraction · CNV segment annotation · SV breakpoint visualization
- Germline/somatic variant filtering · Clinical annotation · Ancestry inference
- VCF filtering/parsing/concordance · MAF distribution · Missingness check

</td>
<td width="50%">

### 📊 [RNA-seq & Expression](./rna-expression/) <sup>34</sup>

DESeq2 · DEG · Normalization · Volcano · Heatmap · WGCNA

- DESeq2 result formatting · Multi-group DEG comparison (Venn/UpSet)
- Volcano plot (interactive/enhanced/label editor) · Clustered heatmap
- TPM/FPKM/RPKM normalization · ERCC spike-in · Z-score transformation
- DEG effect size/FDR correction/meta-analysis · Batch effect inspection
- Expression boxplot/violin/percentile ranking · Splice junction counting

</td>
</tr>

<tr>
<td width="50%">

### 🔬 [Single-Cell Analysis](./single-cell/) <sup>36</sup>

Seurat · Annotation · Clustering · Integration · Pseudotime · CellChat

- Seurat QC pipeline & integration · Auto annotation · Marker gene discovery
- PCA/t-SNE/UMAP · Harmony batch correction · Batch UMAP coloring
- Pseudotime (Monocle3) · RNA velocity · Doublet detection & visualization
- Cell cycle scoring & regression · Variable feature selection · JackStraw test
- Cell proportion analysis · Neighborhood enrichment · Gene module & trend

</td>
<td width="50%">

### 🗺️ [Spatial Transcriptomics](./spatial-transcriptomics/) <sup>13</sup>

Spot annotation · DEG · Deconvolution · Moran · Niche · Neighbor graph

- Spot auto annotation & quality filtering · Spatial DEG discovery
- Deconvolution (SPOTlight) · Moran's I autocorrelation · Geary's test
- Niche detection · Neighbor graph construction · Zone boundary segmentation
- Co-expression map · Distance decay · Variability mapping

</td>
</tr>

<tr>
<td width="50%">

### 🧫 [Epigenomics](./epigenomics/) <sup>14</sup>

ChIP-seq · ATAC-seq · Methylation · Hi-C · TF · Enhancer

- ATAC peak annotation · ChIP peak merging · Chromatin state annotation
- Methylation beta value · TF footprint detection · Motif scanning & enrichment
- Enhancer signal quantification & target linking · Hi-C contact matrix
- CTCF insulator boundary · Replication origin/timing · TF binding site comparison

</td>
<td width="50%">

### 📖 [Genome Annotation](./genome-annotation/) <sup>14</sup>

GTF · BED · Coordinate conversion · Promoter · Intron · Circos

- GTF exon/intron/feature extraction · BED intersection/merge/annotation
- Genome coordinate conversion (hg19↔hg38) · Promoter extraction
- Circos plot · Genome density plot · Multi-track overlay
- Repeat region masking · Genome bin statistics · Coverage interpolation

</td>
</tr>

<tr>
<td width="50%">

### 🧬 [Sequence Analysis](./sequence-analysis/) <sup>15</sup>

FASTA · Alignment · k-mer · Codon · N50 · Synteny · Phylogenetics

- FASTA stats/reverse/slice · Needleman-Wunsch alignment · K-mer frequency
- Codon usage bias (RSCU/CAI) · N50/L50 statistics · Genome size estimation
- GC sliding window · Synteny block detection · Multi-FASTA concatenation
- Phylogenetic tree batch processing · Contig length distribution

</td>
<td width="50%">

### 🌐 [Gene Function & Pathway](./gene-function/) <sup>21</sup>

Enrichment · GSEA · Pathway network · DDR · Co-expression · WGCNA

- GO/KEGG enrichment pipeline · GSEA runner & rank file generation
- WGCNA module extraction · Co-expression network · Pathway cross-talk
- DDR pathway mapping/mutational scoring/damage hotspot/signal correlation
- Gene desert · Ortholog finder · Protein domain · Survival correlation
- Sankey flow diagram · Pathway heatmap/network · Multi-omics integration

</td>
</tr>

<tr>
<td width="50%">

### 🎨 [Visualization & Plotting](./visualization/) <sup>18</sup>

Palette · Heatmap · Venn · Forest · Ridgeline · Dot plot

- Nature/Cell color palettes · Colorblind-safe palette · R plot template library
- Venn diagram (2-5 sets) · Forest plot · Ridgeline plot
- Heatmap annotation & sorting · Enhanced dot plot · Stacked bar chart
- Correlation matrix · Stats summary table · Boxplot outlier detection · Comparison table

</td>
<td width="50%">

### 🔄 [Data Format Conversion](./data-format/) <sup>7</sup>

CSV↔TSV↔JSON↔Excel · ID mapping · FASTQ↔FASTA · SAM↔FASTQ

- Universal format conversion · DPI conversion (300/600) · FASTQ→FASTA
- GFF3→GTF · SAM/BAM→FASTQ · Gene ID version normalization
- Transcript ↔ Gene ID ↔ Gene name mapping

</td>
</tr>

<tr>
<td width="50%">

### 📋 [Lab & Project Management](./lab-project/) <sup>20</sup>

Environment · Init · Logs · Gantt · Reagents · Protocol

- Conda env check & export · Project directory init · Pipeline documentation
- Pipeline log parsing · Gantt chart + milestones · Protocol versioning
- Reagent inventory + expiry alerts · Experiment timer · Meeting minutes
- Grant budget calculator · Experiment design checker · Result aggregation · R template

</td>
<td width="50%">

### 📝 [Academic Writing & Literature](./academic-writing/) <sup>29</sup>

PubMed · DOI · Citation · Notes · Manuscript · Conference · Grant

- PubMed batch search · DOI→citation format · Citation tracking & trends
- Obsidian note template · arXiv downloader · BibTeX network
- Deep paper reading · Readability score · Word/section count
- Figure compliance check/layout/labels · Reference cleanup · Conference abstract
- Thesis outline · Grant budget · Keyword extraction · Plagiarism check

</td>
</tr>
</table>

---

## 🧬 5 Original Sub-Projects

<table>
<tr>
<td width="20%" align="center"><a href="./sequence-analysis/phylo-tools/"><img src="https://img.shields.io/badge/🧬-phylo_tools-6B8E23?style=for-the-badge"/></a><br><br>Phylogenetic tree<br>batch processing<br><sub>3 Python scripts</sub></td>
<td width="20%" align="center"><a href="./visualization/r-plot-templates/"><img src="https://img.shields.io/badge/🎨-r_plot_templates-E91E63?style=for-the-badge"/></a><br><br>R scientific plot<br>template library<br><sub>106 plots + 51 SCI</sub></td>
<td width="20%" align="center"><a href="./academic-writing/paper-deep-read/"><img src="https://img.shields.io/badge/📖-paper_deep_read-1565C0?style=for-the-badge"/></a><br><br>Deep paper reading<br><sub>Reproducer + reviewer</sub></td>
<td width="20%" align="center"><a href="./lab-project/academic-group-meeting-pipeline/"><img src="https://img.shields.io/badge/🎤-group_meeting-7B1FA2?style=for-the-badge"/></a><br><br>Meeting pipeline<br><sub>Paper → PPT → defense</sub></td>
<td width="20%" align="center"><a href="./lab-project/md2ipynb-sync/"><img src="https://img.shields.io/badge/📝-md2ipynb-FF6F00?style=for-the-badge"/></a><br><br>Obsidian↔Jupyter<br>bidirectional sync<br><sub>MD ↔ IPYNB</sub></td>
</tr>
</table>

---

## 📄 License

[MIT License](./LICENSE) — use freely, modify freely, share freely.