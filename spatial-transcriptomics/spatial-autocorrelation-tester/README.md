# spatial-autocorrelation-tester

> 空间自相关检验(Moran/Geary)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| rds_file | Seurat空间对象路径 | spatial_obj.rds |
| gene_list | 基因列表(逗号分隔) | CD68,CD3E,EGFR |
| method | 检验方法(Moran/Geary) | Moran |
| output_file | 结果输出路径 | autocorrelation_results.tsv |


## 使用示例

```bash
cd spatial-autocorrelation-tester
Rscript spatial-autocorrelation-tester.R
```

对空间转录组数据做Moran/Geary自相关检验

## 依赖

参见 `requirements.txt`（R工具，依赖≤5个包）
