# gene-desert-analyzer

> 基因荒漠区分析与注释

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_gtf | GTF注释路径 | annotation.gtf |
| input_fasta | 基因组FASTA路径 | genome.fa |
| min_desert_size | 最小荒漠区大小(bp) | 500000 |
| output_file | 荒漠区列表路径 | gene_deserts.tsv |


## 使用示例

```bash
cd gene-desert-analyzer
python gene-desert-analyzer.py
```

识别并分析基因组中的基因荒漠区

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
