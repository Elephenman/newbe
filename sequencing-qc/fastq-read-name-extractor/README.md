# fastq-read-name-extractor

> FASTQ read名称/ID提取与去重统计

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | FASTQ文件路径 | sample.fastq.gz |
| output_file | 输出文件路径 | read_names.txt |
| check_duplicates | 是否检查重复read名 | yes |
| report_stats | 是否输出统计摘要 | yes |


## 使用示例

```bash
cd fastq-read-name-extractor
python fastq-read-name-extractor.py
```

提取FASTQ中所有read名称，统计总数和重复率

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
