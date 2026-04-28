# ddr-pathway-mapper

> 🔥DNA损伤修复通路映射(NER/BER/HR/NHEJ/MMR等)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_genes | 输入基因列表文件路径 | gene_list.txt |
| output_file | 通路映射结果路径 | ddr_pathway_mapping.tsv |
| plot_output | 通路分布图路径 | ddr_pathway_distribution.png |
| detail_level | 详细程度(brief/full) | full |


## 使用示例

```bash
cd ddr-pathway-mapper
python ddr-pathway-mapper.py
```

🔥将基因映射到DNA损伤修复各通路(NER/BER/HR/NHEJ/MMR/DSB修复)

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
