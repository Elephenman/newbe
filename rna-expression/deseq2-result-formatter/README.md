# 📊 deseq2-result-formatter

**DESeq2结果→发表级表格+火山图**

## 使用方法

```bash
cd deseq2-result-formatter
Rscript deseq2_result_formatter.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `输入DESeq2结果CSV路径` | `deseq2_results.csv` |
| 2 | `padj阈值` | `0.05` |
| 3 | `log2FC阈值` | `1` |
| 4 | `基因名列名(如rowname/gene_id/symbol)` | `rowname` |
| 5 | `是否生成火山图(yes/no)` | `yes` |
| 6 | `火山图标注topN基因` | `10` |
| 7 | `图片格式(png/pdf/tiff)` | `png` |

### 交互式输入示例

```
输入DESeq2结果CSV路径 [默认: deseq2_results.csv]: 
padj阈值 [默认: 0.05]: 
log2FC阈值 [默认: 1]: 
基因名列名(如rowname/gene_id/symbol) [默认: rowname]: 
是否生成火山图(yes/no) [默认: yes]: 
火山图标注topN基因 [默认: 10]: 
图片格式(png/pdf/tiff) [默认: png]: 
```

## 依赖

```r
install.packages('dplyr')  # 或 BiocManager::install('dplyr')
install.packages('ggplot2')  # 或 BiocManager::install('ggplot2')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT