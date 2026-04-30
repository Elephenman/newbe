# 非线性降维UMAP/tSNE

## 📌 本模块目标
掌握 UMAP 和 t-SNE 两种非线性降维方法的原理和使用，学会选择合适的降维方法，理解两种方法的区别。

## 🔧 核心函数
| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `RunUMAP()` | 运行UMAP降维 | `dims`, `reduction`, `n.neighbors` |
| `RunTSNE()` | 运行t-SNE降维 | `dims`, `reduction`, `perplexity` |
| `DimPlot()` | 可视化降维结果 | `reduction`, `group.by`, `label` |

## 📝 详细代码与注释

### 1. 为什么要非线性降维

```r
# ============================================
# PCA 是线性降维，只能捕捉线性关系
# UMAP / t-SNE 是非线性降维，能更好地展示细胞的局部和全局结构
# 
# 注意：UMAP/t-SNE 只用于可视化，不用于后续计算！
# 聚类和差异表达仍然基于 PCA 空间
# ============================================
```

### 2. 运行 UMAP（推荐）

```r
# ============================================
# UMAP：统一流形逼近与投影
# ============================================
# dims = 1:10 表示使用前10个PC作为输入
# ⚠️ 这里的 dims 数量取决于上一步 ElbowPlot 的结果！

pbmc <- RunUMAP(
  pbmc,
  dims = 1:10,              # 使用前10个PC
  reduction = "pca"         # 基于PCA结果（默认）
)

# ⭐ 简写形式
pbmc <- RunUMAP(pbmc, dims = 1:10)

# ============================================
# 调整 UMAP 参数
# ============================================
pbmc <- RunUMAP(
  pbmc,
  dims = 1:10,
  n.neighbors = 30,         # 近邻数（默认30，越大全局结构越明显）
  min.dist = 0.3,           # 最小距离（默认0.3，越小簇越紧密）
  spread = 1.0,             # 嵌入的展布度（默认1.0）
  metric = "cosine"         # 距离度量（默认cosine）
)

# ============================================
# 可视化 UMAP
# ============================================
# 基础版
DimPlot(pbmc, reduction = "umap")

# 添加聚类标签
DimPlot(pbmc, reduction = "umap", label = TRUE)

# 添加标签 + 去掉图例
DimPlot(pbmc, reduction = "umap", label = TRUE, pt.size = 0.5) + NoLegend()

# 自定义颜色和主题
library(ggplot2)
DimPlot(pbmc, reduction = "umap", label = TRUE, label.size = 4.5) +
  xlab("UMAP 1") + ylab("UMAP 2") +
  theme(axis.title = element_text(size = 18),
        legend.text = element_text(size = 18))
```

### 3. 运行 t-SNE

```r
# ============================================
# t-SNE：t-分布随机邻域嵌入
# ============================================
pbmc <- RunTSNE(
  pbmc,
  dims = 1:10,              # 使用前10个PC
  reduction = "pca",        # 基于PCA
  perplexity = 30           # 困惑度（默认30，影响局部/全局结构平衡）
)

# ⭐ 简写形式
pbmc <- RunTSNE(pbmc, dims = 1:10)

# ============================================
# 可视化 t-SNE
# ============================================
DimPlot(pbmc, reduction = "tsne", label = TRUE)
```

### 4. UMAP vs t-SNE 对比

```r
# ============================================
# 同时展示两种降维结果
# ============================================
p1 <- DimPlot(pbmc, reduction = "umap", label = TRUE) + ggtitle("UMAP")
p2 <- DimPlot(pbmc, reduction = "tsne", label = TRUE) + ggtitle("t-SNE")
p1 + p2

# ============================================
# UMAP vs t-SNE 关键区别
# ============================================
# | 特性          | UMAP                         | t-SNE                     |
# |---------------|------------------------------|---------------------------|
# | 速度          | 更快                         | 较慢                      |
# | 全局结构      | 保留更好                     | 保留较差                  |
# | 局部结构      | 保留好                       | 保留好                    |
# | 确定性        | 每次运行结果大致相同         | 每次运行可能不同          |
# | 推荐用途      | 日常可视化首选               | 需要强调局部结构时        |
# | 参数敏感度    | 较低                         | perplexity影响大          |
#
# 🎯 建议：优先使用 UMAP
```

### 5. 在 UMAP 上标注基因表达

```r
# ============================================
# FeaturePlot：在 UMAP 上展示基因表达
# ============================================
# 同时查看多个 marker 基因
FeaturePlot(pbmc,
  features = c("MS4A1", "GNLY", "CD3E", "CD14",
               "FCER1A", "FCGR3A", "LYZ", "PPBP", "CD8A"),
  ncol = 3
)

# MS4A1 → B细胞
# GNLY  → NK细胞
# CD3E  → T细胞
# CD14  → 单核细胞
# FCGR3A → FCGR3A+单核细胞
# PPBP  → 血小板

# ============================================
# 单个基因高分辨率展示
# ============================================
FeaturePlot(pbmc,
  features = "CD3E",
  reduction = "umap",
  order = TRUE,             # 高表达点画在上面
  min.cutoff = "q1",       # 第一四分位数以下不显示
  max.cutoff = "q99"       # 第九十九四分位数以上截断
)
```

### 6. 保存降维结果

```r
# ============================================
# 保存 Seurat 对象（包含所有降维结果）
# ============================================
saveRDS(pbmc, file = "./pbmc_with_umap.rds")

# 下次加载
pbmc <- readRDS("./pbmc_with_umap.rds")

# 导出 UMAP 坐标
umap_coords <- Embeddings(pbmc, "umap")
write.csv(umap_coords, "umap_coordinates.csv")

# 保存图片
ggsave("umap_plot.png", width = 8, height = 6, dpi = 300)
```

## ⚠️ 常见问题与注意事项

- **dims 参数必须正确**：它决定了用多少个PC来计算UMAP，直接影响结果
- **UMAP/t-SNE只用于可视化**：不要用UMAP坐标做聚类或差异分析
- **t-SNE每次结果不同**：设 `set.seed()` 保证可重复性
- **perplexity**：t-SNE的perplexity通常设 5-50，细胞少就设小
- **n.neighbors**：UMAP的近邻数通常设 5-50

## 🔗 相关模块
- [[06_数据缩放与线性降维PCA/数据缩放与线性降维PCA]]
- [[08_细胞聚类/细胞聚类]]
