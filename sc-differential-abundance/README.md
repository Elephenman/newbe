# sc-differential-abundance

单细胞差异丰度分析(比较组间细胞比例变化)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| rds_file | Seurat对象RDS路径 | seurat_obj.rds |
| group_col | 分组列名 | condition |
| celltype_col | 细胞类型列名 | cell_type |
| output_file | 输出CSV路径 | diff_abundance.csv |

## 使用示例

```bash
Rscript sc-differential-abundance.R
```

## 依赖

```
Seurat
dplyr
```
