# vcf-genotype-extractor

从VCF文件提取指定样本的基因型矩阵

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_vcf | 输入VCF文件路径 | input.vcf |
| output_file | 输出基因型矩阵路径 | genotypes.tsv |
| samples | 样本名(逗号分隔,留空=全部) |  |

## 使用示例

```bash
python vcf-genotype-extractor.py
```

## 依赖

```
无额外依赖
```
