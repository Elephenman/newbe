# umi-deduplication-calculator

## 一句话说明
基于UMI标签计算reads去重率和唯一分子数统计。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| FASTQ文件路径 | sample.fastq.gz | 含UMI的序列文件 |
| 输出统计文件 | umi_stats.txt | 去重统计结果 |
| UMI长度(bp) | 8 | UMI序列长度 |

## 使用示例

```bash
python umi_deduplication_calculator.py
```
