# sc-gene-trend-plotter

单细胞基因沿伪时间趋势图

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| rds_file | Seurat对象RDS路径(含伪时间) | seurat_obj.rds |
| genes | 目标基因(逗号分隔) |  |
| pseudotime_col | 伪时间列名 | pseudotime |
| output_plot | 输出图片路径 | gene_trend.png |

## 使用示例

```bash
Rscript sc-gene-trend-plotter.R
```

## 依赖

```
Seurat
ggplot2
```
