# deg-fdr-adjuster

> DEG多重检验校正对比(BH/BY/Q值)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | DEG结果文件路径 | deg_results.csv |
| pval_col | 原始p值列名 | pvalue |
| methods | 校正方法(逗号分隔: BH,BY,bonferroni,qvalue) | BH,BY,bonferroni |
| alpha | 显著性阈值 | 0.05 |
| output_file | 校正结果输出路径 | fdr_adjusted_results.tsv |


## 使用示例

```bash
cd deg-fdr-adjuster
python deg-fdr-adjuster.py
```

对比不同FDR校正方法对DEG结果的影响

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
