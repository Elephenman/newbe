---
tags:
  - Seurat
  - 单细胞
  - RNA-seq
  - R语言
  - 生物信息学
aliases:
  - Seurat完全手册
  - 单细胞分析宝典
created: 2026-04-20
updated: 2026-04-20
version: Seurat v5
---

# 🧬 Seurat 单细胞分析完全手册

> **一站式学习资源** — 整合16个学习模块 + 完整实战案例，代码齐全，即查即用。
> 基于 **Seurat v5**，覆盖从安装到高级分析的全部流程。

---

## 📑 全文目录

### [[#第一阶段：数据准备]]
- [[#M01 安装与环境配置]]
- [[#M02 数据导入与Seurat对象]]

### [[#第二阶段：核心分析流程]]
- [[#M03 质量控制QC]]
- [[#M04 数据归一化]]
- [[#M05 特征选择]]
- [[#M06 数据缩放与线性降维PCA]]
- [[#M07 非线性降维UMAP t-SNE]]
- [[#M08 细胞聚类]]
- [[#M09 差异表达与Marker基因]]
- [[#M10 细胞类型注释]]

### [[#第三阶段：高级分析]]
- [[#M11 多样本整合Integration]]
- [[#M12 空间转录组分析]]
- [[#M13 多模态分析WNN]]
- [[#M14 细胞周期评分]]

### [[#第四阶段：总结与实战]]
- [[#M15 命令速查表]]
- [[#M16 PBMC3k完整实战流程]]

---

## 🗺️ 学习路线图

```
数据准备阶段                核心分析阶段               高级分析阶段
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ M01 安装与环境 │────▶│ M03 质量控制 QC    │────▶│ M11 多样本整合      │
│ M02 数据导入   │     │ M04 数据归一化     │     │ M12 空间转录组      │
└──────────────┘     │ M05 特征选择       │     │ M13 多模态 WNN     │
                     │ M06 缩放与 PCA     │     │ M14 细胞周期评分    │
                     │ M07 UMAP/tSNE     │     └──────────────────┘
                     │ M08 细胞聚类       │
                     │ M09 差异表达       │     ┌──────────────────┐
                     │ M10 细胞类型注释    │────▶│ M15 命令速查表      │
                     └──────────────────┘     │ M16 完整实战案例    │
                                              └──────────────────┘
```

---

## 📚 官方资源

- **Seurat 官方网站**：https://satijalab.org/seurat/
- **Seurat GitHub 仓库**：https://github.com/satijalab/seurat
- **Seurat 官方教程（PBMC3k）**：https://satijalab.org/seurat/articles/pbmc3k_tutorial
- **Seurat v5 快速入门**：https://satijalab.org/seurat/articles/get_started_v5_new
- **Seurat 命令速查表**：https://satijalab.org/seurat/articles/essential_commands
- **Seurat 论文 (v5)**：Hao et al., Nature Biotechnology 2024

---

# 第一阶段：数据准备

---

## M01 安装与环境配置

### 📌 目标
安装 Seurat 及其依赖包，配置单细胞分析所需的 R 语言环境。

### 🔧 核心函数

| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `install.packages()` | 安装CRAN包 | `pkgs` |
| `BiocManager::install()` | 安装Bioconductor包 | `pkgs` |
| `packageVersion()` | 查看包版本 | `pkg` |
| `memory.limit()` | 设置Windows虚拟内存 | `size` |

### 📝 详细代码

#### 1. 安装 Seurat 主包

```r
# ============================================
# 方法一：从 CRAN 安装 Seurat（默认安装 v5）
# ============================================
install.packages("Seurat")

# ============================================
# 方法二：从 r-universe 安装最新开发版
# ============================================
install.packages("Seurat", repos = c(
  "https://satijalab.r-universe.dev",
  "https://cloud.r-project.org"
))

# ============================================
# 方法三：从 GitHub 安装开发版
# ============================================
# install.packages("remotes")
remotes::install_github("satijalab/seurat", "develop")
```

#### 2. 安装常用依赖包

```r
# ============================================
# Bioconductor 包管理器
# ============================================
install.packages("BiocManager")

# ============================================
# 数据处理与可视化
# ============================================
BiocManager::install(c(
  "tidyverse",    # 数据处理全家桶（dplyr, ggplot2, tidyr 等）
  "patchwork",    # 多图拼接
  "ggrepel"       # 标签不重叠
))

# ============================================
# 单细胞相关包
# ============================================
BiocManager::install(c(
  "SeuratData",   # Seurat 内置数据集
  "SeuratObject", # Seurat 对象定义
  "Signac"        # 单细胞ATAC-seq分析（可选）
))

# ============================================
# 富集分析相关包
# ============================================
BiocManager::install(c(
  "clusterProfiler",  # GO/KEGG 富集分析
  "org.Hs.eg.db",    # 人类基因注释
  "org.Mm.eg.db",    # 小鼠基因注释
  "enrichplot"       # 富集结果可视化
))
```

#### 3. 加载包并检查版本

```r
# ============================================
# 加载核心包
# ============================================
library(Seurat)      # 单细胞分析主包
library(dplyr)       # 数据操作
library(patchwork)   # 图形拼接
library(ggplot2)     # 绑图引擎

# ============================================
# 检查版本（确保 Seurat >= 5.0）
# ============================================
packageVersion("Seurat")
# 期望输出：'5.x.x'

packageVersion("SeuratObject")
# 期望输出：'5.x.x'
```

#### 4. Windows 内存优化

```r
# ============================================
# Windows 系统下扩大虚拟内存限制
# 单细胞数据通常很大，默认内存可能不够
# ============================================
memory.limit(size = 9999999999999)

# 查看当前内存限制
memory.limit()
# 返回当前内存限制（MB）
```

#### 5. 下载 Seurat 内置练习数据

```r
# ============================================
# 使用 SeuratData 下载官方练习数据集
# ============================================
library(SeuratData)

# 查看 AvailableData 所有可用数据集
AvailableData()

# 下载 PBMC 3k 教程数据
InstallData("pbmc3k")

# 下载 IFNB 整合教程数据
InstallData("ifnb")

# 下载 WNN 多模态教程数据
InstallData("bm")

# 加载数据
data("pbmc3k")
```

#### 6. 完整环境检查脚本

```r
# ============================================
# 一键检查所有必需包是否安装正确
# ============================================
check_packages <- function() {
  required <- c(
    "Seurat", "SeuratObject", "SeuratData",
    "dplyr", "ggplot2", "patchwork",
    "Matrix", "clusterProfiler", "org.Hs.eg.db"
  )
  
  for (pkg in required) {
    if (requireNamespace(pkg, quietly = TRUE)) {
      ver <- packageVersion(pkg)
      cat("✅", pkg, "-", as.character(ver), "\n")
    } else {
      cat("❌", pkg, "- 未安装！\n")
    }
  }
}

check_packages()

# 期望输出示例：
# ✅ Seurat - 5.1.0
# ✅ SeuratObject - 5.0.2
# ✅ dplyr - 1.1.4
# ...
```

### ⚠️ 常见问题

- **安装超时**：设置国内镜像 `options(repos = c(CRAN = "https://mirrors.tuna.tsinghua.edu.cn/CRAN/"))`
- **版本冲突**：Seurat v5 和 v4 不兼容，确保只安装一个版本
- **R 版本**：Seurat v5 要求 R >= 4.3.0，运行 `R.version.string` 检查
- **内存不足**：单细胞分析建议至少 16GB 内存，大数据集需要 32GB+
- **Mac 用户**：不需要 `memory.limit()`，那是 Windows 专用的
- **BPCells 支持**：Seurat v5 新增 on-disk 存储，需额外安装 `install.packages("BPCells")`

---

## M02 数据导入与Seurat对象

### 📌 目标
学会将各种格式的单细胞数据导入 R，创建 Seurat 对象，理解 Seurat 对象的结构和数据存储方式。

### 🔧 核心函数

| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `Read10X()` | 读取10x Genomics数据 | `data.dir`, `gene.column` |
| `Read10X_h5()` | 读取10x h5格式 | `filename` |
| `CreateSeuratObject()` | 创建Seurat对象 | `counts`, `project`, `min.cells`, `min.features` |
| `dim()` | 查看基因数和细胞数 | — |
| `head()` | 查看前几行 | `n` |

### 📝 详细代码

#### 1. 理解稀疏矩阵（Seurat底层数据结构）

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

#### 2. 读取 10x Genomics 数据

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

#### 3. 创建 Seurat 对象

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

#### 4. 理解 Seurat 对象结构

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

#### 5. 查看特定基因的表达

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

#### 6. 比较稀疏 vs 稠密矩阵内存占用

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

#### 7. 导入其他格式的数据

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

### ⚠️ 常见问题

- **路径问题**：`Read10X()` 的 `data.dir` 必须是包含 matrix.mtx/gene.tsv/barcodes.tsv 的目录
- **基因名格式**：`gene.column = 1` 使用 Ensembl ID，`gene.column = 2` 使用基因符号
- **min.cells/min.features**：初次创建时建议设小一点（如 3 和 200），后续 QC 步骤再严格过滤
- **内存不够**：大数据集用 `memory.limit(size = 9999999999999)` 扩大虚拟内存（Windows）
- **Seurat v5 变化**：v5 用 `$counts` / `$data` / `$scale.data` 替代了 v4 的 `slot()`

---

# 第二阶段：核心分析流程

---

## M03 质量控制QC

### 📌 目标
学会计算和可视化单细胞数据的质量控制指标（线粒体百分比、基因数、UMI数），并根据这些指标过滤低质量细胞。

### 🔧 核心函数

| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `PercentageFeatureSet()` | 计算某类基因的百分比 | `pattern`, `features` |
| `VlnPlot()` | 小提琴图展示QC指标 | `features`, `ncol`, `pt.size` |
| `RidgePlot()` | 山峦图展示QC指标 | `features`, `ncol` |
| `FeatureScatter()` | 散点图看指标相关性 | `feature1`, `feature2` |
| `subset()` | 按条件过滤细胞 | `subset` |

### 📝 详细代码

#### 1. 计算线粒体基因百分比

```r
# ============================================
# 为什么关注线粒体基因？
# → 线粒体基因占比高 = 细胞膜破裂，细胞质RNA流失，只剩线粒体RNA
# → 这些是低质量/死细胞，需要去除
# ============================================

# 方法一：用正则表达式匹配（推荐）
pbmc[["percent.mt"]] <- PercentageFeatureSet(
  pbmc,
  pattern = "^MT-"    # 匹配以 MT- 开头的基因（人类）
)

# 方法二：自定义基因列表
MT_geneSet <- str_subset(rownames(pbmc.data), "^MT-")
pbmc[["percent.mt"]] <- PercentageFeatureSet(
  pbmc,
  features = MT_geneSet
)

# ============================================
# 不同物种的线粒体基因前缀
# ============================================
# 人类（Human）："^MT-"
# 小鼠（Mouse）："^mt-"
# 大鼠（Rat）："^mt-"
# 斑马鱼（Zebrafish）："^mt-"
# 果蝇（Drosophila）："^mt:"

# 同时计算核糖体基因百分比（可选）
pbmc[["percent.rb"]] <- PercentageFeatureSet(pbmc, pattern = "^RP[SL]")
```

#### 2. 查看 QC 指标

```r
# ============================================
# 查看所有 QC 指标
# ============================================
head(pbmc[[]])
# orig.ident nCount_RNA nFeature_RNA percent.mt
# AAACATACAACCAC-1    pbmc3k       2419          779   3.017765
# AAACATTGAGCTAC-1    pbmc3k       4903         1352   3.793596
# AAACATTGATCAGC-1    pbmc3k       3147         1129   0.889736
# ...

# 统计摘要
summary(pbmc$nCount_RNA)
summary(pbmc$nFeature_RNA)
summary(pbmc$percent.mt)
```

#### 3. QC 指标可视化

```r
# ============================================
# 小提琴图 — 最常用的 QC 可视化
# ============================================
VlnPlot(pbmc,
  features = c("nFeature_RNA", "nCount_RNA", "percent.mt"),
  ncol = 3,        # 每行3个图
  pt.size = 0.01   # 点的大小（0=不显示点）
)

# ✅ 小提琴图的优势：
# 相比箱线图，可以更直观地看到数据分布形态（单峰、多峰、偏态）
```

```r
# ============================================
# 山峦图（Ridge Plot）— 多组比较时更直观
# ============================================
RidgePlot(pbmc,
  features = c("nFeature_RNA", "nCount_RNA", "percent.mt"),
  ncol = 1
)

# ✅ 山峦图优势：
# 能够清晰展示多个分组的分布差异
# 适合单细胞测序中不同细胞类型/状态的比较
```

```r
# ============================================
# 散点图 — 查看指标间的相关性
# ============================================
# 基因数量 vs 转录本数量（期望正相关）
p1 <- FeatureScatter(pbmc,
  feature1 = "nCount_RNA",
  feature2 = "nFeature_RNA"
)

# 线粒体百分比 vs 转录本数量（期望无/负相关）
p2 <- FeatureScatter(pbmc,
  feature1 = "nCount_RNA",
  feature2 = "percent.mt"
)

p1 + p2
```

#### 4. 过滤低质量细胞

```r
# ============================================
# 过滤标准详解
# ============================================
# nFeature_RNA > 200：去除基因数太少的细胞（死细胞/空液滴）
# nFeature_RNA < 2500：去除基因数太多的细胞（可能doublets多细胞融合）
# percent.mt < 5：去除线粒体占比过高的细胞（细胞膜破裂）

# 注意：阈值因数据集而异，需要根据小提琴图调整！

pbmc <- subset(pbmc,
  subset = nFeature_RNA > 200 &
           nFeature_RNA < 2500 &
           percent.mt < 5
)

# 查看过滤后的细胞数
dim(pbmc)
# 过滤前 2700 → 过滤后约 2638
```

#### 5. 高级 QC：检测 Doublets

```r
# ============================================
# 方法一：基于 nFeature_RNA 极端值（简单快速）
# ============================================
# nFeature_RNA 异常高的细胞可能是 doublets
# 通常设阈值为中位数 + 3*MAD

upper_threshold <- median(pbmc$nFeature_RNA) + 3 * mad(pbmc$nFeature_RNA)
cat("Doublet阈值:", upper_threshold, "\n")

# ============================================
# 方法二：使用 DoubletFinder 包（更准确）
# ============================================
# install.packages("DoubletFinder")
library(DoubletFinder)

# 预估 doublet 比例（通常 5-10%）
# 具体用法见 DoubletFinder 文档
```

#### 6. 保存过滤后的数据

```r
# ============================================
# 保存过滤后的 Seurat 对象
# ============================================
save(pbmc, file = "./pbmc_after_qc.rdata")

# 下次直接加载
load("./pbmc_after_qc.rdata")
```

### ⚠️ 常见问题

- **阈值不是固定的**：每个数据集的 QC 阈值不同，必须看小提琴图再决定
- **线粒体阈值**：5% 是 PBMC 的常用值，其他组织可能不同（如脑组织可放宽到 10%）
- **不要过度过滤**：宁可保留稍多一些，也不要丢失稀有细胞类型
- **小鼠线粒体前缀是小写**：`"^mt-"` 不是 `"^MT-"`
- **Doublets**：细胞数异常高（nFeature_RNA > 中位数+3MAD）的细胞可能是双细胞

---

## M04 数据归一化

### 📌 目标
理解为什么需要归一化，掌握 LogNormalize 方法的原理和使用，了解不同归一化方法的选择。

### 🔧 核心函数

| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `NormalizeData()` | 数据归一化 | `normalization.method`, `scale.factor` |
| `SCTransform()` | SCTransform归一化（v3+） | `vst.flavor`, `verbose` |

### 📝 详细代码

#### 1. 为什么需要归一化

```r
# ============================================
# 归一化的必要性
# ============================================
# 在 scRNA-seq 中，每个细胞的测序深度（捕获的RNA分子总量）差异很大：
#   • 有的细胞测到的转录本多 → 总表达量高
#   • 有的细胞测到的转录本少 → 总表达量低
# 
# 如果直接比较原始 counts，差异可能是测序深度导致的，不是生物学差异
# 归一化的目的：消除测序深度的技术差异，让细胞之间可比
```

#### 2. LogNormalize（最常用方法）

```r
# ============================================
# LogNormalize 原理
# ============================================
# 步骤1：每个基因的 count ÷ 该细胞的总 count → 得到相对表达量
# 步骤2：乘以 scale.factor（默认10000）→ 标准化到相同总量水平
# 步骤3：取 log(1 + x) → 压缩数据范围，稳定方差
#
# 数学公式：normalized = log(1 + count / total_count × 10000)
# ============================================

pbmc <- NormalizeData(
  pbmc,
  normalization.method = "LogNormalize",  # 归一化方法
  scale.factor = 10000                    # 缩放因子
)

# ⭐ 简写形式（默认参数即可满足大多数需求）
pbmc <- NormalizeData(pbmc)

# ============================================
# 归一化后的数据存储位置
# ============================================
pbmc[["RNA"]]$data     # 归一化后的矩阵
pbmc[["RNA"]]$counts   # 原始计数矩阵（不变）
```

#### 3. SCTransform（推荐用于 v3+）

```r
# ============================================
# SCTransform 原理
# ============================================
# 基于正则化负二项回归（regularized NB regression）
# 优势：
#   1. 同时完成归一化 + 高变基因选择 + 缩放
#   2. 对技术噪音（如线粒体比例）的去除更有效
#   3. 减少下游分析中的假阳性
# ============================================

pbmc <- SCTransform(
  pbmc,
  vst.flavor = "v2",     # 使用 v2 版本（更快更准）
  verbose = FALSE
)

# SCTransform 会自动：
# 1. 归一化数据
# 2. 选择高变基因
# 3. 回归掉 vars.to.regress 指定的变量

# 回归掉线粒体基因比例的影响
pbmc <- SCTransform(
  pbmc,
  vst.flavor = "v2",
  vars.to.regress = "percent.mt",  # 回归线粒体基因比例
  verbose = FALSE
)
```

#### 4. LogNormalize vs SCTransform 对比

```r
# ============================================
# 两种方法如何选择？
# ============================================
# | 特性              | LogNormalize           | SCTransform              |
# |-------------------|------------------------|--------------------------|
# | 速度              | 快                     | 较慢                     |
# | 操作步骤          | 需要单独找HVG+缩放     | 一步完成                 |
# | 技术噪音去除      | 需要手动回归           | 自动回归                 |
# | 整合分析兼容      | CCA/RPCA               | SCTransform专用流程       |
# | 适用场景          | 入门学习、简单数据     | 正式分析、复杂数据       |
#
# 🎯 建议：初学者先用 LogNormalize 学习流程，正式分析用 SCTransform
```

#### 5. 验证归一化效果

```r
# ============================================
# 对比归一化前后的表达值
# ============================================
# 取某个基因在第一个细胞的值
gene <- "CD3D"
cell <- colnames(pbmc)[1]

# 原始 count
raw_val <- pbmc[["RNA"]]$counts[gene, cell]
cat("原始 count:", raw_val, "\n")

# 归一化后的值
norm_val <- pbmc[["RNA"]]$data[gene, cell]
cat("归一化值:", norm_val, "\n")

# 查看归一化后的表达分布
hist(
  pbmc[["RNA"]]$data["CD3D", ],
  breaks = 50,
  main = "CD3D Normalized Expression",
  xlab = "Log-normalized expression"
)
```

### ⚠️ 常见问题

- **不要重复归一化**：`NormalizeData()` 和 `SCTransform()` 只能选一个
- **SCTransform 后不需要**：`FindVariableFeatures()` 和 `ScaleData()`（它一步完成了）
- **scale.factor**：10000 是默认值，一般不需要修改
- **整和分析**：如果用 SCTransform，整合时也要用 SCTransform 流程
- **vst.flavor = "v2"**：Seurat v5 推荐用 v2，速度更快结果更好

---

## M05 特征选择

### 📌 目标
理解高变基因（HVGs）的概念和筛选方法，学会使用 `FindVariableFeatures()` 选择对细胞分群最有价值的基因。

### 🔧 核心函数

| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `FindVariableFeatures()` | 筛选高变基因 | `selection.method`, `nfeatures` |
| `VariableFeatures()` | 获取高变基因列表 | `object` |
| `VariableFeaturePlot()` | 可视化高变基因 | `object` |
| `LabelPoints()` | 给图上的点加标签 | `plot`, `points`, `repel` |

### 📝 详细代码

#### 1. 为什么要筛选高变基因

```r
# ============================================
# 高变基因（Highly Variable Genes, HVGs）的意义
# ============================================
# 在整个基因表达矩阵中，大多数基因的表达在所有细胞里都差不多
# 这些"不变"的基因对区分细胞类型没有帮助
# 
# 高变基因 = 在不同细胞间表达差异很大的基因
# 这些基因更可能反映生物学差异（细胞类型、状态、功能）
# 
# 后续的降维（PCA）和聚类都只使用高变基因
# → 减少计算量 + 去除噪音 + 聚焦关键信息
```

#### 2. 筛选高变基因

```r
# ============================================
# 使用 vst 方法（默认推荐）
# ============================================
pbmc <- FindVariableFeatures(
  pbmc,
  selection.method = "vst",   # 变异稳定变换（推荐）
  nfeatures = 2000            # 选择前2000个高变基因
)

# ⭐ 简写形式
pbmc <- FindVariableFeatures(pbmc)

# ============================================
# selection.method 选项对比
# ============================================
# "vst"       → 变异稳定变换（默认，速度最快，适合大多数情况）
# "mvp"       → 均值-方差百分比（考虑均值对方差的影响）
# "dispersion" → 离散度法（经典方法，倾向于选择低表达高离散的基因）
```

#### 3. 查看高变基因

```r
# ============================================
# 获取高变基因列表
# ============================================
# 前10个高变基因
top10 <- head(VariableFeatures(pbmc), 10)
top10
# [1] "PPBP"   "LYZ"    "S100A9" "IGLL5"  "GNLY"   "FTL"   
# [7] "PF4"    "FTH1"   "GNG11"  "S100A8"

# 全部高变基因数量
length(VariableFeatures(pbmc))
# [1] 2000

# 所有高变基因
all_hvgs <- VariableFeatures(pbmc)
head(all_hvgs, 20)
```

#### 4. 可视化高变基因

```r
# ============================================
# 高变基因散点图
# ============================================
# X轴：基因平均表达量
# Y轴：标准化方差
# 红色点 = 高变基因
plot1 <- VariableFeaturePlot(pbmc)
plot1

# ============================================
# 标注前10个高变基因的名称
# ============================================
plot2 <- LabelPoints(
  plot = plot1,
  points = top10,
  repel = TRUE       # 标签不重叠
)
plot2

# 保存图片
ggsave("variable_features.png", plot2, width = 10, height = 6)
```

#### 5. 自定义高变基因列表

```r
# ============================================
# 手动添加或移除高变基因
# ============================================
# 添加特定的基因到高变基因列表
VariableFeatures(pbmc) <- c(
  VariableFeatures(pbmc),
  "CD3D", "CD3E", "MS4A1"  # 手动添加关注的关键基因
)

# 移除线粒体基因（如果它们被选入了高变基因）
hvgs <- VariableFeatures(pbmc)
hvgs <- hvgs[!grepl("^MT-", hvgs)]
VariableFeatures(pbmc) <- hvgs

# 移除核糖体基因
hvgs <- VariableFeatures(pbmc)
hvgs <- hvgs[!grepl("^RP[SL]", hvgs)]
VariableFeatures(pbmc) <- hvgs
```

#### 6. 不同数量高变基因的影响

```r
# ============================================
# 尝试不同数量的高变基因
# ============================================
# 默认 2000，大数据集可以尝试 3000-5000

# 尝试 3000 个
pbmc_3k <- FindVariableFeatures(pbmc, nfeatures = 3000)
length(VariableFeatures(pbmc_3k))

# 尝试 5000 个
pbmc_5k <- FindVariableFeatures(pbmc, nfeatures = 5000)
length(VariableFeatures(pbmc_5k))

# 🎯 经验值：
# - 小数据集（<5000细胞）：2000
# - 中等数据集（5k-50k细胞）：2000-3000
# - 大数据集（>50k细胞）：3000-5000
```

### ⚠️ 常见问题

- **2000 足够**：大多数情况下 2000 个高变基因就够用了
- **检查线粒体基因**：确保高变基因中没有线粒体基因，否则会影响聚类
- **SCTransform 跳过**：如果使用 SCTransform，它会自动选高变基因，不需要手动调
- **nfeatures 不是越多越好**：太多会引入噪音，太少会丢失信息
- **可视化很重要**：一定要看 VariableFeaturePlot，确认选出的基因合理

---

## M06 数据缩放与线性降维PCA

### 📌 目标
理解数据缩放（Z-score标准化）的目的和操作，掌握 PCA 降维的原理和可视化方法，学会确定用于后续分析的 PC 数量。

### 🔧 核心函数

| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `ScaleData()` | 数据缩放（Z-score） | `features`, `vars.to.regress` |
| `RunPCA()` | 主成分分析 | `features`, `npcs` |
| `VizDimLoadings()` | 可视化PC载荷 | `dims`, `reduction` |
| `DimPlot()` | 绘制降维散点图 | `reduction`, `group.by` |
| `DimHeatmap()` | PC热图 | `dims`, `cells`, `balanced` |
| `ElbowPlot()` | 肘部图选PC数 | `ndims` |
| `JackStraw()` | JackStraw显著性检验 | `num.replicate`, `dims` |

### 📝 详细代码

#### 1. 数据缩放（Scaling）

```r
# ============================================
# 为什么要缩放？
# ============================================
# PCA 要求数据满足：
#   1. 均值为0（中心化）→ 消除基因表达水平的绝对差异
#   2. 方差为1（标准化）→ 让所有基因在PCA中权重相同
# 否则高表达基因会主导PCA结果
#
# 数学操作：scaled = (x - mean) / sd
# ============================================

# 方法一：只对高变基因缩放（默认，更快）
pbmc <- ScaleData(pbmc)

# 方法二：对所有基因缩放（后续画热图需要）
all.genes <- rownames(pbmc)
pbmc <- ScaleData(pbmc, features = all.genes)

# ============================================
# 回归掉干扰因素（重要！）
# ============================================
# 回归线粒体基因比例 → 去除细胞质量差异
# 回归细胞周期 → 去除细胞周期效应
pbmc <- ScaleData(
  pbmc,
  vars.to.regress = c("percent.mt")  # 回归线粒体比例
)

# 同时回归多个因素
pbmc <- ScaleData(
  pbmc,
  vars.to.regress = c("percent.mt", "nCount_RNA")  # 回归线粒体+测序深度
)

# ⚠️ vars.to.regress 会显著增加计算时间
```

#### 2. 缩放结果验证

```r
# ============================================
# 验证缩放后的数据：每行均值为0，方差为1
# ============================================
# 提取缩放后的矩阵前10行
mat <- pbmc[["RNA"]]$scale.data[1:10, ]

# 计算每行的均值和方差
res <- data.frame(
  gene = rownames(mat),
  mean = apply(mat, 1, mean),      # 应该接近 0
  variance = apply(mat, 1, var)     # 应该接近 1
)
print(res)
# 均值 ≈ 0（可能有极小浮点误差）
# 方差 ≈ 1
```

#### 3. 运行 PCA

```r
# ============================================
# 主成分分析（PCA）
# ============================================
# 只使用高变基因进行PCA（默认）
pbmc <- RunPCA(
  pbmc,
  features = VariableFeatures(object = pbmc),
  ncp = 50    # 计算50个主成分（默认）
)

# ⭐ 简写形式
pbmc <- RunPCA(pbmc)
```

#### 4. 查看 PCA 结果

```r
# ============================================
# 查看前5个主成分的载荷基因
# ============================================
print(pbmc[["pca"]], dims = 1:5, nfeatures = 5)
# PC_ 1 
# Positive:  CST3, TYROBP, LST1, AIF1, FTL     → 髓系细胞标记
# Negative:  MALAT1, LTB, IL32, IL7R, CD2       → T细胞标记
# PC_ 2 
# Positive:  CD79A, MS4A1, TCL1A, HLA-DQA1      → B细胞标记
# Negative:  NKG7, PRF1, CST7, GZMB, GZMA       → NK/CTL标记
# ...

# ============================================
# 解读：每个PC的正/负载荷基因代表了该PC捕捉到的生物学差异
```

#### 5. PCA 可视化

```r
# ============================================
# 5.1 PC 载荷基因可视化
# ============================================
VizDimLoadings(pbmc, dims = 1:2, reduction = "pca")
# 显示 PC1 和 PC2 正/负载荷最大的基因

# ============================================
# 5.2 PCA 散点图
# ============================================
DimPlot(pbmc, reduction = "pca") + NoLegend()
# 每个点代表一个细胞，按 PC1 和 PC2 坐标排列

# ============================================
# 5.3 PC 热图（看每个PC的基因表达模式）
# ============================================
# 单个PC的热图
DimHeatmap(pbmc, dims = 1, cells = 500, balanced = TRUE)

# 前15个PC的热图（选择PC数量时参考）
DimHeatmap(pbmc, dims = 1:15, cells = 500, balanced = TRUE)

# 参数详解：
# dims：要绘制的主成分编号
# cells：使用多少个细胞（越多越慢）
# balanced：正负两侧各取等量基因
```

#### 6. 确定使用的 PC 数量（关键步骤！）

```r
# ============================================
# 方法一：肘部图（ElbowPlot）— 最常用
# ============================================
ElbowPlot(pbmc)
# 看拐点：PC 数量取拐点前的值
# 拐点 = 标准差下降明显变缓的位置
# 例如拐点在 PC10-12，就选 dims = 1:10

# 指定展示的 PC 数量
ElbowPlot(pbmc, ndims = 30)

# ============================================
# 方法二：JackStraw 检验（更严谨但更慢）
# ============================================
pbmc <- JackStraw(pbmc, num.replicate = 100, dims = 50)
pbmc <- ScoreJackStraw(pbmc, dims = 1:20)

JackStrawPlot(pbmc, dims = 1:20)
# 红线以上的 PC 是显著的
# 显著 PC 的最后一个就是使用数量

# ============================================
# 🎯 选择 PC 数量的经验法则
# ============================================
# 1. ElbowPlot 看拐点
# 2. JackStraw 看显著性
# 3. 热图看生物学意义
# 4. PBMC3k 通常选 10-20 个 PC
# 5. 宁多勿少（多选几个比少选好）
# 6. 不建议超过 30 个 PC
```

### ⚠️ 常见问题

- **ScaleData 必须在 RunPCA 之前**：先缩放再降维
- **vars.to.regress 很慢**：大数据集可能需要很长时间，可以用 SCTransform 替代
- **PC 数量很重要**：直接影响后续聚类结果，建议多试几个值
- **不要盲目选 10**：每个数据集最佳 PC 数不同
- **热图看生物学意义**：PC 的载荷基因应该有已知的生物学含义

---

## M07 非线性降维UMAP t-SNE

### 📌 目标
掌握 UMAP 和 t-SNE 两种非线性降维方法的原理和使用，学会选择合适的降维方法。

### 🔧 核心函数

| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `RunUMAP()` | 运行UMAP降维 | `dims`, `reduction`, `n.neighbors` |
| `RunTSNE()` | 运行t-SNE降维 | `dims`, `reduction`, `perplexity` |
| `DimPlot()` | 可视化降维结果 | `reduction`, `group.by`, `label` |

### 📝 详细代码

#### 1. 为什么要非线性降维

```r
# ============================================
# PCA 是线性降维，只能捕捉线性关系
# UMAP / t-SNE 是非线性降维，能更好地展示细胞的局部和全局结构
# 
# 注意：UMAP/t-SNE 只用于可视化，不用于后续计算！
# 聚类和差异表达仍然基于 PCA 空间
# ============================================
```

#### 2. 运行 UMAP（推荐）

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

#### 3. 运行 t-SNE

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

#### 4. UMAP vs t-SNE 对比

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

#### 5. 在 UMAP 上标注基因表达

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

#### 6. 保存降维结果

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

### ⚠️ 常见问题

- **dims 参数必须正确**：它决定了用多少个PC来计算UMAP，直接影响结果
- **UMAP/t-SNE只用于可视化**：不要用UMAP坐标做聚类或差异分析
- **t-SNE每次结果不同**：设 `set.seed()` 保证可重复性
- **perplexity**：t-SNE的perplexity通常设 5-50，细胞少就设小
- **n.neighbors**：UMAP的近邻数通常设 5-50

---

## M08 细胞聚类

### 📌 目标
掌握基于图论的细胞聚类方法，理解 FindNeighbors 和 FindClusters 的原理和参数调优，学会选择合适的分辨率（resolution）。

### 🔧 核心函数

| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `FindNeighbors()` | 构建KNN图 | `dims`, `k.param`, `graph.name` |
| `FindClusters()` | 图聚类 | `resolution`, `algorithm` |
| `Idents()` | 查看/设置细胞身份 | `object` |
| `BuildSNN()` | 构建共享最近邻图 | `object` |

### 📝 详细代码

#### 1. 聚类原理

```r
# ============================================
# Seurat 聚类原理（基于图论）
# ============================================
# 步骤1：FindNeighbors → 在PCA空间中构建KNN（K近邻）图
#   每个细胞连接最近的k个邻居
#   计算细胞间的相似度（基于PCA坐标）
#
# 步骤2：FindClusters → 基于KNN图进行社区检测
#   使用 Louvain/Leiden 算法
#   将连接紧密的细胞归为一类（cluster）
#
# 关键参数：resolution 控制分群的粗细程度
```

#### 2. 构建邻居图

```r
# ============================================
# FindNeighbors：构建K近邻图
# ============================================
pbmc <- FindNeighbors(
  pbmc,
  dims = 1:10,          # 使用前10个PC（与UMAP一致！）
  k.param = 20,         # 每个细胞的近邻数（默认20）
  graph.name = c("RNA_nn", "RNA_snn")  # 图的名称
)

# ⭐ 简写形式
pbmc <- FindNeighbors(pbmc, dims = 1:10)

# ============================================
# 参数详解
# ============================================
# dims：使用的PC数量，必须和 RunUMAP 一致
# k.param：近邻数，越大越平滑（默认20）
#   小数据集：10-20
#   大数据集：20-50
```

#### 3. 细胞聚类

```r
# ============================================
# FindClusters：社区检测
# ============================================
pbmc <- FindClusters(
  pbmc,
  resolution = 0.5,     # 分辨率（关键参数！）
  algorithm = 1,        # 1=Louvain, 2=Louvain(mod), 3=SLM, 4=Leiden
  random.seed = 42      # 随机种子，保证可重复
)

# 输出示例：
# Modularity Optimizer version 1.3.0 by Ludo Waltman and Nees Jan van Eck
# Number of nodes: 2638
# Number of edges: 95927
# Running Louvain algorithm...
# Maximum modularity in 10 random starts: 0.8728
# Number of communities: 9

# ============================================
# 查看聚类结果
# ============================================
# 每个细胞的cluster ID
head(Idents(pbmc), 5)
# AAACATACAACCAC-1 AAACATTGAGCTAC-1 AAACATTGATCAGC-1 AAACCGTGCTTCCG-1 AAACCGTGTATGCG-1 
#                2                3                2                1                6 
# Levels: 0 1 2 3 4 5 6 7 8

# 各cluster的细胞数
table(Idents(pbmc))
#    0    1    2    3    4    5    6    7    8 
#  697  483  471  346  315  162  107   42   15
```

#### 4. 调整分辨率（resolution）— 最关键参数

```r
# ============================================
# resolution 参数的影响
# ============================================
# resolution 越大 → 分群越多越细
# resolution 越小 → 分群越少越粗
#
# 经验值：
#   0.4-0.6  → 粗分（3-8个cluster）
#   0.8-1.2  → 中等（8-15个cluster）
#   1.5-2.0  → 细分（15-30个cluster）
#   3k PBMC   → 0.5 合适（9个cluster）

# ============================================
# 尝试不同分辨率
# ============================================
pbmc_04 <- FindClusters(pbmc, resolution = 0.4)
cat("Resolution 0.4:", length(levels(Idents(pbmc_04))), "clusters\n")

pbmc_08 <- FindClusters(pbmc, resolution = 0.8)
cat("Resolution 0.8:", length(levels(Idents(pbmc_08))), "clusters\n")

pbmc_12 <- FindClusters(pbmc, resolution = 1.2)
cat("Resolution 1.2:", length(levels(Idents(pbmc_12))), "clusters\n")

pbmc_20 <- FindClusters(pbmc, resolution = 2.0)
cat("Resolution 2.0:", length(levels(Idents(pbmc_20))), "clusters\n")

# ============================================
# Clustree：可视化不同分辨率下的分群关系
# ============================================
# install.packages("clustree")
library(clustree)

# 在多个分辨率下聚类
pbmc <- FindClusters(pbmc, resolution = c(0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0))

# 生成clustree图
clustree(pbmc, "RNA_snn_res")
```

#### 5. 可视化聚类结果

```r
# ============================================
# 在 UMAP 上展示聚类
# ============================================
# 运行 UMAP（如果还没运行）
pbmc <- RunUMAP(pbmc, dims = 1:10)

# 按聚类着色
DimPlot(pbmc, reduction = "umap", label = TRUE, pt.size = 0.5)

# 按样本着色（检查是否有批次效应）
DimPlot(pbmc, reduction = "umap", group.by = "orig.ident")

# ============================================
# 同时展示不同分辨率
# ============================================
p1 <- DimPlot(pbmc, reduction = "umap", group.by = "RNA_snn_res.0.4", label = TRUE) +
        ggtitle("Resolution 0.4")
p2 <- DimPlot(pbmc, reduction = "umap", group.by = "RNA_snn_res.0.8", label = TRUE) +
        ggtitle("Resolution 0.8")
p3 <- DimPlot(pbmc, reduction = "umap", group.by = "RNA_snn_res.1.2", label = TRUE) +
        ggtitle("Resolution 1.2")

p1 + p2 + p3
```

#### 6. 使用 Leiden 算法（更精确）

```r
# ============================================
# Leiden 算法（比 Louvain 更精确）
# ============================================
# 需要安装 leidenbase 包
# install.packages("leidenbase")

pbmc <- FindClusters(
  pbmc,
  resolution = 0.5,
  algorithm = 4,          # 4 = Leiden
  random.seed = 42
)
```

### ⚠️ 常见问题

- **resolution 是最重要的参数**：需要根据生物学知识调整
- **与UMAP的dims一致**：FindNeighbors 的 dims 必须和 RunUMAP 一致
- **cluster编号不代表顺序**：cluster 0 不一定比 cluster 1 更重要
- **Leiden > Louvain**：有条件建议用 Leiden（algorithm=4）
- **过度分群**：如果小cluster只有几个细胞，可能需要降低resolution
- **检查批次效应**：如果cluster与orig.ident强相关，可能有批次效应

---

## M09 差异表达与Marker基因

### 📌 目标
掌握使用 FindAllMarkers 和 FindMarkers 进行差异表达分析，理解各种统计检验方法的区别，学会筛选和可视化 Marker 基因。

### 🔧 核心函数

| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `FindAllMarkers()` | 所有cluster vs 其他cluster | `only.pos`, `min.pct`, `logfc.threshold` |
| `FindMarkers()` | 指定两组比较 | `ident.1`, `ident.2`, `test.use` |
| `FeaturePlot()` | UMAP上展示基因表达 | `features` |
| `VlnPlot()` | 小提琴图展示基因表达 | `features`, `group.by` |
| `DoHeatmap()` | Marker基因热图 | `features`, `group.by` |
| `DotPlot()` | 气泡图 | `features`, `group.by` |

### 📝 详细代码

#### 1. FindAllMarkers — 全局差异分析

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

#### 2. 筛选显著 Marker 基因

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

#### 3. FindMarkers — 指定两组比较

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

#### 4. 差异表达检验方法对比

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

#### 5. Marker 基因可视化

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

#### 6. 绘制火山图

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

### ⚠️ 常见问题

- **Wilcoxon vs MAST**：Wilcoxon 快且稳健，MAST 更准确但需要额外安装
- **min.pct 影响**：值越小找到的差异基因越多，但假阳性也可能增加
- **logfc.threshold**：设为0.25可以排除微小差异，减少计算量
- **p_val_adj**：务必使用校正后的p值（Bonferroni），原始p值太宽松
- **pct.1 和 pct.2**：如果一个基因 pct.1=0.9, pct.2=0.1，说明该基因高度特异性

---

## M10 细胞类型注释

### 📌 目标
学会基于 Marker 基因对聚类后的细胞群进行类型注释，掌握手动注释和自动注释方法。

### 🔧 核心函数

| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `RenameIdents()` | 重命名cluster为细胞类型 | `object`, `value` |
| `DotPlot()` | 气泡图查看marker表达 | `features`, `group.by` |
| `FeaturePlot()` | UMAP上查看marker | `features` |
| `VlnPlot()` | 小提琴图查看marker | `features` |
| `AddMetaData()` | 添加注释到meta.data | `object`, `metadata` |

### 📝 详细代码

#### 1. 常见细胞类型 Marker 基因速查表

```r
# ============================================
# 人类 PBMC 常见细胞类型 Marker
# ============================================
# | 细胞类型           | Marker基因                    | 说明               |
# |--------------------|-------------------------------|-------------------|
# | Naive CD4 T        | IL7R, CCR7                   | 初始CD4 T细胞      |
# | Memory CD4 T       | IL7R, S100A4                 | 记忆CD4 T细胞      |
# | CD8 T              | CD8A, CD8B                   | 细胞毒性T细胞      |
# | NK                 | GNLY, NKG7, KLRD1            | 自然杀伤细胞       |
# | B cells            | MS4A1, CD79A, CD79B          | B细胞（CD20+）     |
# | CD14+ Mono         | CD14, LYZ                    | CD14+单核细胞      |
# | FCGR3A+ Mono       | FCGR3A, MS4A7                | CD16+单核细胞      |
# | Dendritic          | FCER1A, HLA-DQA1             | 树突状细胞         |
# | Platelet           | PPBP, PF4                    | 血小板             |

# ============================================
# 其他常见组织的 Marker
# ============================================
# 肿瘤相关：
#   EPCAM（上皮），VIM（间质），PECAM1/CD31（内皮），ACTA2（成纤维）
# 神经系统：
#   NEUN/RBFOX3（神经元），GFAP（星形胶质），OLIG2（少突胶质），AIF1/IBA1（小胶质）
# 免疫：
#   PDCD1（CD8耗竭T），FOXP3（Treg），IL3RA（pDC），CD1C（cDC2）
```

#### 2. 手动注释流程

```r
# ============================================
# Step 1：查看每个cluster的top marker基因
# ============================================
pbmc.markers <- FindAllMarkers(pbmc, only.pos = TRUE, min.pct = 0.25, logfc.threshold = 0.25)

# 每个cluster的top5
top5 <- pbmc.markers %>%
  group_by(cluster) %>%
  slice_head(n = 5) %>%
  ungroup()

print(top5 %>% select(cluster, gene, avg_log2FC))

# ============================================
# Step 2：用气泡图综合查看所有marker
# ============================================
markers_to_check <- c(
  "IL7R", "CCR7",          # Naive CD4 T
  "S100A4",                # Memory CD4 T
  "CD8A", "CD8B",          # CD8 T
  "GNLY", "NKG7",          # NK
  "MS4A1", "CD79A",        # B cells
  "CD14", "LYZ",           # CD14+ Mono
  "FCGR3A", "MS4A7",       # FCGR3A+ Mono
  "FCER1A",                # DC
  "PPBP"                   # Platelet
)

DotPlot(pbmc, features = markers_to_check) + RotatedAxis()

# ============================================
# Step 3：用FeaturePlot逐个确认
# ============================================
FeaturePlot(pbmc, features = c("CD3D", "CD8A", "MS4A1", "CD14", "GNLY"),
            ncol = 3)

# ============================================
# Step 4：重命名cluster为细胞类型
# ============================================
new.cluster.ids <- c(
  "Naive CD4 T",      # cluster 0
  "CD14+ Mono",       # cluster 1
  "Memory CD4 T",     # cluster 2
  "B",                # cluster 3
  "CD8 T",            # cluster 4
  "FCGR3A+ Mono",     # cluster 5
  "NK",               # cluster 6
  "DC",               # cluster 7
  "Platelet"          # cluster 8
)

names(new.cluster.ids) <- levels(pbmc)
pbmc <- RenameIdents(pbmc, new.cluster.ids)

# ============================================
# Step 5：可视化注释结果
# ============================================
DimPlot(pbmc, reduction = "umap", label = TRUE, pt.size = 0.5) + NoLegend()

# 美化版
library(ggplot2)
plot <- DimPlot(pbmc, reduction = "umap", label = TRUE, label.size = 4.5) +
  xlab("UMAP 1") + ylab("UMAP 2") +
  theme(axis.title = element_text(size = 18),
        legend.text = element_text(size = 18)) +
  guides(colour = guide_legend(override.aes = list(size = 10)))

plot
ggsave("pbmc3k_annotated_umap.jpg", height = 7, width = 12, plot = plot)
```

#### 3. 将注释存入 meta.data

```r
# ============================================
# 将细胞类型注释保存到 meta.data 中
# ============================================
pbmc$celltype <- Idents(pbmc)

# 查看注释结果
head(pbmc@meta.data)

# 各细胞类型的细胞数
table(pbmc$celltype)

# 保存
saveRDS(pbmc, file = "./pbmc_annotated.rds")
```

#### 4. 自动注释方法

```r
# ============================================
# 方法一：SingleR（最常用自动注释）
# ============================================
BiocManager::install("SingleR")
library(SingleR)

# 获取参考数据集
ref <- HumanPrimaryCellAtlasData()

# 准备输入
test_data <- GetAssayData(pbmc, slot = "data")
test_labels <- pbmc$seurat_clusters

# 运行 SingleR
pred <- SingleR(
  test = test_data,
  ref = ref,
  labels = ref$label.main
)

# 查看注释结果
table(pred$labels)

# 将注释添加到 Seurat 对象
pbmc$SingleR_label <- pred$labels

# ============================================
# 方法二：scCATCH（基于文献marker数据库）
# ============================================
library(scCATCH)

# 准备输入
marker <- findmarkergenes(pbmc, species = "Human", cluster = "all")
annotation <- scCATCH(marker$clustermarker, species = "Human", tissue = "Blood")

# ============================================
# 方法三：基于参考数据集的标签转移
# ============================================
# 需要有已注释的参考 Seurat 对象
# 使用 TransferData 进行标签转移（见模块11）
```

#### 5. 验证注释结果

```r
# ============================================
# 多角度验证注释是否正确
# ============================================

# 1. 看已知的marker是否在正确的cluster高表达
VlnPlot(pbmc, features = c("CD3D", "MS4A1", "CD14", "GNLY"),
        group.by = "celltype", ncol = 2)

# 2. 在UMAP上确认marker表达位置
FeaturePlot(pbmc, features = c("CD3D", "MS4A1", "CD14", "GNLY"),
            ncol = 2)

# 3. 气泡图综合确认
DotPlot(pbmc, features = markers_to_check, group.by = "celltype") + RotatedAxis()

# 4. 热图看top marker的表达模式
top10 <- pbmc.markers %>%
  group_by(cluster) %>%
  dplyr::filter(avg_log2FC > 1) %>%
  slice_head(n = 10) %>%
  ungroup()

DoHeatmap(pbmc, features = top10$gene, group.by = "celltype") + NoLegend()
```

### ⚠️ 常见问题

- **注释顺序**：先手动粗注，再用自动方法验证
- **Marker特异性**：一个marker不一定只对应一种细胞，需要多个marker组合判断
- **参考数据集选择**：SingleR 的参考数据集要与分析数据的组织类型匹配
- **不要100%相信自动注释**：一定要人工检查
- **稀有细胞类型**：细胞数少的cluster可能被自动注释遗漏
- **保存注释**：一定要将注释结果存入 meta.data 和 RDS 文件

---

# 第三阶段：高级分析

---

## M11 多样本整合Integration

### 📌 目标
掌握 Seurat v5 的多样本整合方法，理解 CCA、RPCA、Harmony 等不同整合策略的原理和适用场景，消除批次效应。

### 🔧 核心函数

| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `merge()` | 合并多个Seurat对象 | `x`, `y`, `add.cell.ids` |
| `IntegrateLayers()` | Seurat v5整合方法 | `method`, `orig.reduction`, `new.reduction` |
| `FindIntegrationAnchors()` | 找整合锚点(v4) | `object.list`, `dims` |
| `IntegrateData()` | 整合数据(v4) | `anchorset`, `dims` |
| `RunHarmony()` | Harmony整合 | `group.by.vars` |

### 📝 详细代码

#### 1. 为什么要整合

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

#### 2. 合并多个样本

```r
# ============================================
# 方法一：分别读取后合并
# ============================================
library(SeuratData)
InstallData("ifnb")  # 下载 IFNB 教程数据（包含两个样本）
data("ifnb")

# 或者手动合并
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
```

#### 3. Seurat v5 整合流程（推荐）

```r
# ============================================
# Seurat v5 统一整合框架
# ============================================
data("ifnb")

# Step 1：预处理（每个样本独立处理）
ifnb <- SplitObject(ifnb, split.by = "orig.ident")

ifnb <- lapply(X = ifnb, FUN = function(x) {
  x <- NormalizeData(x)
  x <- FindVariableFeatures(x, selection.method = "vst", nfeatures = 2000)
})

# Step 2：选择整合方法
# CCA (默认) — 适合批次差异较小的数据
# RPCA — 适合批次差异较大的数据（更保守）
# Harmony — 速度最快，适合大数据集

# 选择高变基因（取交集）
features <- SelectIntegrationFeatures(object.list = ifnb)

# Step 3：准备合并对象
ifnb <- merge(x = ifnb[[1]], y = ifnb[-1])
ifnb <- ScaleData(ifnb, features = features)
ifnb <- RunPCA(ifnb, features = features, npcs = 30)

# Step 4：整合（以 CCA 为例）
ifnb <- IntegrateLayers(
  ifnb,
  method = CCAIntegration,
  orig.reduction = "pca",
  new.reduction = "integrated.cca",
  verbose = FALSE
)

# Step 5：后续分析（基于整合后的降维）
ifnb <- RunUMAP(ifnb, reduction = "integrated.cca", dims = 1:30)
ifnb <- FindNeighbors(ifnb, reduction = "integrated.cca", dims = 1:30)
ifnb <- FindClusters(ifnb, resolution = 0.5)

# 可视化
DimPlot(ifnb, reduction = "umap", group.by = "orig.ident")
DimPlot(ifnb, reduction = "umap", label = TRUE)
```

#### 4. RPCA 整合（更保守）

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

#### 5. Harmony 整合（最快）

```r
# ============================================
# Harmony：基于迭代的聚类校正
# ============================================
# install.packages("harmony")
library(harmony)

ifnb <- RunHarmony(
  ifnb,
  group.by.vars = "orig.ident",
  reduction = "pca",
  dims.use = 1:30
)

# 使用 Harmony 结果进行后续分析
ifnb <- RunUMAP(ifnb, reduction = "harmony", dims = 1:30)
ifnb <- FindNeighbors(ifnb, reduction = "harmony", dims = 1:30)
ifnb <- FindClusters(ifnb, resolution = 0.5)

DimPlot(ifnb, reduction = "umap", group.by = "orig.ident")
```

#### 6. 评估整合效果

```r
# ============================================
# 检查批次效应是否消除
# ============================================

# 1. UMAP按样本着色
p1 <- DimPlot(ifnb, reduction = "umap", group.by = "orig.ident") + ggtitle("By Sample")
p2 <- DimPlot(ifnb, reduction = "umap", label = TRUE) + ggtitle("By Cluster")
p1 + p2

# 2. 每个cluster中各样本的比例
table(ifnb$seurat_clusters, ifnb$orig.ident)

# 3. 如果某个cluster几乎全是一个样本 → 批次效应没消除
# 4. 如果同一细胞类型在整合后被强行合并 → 可能过度整合
```

#### 7. SCTransform 整合流程

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

### ⚠️ 常见问题

- **过度整合**：不同细胞类型被强行合并，丢失了真实的生物学差异
- **整合不足**：批次效应未消除，同一细胞类型被分成多个cluster
- **方法选择**：批次差异小用CCA，大用RPCA，大数据用Harmony
- **v5 vs v4**：v5 用 `IntegrateLayers()` 替代了 v4 的 `FindIntegrationAnchors()` + `IntegrateData()`
- **整合后降维**：必须基于整合后的 reduction（如 integrated.cca），不是原始 PCA

---

## M12 空间转录组分析

### 📌 目标
掌握使用 Seurat 分析空间转录组数据的方法，包括数据导入、空间可视化、空间变量基因检测和单细胞数据整合。

### 🔧 核心函数

| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `Load10X_Spatial()` | 加载10x空间数据 | `filename`, `assay` |
| `SpatialFeaturePlot()` | 空间基因表达可视化 | `features`, `alpha` |
| `SpatialDimPlot()` | 空间聚类可视化 | `group.by` |
| `FindSpatialVariableFeatures()` | 找空间变量基因 | `method`, `features` |
| `FindTransferAnchors()` | 单细胞-空间整合 | `reference.query` |

### 📝 详细代码

#### 1. 加载空间转录组数据

```r
# ============================================
# 加载 10x Visium 数据
# ============================================
library(Seurat)
library(SeuratData)

# 下载示例数据
InstallData("stxBrain")
brain <- LoadData("stxBrain", type = "anterior1")

# 或手动加载
brain <- Load10X_Spatial(
  data.dir = "./spatial/",
  filename = "filtered_feature_bc_matrix.h5",
  assay = "Spatial"
)
```

#### 2. 空间数据预处理

```r
# ============================================
# 基本流程与 scRNA-seq 类似
# ============================================
# QC：线粒体比例
brain[["percent.mt"]] <- PercentageFeatureSet(brain, pattern = "^MT-")
VlnPlot(brain, features = c("nCount_Spatial", "nFeature_Spatial", "percent.mt"),
        ncol = 3, pt.size = 0.1)

# 归一化（SCTransform推荐）
brain <- SCTransform(brain, assay = "Spatial", vst.flavor = "v2", verbose = FALSE)

# 降维
brain <- RunPCA(brain, verbose = FALSE)
brain <- RunUMAP(brain, dims = 1:30)

# 聚类
brain <- FindNeighbors(brain, dims = 1:30)
brain <- FindClusters(brain, resolution = 0.5)
```

#### 3. 空间可视化

```r
# ============================================
# SpatialFeaturePlot — 在组织切片上展示基因表达
# ============================================
SpatialFeaturePlot(brain, features = c("Hpca", "Ttr"))

# 调整透明度
SpatialFeaturePlot(brain,
  features = c("Hpca"),
  alpha = c(0.1, 1)
)

# ============================================
# SpatialDimPlot — 在组织切片上展示聚类
# ============================================
SpatialDimPlot(brain, label = TRUE, label.size = 3)

# 只显示特定cluster
SpatialDimPlot(brain, cells.highlight = CellsByIdentities(brain, idents = c(1, 2, 5)))
```

#### 4. 检测空间变量基因

```r
# ============================================
# 方法一：Moran's I 统计
# ============================================
brain <- FindSpatialVariableFeatures(
  brain,
  assay = "SCT",
  features = VariableFeatures(brain)[1:1000],
  method = "moransi"
)

top_spatial <- head(SpatialVariableFeatures(brain, selection.method = "moransi"), 6)
SpatialFeaturePlot(brain, features = top_spatial)

# ============================================
# 方法二：基于空间邻域的模式识别
# ============================================
brain <- FindSpatialVariableFeatures(
  brain,
  method = "markvariogram"
)
```

#### 5. 与单细胞数据整合（空间注释）

```r
# ============================================
# 用单细胞数据注释空间数据中的细胞类型
# ============================================
reference <- pbmc_annotated  # 已注释的单细胞数据

# 找锚点
anchors <- FindTransferAnchors(
  reference = reference,
  query = brain,
  normalization.method = "SCT",
  dims = 1:30
)

# 转移标签
predictions <- TransferData(
  anchorset = anchors,
  refdata = reference$celltype,
  weight.reduction = brain[["pca"]],
  dims = 1:30
)

# 添加预测结果
brain <- AddMetaData(brain, metadata = predictions)

# 可视化预测的细胞类型
SpatialDimPlot(brain, group.by = "predicted.id", label = TRUE)
```

#### 6. 反卷积（更精细的空间注释）

```r
# ============================================
# 使用 SPOTlight 进行反卷积
# 每个spot包含多个细胞，反卷积可估计各细胞类型的比例
# ============================================
# install.packages("SPOTlight")
library(SPOTlight)

seurat_sc <- pbmc_annotated
seurat_sp <- brain

spotlight_ls <- spotlight_deconvolution(
  seurat_sc = seurat_sc,
  seurat_sp = seurat_sp,
  clust_vr = "celltype",
  cluster_markers = pbmc.markers,
  n_top = 20,
  transf = "SCT",
  assay_sc = "SCT",
  assay_sp = "SCT"
)

# 可视化反卷积结果
SpatialFeaturePlot(brain, features = c("B", "CD8 T", "NK"))
```

### ⚠️ 常见问题

- **空间数据分辨率**：10x Visium 每个spot包含多个细胞（约1-10个）
- **SCTransform 更适合空间数据**：推荐用 SCTransform 而不是 LogNormalize
- **空间变量基因**：不一定与高变基因相同，空间模式更重要
- **整合时注意组织匹配**：参考单细胞数据的组织类型要和空间数据一致
- **图片对齐**：确保空间坐标与组织图片对齐

---

## M13 多模态分析WNN

### 📌 目标
掌握 Seurat 的加权最近邻（WNN）方法，整合多种数据模态（如 RNA+ATAC、RNA+蛋白），进行多模态联合分析。

### 🔧 核心函数

| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `FindMultiModalNeighbors()` | 构建WNN图 | `reduction.list`, `dims.list` |
| `RunUMAP()` | WNN UMAP | `nn.name`, `reduction.name` |
| `FindClusters()` | WNN聚类 | `graph.name` |
| `ConnectModalities()` | 连接不同模态 | — |

### 📝 详细代码

#### 1. WNN 原理

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

#### 2. RNA + ATAC 多模态分析

```r
# ============================================
# 使用 10x Multiome 数据（同时测 RNA + ATAC）
# ============================================
library(Seurat)
library(Signac)

# 下载示例数据
library(SeuratData)
InstallData("pbmcMultiome")
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
  reduction.list = list("pca", "lsi"),
  dims.list = list(1:30, 2:30),
  modality.weight.name = c("RNA.weight", "ATAC.weight")
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

#### 3. RNA + 蛋白质（CITE-seq）

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

DimPlot(bm, reduction = "wnn.umap", label = TRUE)
```

#### 4. 比较单模态 vs WNN 结果

```r
# ============================================
# 对比三种降维结果
# ============================================
bm <- RunUMAP(bm, reduction = "pca", dims = 1:30, reduction.name = "rna.umap")
bm <- RunUMAP(bm, reduction = "apca", dims = 1:18, reduction.name = "adt.umap")

p1 <- DimPlot(bm, reduction = "rna.umap", label = TRUE) + ggtitle("RNA Only")
p2 <- DimPlot(bm, reduction = "adt.umap", label = TRUE) + ggtitle("ADT Only")
p3 <- DimPlot(bm, reduction = "wnn.umap", label = TRUE) + ggtitle("WNN")

p1 + p2 + p3
```

#### 5. 查看每种模态的权重

```r
# ============================================
# 每个细胞的模态权重
# ============================================
VlnPlot(bm, features = "RNA.weight", group.by = "seurat_clusters")
VlnPlot(bm, features = "ADT.weight", group.by = "seurat_clusters")

FeaturePlot(bm, features = c("RNA.weight", "ADT.weight"), reduction = "wnn.umap")

# 解读：
# RNA.weight 高 → 该细胞主要靠RNA信息聚类
# ADT.weight 高 → 该细胞主要靠蛋白信息聚类
```

#### 6. 蛋白质 Marker 可视化

```r
# ============================================
# 直接用抗体数据可视化表面蛋白
# ============================================
DefaultAssay(bm) <- "ADT"

FeaturePlot(bm, features = c("CD4-1", "CD8a", "CD19", "CD14"),
            reduction = "wnn.umap", ncol = 2)

VlnPlot(bm, features = c("CD4-1", "CD8a"), group.by = "seurat_clusters")
```

### ⚠️ 常见问题

- **CLR 归一化**：蛋白/ADT 数据必须用 CLR 归一化，不能和 RNA 一样用 LogNormalize
- **ATAC 的 LSI 维度**：通常从第2维开始（第1维与测序深度相关），所以 `dims = 2:30`
- **权重解读**：权重反映的是信息含量，不是重要性
- **内存需求**：WNN 分析内存需求更大，建议 32GB+
- **Signac 包**：ATAC 分析需要额外安装 Signac 包

---

## M14 细胞周期评分

### 📌 目标
学会使用 Seurat 对细胞进行细胞周期评分，理解细胞周期效应对聚类的影响，掌握如何回归掉细胞周期效应。

### 🔧 核心函数

| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `CellCycleScoring()` | 细胞周期评分 | `s.features`, `g2m.features`, `set.ident` |
| `ScaleData()` | 回归细胞周期 | `vars.to.regress` |

### 📝 详细代码

#### 1. 细胞周期基因集

```r
# ============================================
# Seurat 内置的人类细胞周期基因
# ============================================
s.genes <- cc.genes$s.genes
head(s.genes)
# [1] "MCM5"   "PCNA"   "TYMS"   "FANCI"  "MCM7"   "MCM4"

g2m.genes <- cc.genes$g2m.genes
head(g2m.genes)
# [1] "ATAD2"  "TOP2A"  "HMGB2"  "CKS1B"  "ANP32E" "CTCF"

# ============================================
# 小鼠细胞周期基因（首字母大写，其余小写）
# ============================================
s.genes.mouse <- tolower(s.genes)
s.genes.mouse <- paste0(toupper(substr(s.genes.mouse, 1, 1)),
                         substr(s.genes.mouse, 2, nchar(s.genes.mouse)))

g2m.genes.mouse <- tolower(g2m.genes)
g2m.genes.mouse <- paste0(toupper(substr(g2m.genes.mouse, 1, 1)),
                           substr(g2m.genes.mouse, 2, nchar(g2m.genes.mouse)))
```

#### 2. 细胞周期评分

```r
# ============================================
# CellCycleScoring 计算每个细胞的 S 和 G2/M 评分
# ============================================
pbmc <- CellCycleScoring(
  pbmc,
  s.features = s.genes,
  g2m.features = g2m.genes,
  set.ident = TRUE
)

# 查看结果
head(pbmc@meta.data[, c("S.Score", "G2M.Score", "Phase")])
#                S.Score G2M.Score  Phase
# AAACATACAACCAC-1 -0.023   -0.038    G1
# AAACATTGAGCTAC-1  0.045    0.015     S
# AAACATTGATCAGC-1 -0.012   -0.028    G1

# 各阶段的细胞数
table(pbmc$Phase)
#   G1    S  G2M 
# 1622  538  478
```

#### 3. 可视化细胞周期

```r
# ============================================
# 在 PCA 空间看细胞周期分布
# ============================================
pbmc <- ScaleData(pbmc)
pbmc <- RunPCA(pbmc, features = c(s.genes, g2m.genes))

DimPlot(pbmc, reduction = "pca", group.by = "Phase")

# ============================================
# S.Score vs G2M.Score 散点图
# ============================================
library(ggplot2)
ggplot(pbmc@meta.data, aes(x = S.Score, y = G2M.Score, color = Phase)) +
  geom_point(size = 0.5, alpha = 0.5) +
  theme_classic() +
  labs(title = "Cell Cycle Scoring")

# ============================================
# 小提琴图看不同phase的细胞周期评分
# ============================================
VlnPlot(pbmc, features = c("S.Score", "G2M.Score"), group.by = "Phase")
```

#### 4. 回归细胞周期效应

```r
# ============================================
# 方法一：回归 S.Score 和 G2M.Score（去除所有细胞周期效应）
# ============================================
pbmc <- ScaleData(
  pbmc,
  vars.to.regress = c("S.Score", "G2M.Score"),
  features = rownames(pbmc)
)

# ============================================
# 方法二：只回归细胞周期评分的差异（保留增殖信号）
# ============================================
pbmc$CC.Difference <- pbmc$S.Score - pbmc$G2M.Score

pbmc <- ScaleData(
  pbmc,
  vars.to.regress = "CC.Difference",
  features = rownames(pbmc)
)

# 🎯 建议：
# 如果细胞周期不影响你的分析目标 → 不回归
# 如果细胞周期导致同一细胞类型被拆分 → 回归
# 如果增殖状态本身就是研究重点 → 不回归或只回归差异
```

#### 5. 检查回归效果

```r
# ============================================
# 重新运行 PCA 和 UMAP，看细胞周期是否还影响聚类
# ============================================
pbmc <- RunPCA(pbmc)
pbmc <- RunUMAP(pbmc, dims = 1:10)

DimPlot(pbmc, reduction = "umap", group.by = "Phase")

# 如果 G1/S/G2M 的细胞在UMAP上不再分离 → 回归成功
# 如果仍然明显分离 → 可能需要更严格的回归
```

#### 6. 用 SCTransform 回归细胞周期

```r
# ============================================
# SCTransform 可以更优雅地回归细胞周期
# ============================================
pbmc <- SCTransform(
  pbmc,
  vst.flavor = "v2",
  vars.to.regress = c("S.Score", "G2M.Score"),
  verbose = FALSE
)

# SCTransform 的回归效果通常比 ScaleData 更好
```

### ⚠️ 常见问题

- **不是所有数据都需要回归**：如果细胞周期不影响聚类，不要强行回归
- **增殖状态有意义**：肿瘤研究中增殖状态本身是重要的生物学信息
- **基因集匹配**：确保使用正确物种的细胞周期基因集
- **评分是连续值**：S.Score 和 G2M.Score 是连续值，Phase 是离散分类
- **先评分再回归**：必须先 CellCycleScoring 再 ScaleData

---

# 第四阶段：总结与实战

---

## M15 命令速查表

### 📌 目标
提供 Seurat 常用函数的快速查询参考，方便日常分析时随时查阅。

### 1. 数据导入与创建

```r
# 数据读取
Read10X(data.dir = "path/")          # 读取10x标准格式
Read10X_h5(filename = "file.h5")     # 读取10x h5格式
Load10X_Spatial(data.dir = "path/")  # 读取空间转录组

# 创建对象
CreateSeuratObject(counts, project, min.cells, min.features)
merge(obj1, y = obj2, add.cell.ids) # 合并多个对象

# 内置数据
library(SeuratData)
InstallData("pbmc3k")                # 下载PBMC3k
data("pbmc3k")                       # 加载数据
```

### 2. 质量控制

```r
# QC 计算
PercentageFeatureSet(obj, pattern = "^MT-")  # 线粒体百分比
subset(obj, subset = nFeature_RNA > 200 & nFeature_RNA < 2500 & percent.mt < 5)

# QC 可视化
VlnPlot(obj, features, ncol, pt.size)        # 小提琴图
RidgePlot(obj, features, ncol)               # 山峦图
FeatureScatter(obj, feature1, feature2)      # 散点图
```

### 3. 预处理

```r
# 归一化
NormalizeData(obj, normalization.method = "LogNormalize", scale.factor = 10000)
SCTransform(obj, vst.flavor = "v2", vars.to.regress, verbose = FALSE)

# 高变基因
FindVariableFeatures(obj, selection.method = "vst", nfeatures = 2000)
VariableFeatures(obj)                         # 获取高变基因列表
VariableFeaturePlot(obj)                      # 可视化
LabelPoints(plot, points, repel = TRUE)       # 标注标签

# 缩放
ScaleData(obj, features, vars.to.regress)     # Z-score标准化
```

### 4. 降维

```r
# PCA
RunPCA(obj, features, npcs = 50)
VizDimLoadings(obj, dims, reduction = "pca")  # 载荷可视化
DimHeatmap(obj, dims, cells, balanced)        # PC热图
ElbowPlot(obj, ndims = 30)                    # 肘部图
JackStraw(obj, num.replicate, dims)           # JackStraw检验
ScoreJackStraw(obj, dims)
JackStrawPlot(obj, dims)

# UMAP / t-SNE
RunUMAP(obj, dims, reduction)
RunTSNE(obj, dims, reduction, perplexity)
```

### 5. 聚类

```r
FindNeighbors(obj, dims, k.param = 20)
FindClusters(obj, resolution = 0.5, algorithm = 1)
# algorithm: 1=Louvain, 2=Louvain(mod), 3=SLM, 4=Leiden
Idents(obj)                                   # 查看聚类ID
levels(obj)                                   # 查看cluster级别
RenameIdents(obj, new.ids)                   # 重命名cluster
```

### 6. 差异表达

```r
FindAllMarkers(obj, only.pos, test.use, min.pct, logfc.threshold)
FindMarkers(obj, ident.1, ident.2, only.pos, test.use, min.pct)

# test.use 选项:
# "wilcox" (默认) | "MAST" | "DESeq2" | "roc" | "t" | "LR" | "negbinom" | "poisson"
```

### 7. 可视化

```r
# 通用可视化
DimPlot(obj, reduction, group.by, label, pt.size)        # 降维图
FeaturePlot(obj, features, reduction, order, ncol)       # 特征表达图
VlnPlot(obj, features, group.by, ncol, pt.size)          # 小提琴图
DotPlot(obj, features, group.by) + RotatedAxis()         # 气泡图
DoHeatmap(obj, features, group.by) + NoLegend()          # 热图
RidgePlot(obj, features, ncol)                           # 山峦图
FeatureScatter(obj, feature1, feature2)                  # 散点图

# 空间转录组
SpatialFeaturePlot(obj, features, alpha)                 # 空间基因表达
SpatialDimPlot(obj, group.by, label)                     # 空间聚类图
```

### 8. 整合

```r
# 多样本整合
# Seurat v5
IntegrateLayers(obj, method, orig.reduction, new.reduction)
# method: CCAIntegration | RPCAIntegration | HarmonyIntegration

# Harmony
RunHarmony(obj, group.by.vars, reduction)

# 标签转移
FindTransferAnchors(reference, query, normalization.method, dims)
TransferData(anchorset, refdata, weight.reduction, dims)
```

### 9. 多模态 (WNN)

```r
FindMultiModalNeighbors(obj, reduction.list, dims.list, modality.weight.name)
```

### 10. 细胞周期

```r
CellCycleScoring(obj, s.features, g2m.features, set.ident)
# 内置基因集: cc.genes$s.genes, cc.genes$g2m.genes
```

### 11. 数据提取与保存

```r
# 提取数据
GetAssayData(obj, slot = "counts")   # 原始计数
GetAssayData(obj, slot = "data")     # 归一化数据
GetAssayData(obj, slot = "scale.data") # 缩放数据
Embeddings(obj, "umap")              # UMAP坐标
Embeddings(obj, "pca")              # PCA坐标
pbmc@meta.data                       # 元数据
pbmc[["RNA"]]$counts                 # 原始矩阵
pbmc[["RNA"]]$data                   # 归一化矩阵

# 保存/加载
saveRDS(obj, file = "obj.rds")       # 保存Seurat对象
readRDS("obj.rds")                   # 加载Seurat对象
save(obj, file = "obj.rdata")        # 保存为RData
load("obj.rdata")                    # 加载RData
```

### 12. Seurat v4 → v5 迁移速查

```r
# 主要变化
# v4                                  → v5
# ---------------------------------------------------------
# slot(obj, "counts")                 → obj[["RNA"]]$counts
# slot(obj, "data")                   → obj[["RNA"]]$data
# GetAssayData(obj, slot="counts")    → obj[["RNA"]]$counts
# FindIntegrationAnchors() +          → IntegrateLayers()
#   IntegrateData()                     
# Assay() / SetAssay()                → [[  ]] 操作符
# obj$RNA                             → obj[["RNA"]]
```

---

## M16 PBMC3k完整实战流程

### 📌 目标
用一个完整的 PBMC 3k 数据集实战演练，将前面所有模块的知识串联起来，形成可一键运行的分析流程。

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

# 或者手动读取10x数据
# pbmc.data <- Read10X(data.dir = "./filtered_gene_bc_matrices/hg19/")
# pbmc <- CreateSeuratObject(
#   counts = pbmc.data,
#   project = "pbmc3k",
#   min.cells = 3,
#   min.features = 200
# )

# 查看基本信息
print(pbmc)
dim(pbmc)
head(pbmc@meta.data)
```

### 第三部分：质量控制

```r
# ============================================
# 2. 计算QC指标
# ============================================
pbmc[["percent.mt"]] <- PercentageFeatureSet(pbmc, pattern = "^MT-")

summary(pbmc$nCount_RNA)
summary(pbmc$nFeature_RNA)
summary(pbmc$percent.mt)

# ============================================
# 3. QC可视化
# ============================================
VlnPlot(pbmc,
  features = c("nFeature_RNA", "nCount_RNA", "percent.mt"),
  ncol = 3, pt.size = 0.01
)

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

top10 <- head(VariableFeatures(pbmc), 10)
cat("Top 10 HVGs:", paste(top10, collapse = ", "), "\n")

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

print(pbmc[["pca"]], dims = 1:5, nfeatures = 5)

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

table(Idents(pbmc))
head(Idents(pbmc), 5)

# ============================================
# 11. UMAP 降维
# ============================================
pbmc <- RunUMAP(pbmc, dims = 1:10)

DimPlot(pbmc, reduction = "umap", label = TRUE, pt.size = 0.5) + NoLegend()
```

### 第七部分：差异表达与注释

```r
# ============================================
# 12. 寻找Marker基因
# ============================================
pbmc.markers <- FindAllMarkers(pbmc,
  only.pos = TRUE,
  test.use = "wilcox",
  min.pct = 0.25,
  logfc.threshold = 0.25
)

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

### ⚠️ 运行注意事项

- **数据下载**：首次运行 `InstallData("pbmc3k")` 需要网络连接
- **内存需求**：至少 8GB 内存（PBMC3k 是小数据集）
- **运行时间**：整个流程约 5-10 分钟
- **阈值调整**：QC 阈值和 resolution 需要根据你的数据调整
- **更多数据**：大数据集建议用 SCTransform 替代 LogNormalize

---

# 📎 附录

## A. 分析流程速览图

```
原始数据 → CreateSeuratObject → QC过滤 → NormalizeData → FindVariableFeatures
    → ScaleData → RunPCA → ElbowPlot选PC → FindNeighbors → FindClusters
    → RunUMAP → FindAllMarkers → RenameIdents → 完成！
```

## B. 关键参数速查

| 步骤 | 函数 | 关键参数 | 推荐值 |
|------|------|----------|--------|
| 创建对象 | `CreateSeuratObject` | `min.cells`, `min.features` | 3, 200 |
| QC过滤 | `subset` | `nFeature_RNA`, `percent.mt` | 200-2500, <5 |
| 归一化 | `NormalizeData` | `scale.factor` | 10000 |
| 高变基因 | `FindVariableFeatures` | `nfeatures` | 2000 |
| 缩放 | `ScaleData` | `vars.to.regress` | percent.mt |
| PCA | `RunPCA` | `npcs` | 50 |
| 选PC | `ElbowPlot` | — | 10-20 |
| 聚类 | `FindClusters` | `resolution` | 0.4-0.8 |
| 差异表达 | `FindAllMarkers` | `min.pct`, `logfc.threshold` | 0.25, 0.25 |

## C. 物种线粒体基因前缀

| 物种 | 前缀 | 示例 |
|------|------|------|
| 人类 | `"^MT-"` | MT-CO1, MT-ND1 |
| 小鼠 | `"^mt-"` | mt-Co1, mt-Nd1 |
| 大鼠 | `"^mt-"` | mt-Co1 |
| 斑马鱼 | `"^mt-"` | mt-co1 |
| 果蝇 | `"^mt:"` | mt:Co1 |

## D. PBMC常见细胞类型Marker

| 细胞类型 | Marker基因 |
|----------|-----------|
| Naive CD4 T | IL7R, CCR7 |
| Memory CD4 T | IL7R, S100A4 |
| CD8 T | CD8A, CD8B |
| NK | GNLY, NKG7, KLRD1 |
| B cells | MS4A1, CD79A, CD79B |
| CD14+ Mono | CD14, LYZ |
| FCGR3A+ Mono | FCGR3A, MS4A7 |
| Dendritic | FCER1A, HLA-DQA1 |
| Platelet | PPBP, PF4 |

---

> 📌 **使用建议**：本文档为 Obsidian 优化格式，支持 `[[]]` 双链跳转和标签检索。建议配合 Obsidian 的大纲视图和搜索功能快速定位所需模块。