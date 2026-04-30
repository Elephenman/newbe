# paper-method-section-generator

> 论文方法部分模板生成

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| analysis_type | 分析类型(rna-seq/sc-rna-seq/chip-seq/variant) | rna-seq |
| species | 物种 | human |
| reference_genome | 参考基因组版本 | GRCh38 |
| output_file | 方法模板输出路径 | methods_section.md |


## 使用示例

```bash
cd paper-method-section-generator
python paper-method-section-generator.py
```

根据分析类型自动生成论文方法部分模板

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
