# wgcna-module-extractor

WGCNA共表达网络模块识别与可视化

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| expr_file | 表达矩阵CSV(行=基因,列=样本) | expression.csv |
| soft_power | 软阈值幂次(0=自动) | 0 |
| min_module_size | 最小模块大小 | 30 |
| output_dir | 输出目录 | wgcna_results |

## 使用示例

```bash
Rscript wgcna-module-extractor.R
```

## 依赖

```
WGCNA
dynamicTreeCut
```
