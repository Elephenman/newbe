# gsea-rank-file-generator

## 一句话说明
生成GSEA格式的.rnk排序文件用于基因集富集分析。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 表达矩阵文件 | expression.tsv | 用于排序的表达数据 |
| DEG结果文件 | deg_results.tsv | 可选的DEG结果 |
| 输出RANK文件 | gsea_ranks.rnk | GSEA输入文件 |

## 使用示例

```bash
python gsea_rank_file_generator.py
```
