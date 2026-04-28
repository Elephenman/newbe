# mutational-signature-extractor

从VCF提取突变特征(SBS96谱)并可视化

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_vcf | 输入VCF文件路径 | somatic.vcf |
| output_plot | 输出SBS96谱图片路径 | sbs96.png |
| output_file | 输出SBS96计数CSV | sbs96_counts.csv |

## 使用示例

```bash
python mutational-signature-extractor.py
```

## 依赖

```
matplotlib
numpy
```
