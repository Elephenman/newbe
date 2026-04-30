# fastq-read-length-filter

> FASTQ按read长度范围精确过滤

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_fastq | 输入FASTQ路径 | sample.fastq.gz |
| min_length | 最小read长度 | 50 |
| max_length | 最大read长度 | 300 |
| output_fastq | 输出FASTQ路径 | filtered.fastq |
| stats_file | 统计文件路径 | length_filter_stats.txt |


## 使用示例

```bash
cd fastq-read-length-filter
python fastq-read-length-filter.py
```

按read长度范围过滤FASTQ文件

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
