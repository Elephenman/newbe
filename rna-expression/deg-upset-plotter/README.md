# deg-upset-plotter

## 一句话说明
绘制多组差异表达基因交集UpSet图，比Venn图更清晰展示复杂交集。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| DEG文件列表 | deg1.txt,deg2.txt,deg3.txt | 逗号分隔 |
| 输出图片 | upset_plot.png | 结果图 |
| 最小交集大小 | 1 | 过滤小交集 |

## 使用示例

```bash
python deg_upset_plotter.py
```
