# spatial-neighbor-graph

空间邻域图构建与可视化

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| rds_file | Seurat空间对象RDS路径 | spatial.rds |
| output_plot | 输出图片路径 | neighbor_graph.png |
| k_neighbors | K近邻数 | 6 |

## 使用示例

```bash
Rscript spatial-neighbor-graph.R
```

## 依赖

```
Seurat
igraph
```
