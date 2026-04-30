# 📊 enrichment-auto-pipeline

**GO/KEGG富集分析一键流水线**

## 使用方法

```bash
cd enrichment-auto-pipeline
Rscript enrichment_auto_pipeline.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `基因列表文件路径(每行一个基因)` | `genes.txt` |
| 2 | `物种(human/mouse/yeast/zebrafish)` | `human` |
| 3 | `富集类型(GO/KEGG/both)` | `both` |
| 4 | `padj阈值` | `0.05` |
| 5 | `图片类型(dot/bar)` | `dot` |

### 交互式输入示例

```
基因列表文件路径(每行一个基因) [默认: genes.txt]: 
物种(human/mouse/yeast/zebrafish) [默认: human]: 
富集类型(GO/KEGG/both) [默认: both]: 
padj阈值 [默认: 0.05]: 
图片类型(dot/bar) [默认: dot]: 
```

## 依赖

```r
install.packages('clusterProfiler')  # 或 BiocManager::install('clusterProfiler')
install.packages('enrichplot')  # 或 BiocManager::install('enrichplot')
install.packages('ggplot2')  # 或 BiocManager::install('ggplot2')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT