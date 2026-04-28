# 🔬 sc-rna-velocity-runner

**单细胞RNA velocity分析流程包装**

## 使用方法

```bash
cd sc-rna-velocity-runner
Rscript sc-rna-velocity-runner.R
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