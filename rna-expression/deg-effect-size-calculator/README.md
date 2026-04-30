# deg-effect-size-calculator

> DEG效应量计算(log2FC置信区间+效应量)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | DEG结果文件路径(CSV/TSV) | deg_results.csv |
| fc_col | log2FC列名 | log2FoldChange |
| pval_col | p值列名 | pvalue |
| se_col | 标准误列名(可选) | lfcSE |
| output_file | 输出路径 | effect_size_results.tsv |


## 使用示例

```bash
cd deg-effect-size-calculator
python deg-effect-size-calculator.py
```

计算DEG效应量(log2FC置信区间、Cohen's d等)

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
