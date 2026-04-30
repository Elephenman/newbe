# rna-seq-power-calculator

> RNA-seq样本量/功效计算

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| effect_size | 预期效应量(log2FC) | 1 |
| n_samples | 每组样本数(0=计算所需) | 0 |
| alpha | 显著性水平 | 0.05 |
| power | 目标功效 | 0.8 |
| output_file | 结果输出路径 | power_analysis.tsv |


## 使用示例

```bash
cd rna-seq-power-calculator
Rscript rna-seq-power-calculator.R
```

计算RNA-seq实验所需的样本量或功效

## 依赖

参见 `requirements.txt`（R工具，依赖≤5个包）
