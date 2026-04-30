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

| Category | Tools | Description |
|----------|:-----:|-------------|
| [🧬 Sequencing QC](./sequencing-qc/) | 18 | FASTQ/BAM quality control, filtering, trimming, deduplication, sampling tools |
| [🔗 Alignment & BAM](./alignment-bam/) | 8 | BAM/SAM statistics, filtering, coverage, insert size processing tools |
| [🧪 Variant & Genomic Analysis](./variant-analysis/) | 28 | VCF/SNP/Indel/CNV/SV/GWAS/haplotype/mutational signature variant analysis tools |
| [📊 RNA-seq & Expression](./rna-expression/) | 34 | DESeq2/DEG/normalization/volcano/heatmap/WGCNA RNA-seq expression analysis tools |
| [🔬 Single-Cell Analysis](./single-cell/) | 36 | Seurat QC/annotation/clustering/integration/pseudotime/CellChat/doublet single-cell tools |
| [🗺️ Spatial Transcriptomics](./spatial-transcriptomics/) | 13 | Spatial spot annotation/DEG/deconvolution/Moran's I/niche/neighbor graph tools |
| [🧫 Epigenomics](./epigenomics/) | 14 | ChIP-seq/ATAC-seq/methylation/Hi-C/TF motif/enhancer/chromatin state epigenomics tools |
| [📖 Genome Annotation](./genome-annotation/) | 14 | GTF/BED/coordinate conversion/promoter/intron/Circos/genome density annotation tools |
| [🧬 Sequence Analysis](./sequence-analysis/) | 15 | FASTA stats/alignment/k-mer/codon/N50/synteny sequence analysis tools |
| [🌐 Gene Function & Pathway](./gene-function/) | 21 | Enrichment/GSEA/pathway network/DDR/co-expression/WGCNA module gene function tools |
| [🎨 Visualization & Plotting](./visualization/) | 18 | Color palette/heatmap/Venn/Forest/Ridgeline/dot plot/general visualization tools |
| [🔄 Data Format Conversion](./data-format/) | 7 | Format conversion/ID mapping/FASTQ-to-FASTA data format processing tools |
| [📋 Lab & Project Management](./lab-project/) | 20 | Env check/project init/log/Gantt/reagent/protocol management tools |
| [📝 Academic Writing & Literature](./academic-writing/) | 29 | PubMed/DOI/citation/note/manuscript/conference/grant academic writing tools |

| **Total** | **275** | **14 categories covering the full bioinformatics pipeline** |

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

## 📌 Changelog

| Date | Update |
|------|--------|
| 2026-04-30 | Reorganized 275 tools into 14 categorized subfolders |
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
