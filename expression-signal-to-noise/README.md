# expression-signal-to-noise

> 表达信噪比计算+低质量基因过滤

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 表达矩阵文件路径 | expression_matrix.csv |
| snr_threshold | 信噪比阈值 | 2 |
| output_file | 过滤后矩阵路径 | snr_filtered_matrix.tsv |
| report_file | 统计报告路径 | snr_report.txt |


## 使用示例

```bash
cd expression-signal-to-noise
python expression-signal-to-noise.py
```

计算基因表达信噪比并过滤低质量基因

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
