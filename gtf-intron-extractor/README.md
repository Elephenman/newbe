# gtf-intron-extractor

> 从GTF提取内含子坐标+长度统计

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_gtf | GTF文件路径 | annotation.gtf |
| output_file | 输出内含子列表路径 | introns.tsv |
| stats_file | 统计报告路径 | intron_stats.txt |
| plot_output | 长度分布图路径 | intron_length_dist.png |


## 使用示例

```bash
cd gtf-intron-extractor
python gtf-intron-extractor.py
```

从GTF注释文件中推断并提取所有内含子坐标

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
