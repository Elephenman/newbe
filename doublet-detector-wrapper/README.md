# 🔬 doublet-detector-wrapper

**单细胞doublet检测+过滤**

## 使用方法

```bash
cd doublet-detector-wrapper
Rscript doublet_detector_wrapper.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `Seurat对象路径(rds)` | `seurat.rds` |
| 2 | `检测方法(DoubletFinder/scDblFinder)` | `scDblFinder` |
| 3 | `预期doublet率(%)` | `5` |
| 4 | `是否自动移除(yes/no)` | `yes` |

### 交互式输入示例

```
Seurat对象路径(rds) [默认: seurat.rds]: 
检测方法(DoubletFinder/scDblFinder) [默认: scDblFinder]: 
预期doublet率(%) [默认: 5]: 
是否自动移除(yes/no) [默认: yes]: 
```

## 依赖

```r
install.packages('DoubletFinder')  # 或 BiocManager::install('DoubletFinder')
install.packages('Seurat')  # 或 BiocManager::install('Seurat')
install.packages('scDblFinder')  # 或 BiocManager::install('scDblFinder')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT