# spatial-spot-quality-filter

> 空间spot质量过滤+阈值推荐

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| rds_file | 空间Seurat对象路径 | spatial_obj.rds |
| min_nFeature | 最小nFeature_RNA | 200 |
| max_nFeature | 最大nFeature_RNA | 8000 |
| max_percent_mt | 最大线粒体比例 | 20 |
| output_file | 过滤后对象路径 | filtered_spatial.rds |


## 使用示例

```bash
cd spatial-spot-quality-filter
Rscript spatial-spot-quality-filter.R
```

对空间转录组数据做spot质量过滤，自动推荐阈值

## 依赖

参见 `requirements.txt`（R工具，依赖≤5个包）
