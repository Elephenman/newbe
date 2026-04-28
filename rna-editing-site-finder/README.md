# rna-editing-site-finder

从RNA-seq VCF中筛选候选RNA编辑位点(A>I/G等)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_vcf | RNA-seq变异VCF路径 | rna_variants.vcf |
| output_file | 候选编辑位点输出 | rna_editing.tsv |
| min_alt_freq | 最低变异频率 | 0.1 |
| min_depth | 最低测序深度 | 10 |

## 使用示例

```bash
python rna-editing-site-finder.py
```

## 依赖

```
无额外依赖
```
