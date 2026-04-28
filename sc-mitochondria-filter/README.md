# sc-mitochondria-filter

根据线粒体基因比例过滤单细胞低质量细胞

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| rds_file | Seurat对象RDS路径 | seurat_obj.rds |
| output_rds | 过滤后RDS路径 | filtered.rds |
| mt_threshold | 线粒体百分比阈值 | 20 |
| min_features | 最低feature数 | 200 |
| max_features | 最高feature数 | 6000 |

## 使用示例

```bash
Rscript sc-mitochondria-filter.R
```

## 依赖

```
Seurat
```
