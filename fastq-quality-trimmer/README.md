# fastq-quality-trimmer

根据质量值对FASTQ reads进行3'/5'端截尾修剪

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 输入FASTQ文件路径 | input.fastq |
| output_file | 输出FASTQ文件路径 | trimmed.fastq |
| min_quality | 最低质量阈值(Phred33) | 20 |
| min_length | 修剪后最短read长度 | 30 |
| trim_end | 修剪方向(3prime/5prime/both) | 3prime |

## 使用示例

```bash
python fastq-quality-trimmer.py
```

## 依赖

```
biopython
```
