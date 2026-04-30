# 📊 gsea-runner

**GSEA分析一键运行**

## 使用方法

```bash
cd gsea-runner
Rscript gsea_runner.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `表达矩阵路径(行=基因,列=样本)` | `expression.csv` |
| 2 | `分组标签文件(样本名+分组,逗号分隔)` | `groups.txt` |
| 3 | `基因集(KEGG/Reactome/custom)` | `KEGG` |
| 4 | `pvalue阈值` | `0.05` |
| 5 | `物种(human/mouse)` | `human` |

### 交互式输入示例

```
表达矩阵路径(行=基因,列=样本) [默认: expression.csv]: 
分组标签文件(样本名+分组,逗号分隔) [默认: groups.txt]: 
基因集(KEGG/Reactome/custom) [默认: KEGG]: 
pvalue阈值 [默认: 0.05]: 
物种(human/mouse) [默认: human]: 
```

## 依赖

```r
install.packages('ReactomePA')  # 或 BiocManager::install('ReactomePA')
install.packages('clusterProfiler')  # 或 BiocManager::install('clusterProfiler')
install.packages('fgsea')  # 或 BiocManager::install('fgsea')
install.packages('ggplot2')  # 或 BiocManager::install('ggplot2')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT