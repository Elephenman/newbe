# gene-set-enrichment-visualizer

> 富集结果多维度可视化（气泡/条形/网络）

## 一句话说明

富集结果多维度可视化（气泡/条形/网络） — 针对浙大生信研究生+陆慧智课题组（DNA损伤修复）方向优化。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 输入文件路径 | input.txt |
| output_file | 输出文件路径 | output_gene_set_enrichment_visualizer.txt |
| param1 | 主参数（阈值/数值） | 0.05 |
| param2 | 辅参数（模式/格式） | default |

## 使用示例

```bash
# Python工具
cd gene-set-enrichment-visualizer
python gene_set_enrichment_visualizer.R

# R工具
cd gene-set-enrichment-visualizer
Rscript gene_set_enrichment_visualizer.R
```

所有参数通过交互式 `input()` 输入，带默认值可直接回车跳过。

## 输出格式

- TSV表格文件，带注释行
- 包含处理统计摘要

## 依赖

见 [requirements.txt](./requirements.txt)

## 许可

MIT License — [Newbe](https://github.com/Elephenman/newbe)
