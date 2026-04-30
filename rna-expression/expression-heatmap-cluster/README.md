# 📊 expression-heatmap-cluster

**表达矩阵→聚类热图**

## 使用方法

```bash
cd expression-heatmap-cluster
Rscript expression_heatmap_cluster.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `表达矩阵CSV路径(行=基因,列=样本)` | `expression.csv` |
| 2 | `是否log2转换(yes/no)` | `yes` |
| 3 | `聚类方法(hierarchical/kmeans)` | `hierarchical` |
| 4 | `取topN高变异基因` | `500` |
| 5 | `配色(Nature/Cell/BlueRed)` | `Nature` |

### 交互式输入示例

```
表达矩阵CSV路径(行=基因,列=样本) [默认: expression.csv]: 
是否log2转换(yes/no) [默认: yes]: 
聚类方法(hierarchical/kmeans) [默认: hierarchical]: 
取topN高变异基因 [默认: 500]: 
配色(Nature/Cell/BlueRed) [默认: Nature]: 
```

## 依赖

```r
install.packages('ggplot2')  # 或 BiocManager::install('ggplot2')
install.packages('pheatmap')  # 或 BiocManager::install('pheatmap')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT