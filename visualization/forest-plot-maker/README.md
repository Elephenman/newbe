# forest-plot-maker

> Forest图(效应量+置信区间)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 数据文件路径(CSV) | forest_data.csv |
| label_col | 标签列名 | feature |
| effect_col | 效应量列名 | odds_ratio |
| ci_low_col | CI下限列名 | ci_low |
| ci_high_col | CI上限列名 | ci_high |
| output_file | 输出图片路径 | forest_plot.png |


## 使用示例

```bash
cd forest-plot-maker
Rscript forest-plot-maker.R
```

绘制Forest图展示效应量和置信区间

## 依赖

参见 `requirements.txt`（R工具，依赖≤5个包）
