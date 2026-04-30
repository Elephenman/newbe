# 🔬 sc-subset-extractor

**按条件提取单细胞子集并保存为新Seurat对象**

## 使用方法

```bash
cd sc-subset-extractor
Rscript sc-subset-extractor.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

## 依赖

```r
install.packages('Seurat')  # 或 BiocManager::install('Seurat')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT