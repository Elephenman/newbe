# fastq-strand-detector

## 一句话说明
根据SAM/BAM比对结果推断FASTQreads的链特异性信息（RF/FR/RR/FF）。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| SAM/BAM文件路径 | aligned.sam | 比对结果文件 |
| 输出文件 | strand_info.txt | 链特异性结果 |

## 使用示例

```bash
python fastq_strand_detector.py
```
