# expression-violin-plotter

绘制多基因/多样本表达量小提琴图

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| expression_file | 表达矩阵CSV | expression.csv |
| genes | 目标基因(逗号分隔) |  |
| output_plot | 输出图片路径 | violin_plot.png |
| group_file | 分组CSV(样本,组) |  |

## 使用示例

```bash
Rscript expression-violin-plotter.R
```

## 依赖

```
ggplot2
reshape2
```
