# 🔬 spatial-spot-annotator

**空间转录组spot自动注释**

## 使用方法

```bash
cd spatial-spot-annotator
Rscript spatial_spot_annotator.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `空间Seurat对象路径(rds)` | `spatial.rds` |
| 2 | `参考Seurat对象路径(含注释)` | `annotated.rds` |
| 3 | `注释方法(transfer/marker)` | `transfer` |
| 4 | `是否出空间图(yes/no)` | `yes` |
| 5 | `marker基因文件路径` | `markers.csv` |

### 交互式输入示例

```
空间Seurat对象路径(rds) [默认: spatial.rds]: 
参考Seurat对象路径(含注释) [默认: annotated.rds]: 
注释方法(transfer/marker) [默认: transfer]: 
是否出空间图(yes/no) [默认: yes]: 
marker基因文件路径 [默认: markers.csv]: 
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