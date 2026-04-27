# 🎯 enrichment-auto-pipeline
**GO/KEGG富集分析一键流水线** — clusterProfiler封装

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 基因列表文件路径 | 每行一个基因符号 | genes.txt |
| 物种 | human/mouse/yeast/zebrafish | human |
| 富集类型 | GO/KEGG/both | both |
| padj阈值 | 显著性阈值 | 0.05 |
| 图片类型 | dot/bar | dot |

依赖: clusterProfiler, org.Hs.eg.db, enrichplot

MIT License