# spatial-moran-plotter

计算空间基因表达的Moran's I自相关统计量

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| rds_file | Seurat空间对象RDS路径 | spatial.rds |
| genes | 目标基因(逗号分隔) |  |
| output_file | 输出CSV路径 | moran_results.csv |

## 使用示例

```bash
Rscript spatial-moran-plotter.R
```

## 依赖

```
Seurat
spdep
```
