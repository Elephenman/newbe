# 🔍 batch-effect-inspector
**批次效应检测+可视化** — PCA/相关性矩阵

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 表达矩阵CSV | 行=基因,列=样本 | expression.csv |
| 批次信息文件 | 样本名+批次 | 留空=无 |
| 检测方法 | PCA/boxplot | PCA |

依赖: numpy, matplotlib, scikit-learn

MIT License