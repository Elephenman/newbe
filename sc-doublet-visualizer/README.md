# sc-doublet-visualizer

可视化单细胞双细胞检测结果(UMAP标注+分布统计)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| rds_file | Seurat对象RDS路径 | seurat_obj.rds |
| output_plot | 输出图片路径 | doublet_viz.png |
| doublet_col | 双细胞注释列名 | doublet_score |

## 使用示例

```bash
Rscript sc-doublet-visualizer.R
```

## 依赖

```
Seurat
ggplot2
```
