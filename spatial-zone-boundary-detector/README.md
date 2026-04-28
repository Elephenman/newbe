# spatial-zone-boundary-detector

> 空间区域边界检测+分割

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| rds_file | 空间Seurat对象路径 | spatial_obj.rds |
| n_zones | 预期区域数 | 3 |
| method | 边界检测方法(kmeans/spatial) | kmeans |
| output_file | 边界结果路径 | zone_boundaries.tsv |


## 使用示例

```bash
cd spatial-zone-boundary-detector
Rscript spatial-zone-boundary-detector.R
```

检测空间转录组数据中的区域边界

## 依赖

参见 `requirements.txt`（R工具，依赖≤5个包）
