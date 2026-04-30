# 🧬 genome-fasta-slicer

**从参考基因组按坐标切片提取序列**

## 使用方法

```bash
cd genome-fasta-slicer
python genome_fasta_slicer.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `参考基因组FASTA路径` | `genome.fa` |
| 2 | `坐标文件路径(BED/TSV)` | `regions.bed` |
| 3 | `上下游flank长度(bp)` | `0` |
| 4 | `输出FASTA路径` | `genome_slices.fasta` |

### 交互式输入示例

```
参考基因组FASTA路径 [默认: genome.fa]: 
坐标文件路径(BED/TSV) [默认: regions.bed]: 
上下游flank长度(bp) [默认: 0]: 
输出FASTA路径 [默认: genome_slices.fasta]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT