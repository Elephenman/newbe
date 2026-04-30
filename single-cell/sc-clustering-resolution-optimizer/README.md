# sc-clustering-resolution-optimizer

> 聚类分辨率自动优化+稳定性评估

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| rds_file | Seurat对象路径 | seurat_obj.rds |
| min_res | 最小分辨率 | 0.1 |
| max_res | 最大分辨率 | 2.0 |
| step | 分辨率步长 | 0.1 |
| output_file | 优化结果路径 | resolution_optimization.tsv |


## 使用示例

```bash
cd sc-clustering-resolution-optimizer
Rscript sc-clustering-resolution-optimizer.R
```

自动搜索最优聚类分辨率并评估稳定性

## 依赖

参见 `requirements.txt`（R工具，依赖≤5个包）
