# bam-filter-by-flag

根据SAM flag过滤BAM文件中的reads

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_bam | 输入BAM文件路径 | input.bam |
| output_bam | 输出BAM文件路径 | filtered.bam |
| exclude_flags | 排除flag值(如1024=PCR重复) | 1024 |
| require_flags | 要求flag值 | 0 |
| min_mapq | 最低MAPQ | 0 |

## 使用示例

```bash
python bam-filter-by-flag.py
```

## 依赖

```
pysam
```
