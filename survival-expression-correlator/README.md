# 📊 survival-expression-correlator

**基因表达与生存关联分析**

## 使用方法

```bash
cd survival-expression-correlator
Rscript survival_expression_correlator.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `表达矩阵CSV路径(行=基因,列=样本)` | `expression.csv` |
| 2 | `临床数据CSV路径(含OS时间+事件)` | `clinical.csv` |
| 3 | `候选基因(逗号分隔)` | `BRCA1,BRCA2,TP53` |
| 4 | `分组方法(median/quantile/optimal)` | `median` |
| 5 | `是否出KM曲线(yes/no)` | `yes` |

### 交互式输入示例

```
表达矩阵CSV路径(行=基因,列=样本) [默认: expression.csv]: 
临床数据CSV路径(含OS时间+事件) [默认: clinical.csv]: 
候选基因(逗号分隔) [默认: BRCA1,BRCA2,TP53]: 
分组方法(median/quantile/optimal) [默认: median]: 
是否出KM曲线(yes/no) [默认: yes]: 
```

## 依赖

```r
install.packages('ggplot2')  # 或 BiocManager::install('ggplot2')
install.packages('survival')  # 或 BiocManager::install('survival')
install.packages('survminer')  # 或 BiocManager::install('survminer')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT