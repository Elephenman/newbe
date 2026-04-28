# 🔬 spatial-neighbor-graph

**空间邻域图构建与可视化**

## 使用方法

```bash
cd spatial-neighbor-graph
Rscript spatial-neighbor-graph.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

## 依赖

```r
install.packages('Seurat')  # 或 BiocManager::install('Seurat')
install.packages('igraph')  # 或 BiocManager::install('igraph')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT