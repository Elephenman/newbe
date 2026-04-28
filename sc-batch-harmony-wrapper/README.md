# sc-batch-harmony-wrapper

> Harmony批次校正包装

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| rds_file | Seurat对象路径 | seurat_obj.rds |
| batch_key | 批次变量列名 | batch |
| theta | Harmony theta参数 | 2 |
| output_file | 校正后对象路径 | harmony_corrected.rds |


## 使用示例

```bash
cd sc-batch-harmony-wrapper
Rscript sc-batch-harmony-wrapper.R
```

使用Harmony对Seurat对象进行批次校正

## 依赖

参见 `requirements.txt`（R工具，依赖≤5个包）
