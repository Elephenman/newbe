# 📊 deg-pathway-annotator

**将DEG结果自动注释到KEGG/GO通路并生成富集报告**

## 使用方法

```bash
cd deg-pathway-annotator
Rscript deg-pathway-annotator.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

## 依赖

```r
install.packages('clusterProfiler')  # 或 BiocManager::install('clusterProfiler')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT