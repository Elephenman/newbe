# 🔬 fastq-filter
**FASTQ按质量/长度/GC含量过滤** — 逐read判断，统计丢弃原因

| 参数 | 说明 | 默认值 |
|------|------|--------|
| FASTQ文件路径 | 输入文件 | sample.fastq |
| 最小平均质量阈值 | 丢弃低质量read | 20 |
| 最小序列长度(bp) | 丢弃过短read | 50 |
| GC含量范围 | 如0.3-0.7 | 0.3-0.7 |
| 输出文件路径 | 留空自动命名 | 自动 |

```bash
python fastq_filter.py
```

MIT License