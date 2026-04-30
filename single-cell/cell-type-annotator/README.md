# 🔬 cell-type-annotator

**单细胞自动注释辅助**

## 使用方法

```bash
cd cell-type-annotator
Rscript cell_type_annotator.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `Seurat对象路径(rds)` | `seurat.rds` |
| 2 | `标记基因文件(细胞类型→基因,CSV)` | `markers.csv` |
| 3 | `是否出UMAP标注图(yes/no)` | `yes` |

### 交互式输入示例

```
Seurat对象路径(rds) [默认: seurat.rds]: 
标记基因文件(细胞类型→基因,CSV) [默认: markers.csv]: 
是否出UMAP标注图(yes/no) [默认: yes]: 
```

## 依赖

```r
install.packages('Seurat')  # 或 BiocManager::install('Seurat')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT