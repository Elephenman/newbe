# 🔬 spatial-deconvolution-wrapper

**空间转录组细胞类型反卷积(SPOTlight)**

## 使用方法

```bash
cd spatial-deconvolution-wrapper
Rscript spatial-deconvolution-wrapper.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

## 依赖

```r
install.packages('SPOTlight')  # 或 BiocManager::install('SPOTlight')
install.packages('Seurat')  # 或 BiocManager::install('Seurat')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT