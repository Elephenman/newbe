# bed-coverage-interpolator

## 一句话说明
对BED指定区域的覆盖深度进行插值计算。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| BED文件路径 | regions.bed | 目标区域 |
| BAM文件路径 | sample.bam | 覆盖数据 |
| 输出文件 | interpolated.bed | 结果输出 |

## 使用示例

```bash
python bed_coverage_interpolator.py
```
