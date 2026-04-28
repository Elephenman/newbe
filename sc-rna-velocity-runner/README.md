# sc-rna-velocity-runner

单细胞RNA velocity分析流程包装

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| loom_file | Velocyto loom文件路径 | velocyto.loom |
| rds_file | Seurat对象RDS路径 | seurat_obj.rds |
| output_dir | 输出目录 | velocity_results |

## 使用示例

```bash
Rscript sc-rna-velocity-runner.R
```

## 依赖

```
Seurat
velocyto.R
```
