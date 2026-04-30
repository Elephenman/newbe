<div align="center">

# 🧬 Sequencing QC

**FASTQ/BAM quality control, filtering, trimming, deduplication, sampling tools** (18 tools)

</div>

---

## Tool List

| # | Tool | Language | Description |
|---|------|:--------:|-------------|
| 1 | [adapter-trimmer-wrapper](./adapter-trimmer-wrapper/) | Python | FASTQ adapter detection + trimming report |
| 2 | [base-quality-plotter](./base-quality-plotter/) | Python | Per-position base quality distribution plot |
| 3 | [fastq-barcode-splitter](./fastq-barcode-splitter/) | Python | Split FASTQ by barcode/index tags |
| 4 | [fastq-duplicate-remover](./fastq-duplicate-remover/) | Python | Remove exact duplicate reads from FASTQ |
| 5 | [fastq-filter](./fastq-filter/) | Python | Filter FASTQ by quality/length/GC content |
| 6 | [fastq-interleave-splitter](./fastq-interleave-splitter/) | Python | Split interleaved paired-end FASTQ into R1/R2 |
| 7 | [fastq-qc-checker](./fastq-qc-checker/) | Python | FASTQ quality report (Q20/Q30/GC/Adapter, no FastQC dependency) |
| 8 | [fastq-quality-trimmer](./fastq-quality-trimmer/) | Python | Trim FASTQ reads by 3'/5' quality scores |
| 9 | [fastq-read-length-filter](./fastq-read-length-filter/) | Python | Filter FASTQ by read length range |
| 10 | [fastq-read-name-extractor](./fastq-read-name-extractor/) | Python | Extract and deduplicate FASTQ read names |
| 11 | [fastq-strand-detector](./fastq-strand-detector/) | Python | Detect paired-end strand orientation (FR/RF/FF/RR) |
| 12 | [fastq-subset-sampler](./fastq-subset-sampler/) | Python | Random sampling of FASTQ reads by count or ratio |
| 13 | [paired-end-sync-checker](./paired-end-sync-checker/) | Python | Verify paired-end FASTQ file consistency |
| 14 | [qc-report-aggregator](./qc-report-aggregator/) | Python | Aggregate multiple QC reports with composite scoring |
| 15 | [read-duplication-calculator](./read-duplication-calculator/) | Python | Calculate read duplication rate + distribution |
| 16 | [sample-sheet-validator](./sample-sheet-validator/) | Python | Validate sample sheet format and metadata |
| 17 | [sequencing-depth-calculator](./sequencing-depth-calculator/) | Python | Calculate sequencing depth from FASTQ + genome size |
| 18 | [umi-deduplication-calculator](./umi-deduplication-calculator/) | Python | Calculate UMI deduplication statistics from read headers |

---

← [Back to main directory](../)
