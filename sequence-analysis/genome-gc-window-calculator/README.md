# genome-gc-window-calculator

> 基因组GC含量滑动窗口计算

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_fasta | 基因组FASTA路径 | genome.fa |
| window_size | 滑动窗口大小(bp) | 1000 |
| step_size | 滑动步长(bp) | 500 |
| output_file | 输出文件路径 | gc_windows.tsv |
| plot_output | GC分布图路径 | gc_distribution.png |


## 使用示例

```bash
cd genome-gc-window-calculator
python genome-gc-window-calculator.py
```

沿基因组计算GC含量滑动窗口并可视化

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
