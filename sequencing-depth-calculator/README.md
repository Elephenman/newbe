# sequencing-depth-calculator

根据FASTQ和基因组大小计算测序深度

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 输入FASTQ文件路径 | input.fastq |
| genome_size | 基因组大小(bp) | 3000000000 |
| read_length | 平均read长度(bp) | 150 |

## 使用示例

```bash
python sequencing-depth-calculator.py
```

## 依赖

```
无额外依赖
```
