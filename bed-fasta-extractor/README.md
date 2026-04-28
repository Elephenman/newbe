# bed-fasta-extractor

根据BED坐标从基因组FASTA中提取对应序列

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| bed_file | 输入BED文件路径 | regions.bed |
| fasta_file | 基因组FASTA路径 | genome.fa |
| output_file | 输出FASTA路径 | extracted.fa |
| flank | 两侧扩展碱基数 | 0 |

## 使用示例

```bash
python bed-fasta-extractor.py
```

## 依赖

```
无额外依赖
```
