# 🎯 pca-tsne-umap-plotter
**表达矩阵降维可视化三合一** — PCA/tSNE/UMAP

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 表达矩阵CSV路径 | 行=基因,列=样本 | expression.csv |
| 分组标签文件 | 样本名+分组(TSV) | 留空=无分组 |
| 降维方法 | PCA/tSNE/UMAP/all | all |
| 是否标注样本名 | yes/no | no |
| 配色方案 | default/Set2/tab10 | default |

依赖: numpy, matplotlib, scikit-learn, umap-learn(可选)

MIT License