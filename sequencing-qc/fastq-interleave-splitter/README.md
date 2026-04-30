# fastq-interleave-splitter

## 一句话说明
将两个配对FASTQ文件交叉合并为单个交错文件。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| Read1 FASTQ | sample_R1.fastq.gz | 配对端1 |
| Read2 FASTQ | sample_R2.fastq.gz | 配对端2 |
| 输出交叉文件 | interleaved.fastq | 交叉合并结果 |

## 使用示例

```bash
python fastq_interleave_splitter.py
```
