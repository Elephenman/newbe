# 🔥 expression-heatmap-cluster
**表达矩阵→聚类热图** — R脚本，pheatmap，Nature/Cell配色

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 表达矩阵CSV路径 | 行=基因,列=样本 | expression.csv |
| 是否log2转换 | yes/no | yes |
| 聚类方法 | hierarchical/kmeans | hierarchical |
| topN高变异基因 | 取变异最大的N个 | 500 |
| 配色 | Nature/Cell/BlueRed | Nature |

```bash
Rscript expression_heatmap_cluster.R
```

依赖: ggplot2, pheatmap

MIT License