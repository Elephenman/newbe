# 🔬 vcf-filter-annotate
**VCF变异过滤+注释格式化** — 按QUAL/DP/缺失率过滤，输出VCF或TSV

| 参数 | 说明 | 默认值 |
|------|------|--------|
| VCF文件路径 | 输入文件 | variants.vcf |
| 最小QUAL阈值 | 质量过滤 | 30 |
| 最小DP阈值 | 深度过滤 | 10 |
| 最大缺失率 | 缺失比例 | 0.5 |
| 是否保留INDEL | yes/no | yes |
| 输出格式 | vcf/tsv | tsv |

MIT License