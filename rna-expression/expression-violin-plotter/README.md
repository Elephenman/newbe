# 📊 expression-violin-plotter

**绘制多基因/多样本表达量小提琴图**

## 使用方法

```bash
cd expression-violin-plotter
Rscript expression-violin-plotter.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

## 依赖

```r
install.packages('ggplot2')  # 或 BiocManager::install('ggplot2')
install.packages('reshape2')  # 或 BiocManager::install('reshape2')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT