# sc-filtering-threshold-optimizer

## 一句话说明
基于单细胞数据分布自动优化质控过滤阈值。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| Seurat对象RDS | seurat_object.rds | R中的Seurat对象 |
| 输出阈值文件 | optimal_thresholds.txt | 优化结果 |

## 使用示例

```bash
python sc_filtering_threshold_optimizer.py
```
