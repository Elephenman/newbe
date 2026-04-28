# insulator-boundary-finder

> CTCF绝缘子边界识别

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| ctcf_peaks | CTCF peak BED文件路径 | ctcf_peaks.bed |
| hic_file | Hi-C接触矩阵路径(可选) | NA |
| min_boundary_score | 最小边界评分 | 0.5 |
| output_file | 绝缘子边界路径 | insulator_boundaries.tsv |


## 使用示例

```bash
cd insulator-boundary-finder
python insulator-boundary-finder.py
```

识别CTCF绝缘子/拓扑关联边界

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
