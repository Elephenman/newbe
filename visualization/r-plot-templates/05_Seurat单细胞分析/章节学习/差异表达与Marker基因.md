# 差异表达与Marker基因

## 📌 本模块目标
掌握使用 FindAllMarkers 和 FindMarkers 进行差异表达分析，理解各种统计检验方法的区别，学会筛选和可视化 Marker 基因。

## 🔧 核心函数
| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `FindAllMarkers()` | 所有cluster vs 其他cluster | `only.pos`, `min.pct`, `logfc.threshold` |
| `FindMarkers()` | 指定两组比较 | `ident.1`, `ident.2`, `test.use` |
| `FeaturePlot()` | UMAP上展示基因表达 | `features` |
| `VlnPlot()` | 小提琴图展示基因表达 | `features`, `group.by` |
| `DoHeatmap()` | Marker基因热图 | `features`, `group.by` |
| `DotPlot()` | 气泡图 | `features`, `group.by` |

## 📝 详细代码与注释

### 1. FindAllMarkers — 全局差异分析

```r
# ============================================
# FindAllMarkers：每个cluster vs 其余所有细胞
# ============================================
pbmc.markers <- FindAllMarkers(
  pbmc,
  only.pos = TRUE,           # 只保留上调基因（正表达差异）
  test.use = "wilcox",       # 统计检验方法（默认Wilcoxon秩和检验）
  min.pct = 0.25,            # 基因至少在25%的细胞中表达
  logfc.threshold = 0.25     # log2FC阈值
)

# 查看结果
head(pbmc.markers)
#         p_val avg_log2FC pct.1 pct.2     p_val_adj cluster gene
# LYZ   0.00000   1.182497 0.949 0.216     0.00000       0  LYZ
# S100A9 0.00000   1.069747 0.901 0.134     0.00000       0 S100A9

# ============================================
# 结果列解释
# ============================================
# p_val：原始p值
# avg_log2FC：平均log2倍数变化（正值=该cluster中表达更高）
# pct.1：该基因在目标cluster中的表达比例
# pct.2：该基因在其他cluster中的表达比例
# p_val_adj：校正后的p值（Bonferroni校正）
# cluster：cluster编号
# gene：基因名
```

### 2. 筛选显著 Marker 基因

```r
# ============================================
# 每个cluster取前10个Marker基因
# ============================================
top10_markers <- pbmc.markers %>%
  group_by(cluster) %>%
  dplyr::filter(avg_log2FC > 1) %>%    # log2FC > 1
  slice_head(n = 10) %>%
  ungroup()

# 查看每个cluster的top marker
top10_markers %>% group_by(cluster) %>% summarise(genes = paste(gene, collapse = ", "))
```

### 3. FindMarkers — 指定两组比较

```r
# ============================================
# 比较两个特定cluster
# ============================================
# Cluster 1 vs Cluster 5
markers_1_vs_5 <- FindMarkers(
  pbmc,
  ident.1 = 1,               # 第一组
  ident.2 = 5,               # 第二组
  only.pos = FALSE,           # 保留上调和下调基因
  min.pct = 0.1,              # 放宽阈值以获取更多基因
  logfc.threshold = 0.25
)

# 添加基因名列
markers_1_vs_5$gene <- rownames(markers_1_vs_5)
head(markers_1_vs_5)

# ============================================
# 比较特定细胞类型
# ============================================
# 需要先注释好细胞类型（见模块10）
markers <- FindMarkers(
  pbmc,
  ident.1 = "Memory CD4 T",    # 细胞类型1
  ident.2 = "CD8 T",           # 细胞类型2
  only.pos = FALSE,
  min.pct = 0.1,
  logfc.threshold = 0.25
)

# 筛选显著差异基因
significant_DEGs <- markers %>%
  filter(p_val_adj < 0.05 & abs(avg_log2FC) > 0.5)

cat("差异基因数量:", nrow(significant_DEGs), "\n")
```

### 4. 差异表达检验方法对比

