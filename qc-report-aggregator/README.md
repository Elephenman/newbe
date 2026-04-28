# qc-report-aggregator

> 多QC报告汇总+综合评分

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| qc_dir | QC报告目录路径 | qc_reports |
| report_type | 报告类型(fastqc/multiqc/custom) | fastqc |
| output_file | 汇总报告路径 | qc_summary.tsv |
| score_threshold | 综合评分阈值(通过/失败) | 80 |


## 使用示例

```bash
cd qc-report-aggregator
python qc-report-aggregator.py
```

汇总多个QC报告并计算综合评分

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
