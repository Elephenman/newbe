# expression-z-score-transformer

> 表达矩阵Z-score标准化+热图

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 表达矩阵文件路径 | expression_matrix.csv |
| gene_list | 目标基因列表文件(可选) | NA |
| center_method | 中心化方法(mean/median) | mean |
| output_matrix | 输出矩阵路径 | zscore_matrix.tsv |
| heatmap_output | 热图路径 | zscore_heatmap.png |


## 使用示例

```bash
cd expression-z-score-transformer
python expression-z-score-transformer.py
```

将表达矩阵Z-score标准化并绘制热图

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
