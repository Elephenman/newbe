# 🔬 seurat-qc-pipeline

**Seurat质控一键流水线**

## 使用方法

```bash
cd seurat-qc-pipeline
Rscript seurat_qc_pipeline.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `数据路径(10X目录/h5/matrix.csv)` | `data/` |
| 2 | `物种(human/mouse)` | `human` |
| 3 | `nFeature最小值` | `200` |
| 4 | `nFeature最大值` | `5000` |
| 5 | `mito%上限` | `20` |
| 6 | `是否出QC图(yes/no)` | `yes` |

### 交互式输入示例

```
数据路径(10X目录/h5/matrix.csv) [默认: data/]: 
物种(human/mouse) [默认: human]: 
nFeature最小值 [默认: 200]: 
nFeature最大值 [默认: 5000]: 
mito%上限 [默认: 20]: 
是否出QC图(yes/no) [默认: yes]: 
```

## 依赖

```r
install.packages('Seurat')  # 或 BiocManager::install('Seurat')
install.packages('ggplot2')  # 或 BiocManager::install('ggplot2')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT