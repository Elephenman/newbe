# 数据导入与Seurat对象

## 📌 本模块目标
学会将各种格式的单细胞数据导入 R，创建 Seurat 对象，理解 Seurat 对象的结构和数据存储方式。

## 🔧 核心函数
| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `Read10X()` | 读取10x Genomics数据 | `data.dir`, `gene.column` |
| `Read10X_h5()` | 读取10x h5格式 | `filename` |
| `CreateSeuratObject()` | 创建Seurat对象 | `counts`, `project`, `min.cells`, `min.features` |
| `dim()` | 查看基因数和细胞数 | — |
| `head()` | 查看前几行 | `n` |

## 📝 详细代码与注释

### 1. 理解稀疏矩阵（Seurat底层数据结构）

```r
# ============================================
# 稀疏矩阵 vs 稠密矩阵
# 单细胞数据中 90% 以上是 0，用稀疏矩阵存储可节省大量内存
# ============================================
library(Matrix)

# 创建一个普通矩阵（大量0值）
mx <- matrix(c(0, 0, 3, 0, 0, 0, 0, 4, 0), nrow = 3, byrow = TRUE)
mx
#      [,1] [,2] [,3]
# [1,]    0    0    3
# [2,]    0    0    0
# [3,]    0    4    0

# 转换为稀疏矩阵（0 变成 "."）
mx_sparse <- Matrix(mx, sparse = TRUE)
mx_sparse
# 3 x 3 sparse Matrix of class "dgCMatrix"
# [1,] . . 3
# [2,] . . .
# [3,] . 4 .

# 转回稠密矩阵
mx_raw <- as.matrix(mx_sparse)
```

### 2. 读取 10x Genomics 数据

```r
# ============================================
# 方法一：读取标准 10x 输出目录（3个文件：matrix.mtx, genes.tsv, barcodes.tsv）
# ============================================
pbmc.data <- Read10X(data.dir = "./filtered_gene_bc_matrices/hg19/")

# 查看数据类型
class(pbmc.data)
# [1] "dgCMatrix"  → 稀疏矩阵

# ============================================
# 方法二：读取 h5 格式
# ============================================
pbmc.data <- Read10X_h5(filename = "./filtered_feature_bc_matrix.h5")

# ============================================
# 方法三：读取 SeuratData 内置数据
# ============================================
library(SeuratData)
InstallData("pbmc3k")  # 首次需要下载
data("pbmc3k")
pbmc <- pbmc3k  # 直接获取Seurat对象
```

### 3. 创建 Seurat 对象

```r
# ============================================
# CreateSeuratObject 核心参数详解
# ============================================
pbmc <- CreateSeuratObject(
  counts = pbmc.data,    # 原始计数矩阵（稀疏或稠密都行）
  project = "pbmc3k",    # 项目名称，会存入 meta.data$orig.ident
  min.cells = 3,         # 基因至少在3个细胞中表达才保留（过滤低表达基因）
  min.features = 200     # 细胞至少表达200个基因才保留（过滤低质量细胞）
)

# 查看对象基本信息
print(pbmc)
# An object of class Seurat 
# 13714 features across 2700 samples within 1 assay 
# Active assay: RNA (13714 features, 0 variable features)
# 1 layer present: counts
```

### 4. 理解 Seurat 对象结构

```r
# ============================================
# Seurat 对象的 5 个核心部分
# ============================================

# ① 基因和细胞维度：行=基因，列=细胞
dim(pbmc)
# [1] 13714  2700  → 13714个基因，2700个细胞

# ② meta.data：细胞级别的元数据（类似 Excel 表格）
head(pbmc@meta.data)
#                orig.ident nCount_RNA nFeature_RNA
# AAACATACAACCAC-1    pbmc3k       2419          779
# AAACATTGAGCTAC-1    pbmc3k       4903         1352
# AAACATTGATCAGC-1    pbmc3k       3147         1129
# ...

# nCount_RNA：该细胞中检测到的转录本总数（UMI数）
# nFeature_RNA：该细胞中检测到的基因种类数

# ③ 原始计数矩阵
pbmc[["RNA"]]$counts  # 原始 raw counts

# ④ 标准化后的矩阵（归一化后才有）
pbmc[["RNA"]]$data    # normalized data（后面步骤生成）

# ⑤ 缩放后的矩阵（缩放后才有）
pbmc[["RNA"]]$scale.data  # scaled data（后面步骤生成）
```

### 5. 查看特定基因的表达

```r
# ============================================
# 查看前30个细胞中几个关键基因的表达
# ============================================
pbmc.data[c("CD3D", "TCL1A", "MS4A1"), 1:30]
# CD3D  T细胞标记
# MS4A1 B细胞标记（CD20）
# TCL1A B细胞标记

# 稀疏矩阵中 "." 代表 0
```

### 6. 比较稀疏 vs 稠密矩阵内存占用

```r
# ============================================
# 实际看看稀疏矩阵省了多少内存
# ============================================
dense.size <- object.size(as.matrix(pbmc.data))
dense.size
# 709,591,472 bytes（约 677 MB）

sparse.size <- object.size(pbmc.data)
sparse.size
# 29,905,192 bytes（约 28.5 MB）

# 稀疏矩阵仅为稠密矩阵的 4.2%！
as.numeric(sparse.size) / as.numeric(dense.size) * 100
# [1] 4.2
```

### 7. 导入其他格式的数据

```r
# ============================================
# 从 CSV 读取（行为基因，列为细胞）
# ============================================
expr_matrix <- read.csv("expression_matrix.csv", row.names = 1)
seurat_obj <- CreateSeuratObject(counts = expr_matrix)

# ============================================
# 从表达矩阵直接创建
# ============================================
# 假设你已经有 count_matrix（行=基因，列=细胞）
seurat_obj <- CreateSeuratObject(
  counts = count_matrix,
  project = "my_project",
  min.cells = 0,         # 不过滤
  min.features = 0       # 不过滤
)

# ============================================
# 读取多个样本并合并
# ============================================
# 分别读取每个样本
sample1 <- Read10X(data.dir = "./sample1/outs/filtered_feature_bc_matrix/")
sample2 <- Read10X(data.dir = "./sample2/outs/filtered_feature_bc_matrix/")

# 分别创建对象
obj1 <- CreateSeuratObject(sample1, project = "sample1")
obj2 <- CreateSeuratObject(sample2, project = "sample2")

# 合并
combined <- merge(obj1, y = obj2, add.cell.ids = c("S1", "S2"))
# 合并后细胞名前会加上 S1_ 和 S2_ 前缀
```

## ⚠️ 常见问题与注意事项

- **路径问题**：`Read10X()` 的 `data.dir` 必须是包含 matrix.mtx/gene.tsv/barcodes.tsv 的目录
- **基因名格式**：`gene.column = 1` 使用 Ensembl ID，`gene.column = 2` 使用基因符号
- **min.cells/min.features**：初次创建时建议设小一点（如 3 和 200），后续 QC 步骤再严格过滤
- **内存不够**：大数据集用 `memory.limit(size = 9999999999999)` 扩大虚拟内存（Windows）
- **Seurat v5 变化**：v5 用 `$counts` / `$data` / `$scale.data` 替代了 v4 的 `slot()`

## 🔗 相关模块
- [[01_安装与环境配置/安装与环境配置]]
- [[03_质量控制QC/质量控制QC]]
- [[11_多样本整合Integration/多样本整合Integration]]
