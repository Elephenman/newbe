# vcf-info-field-parser

> VCF INFO字段批量解析到表格

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_vcf | VCF文件路径 | variants.vcf |
| fields | 要解析的INFO字段(逗号分隔) | AF,DP,AC |
| output_file | 输出表格路径 | vcf_info_table.tsv |
| filter_expression | 过滤条件(如DP>10) | none |


## 使用示例

```bash
cd vcf-info-field-parser
python vcf-info-field-parser.py
```

从VCF INFO字段提取指定信息到TSV表格

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
