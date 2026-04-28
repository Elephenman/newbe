# sc-cell-cycle-regressor

> 单细胞周期效应回归消除

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| rds_file | Seurat对象路径 | seurat_obj.rds |
| species | 物种(human/mouse) | human |
| regress_out | 是否回归消除周期效应 | yes |
| output_file | 处理后对象路径 | cycle_regressed.rds |


## 使用示例

```bash
cd sc-cell-cycle-regressor
Rscript sc-cell-cycle-regressor.R
```

对单细胞数据回归消除细胞周期效应

## 依赖

参见 `requirements.txt`（R工具，依赖≤5个包）
