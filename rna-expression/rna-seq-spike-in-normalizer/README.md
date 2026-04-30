# rna-seq-spike-in-normalizer

> RNA-seq ERCC spike-in标准化

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| count_file | count矩阵文件路径 | counts.csv |
| spike_file | ERCC spike-in信息文件路径 | ercc_mix.csv |
| output_file | 标准化结果路径 | spike_normalized.tsv |
| plot_output | 校准图路径 | spike_calibration.png |


## 使用示例

```bash
cd rna-seq-spike-in-normalizer
Rscript rna-seq-spike-in-normalizer.R
```

使用ERCC spike-in对RNA-seq数据进行标准化

## 依赖

参见 `requirements.txt`（R工具，依赖≤5个包）
