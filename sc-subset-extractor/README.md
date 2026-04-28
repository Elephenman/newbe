# sc-subset-extractor

按条件提取单细胞子集并保存为新Seurat对象

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| rds_file | Seurat对象RDS路径 | seurat_obj.rds |
| output_rds | 子集RDS输出路径 | subset.rds |
| subset_col | 筛选列名 | seurat_clusters |
| subset_val | 筛选值(逗号分隔) | 0,1,2 |

## 使用示例

```bash
Rscript sc-subset-extractor.R
```

## 依赖

```
Seurat
```
