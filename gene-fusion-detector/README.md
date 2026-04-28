# gene-fusion-detector

从STAR-Fusion/Arriba输出中筛选基因融合事件

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 融合检测结果路径 | fusions.tsv |
| output_file | 筛选输出路径 | filtered_fusions.tsv |
| min_junction | 最低junction reads | 3 |
| tool | 工具格式(star_fusion/arriba) | star_fusion |

## 使用示例

```bash
python gene-fusion-detector.py
```

## 依赖

```
无额外依赖
```
