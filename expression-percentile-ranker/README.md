# expression-percentile-ranker

> 基因表达百分位排名+分箱

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 表达矩阵文件路径 | expression_matrix.csv |
| gene_list | 目标基因列表(可选) | NA |
| percentiles | 百分位阈值(逗号分隔) | 25,50,75,90 |
| output_file | 排名结果路径 | percentile_rank.tsv |


## 使用示例

```bash
cd expression-percentile-ranker
python expression-percentile-ranker.py
```

计算每个基因在各样本中的表达百分位排名

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
