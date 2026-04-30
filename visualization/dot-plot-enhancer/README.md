# dot-plot-enhancer

> 点图增强版(大小+颜色双维度)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 数据文件路径(CSV) | dotplot_data.csv |
| x_col | X轴列名 | pathway |
| y_col | Y轴列名 | gene |
| size_col | 点大小映射列名 | gene_count |
| color_col | 点颜色映射列名 | pvalue |
| output_file | 输出图片路径 | enhanced_dotplot.png |


## 使用示例

```bash
cd dot-plot-enhancer
Rscript dot-plot-enhancer.R
```

生成双维度点图(大小=基因数，颜色=p值)

## 依赖

参见 `requirements.txt`（R工具，依赖≤5个包）
