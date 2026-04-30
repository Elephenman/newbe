# sc-metadata-merger

> 单细胞metadata与表达矩阵合并

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| matrix_file | 表达矩阵路径 | matrix.csv |
| metadata_file | metadata文件路径 | metadata.csv |
| merge_key | 合并键列名 | cell_id |
| output_file | 合并结果路径 | merged_data.tsv |


## 使用示例

```bash
cd sc-metadata-merger
python sc-metadata-merger.py
```

将单细胞表达矩阵与metadata合并

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
