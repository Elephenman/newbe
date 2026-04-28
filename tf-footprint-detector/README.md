# tf-footprint-detector

## 一句话说明
基于ATAC-seq数据检测转录因子结合足迹。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| BAM文件路径 | atac.bam | ATAC-seq比对文件 |
| peak BED文件 | peaks.bed | peak区域 |
| 输出文件 | tf_footprints.bed | 足迹结果 |

## 使用示例

```bash
python tf_footprint_detector.py
```
