# 🔬 spatial-moran-plotter

**计算空间基因表达的Moran's I自相关统计量**

## 使用方法

```bash
cd spatial-moran-plotter
Rscript spatial-moran-plotter.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

## 依赖

```r
install.packages('Seurat')  # 或 BiocManager::install('Seurat')
install.packages('spdep')  # 或 BiocManager::install('spdep')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT