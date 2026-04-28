# deg-direction-plotter

> DEG方向一致性箭头图

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_files | DEG结果文件(逗号分隔多个) | deg1.csv,deg2.csv |
| fc_col | log2FC列名 | log2FoldChange |
| gene_col | 基因名列名 | gene |
| output_file | 箭头图输出路径 | deg_direction.png |


## 使用示例

```bash
cd deg-direction-plotter
python deg-direction-plotter.py
```

绘制多个DEG结果间的方向一致性箭头图

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
