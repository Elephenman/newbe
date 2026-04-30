<div align="center">

# 🔬 单细胞分析

**Seurat质控/注释/聚类/整合/拟时序/CellChat/双重细胞等单细胞工具** (36个工具)

</div>

---

## 工具列表

| # | 工具 | 语言 | 说明 |
|---|------|:----:|------|
| 1 | [cell-contact-rank-calculator](./cell-contact-rank-calculator/) | Python | 计算单细狍/CellChat数据中细胞间接触强度排名。 |
| 2 | [cell-cycle-scorer](./cell-cycle-scorer/) | R | Single-cell cycle scoring + G1/S/G2M classification |
| 3 | [cell-proportion-analyzer](./cell-proportion-analyzer/) | R | Cell type proportion analysis + stacked bar chart |
| 4 | [cell-type-annotator](./cell-type-annotator/) | R | Single-cell auto-annotation (marker gene matching) |
| 5 | [cellchat-interaction-parser](./cellchat-interaction-parser/) | R | CellChat cell communication analysis wrapper |
| 6 | [deconvolution-estimator](./deconvolution-estimator/) | Python | 基于表达矩阵估算混合样本中各细胞类型的比例。 |
| 7 | [doublet-detector-wrapper](./doublet-detector-wrapper/) | R | Single-cell doublet detection + filtering |
| 8 | [neighborhood-enrichment-calculator](./neighborhood-enrichment-calculator/) | R | Neighborhood enrichment analysis (spatial proximity) |
| 9 | [pca-tsne-umap-plotter](./pca-tsne-umap-plotter/) | Python | PCA/t-SNE/UMAP dimensionality reduction trio |
| 10 | [pseudotime-setup](./pseudotime-setup/) | R | Pseudotime analysis launcher (Monocle3/Slingshot) |
| 11 | [sc-batch-harmony-wrapper](./sc-batch-harmony-wrapper/) | R | Harmony batch correction wrapper |
| 12 | [sc-ccs-regression-visualizer](./sc-ccs-regression-visualizer/) | Python | 可视化单细胞数据细胞周期(CC)回归前后的PC方差变化。 |
| 13 | [sc-cell-cycle-regressor](./sc-cell-cycle-regressor/) | R | Single-cell cell cycle effect regression removal |
| 14 | [sc-cluster-stability-checker](./sc-cluster-stability-checker/) | R | Clustering stability assessment + resolution optimization |
| 15 | [sc-clustering-resolution-optimizer](./sc-clustering-resolution-optimizer/) | R | Auto-optimize clustering resolution + stability |
| 16 | [sc-differential-abundance](./sc-differential-abundance/) | R | Differential abundance analysis for single-cell |
| 17 | [sc-dim-loadings-extractor](./sc-dim-loadings-extractor/) | Python | 从单细胞Seurat对象提取PCA等降维的基因载荷信息。 |
| 18 | [sc-doublet-visualizer](./sc-doublet-visualizer/) | R | Doublet detection results UMAP visualization |
| 19 | [sc-feature-plot-batcher](./sc-feature-plot-batcher/) | R | Batch FeaturePlot generation + PDF output |
| 20 | [sc-filtering-threshold-optimizer](./sc-filtering-threshold-optimizer/) | Python | 基于单细胞数据分布自动优化质控过滤阈值。 |
| 21 | [sc-gene-module-extractor](./sc-gene-module-extractor/) | R | Extract single-cell gene modules + activity scoring |
| 22 | [sc-gene-trend-plotter](./sc-gene-trend-plotter/) | R | Gene expression trend along pseudotime |
| 23 | [sc-jackstraw-wrapper](./sc-jackstraw-wrapper/) | Python | 运行JackStraw分析确定单细胞数据中显著的主成分数量。 |
| 24 | [sc-label-transfer-validator](./sc-label-transfer-validator/) | Python | 验证单细狍标签转移结果的准确性和一致性。 |
| 25 | [sc-marker-finder](./sc-marker-finder/) | R | Batch single-cell marker gene discovery |
| 26 | [sc-metadata-merger](./sc-metadata-merger/) | Python | Merge single-cell metadata with expression matrix |
| 27 | [sc-mitochondria-filter](./sc-mitochondria-filter/) | R | Filter low-quality cells by mitochondrial gene ratio |
| 28 | [sc-novel-gene-finder](./sc-novel-gene-finder/) | Python | Discover novel/unannotated genes in single-cell data |
| 29 | [sc-rna-velocity-runner](./sc-rna-velocity-runner/) | R | RNA velocity analysis workflow wrapper |
| 30 | [sc-subset-extractor](./sc-subset-extractor/) | R | Extract cell subsets by metadata conditions |
| 31 | [sc-trajectory-comparer](./sc-trajectory-comparer/) | R | Compare multiple pseudotime methods + consistency |
| 32 | [sc-variable-feature-selector](./sc-variable-feature-selector/) | Python | 选择单细狍表达矩阵中的高变特征基因用于下游分析。 |
| 33 | [sc-vega-pathway-plotter](./sc-vega-pathway-plotter/) | R | Single-cell pathway activity violin plot + statistics |
| 34 | [seurat-integration-helper](./seurat-integration-helper/) | R | Seurat multi-sample integration + batch correction evaluation |
| 35 | [seurat-qc-pipeline](./seurat-qc-pipeline/) | R | Seurat QC one-click pipeline |
| 36 | [umap-batch-plotter](./umap-batch-plotter/) | R | Batch UMAP coloring by multiple dimensions |

---

← [返回主目录](../)
