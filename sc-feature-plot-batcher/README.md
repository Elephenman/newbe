# sc-feature-plot-batcher

> FeaturePlot批量生成+PDF输出

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| rds_file | Seurat对象路径 | seurat_obj.rds |
| gene_list | 基因列表文件路径 | genes.txt |
| reduction | 降维方法(umap/tsne) | umap |
| output_dir | 输出目录 | feature_plots |


## 使用示例

```bash
cd sc-feature-plot-batcher
Rscript sc-feature-plot-batcher.R
```

批量生成Seurat FeaturePlot并输出为PDF

## 依赖

参见 `requirements.txt`（R工具，依赖≤5个包）
