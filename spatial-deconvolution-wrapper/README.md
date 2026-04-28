# spatial-deconvolution-wrapper

空间转录组细胞类型反卷积(SPOTlight)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| spatial_rds | 空间Seurat对象RDS | spatial.rds |
| sc_rds | 单细胞参考Seurat对象RDS | reference.rds |
| output_rds | 反卷积结果RDS路径 | deconv.rds |

## 使用示例

```bash
Rscript spatial-deconvolution-wrapper.R
```

## 依赖

```
Seurat
SPOTlight
```
