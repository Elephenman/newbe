# 📊 tpm-fpkm-calculator
**raw counts → TPM/FPKM/CPM转换器** — 纯Python矩阵运算

| 参数 | 说明 | 默认值 |
|------|------|--------|
| count矩阵CSV路径 | 行=基因,列=样本 | counts.csv |
| 基因长度文件路径 | 基因名+长度(TSV) | gene_lengths.tsv |
| 转换类型 | TPM/FPKM/CPM/all | TPM |
| 是否log2转换 | yes/no | no |

依赖: numpy

MIT License