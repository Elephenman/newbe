# PBMC3k完整流程

## 📌 本模块目标
用一个完整的 PBMC 3k 数据集实战演练，将前面所有模块的知识串联起来，形成可一键运行的分析流程。

## 📝 完整代码

### 第一部分：环境准备

```r
# ============================================
# 🧬 PBMC 3k 单细胞RNA-seq完整分析流程
# 基于 Seurat v5 官方教程
# 数据来源：10x Genomics PBMC 3k
# ============================================

# 清空环境
rm(list = ls())

# 加载包
library(Seurat)
library(dplyr)
library(patchwork)
library(ggplot2)

# Windows内存优化
memory.limit(size = 9999999999999)

# 检查版本
cat("Seurat版本:", as.character(packageVersion("Seurat")), "\n")
# 期望: 5.x.x
```

### 第二部分：数据导入

```r
# ============================================
# 1. 下载数据（使用SeuratData）
# ============================================
library(SeuratData)
InstallData("pbmc3k")

# 加载数据（已经是一个Seurat对象）
data("pbmc3k")
pbmc <- pbmc3k

# ============================================
# 或者手动读取10x数据
# ============================================
# pbmc.data <- Read10X(data.dir = "./filtered_gene_bc_matrices/hg19/")
# pbmc <- CreateSeuratObject(
#   counts = pbmc.data,
#   project = "pbmc3k",
#   min.cells = 3,
#   min.features = 200
# )

# 查看基本信息
print(pbmc)
# 13714 features across 2700 samples
dim(pbmc)
# [1] 13714  2700

head(pbmc@meta.data)
```

### 第三部分：质量控制

```r
# ============================================
# 2. 计算QC指标
# ============================================
# 线粒体基因百分比
pbmc[["percent.mt"]] <- PercentageFeatureSet(pbmc, pattern = "^MT-")

# 查看QC统计
summary(pbmc$nCount_RNA)
summary(pbmc$nFeature_RNA)
summary(pbmc$percent.mt)

# ============================================
# 3. QC可视化
# ============================================
# 小提琴图
VlnPlot(pbmc,
  features = c("nFeature_RNA", "nCount_RNA", "percent.mt"),
  ncol = 3, pt.size = 0.01
)

# 散点图
p1 <- FeatureScatter(pbmc, feature1 = "nCount_RNA", feature2 = "nFeature_RNA")
p2 <- FeatureScatter(pbmc, feature1 = "nCount_RNA", feature2 = "percent.mt")
p1 + p2

# ============================================
# 4. 过滤低质量细胞
# ============================================
pbmc <- subset(pbmc,
  subset = nFeature_RNA > 200 &
           nFeature_RNA < 2500 &
           percent.mt < 5
)

dim(pbmc)
# 过滤后约 2638 个细胞
```

### 第四部分：归一化与特征选择

```r
# ============================================
# 5. 归一化
# ============================================
pbmc <- NormalizeData(pbmc,
  normalization.method = "LogNormalize",
  scale.factor = 10000
)

# ============================================
# 6. 选择高变基因
# ============================================
pbmc <- FindVariableFeatures(pbmc,
  selection.method = "vst",
  nfeatures = 2000
)

# 前10个高变基因
top10 <- head(VariableFeatures(pbmc), 10)
cat("Top 10 HVGs:", paste(top10, collapse = ", "), "\n")

# 可视化
plot1 <- VariableFeaturePlot(pbmc)
plot2 <- LabelPoints(plot = plot1, points = top10, repel = TRUE)
plot2
```

### 第五部分：缩放与降维

```r
# ============================================
# 7. 数据缩放
# ============================================
all.genes <- rownames(pbmc)
pbmc <- ScaleData(pbmc, features = all.genes)

# ============================================
# 8. PCA 降维
# ============================================
pbmc <- RunPCA(pbmc, features = VariableFeatures(object = pbmc))

# 查看PC载荷
print(pbmc[["pca"]], dims = 1:5, nfeatures = 5)

# 可视化
VizDimLoadings(pbmc, dims = 1:2, reduction = "pca")
DimPlot(pbmc, reduction = "pca") + NoLegend()
DimHeatmap(pbmc, dims = 1:15, cells = 500, balanced = TRUE)

# ============================================
# 9. 确定PC数量
# ============================================
ElbowPlot(pbmc)
# 根据肘部图，选择前10个PC
```

