<div align="center">

# 🧬 测序数据质控

**FASTQ/BAM质控、过滤、修剪、去重、采样等原始测序数据处理工具** (18个工具)

</div>

---

## 工具列表

| # | 工具 | 语言 | 说明 |
|---|------|:----:|------|
| 1 | [adapter-trimmer-wrapper](./adapter-trimmer-wrapper/) | Python | FASTQ adapter detection + trimming report |
| 2 | [base-quality-plotter](./base-quality-plotter/) | Python | Per-position base quality distribution plot |
| 3 | [fastq-barcode-splitter](./fastq-barcode-splitter/) | Python | Split FASTQ by barcode/index tags |
| 4 | [fastq-duplicate-remover](./fastq-duplicate-remover/) | Python | Remove exact duplicate reads from FASTQ |
| 5 | [fastq-filter](./fastq-filter/) | Python | Filter FASTQ by quality/length/GC content |
| 6 | [fastq-interleave-splitter](./fastq-interleave-splitter/) | Python | 将两个配对FASTQ文件交叉合并为单个交错文件。 |
| 7 | [fastq-qc-checker](./fastq-qc-checker/) | Python | FASTQ quality report (Q20/Q30/GC/Adapter, no FastQC dependency) |
| 8 | [fastq-quality-trimmer](./fastq-quality-trimmer/) | Python | Trim FASTQ reads by 3'/5' quality scores |
| 9 | [fastq-read-length-filter](./fastq-read-length-filter/) | Python | Filter FASTQ by read length range |
| 10 | [fastq-read-name-extractor](./fastq-read-name-extractor/) | Python | Extract and deduplicate FASTQ read names |
| 11 | [fastq-strand-detector](./fastq-strand-detector/) | Python | 根据SAM/BAM比对结果推断FASTQreads的链特异性信息（RF/FR/RR/FF）。 |
| 12 | [fastq-subset-sampler](./fastq-subset-sampler/) | Python | Random sampling of FASTQ reads by count or ratio |
| 13 | [paired-end-sync-checker](./paired-end-sync-checker/) | Python | Verify paired-end FASTQ file consistency |
| 14 | [qc-report-aggregator](./qc-report-aggregator/) | Python | Aggregate multiple QC reports with composite scoring |
| 15 | [read-duplication-calculator](./read-duplication-calculator/) | Python | Calculate read duplication rate + distribution |
| 16 | [sample-sheet-validator](./sample-sheet-validator/) | Python | Validate sample sheet format and metadata |
| 17 | [sequencing-depth-calculator](./sequencing-depth-calculator/) | Python | Calculate sequencing depth from FASTQ + genome size |
| 18 | [umi-deduplication-calculator](./umi-deduplication-calculator/) | Python | 基于UMI标签计算reads去重率和唯一分子数统计。 |

---

← [返回主目录](../)
