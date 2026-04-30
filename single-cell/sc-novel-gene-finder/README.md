# sc-novel-gene-finder

> 单细胞新型基因发现(未注释表达特征)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 表达矩阵路径 | matrix.csv |
| annotation_file | 基因注释文件路径 | gene_annotations.tsv |
| min_expression | 最小表达阈值 | 1 |
| min_cells | 最少表达细胞数 | 10 |
| output_file | 新型基因列表路径 | novel_genes.tsv |


## 使用示例

```bash
cd sc-novel-gene-finder
python sc-novel-gene-finder.py
```

发现表达矩阵中未在注释文件中出现的基因

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
