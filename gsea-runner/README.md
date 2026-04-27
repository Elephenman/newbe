# 🌊 gsea-runner
**GSEA分析一键运行** — fgsea/clusterProfiler封装

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 表达矩阵路径 | 行=基因,列=样本 | expression.csv |
| 分组标签文件 | 样本名+分组 | groups.txt |
| 基因集 | KEGG/Reactome/custom | KEGG |
| pvalue阈值 | 显著性 | 0.05 |
| 物种 | human/mouse | human |

依赖: fgsea, ggplot2, clusterProfiler(可选)

MIT License