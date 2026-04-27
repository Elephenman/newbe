# 🧬 seurat-qc-pipeline
**Seurat质控一键流水线** — 加载+过滤+QC图+保存对象

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 数据路径 | 10X目录/h5/matrix | data/ |
| 物种 | human/mouse | human |
| nFeature最小值 | 过滤阈值 | 200 |
| nFeature最大值 | 过滤阈值 | 5000 |
| mito%上限 | 过滤阈值 | 20 |
| 是否出QC图 | yes/no | yes |

依赖: Seurat

MIT License