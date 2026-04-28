# germline-variant-filter

胚系变异过滤与分类(Pathogenic/Likely Pathogenic/Benign等)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_vcf | 输入VCF文件路径 | germline.vcf |
| output_file | 过滤后VCF输出路径 | filtered_germline.vcf |
| min_qual | 最低QUAL值 | 30 |
| min_depth | 最低DP | 10 |
| af_threshold | 等位基因频率阈值(0=不过滤) | 0 |

## 使用示例

```bash
python germline-variant-filter.py
```

## 依赖

```
无额外依赖
```
