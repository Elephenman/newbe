# isoform-expression-comparer

比较同一基因不同亚型的表达量差异并可视化

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| expression_file | 亚型表达矩阵CSV | isoform_exp.csv |
| gene_id | 目标基因ID | BRCA1 |
| output_plot | 输出图片路径 | isoform_compare.png |

## 使用示例

```bash
Rscript isoform-expression-comparer.R
```

## 依赖

```
ggplot2
reshape2
```
