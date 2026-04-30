# 多样本整合Integration

## 📌 本模块目标
掌握 Seurat v5 的多样本整合方法，理解 CCA、RPCA、Harmony 等不同整合策略的原理和适用场景，消除批次效应。

## 🔧 核心函数
| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `merge()` | 合并多个Seurat对象 | `x`, `y`, `add.cell.ids` |
| `IntegrateLayers()` | Seurat v5整合方法 | `method`, `orig.reduction`, `new.reduction` |
| `FindIntegrationAnchors()` | 找整合锚点(v4) | `object.list`, `dims` |
| `IntegrateData()` | 整合数据(v4) | `anchorset`, `dims` |
| `RunHarmony()` | Harmony整合 | `group.by.vars` |

## 📝 详细代码与注释

### 1. 为什么要整合

```r
# ============================================
# 批次效应（Batch Effect）
# ============================================
# 多个样本/实验/批次的数据合并后，同一细胞类型可能因技术原因被分到不同cluster
# 整合的目的：消除技术差异，保留生物学差异
#
# 何时需要整合：
# ✅ 不同实验批次
# ✅ 不同测序平台
# ✅ 不同实验室
# ✅ 不同时间点
# ❌ 同一批次的重复样本不需要
```

### 2. 合并多个样本

```r
# ============================================
# 方法一：分别读取后合并
# ============================================
library(SeuratData)
InstallData("ifnb")  # 下载 IFNB 教程数据（包含两个样本）
data("ifnb")

# 或者手动合并
# 假设已经有两个 Seurat 对象：obj1, obj2
combined <- merge(
  x = obj1,
  y = obj2,
  add.cell.ids = c("CTRL", "STIM"),  # 细胞名前缀
  project = "IFNB"
)

# 合并3个以上样本
combined <- merge(obj1, y = c(obj2, obj3),
                  add.cell.ids = c("S1", "S2", "S3"))

# ============================================
# 合并后检查
# ============================================
table(combined$orig.ident)
# CTRL STIM 
# 6548  7452
```

### 3. Seurat v5 整合流程（推荐）

```r
# ============================================
# Seurat v5 统一整合框架
# ============================================
# 使用 ifnb 数据集演示
data("ifnb")

# Step 1：预处理（每个样本独立处理）
ifnb <- SplitObject(ifnb, split.by = "orig.ident")  # 按样本拆分

ifnb <- lapply(X = ifnb, FUN = function(x) {
  x <- NormalizeData(x)
  x <- FindVariableFeatures(x, selection.method = "vst", nfeatures = 2000)
})

# Step 2：选择整合方法
# ============================================
# CCA (默认) — 适合批次差异较小的数据
# RPCA — 适合批次差异较大的数据（更保守）
# Harmony — 速度最快，适合大数据集
# ============================================

# 选择高变基因（取交集）
features <- SelectIntegrationFeatures(object.list = ifnb)

# Step 3：准备合并对象
ifnb <- merge(x = ifnb[[1]], y = ifnb[-1])
ifnb <- ScaleData(ifnb, features = features)
ifnb <- RunPCA(ifnb, features = features, npcs = 30)

# Step 4：整合（以 CCA 为例）
ifnb <- IntegrateLayers(
  ifnb,
  method = CCAIntegration,       # 或 RPCAIntegration, HarmonyIntegration
  orig.reduction = "pca",
  new.reduction = "integrated.cca",
  verbose = FALSE
)

# Step 5：后续分析（基于整合后的降维）
ifnb <- RunUMAP(ifnb, reduction = "integrated.cca", dims = 1:30)
ifnb <- FindNeighbors(ifnb, reduction = "integrated.cca", dims = 1:30)
ifnb <- FindClusters(ifnb, resolution = 0.5)

# 可视化
DimPlot(ifnb, reduction = "umap", group.by = "orig.ident")   # 按样本看
DimPlot(ifnb, reduction = "umap", label = TRUE)              # 按cluster看
```

### 4. RPCA 整合（更保守）

```r
# ============================================
# RPCA：Reciprocal PCA
# 适合批次差异大的数据，过度整合风险低
# ============================================
ifnb <- IntegrateLayers(
  ifnb,
  method = RPCAIntegration,
  orig.reduction = "pca",
  new.reduction = "integrated.rpca",
  verbose = FALSE
)

ifnb <- RunUMAP(ifnb, reduction = "integrated.rpca", dims = 1:30)
DimPlot(ifnb, reduction = "umap", group.by = "orig.ident")
```

### 5. Harmony 整合（最快）

```r
# ============================================
# Harmony：基于迭代的聚类校正
# 速度最快，适合大数据集
# ============================================
# install.packages("harmony")
library(harmony)

ifnb <- RunHarmony(
  ifnb,
  group.by.vars = "orig.ident",    # 指定批次变量
  reduction = "pca",
  dims.use = 1:30
)

# 使用 Harmony 结果进行后续分析
ifnb <- RunUMAP(ifnb, reduction = "harmony", dims = 1:30)
ifnb <- FindNeighbors(ifnb, reduction = "harmony", dims = 1:30)
ifnb <- FindClusters(ifnb, resolution = 0.5)

DimPlot(ifnb, reduction = "umap", group.by = "orig.ident")
```

### 6. 评估整合效果

```r
# ============================================
# 检查批次效应是否消除
# ============================================

# 1. UMAP按样本着色：同一细胞类型的细胞应该混合在一起
p1 <- DimPlot(ifnb, reduction = "umap", group.by = "orig.ident") + ggtitle("By Sample")
p2 <- DimPlot(ifnb, reduction = "umap", label = TRUE) + ggtitle("By Cluster")
p1 + p2

# 2. 每个cluster中各样本的比例
table(ifnb$seurat_clusters, ifnb$orig.ident)

# 3. 如果某个cluster几乎全是一个样本 → 批次效应没消除
# 4. 如果同一细胞类型在整合后被强行合并 → 可能过度整合
```

### 7. SCTransform 整合流程

```r
# ============================================
# 基于 SCTransform 的整合（v5推荐）
# ============================================
ifnb <- SplitObject(ifnb, split.by = "orig.ident")

ifnb <- lapply(X = ifnb, FUN = function(x) {
  x <- SCTransform(x, vst.flavor = "v2", verbose = FALSE)
})

features <- SelectIntegrationFeatures(object.list = ifnb, nfeatures = 3000)
ifnb <- PrepSCTIntegration(object.list = ifnb, anchor.features = features)

ifnb <- merge(x = ifnb[[1]], y = ifnb[-1])

ifnb <- IntegrateLayers(
  ifnb,
  method = CCAIntegration,
  orig.reduction = "pca",
  new.reduction = "integrated.cca",
  verbose = FALSE
)
```

## ⚠️ 常见问题与注意事项

- **过度整合**：不同细胞类型被强行合并，丢失了真实的生物学差异
- **整合不足**：批次效应未消除，同一细胞类型被分成多个cluster
- **方法选择**：批次差异小用CCA，大用RPCA，大数据用Harmony
- **v5 vs v4**：v5 用 `IntegrateLayers()` 替代了 v4 的 `FindIntegrationAnchors()` + `IntegrateData()`
- **整合后降维**：必须基于整合后的 reduction（如 integrated.cca），不是原始 PCA

## 🔗 相关模块
- [[08_细胞聚类/细胞聚类]]
- [[10_细胞类型注释/细胞类型注释]]
