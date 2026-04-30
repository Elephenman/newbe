# bed-intersect-counter

> BED文件交集计数+重叠统计

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| bed_a | BED文件A路径 | file_a.bed |
| bed_b | BED文件B路径 | file_b.bed |
| min_overlap | 最小重叠比例 | 0.5 |
| output_file | 输出结果路径 | intersect_results.tsv |
| report_file | 统计报告路径 | intersect_report.txt |


## 使用示例

```bash
cd bed-intersect-counter
python bed-intersect-counter.py
```

计算两个BED文件的区间交集和重叠统计

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
