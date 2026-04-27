# 🧬 genome-fasta-slicer
**从参考基因组按坐标切片提取序列** — 支持BED批量输入和上下游flank

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 参考基因组FASTA路径 | 输入 | genome.fa |
| 坐标文件路径(BED/TSV) | 区域定义 | regions.bed |
| 上下游flank长度(bp) | 提取额外区域 | 0 |
| 输出FASTA路径 | 输出 | genome_slices.fasta |

MIT License