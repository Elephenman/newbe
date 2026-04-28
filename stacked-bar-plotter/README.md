# stacked-bar-plotter

> 堆叠条形图(细胞比例/通路占比)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 数据文件路径(CSV) | proportion_data.csv |
| group_col | 分组列名 | sample |
| category_col | 类别列名 | cell_type |
| value_col | 数值列名(比例) | percentage |
| output_file | 输出图片路径 | stacked_barplot.png |


## 使用示例

```bash
cd stacked-bar-plotter
Rscript stacked-bar-plotter.R
```

绘制堆叠条形图展示细胞比例或通路占比

## 依赖

参见 `requirements.txt`（R工具，依赖≤5个包）
