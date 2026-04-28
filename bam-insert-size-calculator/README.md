# bam-insert-size-calculator

> BAM插入片段大小统计+分布图

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_bam | BAM文件路径 | sample.bam |
| min_isize | 最小插入片段大小 | 0 |
| max_isize | 最大插入片段大小 | 1000 |
| plot_output | 分布图输出路径 | insert_size_distribution.png |
| stats_output | 统计结果路径 | insert_size_stats.txt |


## 使用示例

```bash
cd bam-insert-size-calculator
python bam-insert-size-calculator.py
```

统计BAM中paired-end read的插入片段大小分布

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