```r
# ============================================
# Seurat 支持的检验方法
# ============================================
# | 方法           | test.use      | 特点                          |
# |----------------|---------------|-------------------------------|
# | Wilcoxon       | "wilcox"      | 默认，非参数，稳健            |
# | MAST           | "MAST"        | 考虑细胞检测率，推荐          |
# | DESeq2         | "DESeq2"      | 基于负二项分布，适合bulk比较  |
# | ROC            | "roc"         | 快速，适合初步筛选            |
# | Student's t    | "t"           | 参数检验，需要正态假设        |
# | LR             | "LR"          | 逻辑回归                      |
# | negbinom       | "negbinom"    | 负二项检验                    |
# | poisson        | "poisson"     | 泊松检验                      |

# ============================================
# 使用 MAST 检验（推荐用于正式分析）
# ============================================
# 需要安装 MAST 包
# install.packages("MAST")

pbmc.markers_mast <- FindAllMarkers(
  pbmc,
  test.use = "MAST",
  only.pos = TRUE,
  min.pct = 0.25,
  logfc.threshold = 0.25
)
```

### 5. Marker 基因可视化

```r
# ============================================
# 5.1 小提琴图 — 看单个基因在不同cluster的表达
# ============================================
VlnPlot(pbmc,
  features = c("CD3D", "MS4A1", "CD14", "GNLY"),
  ncol = 2
)

# ============================================
# 5.2 FeaturePlot — 在UMAP上看基因表达
# ============================================
FeaturePlot(pbmc,
  features = c("MS4A1", "GNLY", "CD3E", "CD14",
               "FCER1A", "FCGR3A", "LYZ", "PPBP", "CD8A"),
  ncol = 3
)

# ============================================
# 5.3 热图 — 多个cluster的top marker
# ============================================
top10 <- pbmc.markers %>%
  group_by(cluster) %>%
  dplyr::filter(avg_log2FC > 1) %>%
  slice_head(n = 10) %>%
  ungroup()

DoHeatmap(pbmc, features = top10$gene) + NoLegend()

# ============================================
# 5.4 气泡图 — 综合展示多个基因和cluster
# ============================================
markers_of_interest <- c(
  "CD3D", "CD3E", "CD8A",     # T细胞
  "MS4A1", "CD79A",            # B细胞
  "CD14", "LYZ",               # 单核细胞
  "GNLY", "NKG7",              # NK细胞
  "PPBP"                       # 血小板
)

DotPlot(pbmc, features = markers_of_interest) +
  RotatedAxis() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# 气泡大小 = 表达该基因的细胞比例
# 气泡颜色 = 平均表达水平
```

### 6. 绘制火山图

```r
# ============================================
# 火山图 — 差异基因全景
# ============================================
library(ggrepel)

# 获取两组比较结果
degs <- FindMarkers(pbmc, ident.1 = "Memory CD4 T", ident.2 = "CD8 T",
                    only.pos = FALSE, min.pct = 0.1)
degs$gene <- rownames(degs)

# 筛选显著差异基因
degs_sig <- degs %>%
  filter(p_val_adj < 0.05 & abs(avg_log2FC) > 0.5) %>%
  mutate(label = ifelse(abs(avg_log2FC) >= 1, gene, NA))

# 绘图
ggplot(degs_sig, aes(x = avg_log2FC, y = -log10(p_val_adj),
                     size = pct.1, color = avg_log2FC)) +
  geom_point() +
  geom_text_repel(aes(label = label), size = 3, color = "black") +
  ggtitle("Memory CD4 T vs CD8 T") +
  theme_bw() +
  scale_color_gradient2(low = "olivedrab", high = "salmon2",
                        mid = "grey", midpoint = 0) +
  scale_size(range = c(1, 3))
```

## ⚠️ 常见问题与注意事项

- **Wilcoxon vs MAST**：Wilcoxon 快且稳健，MAST 更准确但需要额外安装
- **min.pct 影响**：值越小找到的差异基因越多，但假阳性也可能增加
- **logfc.threshold**：设为0.25可以排除微小差异，减少计算量
- **p_val_adj**：务必使用校正后的p值（Bonferroni），原始p值太宽松
- **pct.1 和 pct.2**：如果一个基因 pct.1=0.9, pct.2=0.1，说明该基因高度特异性

## 🔗 相关模块
- [[08_细胞聚类/细胞聚类]]
- [[10_细胞类型注释/细胞类型注释]]
