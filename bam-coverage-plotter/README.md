# bam-coverage-plotter

从BAM文件计算并绘制基因组覆盖度分布图

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_bam | 输入BAM文件路径 | input.bam |
| output_plot | 输出图片路径 | coverage.png |
| bin_size | 窗口大小(bp) | 1000 |
| chrom | 指定染色体(留空=全部) |  |

## 使用示例

```bash
python bam-coverage-plotter.py
```

## 依赖

```
pysam
matplotlib
numpy
```
