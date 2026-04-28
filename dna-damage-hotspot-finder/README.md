# dna-damage-hotspot-finder

DNA损伤修复热点区域识别(DDR相关)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | DNA损伤信号文件BED路径 | damage_peaks.bed |
| gene_file | 基因注释GTF路径 | genes.gtf |
| output_file | 输出热点区域路径 | damage_hotspots.tsv |
| merge_distance | 合并距离(bp) | 500 |

## 使用示例

```bash
python dna-damage-hotspot-finder.py
```

## 依赖

```
无额外依赖
```