### 第六部分：聚类与可视化

```r
# ============================================
# 10. 细胞聚类
# ============================================
pbmc <- FindNeighbors(pbmc, dims = 1:10)
pbmc <- FindClusters(pbmc, resolution = 0.5)

# 查看聚类结果
table(Idents(pbmc))
head(Idents(pbmc), 5)

# ============================================
# 11. UMAP 降维
# ============================================
pbmc <- RunUMAP(pbmc, dims = 1:10)

# 可视化聚类
DimPlot(pbmc, reduction = "umap", label = TRUE, pt.size = 0.5) + NoLegend()
```

### 第七部分：差异表达与注释

```r
# ============================================
# 12. 寻找Marker基因
# ============================================
# 所有cluster的marker
pbmc.markers <- FindAllMarkers(pbmc,
  only.pos = TRUE,
  test.use = "wilcox",
  min.pct = 0.25,
  logfc.threshold = 0.25
)

# 每个cluster的top10
top10 <- pbmc.markers %>%
  group_by(cluster) %>%
  dplyr::filter(avg_log2FC > 1) %>%
  slice_head(n = 10) %>%
  ungroup()

# ============================================
# 13. 查看特定基因的表达
# ============================================
FeaturePlot(pbmc,
  features = c("MS4A1", "GNLY", "CD3E", "CD14",
               "FCER1A", "FCGR3A", "LYZ", "PPBP", "CD8A"),
  ncol = 3
)

# 热图
DoHeatmap(pbmc, features = top10$gene) + NoLegend()

# ============================================
# 14. 细胞类型注释
# ============================================
new.cluster.ids <- c(
  "Naive CD4 T",      # 0: IL7R, CCR7
  "CD14+ Mono",       # 1: CD14, LYZ
  "Memory CD4 T",     # 2: IL7R, S100A4
  "B",                # 3: MS4A1, CD79A
  "CD8 T",            # 4: CD8A
  "FCGR3A+ Mono",     # 5: FCGR3A, MS4A7
  "NK",               # 6: GNLY, NKG7
  "DC",               # 7: FCER1A
  "Platelet"          # 8: PPBP
)

names(new.cluster.ids) <- levels(pbmc)
pbmc <- RenameIdents(pbmc, new.cluster.ids)

# 保存注释到meta.data
pbmc$celltype <- Idents(pbmc)

# ============================================
# 15. 注释后的UMAP
# ============================================
plot <- DimPlot(pbmc, reduction = "umap",
                label = TRUE, label.size = 4.5, pt.size = 0.5) +
  xlab("UMAP 1") + ylab("UMAP 2") +
  theme(axis.title = element_text(size = 18),
        legend.text = element_text(size = 18)) +
  guides(colour = guide_legend(override.aes = list(size = 10)))

plot
ggsave("pbmc3k_annotated_umap.png", plot, width = 12, height = 7, dpi = 300)
```

### 第八部分：差异分析

```r
# ============================================
# 16. 两组比较差异分析
# ============================================
T_cell_DEGs <- FindMarkers(
  pbmc,
  ident.1 = "Memory CD4 T",
  ident.2 = "CD8 T",
  only.pos = FALSE,
  min.pct = 0.1,
  logfc.threshold = 0.25
)
T_cell_DEGs$gene <- rownames(T_cell_DEGs)

# 筛选显著差异基因
T_cell_DEGs_filtered <- T_cell_DEGs %>%
  filter(p_val_adj < 0.05 & abs(avg_log2FC) > 0.5)

cat("显著差异基因数:", nrow(T_cell_DEGs_filtered), "\n")

# ============================================
# 17. 火山图
# ============================================
library(ggrepel)

plotdf <- T_cell_DEGs_filtered %>%
  mutate(label = ifelse(abs(avg_log2FC) >= 1, gene, NA))

ggplot(plotdf, aes(x = avg_log2FC, y = -log10(p_val_adj),
                   size = pct.1, color = avg_log2FC)) +
  geom_point() +
  ggtitle("Memory CD4 T vs CD8 T") +
  geom_text_repel(aes(label = label), size = 3, color = "black") +
  theme_bw() +
  scale_color_gradient2(low = "olivedrab", high = "salmon2",
                        mid = "grey", midpoint = 0) +
  scale_size(range = c(1, 3))

ggsave("volcano_plot.png", width = 8, height = 6, dpi = 300)
```

