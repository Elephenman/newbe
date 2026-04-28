# sc-variable-feature-selector

## 一句话说明
选择单细狍表达矩阵中的高变特征基因用于下游分析。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 表达矩阵文件 | expression.tsv | 原始表达矩阵 |
| 输出基因列表 | variable_genes.txt | 选中的基因 |
| 选择基因数 | 2000 | 高变基因数量 |

## 使用示例

```bash
python sc_variable_feature_selector.py
```
