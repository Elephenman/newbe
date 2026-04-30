# vcf-allele-frequency-plotter

> VCF等位基因频率分布可视化

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_vcf | VCF文件路径 | variants.vcf |
| af_field | 等位基因频率字段名 | AF |
| min_af | 最小频率阈值 | 0 |
| max_af | 最大频率阈值 | 1 |
| plot_output | 输出图片路径 | af_distribution.png |


## 使用示例

```bash
cd vcf-allele-frequency-plotter
python vcf-allele-frequency-plotter.py
```

从VCF中提取等位基因频率并绘制分布图

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
