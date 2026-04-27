# 📈 survival-expression-correlator
**基因表达与生存关联分析** — KM曲线+log-rank+coxPH

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 表达矩阵CSV | 行=基因,列=样本 | expression.csv |
| 临床数据CSV | 含OS时间+事件 | clinical.csv |
| 候选基因 | 逗号分隔 | BRCA1,BRCA2,TP53 |
| 分组方法 | median/quantile/optimal | median |
| 是否出KM曲线 | yes/no | yes |

依赖: survival, survminer, ggplot2

MIT License