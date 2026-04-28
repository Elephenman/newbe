# deg-pathway-annotator

将DEG结果自动注释到KEGG/GO通路并生成富集报告

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| deg_file | DEG结果CSV路径(含gene/log2FC/padj) | deg_results.csv |
| organism | 物种(hsa/mmu) | hsa |
| pvalue_cutoff | P值阈值 | 0.05 |
| qvalue_cutoff | q值阈值 | 0.2 |
| output_dir | 输出目录 | pathway_results |

## 使用示例

```bash
Rscript deg-pathway-annotator.R
```

## 依赖

```
clusterProfiler
org.Hs.eg.db
```
