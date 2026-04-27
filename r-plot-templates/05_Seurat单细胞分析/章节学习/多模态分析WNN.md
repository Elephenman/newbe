# 多模态分析WNN

## 📌 本模块目标
掌握 Seurat 的加权最近邻（WNN）方法，整合多种数据模态（如 RNA+ATAC、RNA+蛋白），进行多模态联合分析。

## 🔧 核心函数
| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `FindMultiModalNeighbors()` | 构建WNN图 | `reduction.list`, `dims.list` |
| `RunUMAP()` | WNN UMAP | `nn.name`, `reduction.name` |
| `FindClusters()` | WNN聚类 | `graph.name` |
| `ConnectModalities()` | 连接不同模态 | — |

## 📝 详细代码与注释

### 1. WNN 原理

```r
# ============================================
# Weighted Nearest Neighbor（WNN）
# ============================================
# 核心思想：
#   每个细胞有两种（或更多）模态的邻居图
#   WNN 根据每种模态的信息含量，为每个细胞自动学习权重
#   最终的邻居图 = RNA权重 × RNA邻居 + ATAC权重 × ATAC邻居
#
# 优势：
#   1. 自动学习权重，不需要手动设置
#   2. 稀有细胞类型可能被某种模态更好地捕捉
#   3. 结果比任何单一模态都更稳健
```

### 2. RNA + ATAC 多模态分析

```r
# ============================================
# 使用 10x Multiome 数据（同时测 RNA + ATAC）
# ============================================
library(Seurat)
library(Signac)

# 下载示例数据
library(SeuratData)
InstallData("pbmcMultiome")

# 加载数据
pbmc.multi <- LoadData("pbmcMultiome")

# ============================================
# RNA 部分处理
# ============================================
DefaultAssay(pbmc.multi) <- "RNA"
pbmc.multi <- NormalizeData(pbmc.multi)
pbmc.multi <- FindVariableFeatures(pbmc.multi)
pbmc.multi <- ScaleData(pbmc.multi)
pbmc.multi <- RunPCA(pbmc.multi)

# ============================================
# ATAC 部分处理
# ============================================
DefaultAssay(pbmc.multi) <- "ATAC"
pbmc.multi <- RunTFM(pbmc.multi)  # 运行TF motif分析
pbmc.multi <- FindTopFeatures(pbmc.multi, min.cutoff = "q0")
pbmc.multi <- RunSVD(pbmc.multi)  # LSI降维（ATAC用LSI而非PCA）

# ============================================
# WNN 整合
# ============================================
pbmc.multi <- FindMultiModalNeighbors(
  pbmc.multi,
  reduction.list = list("pca", "lsi"),          # 两种模态的降维
  dims.list = list(1:30, 2:30),                 # 各自使用的维度
  modality.weight.name = c("RNA.weight", "ATAC.weight")  # 权重名
)

# WNN UMAP
pbmc.multi <- RunUMAP(
  pbmc.multi,
  nn.name = "weighted.nn",
  reduction.name = "wnn.umap",
  reduction.key = "wnnUMAP_"
)

# WNN 聚类
pbmc.multi <- FindClusters(
  pbmc.multi,
  graph.name = "wsnn",
  algorithm = 3,
  resolution = 0.8
)
```

### 3. RNA + 蛋白质（CITE-seq）

```r
# ============================================
# CITE-seq：同时测 RNA + 表面蛋白
# ============================================
library(SeuratData)
InstallData("bm")
data("bm")

# ============================================
# RNA 处理
# ============================================
DefaultAssay(bm) <- "RNA"
bm <- NormalizeData(bm)
bm <- FindVariableFeatures(bm)
bm <- ScaleData(bm)
bm <- RunPCA(bm)

# ============================================
# 蛋白质处理
# ============================================
DefaultAssay(bm) <- "ADT"  # Antibody-Derived Tags
bm <- NormalizeData(bm, normalization.method = "CLR", margin = 2)
bm <- ScaleData(bm)
bm <- RunPCA(bm, reduction.name = "apca")

# ============================================
# WNN 整合
# ============================================
bm <- FindMultiModalNeighbors(
  bm,
  reduction.list = list("pca", "apca"),
  dims.list = list(1:30, 1:18),
  modality.weight.name = c("RNA.weight", "ADT.weight")
)

bm <- RunUMAP(bm, nn.name = "weighted.nn", reduction.name = "wnn.umap")
bm <- FindClusters(bm, graph.name = "wsnn", algorithm = 3, resolution = 0.8)

# 可视化
DimPlot(bm, reduction = "wnn.umap", label = TRUE)
```

### 4. 比较单模态 vs WNN 结果

```r
# ============================================
# 对比三种降维结果
# ============================================
# RNA only
bm <- RunUMAP(bm, reduction = "pca", dims = 1:30, reduction.name = "rna.umap")
# ADT only
bm <- RunUMAP(bm, reduction = "apca", dims = 1:18, reduction.name = "adt.umap")

# 三图对比
p1 <- DimPlot(bm, reduction = "rna.umap", label = TRUE) + ggtitle("RNA Only")
p2 <- DimPlot(bm, reduction = "adt.umap", label = TRUE) + ggtitle("ADT Only")
p3 <- DimPlot(bm, reduction = "wnn.umap", label = TRUE) + ggtitle("WNN")

p1 + p2 + p3
```

### 5. 查看每种模态的权重

```r
# ============================================
# 每个细胞的模态权重
# ============================================
# RNA 权重
VlnPlot(bm, features = "RNA.weight", group.by = "seurat_clusters")

# ADT 权重
VlnPlot(bm, features = "ADT.weight", group.by = "seurat_clusters")

# 在 UMAP 上展示权重
FeaturePlot(bm, features = c("RNA.weight", "ADT.weight"), reduction = "wnn.umap")

# 解读：
# RNA.weight 高 → 该细胞主要靠RNA信息聚类
# ADT.weight 高 → 该细胞主要靠蛋白信息聚类
# 这有助于理解不同细胞类型的特征来源
```

### 6. 蛋白质 Marker 可视化

```r
# ============================================
# 直接用抗体数据可视化表面蛋白
# ============================================
DefaultAssay(bm) <- "ADT"

FeaturePlot(bm, features = c("CD4-1", "CD8a", "CD19", "CD14"),
            reduction = "wnn.umap", ncol = 2)

# 小提琴图
VlnPlot(bm, features = c("CD4-1", "CD8a"), group.by = "seurat_clusters")
```

## ⚠️ 常见问题与注意事项

- **CLR 归一化**：蛋白/ADT 数据必须用 CLR 归一化，不能和 RNA 一样用 LogNormalize
- **ATAC 的 LSI 维度**：通常从第2维开始（第1维与测序深度相关），所以 `dims = 2:30`
- **权重解读**：权重反映的是信息含量，不是重要性
- **内存需求**：WNN 分析内存需求更大，建议 32GB+
- **Signac 包**：ATAC 分析需要额外安装 Signac 包

## 🔗 相关模块
- [[11_多样本整合Integration/多样本整合Integration]]
- [[12_空间转录组分析/空间转录组分析]]
