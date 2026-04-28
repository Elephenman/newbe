# replication-timing-plotter

复制时序(Repli-seq)数据可视化

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | Repli-seq信号文件(CSV: chr,start,end,early,late) | repliseq.csv |
| output_plot | 输出图片路径 | replication_timing.png |
| chrom | 指定染色体 | chr1 |

## 使用示例

```bash
python replication-timing-plotter.py
```

## 依赖

```
pandas
matplotlib
```
