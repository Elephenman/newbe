# 🔧 sc-marker-finder

**单细胞marker基因批量查找**

## 使用方法

```bash
cd sc-marker-finder
Rscript sc_marker_finder.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `Seurat对象路径(rds)` | `seurat.rds` |
| 2 | `查找方法(FindAllMarkers/cosg)` | `FindAllMarkers` |
| 3 | `logFC阈值` | `0.25` |
| 4 | `min.pct` | `0.1` |
| 5 | `每cluster取topN` | `10` |
| 6 | `是否出热图(yes/no)` | `yes` |
| 7 | `是否出dot plot(yes/no)` | `yes` |

### 交互式输入示例

```
Seurat对象路径(rds) [默认: seurat.rds]: 
查找方法(FindAllMarkers/cosg) [默认: FindAllMarkers]: 
logFC阈值 [默认: 0.25]: 
min.pct [默认: 0.1]: 
每cluster取topN [默认: 10]: 
是否出热图(yes/no) [默认: yes]: 
是否出dot plot(yes/no) [默认: yes]: 
```

## 依赖

```r
install.packages('Seurat')  # 或 BiocManager::install('Seurat')
install.packages('cosg')  # 或 BiocManager::install('cosg')
install.packages('ggplot2')  # 或 BiocManager::install('ggplot2')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT