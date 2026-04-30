# genome-bin-stat-calculator

> 基因组窗口bin统计(GC/基因密度/SNP密度)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_fasta | 基因组FASTA路径 | genome.fa |
| input_gtf | GTF注释路径(可选) | NA |
| input_vcf | VCF变异文件路径(可选) | NA |
| bin_size | bin窗口大小(bp) | 100000 |
| output_file | 统计结果路径 | genome_bin_stats.tsv |


## 使用示例

```bash
cd genome-bin-stat-calculator
python genome-bin-stat-calculator.py
```

沿基因组计算各bin窗口的GC/基因密度/SNP密度

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
