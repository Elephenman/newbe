# deg-venn-plotter

对多组DEG结果绘制韦恩图，展示共有/特有基因

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| deg_files | DEG基因列表文件(逗号分隔) | deg1.txt,deg2.txt,deg3.txt |
| output_plot | 输出图片路径 | deg_venn.png |
| labels | 组标签(逗号分隔) | G1,G2,G3 |

## 使用示例

```bash
python deg-venn-plotter.py
```

## 依赖

```
matplotlib
matplotlib-venn
```
