# benchmark-result-comparator

基准测试结果比较与排名(多方法/多指标)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 基准结果CSV(方法,指标1,指标2,...) | benchmark.csv |
| output_file | 比较报告路径 | benchmark_report.txt |
| higher_is_better | 指标方向(逗号分隔,1=越高越好,0=越低越好) | 1,1,0 |

## 使用示例

```bash
python benchmark-result-comparator.py
```

## 依赖

```
pandas
```
