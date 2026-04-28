# spatial-co-expression-map

> 空间共表达基因地图

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| rds_file | 空间Seurat对象路径 | spatial_obj.rds |
| gene_a | 基因A | CD68 |
| gene_b | 基因B | CD3E |
| output_file | 共表达图路径 | coexpression_map.png |


## 使用示例

```bash
cd spatial-co-expression-map
Rscript spatial-co-expression-map.R
```

在空间转录组数据中绘制两个基因的共表达地图

## 依赖

参见 `requirements.txt`（R工具，依赖≤5个包）
