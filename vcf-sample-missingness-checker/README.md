# vcf-sample-missingness-checker

> VCF样本缺失率检查+过滤

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_vcf | VCF文件路径 | variants.vcf |
| max_missing_rate | 最大缺失率阈值 | 0.1 |
| output_file | 过滤结果路径 | filtered_variants.vcf |
| report_file | 缺失率报告路径 | missingness_report.txt |


## 使用示例

```bash
cd vcf-sample-missingness-checker
python vcf-sample-missingness-checker.py
```

检查VCF中每个样本的变异缺失率并过滤

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
