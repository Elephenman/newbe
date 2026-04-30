# variant-clinical-annotator

> 变异临床注释(ClinVar/COSMIC信息整合)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_vcf | VCF文件路径 | variants.vcf |
| clinvar_file | ClinVar注释文件路径 | clinvar.tsv |
| output_file | 注释结果路径 | clinically_annotated.tsv |
| pathogenic_only | 仅保留致病性变异(yes/no) | no |


## 使用示例

```bash
cd variant-clinical-annotator
python variant-clinical-annotator.py
```

将ClinVar/COSMIC临床注释整合到VCF变异中

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