### 第九部分：功能富集

```r
# ============================================
# 18. GO/KEGG 富集分析
# ============================================
BiocManager::install(c("clusterProfiler", "org.Hs.eg.db", "enrichplot"))
library(clusterProfiler)
library(enrichplot)
library(org.Hs.eg.db)

# 基因ID转换
ids <- bitr(T_cell_DEGs_filtered$gene, "SYMBOL", "ENTREZID", "org.Hs.eg.db")
T_cell_DEGs_filtered <- merge(T_cell_DEGs_filtered, ids, by.x = "gene", by.y = "SYMBOL")

# 按logFC排序
T_cell_DEGs_filtered <- T_cell_DEGs_filtered[order(T_cell_DEGs_filtered$avg_log2FC, decreasing = TRUE), ]

# GO富集
cluster_gene <- T_cell_DEGs_filtered$ENTREZID[abs(T_cell_DEGs_filtered$avg_log2FC) > 1]
cluster_GO <- enrichGO(cluster_gene, OrgDb = "org.Hs.eg.db", ont = "BP", readable = TRUE)
dotplot(cluster_GO, showCategory = 10, title = "GO Enrichment")

# KEGG富集
cluster_kegg <- enrichKEGG(gene = cluster_gene, organism = "hsa", pvalueCutoff = 0.05)
dotplot(cluster_kegg, showCategory = 10, title = "KEGG Enrichment")
```

### 第十部分：保存结果

```r
# ============================================
# 19. 保存最终对象
# ============================================
# 保存完整Seurat对象
saveRDS(pbmc, file = "./pbmc3k_final.rds")

# 保存元数据
write.csv(pbmc@meta.data, "pbmc3k_metadata.csv")

# 保存Marker基因
write.csv(pbmc.markers, "pbmc3k_all_markers.csv")

# 保存差异基因
write.csv(T_cell_DEGs_filtered, "T_cell_DEGs.csv")

cat("\n✅ 分析完成！所有结果已保存。\n")
cat("  - Seurat对象: pbmc3k_final.rds\n")
cat("  - 元数据: pbmc3k_metadata.csv\n")
cat("  - Marker基因: pbmc3k_all_markers.csv\n")
cat("  - 差异基因: T_cell_DEGs.csv\n")
```

## ⚠️ 运行注意事项

- **数据下载**：首次运行 `InstallData("pbmc3k")` 需要网络连接
- **内存需求**：至少 8GB 内存（PBMC3k 是小数据集）
- **运行时间**：整个流程约 5-10 分钟
- **阈值调整**：QC 阈值和 resolution 需要根据你的数据调整
- **更多数据**：大数据集建议用 SCTransform 替代 LogNormalize

## 🔗 相关模块
- [[01_安装与环境配置/安装与环境配置]] → [[02_数据导入与Seurat对象/数据导入与Seurat对象]]
- [[03_质量控制QC/质量控制QC]] → [[04_数据归一化/数据归一化]]
- [[05_特征选择/特征选择]] → [[06_数据缩放与线性降维PCA/数据缩放与线性降维PCA]]
- [[07_非线性降维UMAP_tSNE/非线性降维UMAP_tSNE]] → [[08_细胞聚类/细胞聚类]]
- [[09_差异表达与Marker基因/差异表达与Marker基因]] → [[10_细胞类型注释/细胞类型注释]]
- [[15_命令速查表/命令速查表]]
