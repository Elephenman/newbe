# volcano-label-editor

火山图标签编辑器(添加/修改/删除基因标签)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | DEG结果CSV(基因,log2FC,padj) | deg_results.csv |
| output_plot | 输出火山图路径 | volcano_labeled.png |
| label_genes | 标注基因(逗号分隔) | TP53,BRCA1,MYC |
| log2fc_threshold | log2FC阈值 | 1 |
| padj_threshold | padj阈值 | 0.05 |

## 使用示例

```bash
python volcano-label-editor.py
```

## 依赖

```
pandas
matplotlib
```
