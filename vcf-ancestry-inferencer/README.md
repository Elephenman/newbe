# vcf-ancestry-inferencer

> VCF样本祖源推断

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_vcf | VCF文件路径 | variants.vcf |
| reference_pca | 参考PCA坐标文件路径 | reference_pca.tsv |
| output_file | 祖源推断结果路径 | ancestry_results.tsv |
| n_pcs | 使用的主成分数 | 10 |


## 使用示例

```bash
cd vcf-ancestry-inferencer
python vcf-ancestry-inferencer.py
```

基于VCF变异信息推断样本的祖源构成

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
