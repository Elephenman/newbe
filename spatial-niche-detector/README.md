# spatial-niche-detector

空间转录组生态位(Niche)检测与可视化

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| rds_file | Seurat空间对象RDS路径 | spatial.rds |
| output_plot | 输出图片路径 | niche_plot.png |
| n_niches | Niche数量 | 4 |

## 使用示例

```bash
Rscript spatial-niche-detector.R
```

## 依赖

```
Seurat
```
