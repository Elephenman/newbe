---
tags:
  - Seurat
  - 单细胞
  - RNA-seq
  - 实战代码
  - 一键运行
aliases:
  - Seurat代码库
  - 单细胞代码速查
  - Seurat实战宝典
created: 2026-04-20
updated: 2026-04-20
version: Seurat v5
description: 生物信息学实战级代码库，封装函数+一键脚本，改参数即跑
---

# 🧬 Seurat 单细胞实战代码库

> **定位**：复制→改参数→直接跑。所有核心流程封装为函数，自动化 QC 阈值、批量出图、一键完成。
> 基于 **Seurat v5**，新增 Sketch/BPCells 大数据支持、IntegrateLayers 统一整合、SCTransform v2。

---

## 📑 快速导航

| 需求 | 跳转 |
|------|------|
| 一键完整分析流程 | [[#🚀 一键全流程脚本]] |
| 环境安装 | [[#📦 环境安装一键脚本]] |
| 数据导入 | [[#📂 数据导入封装]] |
| 自动QC | [[#🔬 自动化质量控制]] |
| 标准处理 | [[#⚙️ 标准预处理流水线]] |
| SCTransform | [[#⚡ SCTransform v2 一键流程]] |
| 聚类调参 | [[#🎯 聚类与分辨率优化]] |
| 差异分析 | [[#📊 差异表达与Marker分析]] |
| 细胞注释 | [[#🏷️ 细胞类型注释]] |
| 多样本整合 | [[#🔗 多样本整合]] |
| 空间转录组 | [[#🧫 空间转录组]] |
| WNN多模态 | [[#🔀 WNN多模态分析]] |
| 大数据Sketch | [[#💾 百万级Sketch分析]] |
| 批量出图 | [[#🎨 批量可视化出图]] |
| 数据导出 | [[#💾 数据导出与保存]] |
| 速查表 | [[#📋 函数速查表]] |

---

## 📦 环境安装一键脚本

> 📖 **这段代码是干什么的？**
> 在跑任何单细胞分析之前，你需要先安装所有依赖的R包。这段代码会**自动检测你是否已经装了每个包**，装了就跳过，没装才安装。不用担心重复安装的问题。
>
> 🤔 **为什么这么写？**
> - `install_if_missing` 这个自定义函数用了 `requireNamespace()` 来检测包是否存在，这比直接调用 `installed.packages()` 更快更安全
> - 分两批安装：CRAN包（普通R包）和 Bioconductor包（生信专用包），因为安装命令不一样
> - `bioc = TRUE` 时走 `BiocManager::install()`，这是Bioconductor官方推荐的安装方式
> - Windows系统 `memory.limit(size = 9999...)` 是为了突破默认内存限制，单细胞数据很吃内存

```r
# ============================================================
# Seurat v5 全环境安装（复制即跑）
# ============================================================
install_if_missing <- function(packages, bioconductor = FALSE) {
  for (pkg in packages) {
    if (!requireNamespace(pkg, quietly = TRUE)) {
      cat("安装:", pkg, "\n")
      if (bioconductor) {
        BiocManager::install(pkg, ask = FALSE, update = FALSE)
      } else {
        install.packages(pkg)
      }
    } else {
      cat("✅", pkg, as.character(packageVersion(pkg)), "\n")
    }
  }
}

# CRAN 包
install_if_missing(c(
  "Seurat", "remotes", "patchwork", "ggrepel", "ggplot2",
  "dplyr", "tidyr", "Matrix", "cowplot", "clustree",
  "RColorBrewer", "viridis", "ggsci", "harmony",
  "DoubletFinder", "BPCells"
))

# Bioconductor 包
if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
install_if_missing(c(
  "SeuratData", "SeuratObject", "Signac",
  "SingleR", "celldex", "SingleCellExperiment",
  "clusterProfiler", "org.Hs.eg.db", "org.Mm.eg.db",
  "enrichplot", "scRNAseq", "scater"
), bioconductor = TRUE)

# 验证
cat("\n===== 环境检查 =====\n")
cat("Seurat:", as.character(packageVersion("Seurat")), "\n")
cat("SeuratObject:", as.character(packageVersion("SeuratObject")), "\n")
cat("R版本:", R.version.string, "\n")

# Windows 内存
if (.Platform$OS.type == "windows") memory.limit(size = 9999999999999)
```

> ✅ **怎么用？**
> 1. 直接复制全部代码到R控制台，回车运行
> 2. 第一次运行会自动下载安装，可能需要5-30分钟
> 3. 之后再运行只会显示 ✅ 已安装，不会重复安装

---

## 📂 数据导入封装

> 📖 **这段代码是干什么的？**
> 单细胞数据有好几种格式（10X Genomics的文件夹、h5文件、CSV等），这个封装函数帮你**一个接口搞定所有格式**。你只需要改 `source` 参数告诉它你的数据类型，其他参数有默认值。
>
> 🤔 **为什么这么写？**
> - `source` 参数做了分支控制，不同格式走不同的读取函数：
>   - `"10x"` → `Read10X()` 读取CellRanger输出的三文件（barcodes.tsv, features.tsv, matrix.mtx）
>   - `"h5"` → `Read10X_h5()` 读取压缩的HDF5格式，更省空间
>   - `"csv"` → `read.csv()` 然后 `as.sparse()` 转为**稀疏矩阵**——这个很关键！单细胞数据99%都是0，用稀疏矩阵能节省10倍以上内存
> - `min.cells = 3` 和 `min.features = 200` 是过滤参数：只保留至少在3个细胞里表达的基因，只保留至少表达200个基因的细胞——这是国际通用的初步过滤标准

```r
# ============================================================
# 通用数据导入函数 — 支持10x/h5/CSV/mtx/SeuratData
# ============================================================
load_sc_data <- function(
    source,              # "10x" / "h5" / "csv" / "pbmc3k" / "ifnb" / "bm"
    data.dir = NULL,     # 10x 目录路径
    filename = NULL,     # h5/csv 文件路径
    project = "scRNA",   # 项目名
    min.cells = 3,       # 最少表达细胞数
    min.features = 200,  # 最少表达基因数
    gene.column = 2,     # 基因名列：1=Ensembl ID, 2=基因符号
    species = "human"    # "human" / "mouse"
) {
  library(Seurat)
  
  if (source == "10x") {
    counts <- Read10X(data.dir = data.dir, gene.column = gene.column)
    obj <- CreateSeuratObject(counts, project = project,
                              min.cells = min.cells, min.features = min.features)
  } else if (source == "h5") {
    counts <- Read10X_h5(filename = filename)
    obj <- CreateSeuratObject(counts, project = project,
                              min.cells = min.cells, min.features = min.features)
  } else if (source == "csv") {
    counts <- read.csv(filename, row.names = 1)
    counts <- as.sparse(as.matrix(counts))  # 转稀疏矩阵省内存
    obj <- CreateSeuratObject(counts, project = project,
                              min.cells = min.cells, min.features = min.features)
  } else if (source == "pbmc3k") {
    library(SeuratData)
    InstallData("pbmc3k"); data("pbmc3k")
    obj <- pbmc3k
  } else if (source == "ifnb") {
    library(SeuratData)
    InstallData("ifnb"); data("ifnb")
    obj <- ifnb
  } else if (source == "bm") {
    library(SeuratData)
    InstallData("bm"); data("bm")
    obj <- bm
  } else {
    stop("不支持的source类型，可选: 10x/h5/csv/pbmc3k/ifnb/bm")
  }
  
  cat("✅ 数据加载完成:", dim(obj)[1], "基因,", dim(obj)[2], "细胞\n")
  return(obj)
}

# ============================================================
# 批量加载多样本 + 自动合并
# ============================================================
load_multi_samples <- function(
    sample_dirs,         # 命名向量: c(SampleA="path/A", SampleB="path/B")
    min.cells = 3,
    min.features = 200
) {
  obj_list <- list()
  for (nm in names(sample_dirs)) {
    cat("加载样本:", nm, "→", sample_dirs[nm], "\n")
    counts <- Read10X(data.dir = sample_dirs[nm])
    obj_list[[nm]] <- CreateSeuratObject(
      counts, project = nm,
      min.cells = min.cells, min.features = min.features
    )
  }
  # 合并
  combined <- merge(
    obj_list[[1]], y = obj_list[-1],
    add.cell.ids = names(sample_dirs),
    project = "merged"
  )
  cat("✅ 合并完成:", dim(combined)[2], "细胞\n")
  table(combined$orig.ident)  # 各样本细胞数
  return(combined)
}

# ========== 使用示例 ==========
# obj <- load_sc_data("10x", data.dir = "./data/filtered_feature_bc_matrix/")
# obj <- load_sc_data("h5", filename = "./data/pbmc.h5")
# obj <- load_sc_data("csv", filename = "./data/expr.csv")
# obj <- load_sc_data("pbmc3k")  ← 初学者推荐，直接用内置数据集练习
#
# 多样本：
# samples <- c(Ctrl="./data/ctrl/", Treat="./data/treat/")
# combined <- load_multi_samples(samples)
```

> ✅ **怎么用？**
> - **初学者最推荐**：`obj <- load_sc_data("pbmc3k")` 直接下载经典的PBMC3k数据集练手
> - 自己的10x数据：把 `data.dir` 改成你的 `filtered_feature_bc_matrix` 文件夹路径
> - 多样本分析：用 `load_multi_samples()` 一次性加载多个样本并自动合并

---

## 🔬 自动化质量控制

> 📖 **这段代码是干什么的？**
> QC（质量控制）是单细胞分析最重要的步骤之一，目的是**过滤掉死细胞、双细胞、低质量细胞**。这个函数帮你自动计算QC指标、自动设定过滤阈值、自动出图、自动过滤——全套一键搞定。
>
> 🤔 **为什么要做QC？需要看哪几个指标？**
> - **nFeature_RNA**（每个细胞检测到的基因数）：太低（<200）说明细胞死亡或空液滴；太高（>6000）可能是双细胞（两个细胞粘在一起）
> - **nCount_RNA**（每个细胞的总UMI数）：和基因数类似，太高太低都有问题
> - **percent.mt**（线粒体基因比例）：细胞死亡时线粒体基因相对增多，通常 >20-25% 表示死细胞
> - **percent.rb**（核糖体基因比例）：辅助指标，看细胞状态
>
> 🤔 **为什么用MAD法自动设阈值？**
> - 传统方法是凭经验手动设（如 nFeature < 200 过滤），但不同数据集差异很大
> - MAD（中位绝对偏差）是稳健的统计方法，比均值±3SD更不容易受极端值影响
> - `median ± mad_multiplier * MAD` 能自动适应不同数据集的分布

```r
# ============================================================
# 自动化QC — 自动计算指标 + 智能阈值 + 出图 + 过滤
# ============================================================
auto_qc <- function(
    obj,
    species = "human",         # "human" / "mouse"
    mt_pattern = NULL,         # 自定义线粒体前缀，覆盖默认
    rb_pattern = "^RP[SL]",   # 核糖体基因前缀
    calculate_rb = TRUE,       # 是否计算核糖体基因比例
    nFeature_lower = NULL,     # 手动设下限（NULL则自动）
    nFeature_upper = NULL,     # 手动设上限
    nCount_upper = NULL,       # UMI数上限
    mt_upper = NULL,           # 线粒体比例上限
    auto_threshold = TRUE,     # 自动计算阈值（MAD法）
    mad_multiplier = 3,        # MAD倍数
    plot = TRUE,               # 是否出图
    filter = TRUE,             # 是否执行过滤
    output_dir = "./qc_output/" # 图片输出目录
) {
  library(Seurat); library(ggplot2); library(patchwork)
  
  # 自动确定线粒体前缀
  if (is.null(mt_pattern)) {
    mt_pattern <- switch(species,
                         human = "^MT-", mouse = "^mt-",
                         rat = "^mt-", "^MT-")
  }
  
  # 1. 计算 QC 指标
  obj[["percent.mt"]] <- PercentageFeatureSet(obj, pattern = mt_pattern)
  if (calculate_rb) {
    obj[["percent.rb"]] <- PercentageFeatureSet(obj, pattern = rb_pattern)
  }
  
  # 2. 自动阈值（基于 MAD）
  if (auto_threshold) {
    qc_stats <- summary(obj$nFeature_RNA)
    med <- median(obj$nFeature_RNA)
    mad_val <- mad(obj$nFeature_RNA)
    
    if (is.null(nFeature_lower)) nFeature_lower <- max(200, med - mad_multiplier * mad_val)
    if (is.null(nFeature_upper)) nFeature_upper <- med + mad_multiplier * mad_val
    if (is.null(mt_upper)) {
      mt_med <- median(obj$percent.mt)
      mt_mad <- mad(obj$percent.mt)
      mt_upper <- min(mt_med + mad_multiplier * mt_mad, 20)  # 上限20%
    }
    if (is.null(nCount_upper)) {
      cnt_med <- median(obj$nCount_RNA)
      cnt_mad <- mad(obj$nCount_RNA)
      nCount_upper <- cnt_med + mad_multiplier * cnt_mad
    }
    
    cat("📊 自动QC阈值:\n")
    cat(sprintf("  nFeature_RNA: %.0f ~ %.0f\n", nFeature_lower, nFeature_upper))
    cat(sprintf("  nCount_RNA: < %.0f\n", nCount_upper))
    cat(sprintf("  percent.mt: < %.1f%%\n", mt_upper))
  }
  
  # 3. 出图
  if (plot) {
    if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)
    
    feats <- if (calculate_rb) c("nFeature_RNA", "nCount_RNA", "percent.mt", "percent.rb")
             else c("nFeature_RNA", "nCount_RNA", "percent.mt")
    
    # 小提琴图
    p1 <- VlnPlot(obj, features = feats, ncol = length(feats), pt.size = 0)
    ggsave(file.path(output_dir, "01_violin_qc.png"), p1, width = 4*length(feats), height = 5, dpi = 300)
    
    # 散点图
    p2 <- FeatureScatter(obj, feature1 = "nCount_RNA", feature2 = "percent.mt")
    p3 <- FeatureScatter(obj, feature1 = "nCount_RNA", feature2 = "nFeature_RNA")
    ggsave(file.path(output_dir, "02_scatter_qc.png"), p2 + p3, width = 12, height = 5, dpi = 300)
    
    cat("📁 QC图已保存至:", output_dir, "\n")
  }
  
  # 4. 过滤
  if (filter) {
    n_before <- ncol(obj)
    obj <- subset(obj, subset = nFeature_RNA >= nFeature_lower &
                            nFeature_RNA <= nFeature_upper &
                            percent.mt <= mt_upper)
    if (!is.null(nCount_upper)) {
      obj <- subset(obj, subset = nCount_RNA <= nCount_upper)
    }
    n_after <- ncol(obj)
    cat(sprintf("🔄 过滤: %d → %d 细胞 (去除 %.1f%%)\n",
                n_before, n_after, (1 - n_after/n_before)*100))
  }
  
  return(obj)
}

# ============================================================
# Doublet 检测（简化版）
# ============================================================
detect_doublets <- function(obj, pN = 0.25, nExp = NULL, PCs = 1:10) {
  if (!requireNamespace("DoubletFinder", quietly = TRUE)) {
    cat("⚠️ 需安装 DoubletFinder: install.packages('DoubletFinder')\n")
    return(obj)
  }
  library(DoubletFinder)
  
  # 自动估计 doublet 数量
  if (is.null(nExp)) {
    homotypic.prop <- modelHomotypic(obj$seurat_clusters)
    nExp_poi <- round(0.075 * ncol(obj))  # 7.5% doublet rate
    nExp <- round(nExp_poi * (1 - homotypic.prop))
  }
  
  obj <- doubletFinder_v3(obj, PCs = PCs, pN = pN, pK = 0.005, nExp = nExp)
  # 标记 doublet
  df_col <- grep("DF.classifications", colnames(obj@meta.data), value = TRUE)
  obj$doublet <- obj@meta.data[[df_col]] == "Doublet"
  cat("🔍 检测到", sum(obj$doublet), "个 doublets\n")
  return(obj)
}

# ========== 使用示例 ==========
# obj <- auto_qc(obj, species = "human")                 ← 推荐：全自动
# obj <- auto_qc(obj, species = "mouse", mt_upper = 10)  ← 小鼠数据
# obj <- auto_qc(obj, auto_threshold = FALSE,            ← 手动设阈值
#                nFeature_lower = 200, nFeature_upper = 6000, mt_upper = 15)
# obj <- detect_doublets(obj)                            ← 检测双细胞（可选）
```

> ✅ **怎么用？**
> 1. 先跑 `auto_qc(obj)` 看看自动生成的QC图（在 `./qc_output/` 文件夹里）
> 2. 看图后觉得阈值不合适，可以手动指定：`auto_qc(obj, nFeature_upper = 5000, mt_upper = 10)`
> 3. 过滤后细胞减少量通常在5-30%之间是正常的

---

## ⚙️ 标准预处理流水线

> 📖 **这段代码是干什么的？**
> QC之后，原始的计数数据（整数，不同样本之间不可比较）需要经过**归一化→找高变基因→缩放→降维（PCA）**这4步处理，才能进行后续的聚类分析。
>
> 🤔 **每步在干什么？为什么这么写？**
> - **NormalizeData（归一化）**：把每个细胞的计数除以细胞的总计数×10000，再取log，这样不同测序深度的细胞就可比较了。`scale.factor = 10000` 是国际惯例，叫做 "library size normalization"
> - **FindVariableFeatures（找高变基因）**：只选那些在细胞间变化最大的2000个基因，因为这些基因携带了区分细胞类型的主要信息。用所有基因（约20000个）做后续分析太慢且引入噪音
> - **ScaleData（缩放）**：把每个基因的表达值标准化为均值0、方差1，消除基因间表达量绝对值差异的影响（不然PCA会被高表达基因主导）
> - **RunPCA（主成分分析）**：把2000个高变基因的信息压缩到50个主成分，大幅降低维度，同时保留主要的生物学变异信息
>
> 🤔 **什么时候用 SCT 代替 LogNormalize？**
> - SCTransform 是更新的方法，能更好地处理技术噪音，特别适合细胞间测序深度差异很大时
> - 简单项目用 LogNormalize 就够，数据质量要求高时用 SCT

```r
# ============================================================
# 标准预处理：NormalizeData + FindVariableFeatures + ScaleData + PCA
# ============================================================
standard_preprocess <- function(
    obj,
    norm.method = "LogNormalize",  # "LogNormalize" / "SCT"
    scale.factor = 10000,
    nfeatures = 2000,              # 高变基因数
    npcs = 50,                     # PCA主成分数
    vars.to.regress = NULL,        # 回归变量: c("percent.mt", "nCount_RNA")
    scale_all = FALSE,             # 是否缩放全部基因（热图需要）
    verbose = TRUE
) {
  library(Seurat)
  
  if (norm.method == "LogNormalize") {
    if (verbose) cat("🔹 LogNormalize...\n")
    obj <- NormalizeData(obj, normalization.method = "LogNormalize",
                         scale.factor = scale.factor)
    
    if (verbose) cat("🔹 FindVariableFeatures (n=", nfeatures, ")...\n", sep = "")
    obj <- FindVariableFeatures(obj, selection.method = "vst", nfeatures = nfeatures)
    
    if (verbose) cat("🔹 ScaleData...\n")
    features_to_scale <- if (scale_all) rownames(obj) else VariableFeatures(obj)
    obj <- ScaleData(obj, features = features_to_scale,
                     vars.to.regress = vars.to.regress)
    
    if (verbose) cat("🔹 RunPCA (npcs=", npcs, ")...\n", sep = "")
    obj <- RunPCA(obj, npcs = npcs, verbose = FALSE)
    
  } else if (norm.method == "SCT") {
    # SCTransform 一步完成
    if (verbose) cat("🔹 SCTransform v2 (一步完成归一化+HVG+缩放)...\n")
    obj <- SCTransform(obj, vst.flavor = "v2",
                       vars.to.regress = vars.to.regress,
                       verbose = FALSE)
    if (verbose) cat("🔹 RunPCA (npcs=", npcs, ")...\n", sep = "")
    obj <- RunPCA(obj, npcs = npcs, verbose = FALSE)
  }
  
  if (verbose) cat("✅ 预处理完成\n")
  return(obj)
}

# ============================================================
# 自动选择PC数量（ElbowPlot + 近似法）
# ============================================================
auto_select_pcs <- function(
    obj,
    method = "elbow",       # "elbow" / "jackstraw" / "fixed"
    fixed_pcs = NULL,       # method="fixed" 时指定
    elbow_cutoff = 0.1,     # 标准差下降比例阈值
    max_pcs = 30,           # 最大PC数
    plot = TRUE
) {
  if (method == "fixed" && !is.null(fixed_pcs)) {
    cat("📌 使用固定PC数:", fixed_pcs, "\n")
    return(fixed_pcs)
  }
  
  if (method == "jackstraw") {
    cat("⏳ JackStraw 检验（较慢）...\n")
    obj <- JackStraw(obj, num.replicate = 100, dims = max_pcs)
    obj <- ScoreJackStraw(obj, dims = 1:max_pcs)
    if (plot) JackStrawPlot(obj, dims = 1:max_pcs)
    # 找最后一个显著PC
    js_scores <- obj[["jackstraw"]]$overall.p.values
    sig_pcs <- js_scores[js_scores[, 2] < 0.05, 1]
    n_pcs <- min(max(sig_pcs), max_pcs)
    cat("📌 JackStraw推荐PC数:", n_pcs, "\n")
    return(n_pcs)
  }
  
  # ElbowPlot 近似法
  if (method == "elbow") {
    stdevs <- Stdev(obj, reduction = "pca")
    stdevs <- stdevs[1:min(length(stdevs), max_pcs)]
    # 计算差分
    diffs <- diff(stdevs)
    # 找到差分小于阈值的位置
    cutoff <- max(stdevs) * elbow_cutoff
    n_pcs <- which(stdevs < cutoff)[1]
    if (is.na(n_pcs)) n_pcs <- max_pcs
    n_pcs <- max(n_pcs, 10)  # 至少10个
    cat("📌 ElbowPlot推荐PC数:", n_pcs, "\n")
    if (plot) {
      print(ElbowPlot(obj, ndims = max_pcs) +
              geom_hline(yintercept = cutoff, color = "red", linetype = "dashed"))
    }
    return(n_pcs)
  }
}

# ========== 使用示例 ==========
# obj <- standard_preprocess(obj)                              ← 标准流程
# obj <- standard_preprocess(obj, vars.to.regress = c("percent.mt"))  ← 回归线粒体效应
# obj <- standard_preprocess(obj, norm.method = "SCT")        ← SCTransform流程
# n_pcs <- auto_select_pcs(obj, method = "elbow")             ← 自动选PC数
# n_pcs <- auto_select_pcs(obj, method = "fixed", fixed_pcs = 15)  ← 手动指定15个PC
```

> ✅ **怎么用？**
> 1. 先跑 `obj <- standard_preprocess(obj)` 完成预处理
> 2. 再跑 `n_pcs <- auto_select_pcs(obj)` 看 ElbowPlot，找"拐点"在哪个PC
> 3. 一般用 10-20 个PC做后续分析，看拐点在哪就用哪里的值

---

## ⚡ SCTransform v2 一键流程

> 📖 **这段代码是干什么的？**
> SCTransform 是比 LogNormalize 更先进的归一化方法，能**一步完成归一化+高变基因+缩放**，不需要分步骤。v2版本（`vst.flavor = "v2"`）精度更高。
>
> 🤔 **为什么要用 SCTransform？它跟 LogNormalize 的区别？**
> - LogNormalize 假设每个细胞里表达的总RNA量相同（除以library size来校正），但这个假设其实不总成立
> - SCTransform 用的是负二项回归模型，能更准确地建模技术噪音和生物学变异，特别是当细胞间测序深度差异很大时效果更好
> - `vars.to.regress = "percent.mt"` 是为了去掉线粒体基因比例对结果的影响（这是一种技术噪音来源）
> - 注意：SCTransform 后不需要再跑 `NormalizeData` 和 `ScaleData`

```r
# ============================================================
# SCTransform v2 完整流程（归一化+HVG+缩放+PCA一步到位）
# ============================================================
sctransform_pipeline <- function(
    obj,
    vars.to.regress = "percent.mt",
    npcs = 50,
    verbose = TRUE
) {
  library(Seurat)
  
  if (verbose) cat("⚡ SCTransform v2...\n")
  obj <- SCTransform(obj, vst.flavor = "v2",
                     vars.to.regress = vars.to.regress,
                     verbose = FALSE)
  
  if (verbose) cat("⚡ RunPCA...\n")
  obj <- RunPCA(obj, npcs = npcs, verbose = FALSE)
  
  if (verbose) {
    cat("✅ SCTransform流程完成\n")
    cat("  HVG数量:", length(VariableFeatures(obj)), "\n")
  }
  return(obj)
}

# ============================================================
# 对比 LogNormalize vs SCTransform
# ============================================================
compare_norm_methods <- function(obj) {
  library(Seurat); library(patchwork)
  
  # LogNormalize 路线
  obj1 <- NormalizeData(obj)
  obj1 <- FindVariableFeatures(obj1, nfeatures = 2000)
  obj1 <- ScaleData(obj1)
  obj1 <- RunPCA(obj1, verbose = FALSE)
  obj1 <- RunUMAP(obj1, dims = 1:15, reduction.name = "ln_umap")
  
  # SCTransform 路线
  obj2 <- SCTransform(obj, vst.flavor = "v2", verbose = FALSE)
  obj2 <- RunPCA(obj2, verbose = FALSE)
  obj2 <- RunUMAP(obj2, dims = 1:15, reduction.name = "sct_umap")
  
  p1 <- DimPlot(obj1, reduction = "ln_umap") + ggtitle("LogNormalize")
  p2 <- DimPlot(obj2, reduction = "sct_umap") + ggtitle("SCTransform v2")
  print(p1 + p2)
  cat("✅ 对比完成\n")
  return(list(lognorm = obj1, sctransform = obj2))
}
```

> ✅ **怎么用？**
> - 直接用：`obj <- sctransform_pipeline(obj)`
> - 如果你想比较两种方法效果：`results <- compare_norm_methods(obj)` 会并排显示UMAP图

---

## 🎯 聚类与分辨率优化

> 📖 **这段代码是干什么的？**
> 这是单细胞分析的核心步骤：把细胞**按照基因表达相似性分成若干个簇（cluster）**。每个cluster可能代表一种细胞类型。
>
> 🤔 **聚类流程：3步走**
> 1. **FindNeighbors**：先构建细胞间的"邻居关系图"，相似的细胞互为邻居（用KNN算法）
> 2. **FindClusters**：在邻居图上寻找密集的社区（用Louvain或Leiden算法）
> 3. **RunUMAP**：把高维数据压缩到2D用于可视化（UMAP不改变聚类结果，只是让你能画图）
>
> 🤔 **为什么要扫多个分辨率（resolutions）？**
> - `resolution` 参数控制聚类粒度：越大 → cluster越多（分得越细），越小 → cluster越少（分得越粗）
> - 没有唯一正确的分辨率，需要根据你对组织的了解来选
> - 先跑多个分辨率，再用 Clustree 图看哪个分辨率最稳定
>
> 🤔 **为什么用 algorithm = 4（Leiden）？**
> - Louvain (algorithm=1) 是传统方法，但会产生不连通的cluster
> - Leiden (algorithm=4) 是2019年提出的改进版，cluster质量更好，是现在的推荐标准

```r
# ============================================================
# 聚类 + UMAP + 自动分辨率扫描
# ============================================================
auto_cluster <- function(
    obj,
    dims = 1:15,                     # PC维度
    resolutions = c(0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5),
    algorithm = 4,                   # 4=Leiden(推荐), 1=Louvain
    k.param = 20,
    run_umap = TRUE,
    run_tsne = FALSE,
    plot_clustree = TRUE,
    output_dir = "./cluster_output/"
) {
  library(Seurat); library(patchwork)
  if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)
  
  # 构建邻居图
  obj <- FindNeighbors(obj, dims = dims, k.param = k.param)
  
  # 多分辨率聚类
  obj <- FindClusters(obj, resolution = resolutions,
                      algorithm = algorithm, random.seed = 42)
  
  # UMAP
  if (run_umap) {
    obj <- RunUMAP(obj, dims = dims, verbose = FALSE)
  }
  
  # t-SNE
  if (run_tsne) {
    obj <- RunTSNE(obj, dims = dims, verbose = FALSE)
  }
  
  # Clustree 图
  if (plot_clustree && requireNamespace("clustree", quietly = TRUE)) {
    library(clustree)
    p_clustree <- clustree(obj, "RNA_snn_res.")
    ggsave(file.path(output_dir, "clustree.png"), p_clustree,
           width = 10, height = 8, dpi = 300)
    cat("📁 Clustree图已保存\n")
  }
  
  # 汇总各分辨率cluster数
  res_cols <- grep("RNA_snn_res", colnames(obj@meta.data), value = TRUE)
  cat("\n📊 各分辨率cluster数:\n")
  for (rc in res_cols) {
    cat(sprintf("  %s → %d clusters\n", rc, length(unique(obj@meta.data[[rc]]))))
  }
  
  return(obj)
}

# ============================================================
# 选择最佳分辨率并可视化
# ============================================================
visualize_clusters <- function(
    obj,
    resolution = 0.5,
    reduction = "umap",
    output_dir = "./cluster_output/"
) {
  library(Seurat); library(patchwork)
  if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)
  
  # 设定 active identity
  res_col <- paste0("RNA_snn_res.", resolution)
  if (res_col %in% colnames(obj@meta.data)) {
    Idents(obj) <- res_col
  }
  
  # 按cluster
  p1 <- DimPlot(obj, reduction = reduction, label = TRUE, pt.size = 0.5) + NoLegend() +
    ggtitle(paste0("Clusters (res=", resolution, ")"))
  
  # 按样本（检查批次效应）
  p2 <- DimPlot(obj, reduction = reduction, group.by = "orig.ident") +
    ggtitle("By Sample")
  
  # 各cluster细胞数
  p3 <- ggplot(data.frame(cluster = Idents(obj)), aes(cluster)) +
    geom_bar(fill = "steelblue") + theme_minimal() +
    ggtitle("Cells per Cluster") + xlab("Cluster") + ylab("Count")
  
  ggsave(file.path(output_dir, "umap_clusters.png"),
         p1 / (p2 | p3), width = 14, height = 10, dpi = 300)
  cat("📁 聚类图已保存\n")
  return(list(umap_cluster = p1, umap_sample = p2, barplot = p3))
}

# ========== 使用示例 ==========
# obj <- auto_cluster(obj, dims = 1:15, resolutions = c(0.2, 0.4, 0.6, 0.8, 1.0))
# plots <- visualize_clusters(obj, resolution = 0.5)  ← 选择你认为合适的分辨率
```

> ✅ **怎么用？**
> 1. `obj <- auto_cluster(obj, dims = 1:15)` — 先跑，会自动扫多个分辨率
> 2. 查看 `cluster_output/clustree.png` — Clustree图帮你选合适分辨率（看哪里分叉最稳定）
> 3. `plots <- visualize_clusters(obj, resolution = 0.5)` — 选定分辨率后可视化

---

## 📊 差异表达与Marker分析

> 📖 **这段代码是干什么的？**
> 聚完类之后，你需要知道**每个cluster有哪些特征基因（marker基因）**，才能判断它是什么细胞类型。差异表达分析就是找出在某个cluster里显著高表达（区别于其他cluster）的基因。
>
> 🤔 **为什么这么写？**
> - `FindAllMarkers()` 是Seurat内置函数，一次性找所有cluster的marker基因
> - `only.pos = TRUE` 只找上调基因，因为你想要的是"这个cluster特有的基因"，而不是下调基因
> - `min.pct = 0.25` 要求基因至少在25%的细胞里表达，过滤掉只在极少数细胞里表达的噪音基因
> - `logfc.threshold = 0.25` 要求至少有0.25的log2FC差异，过滤掉差异太小的基因
> - 最后用 `p_val_adj < 0.05` 和 `avg_log2FC > 1` 筛选显著marker，这是国际通用标准
>
> 🤔 **`pairwise_de` 和 `auto_marker_analysis` 的区别？**
> - `auto_marker_analysis`：每个cluster vs 所有其他细胞（找marker基因，用于细胞注释）
> - `pairwise_de`：指定A组 vs B组（用于两种条件或两种细胞类型的比较，出火山图）

```r
# ============================================================
# 一键差异表达分析（FindAllMarkers + 筛选 + 可视化）
# ============================================================
auto_marker_analysis <- function(
    obj,
    ident = NULL,             # 指定group列，NULL用active identity
    test.use = "wilcox",     # "wilcox" / "MAST" / "DESeq2"
    only.pos = TRUE,
    min.pct = 0.25,
    logfc.threshold = 0.25,
    top_n = 10,              # 每个cluster取top N
    fc_cutoff = 1,           # log2FC筛选阈值
    output_dir = "./marker_output/"
) {
  library(Seurat); library(dplyr); library(ggplot2)
  if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)
  
  if (!is.null(ident)) Idents(obj) <- ident
  
  # FindAllMarkers
  cat("🔍 FindAllMarkers (test=", test.use, ")...\n", sep = "")
  all_markers <- FindAllMarkers(
    obj, only.pos = only.pos, test.use = test.use,
    min.pct = min.pct, logfc.threshold = logfc.threshold
  )
  
  # 筛选显著marker
  sig_markers <- all_markers %>%
    filter(avg_log2FC > fc_cutoff & p_val_adj < 0.05)
  
  # Top N
  top_markers <- sig_markers %>%
    group_by(cluster) %>%
    slice_max(order_by = avg_log2FC, n = top_n) %>%
    ungroup()
  
  # 保存
  write.csv(all_markers, file.path(output_dir, "all_markers.csv"), row.names = FALSE)
  write.csv(sig_markers, file.path(output_dir, "significant_markers.csv"), row.names = FALSE)
  write.csv(top_markers, file.path(output_dir, "top_markers.csv"), row.names = FALSE)
  
  cat("📊 结果:\n")
  cat("  总marker数:", nrow(all_markers), "\n")
  cat("  显著marker数:", nrow(sig_markers), "\n")
  cat("  Top markers:", nrow(top_markers), "\n")
  
  return(list(all = all_markers, significant = sig_markers, top = top_markers))
}

# ============================================================
# 两组差异分析（FindMarkers封装）+ 火山图
# ============================================================
pairwise_de <- function(
    obj,
    ident.1,
    ident.2,
    ident.col = NULL,       # 指定meta.data列
    test.use = "wilcox",
    only.pos = FALSE,
    min.pct = 0.1,
    logfc.threshold = 0.25,
    fc_cutoff = 0.5,
    padj_cutoff = 0.05,
    plot_volcano = TRUE,
    output_dir = "./de_output/"
) {
  library(Seurat); library(dplyr); library(ggplot2); library(ggrepel)
  if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)
  
  if (!is.null(ident.col)) Idents(obj) <- ident.col
  
  cat("🔍", ident.1, "vs", ident.2, "\n")
  de_res <- FindMarkers(obj, ident.1 = ident.1, ident.2 = ident.2,
                        test.use = test.use, only.pos = only.pos,
                        min.pct = min.pct, logfc.threshold = logfc.threshold)
  de_res$gene <- rownames(de_res)
  de_res$significant <- with(de_res, p_val_adj < padj_cutoff & abs(avg_log2FC) > fc_cutoff)
  de_res$label <- ifelse(de_res$significant & abs(de_res$avg_log2FC) >= 1, de_res$gene, "")
  
  # 保存
  write.csv(de_res, file.path(output_dir,
             paste0(ident.1, "_vs_", ident.2, ".csv")), row.names = FALSE)
  
  # 火山图
  if (plot_volcano) {
    p <- ggplot(de_res, aes(x = avg_log2FC, y = -log10(p_val_adj),
                            color = significant, label = label)) +
      geom_point(size = 0.8, alpha = 0.6) +
      geom_text_repel(size = 2.5, max.overlaps = 20, color = "black") +
      scale_color_manual(values = c("grey", "red")) +
      geom_vline(xintercept = c(-fc_cutoff, fc_cutoff), linetype = "dashed", alpha = 0.5) +
      geom_hline(yintercept = -log10(padj_cutoff), linetype = "dashed", alpha = 0.5) +
      theme_bw() +
      labs(title = paste(ident.1, "vs", ident.2),
           x = "avg log2FC", y = "-log10(adj p-value)")
    ggsave(file.path(output_dir,
             paste0(ident.1, "_vs_", ident.2, "_volcano.png")),
           p, width = 8, height = 6, dpi = 300)
    print(p)
  }
  
  n_up <- sum(de_res$significant & de_res$avg_log2FC > 0)
  n_down <- sum(de_res$significant & de_res$avg_log2FC < 0)
  cat("📊 上调:", n_up, "下调:", n_down, "\n")
  
  return(de_res)
}

# ========== 使用示例 ==========
# markers <- auto_marker_analysis(obj)                        ← 找所有cluster的marker
# de_res <- pairwise_de(obj, "CD14+ Mono", "FCGR3A+ Mono")   ← 两种细胞类型比较
# de_res <- pairwise_de(obj, 0, 5, test.use = "MAST")        ← cluster 0 vs cluster 5
```

---

## 🏷️ 细胞类型注释

> 📖 **这段代码是干什么的？**
> 聚类完成后，cluster只是"0、1、2、3..."这样的数字，没有生物学意义。注释就是给每个cluster打上细胞类型的标签，比如"CD4 T细胞"、"B细胞"、"单核细胞"等。有**手动注释**（你自己查文献确认）和**自动注释**（SingleR程序自动匹配）两种方式。
>
> 🤔 **手动注释 vs SingleR 哪个更好？**
> - **手动注释**：你根据每个cluster的marker基因（对照已知的细胞marker数据库如CellMarker）来判断。准确但费时，需要生物学知识
> - **SingleR自动注释**：用机器学习跟参考数据集比对，快但可能不准确，适合做初步筛选
> - **推荐做法**：先用SingleR快速看一下大概，再结合marker基因手动确认
>
> 🤔 **`check_markers` 函数里为什么内置了好多基因？**
> - 这是常见细胞类型的已知marker基因，来自文献和数据库
> - 比如 `MS4A1, CD79A` 是B细胞的经典marker，`CD14, LYZ` 是单核细胞marker
> - 有了这个预设库，初学者不用自己查文献，直接传入 `tissue = "pbmc"` 就能看到所有常见免疫细胞的marker表达

```r
# ============================================================
# 手动注释封装
# ============================================================
manual_annotate <- function(
    obj,
    cluster_to_celltype,   # 命名向量: c("0"="Naive CD4 T", "1"="B cell", ...)
    save_col = "celltype"  # 存入meta.data的列名
) {
  names(cluster_to_celltype) <- as.character(names(cluster_to_celltype))
  # 检查是否所有cluster都有映射
  current_ids <- as.character(levels(Idents(obj)))
  missing <- setdiff(current_ids, names(cluster_to_celltype))
  if (length(missing) > 0) {
    cat("⚠️ 以下cluster未注释:", paste(missing, collapse = ", "), "\n")
  }
  
  obj <- RenameIdents(obj, cluster_to_celltype)
  obj[[save_col]] <- Idents(obj)
  
  cat("✅ 注释完成\n")
  print(table(obj[[save_col]]))
  return(obj)
}

# ============================================================
# SingleR 自动注释
# ============================================================
autor_annotate_SingleR <- function(
    obj,
    ref = NULL,              # 参考数据集，NULL自动选
    ref_type = "human",      # "human" / "mouse"
    label.level = "main",    # "main" / "fine"
    save_col = "SingleR_label"
) {
  if (!requireNamespace("SingleR", quietly = TRUE)) {
    stop("请安装: BiocManager::install('SingleR')")
  }
  library(SingleR); library(celldex)
  
  # 自动选参考
  if (is.null(ref)) {
    cat("📥 下载参考数据集...\n")
    ref <- switch(ref_type,
                  human = HumanPrimaryCellAtlasData(),
                  mouse = ImmGenData(),
                  HumanPrimaryCellAtlasData())
  }
  
  test_data <- GetAssayData(obj, layer = "data")
  pred <- SingleR(test = test_data, ref = ref,
                  labels = if (label.level == "main") ref$label.main else ref$label.fine)
  
  obj[[save_col]] <- pred$labels
  
  # 输出结果
  cat("✅ SingleR注释完成\n")
  print(table(pred$labels))
  
  # 可视化
  if (requireNamespace("scater", quietly = TRUE)) {
    plotScoreHeatmap(pred)
  }
  
  return(obj)
}

# ============================================================
# 常用细胞类型 Marker 速查（一键出图）
# ============================================================
check_markers <- function(
    obj,
    markers = NULL,          # 基因向量
    tissue = "pbmc",         # "pbmc" / "tumor" / "brain" / "immune"
    plot_type = "all",       # "dot" / "feature" / "vln" / "heatmap" / "all"
    reduction = "umap",
    output_dir = "./annotation_output/"
) {
  library(Seurat); library(patchwork)
  if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)
  
  # 预设 Marker 集合
  marker_db <- list(
    pbmc = c(
      "IL7R", "CCR7",                     # Naive CD4 T
      "S100A4",                            # Memory CD4 T
      "CD8A", "CD8B",                      # CD8 T
      "GNLY", "NKG7",                      # NK
      "MS4A1", "CD79A",                    # B
      "CD14", "LYZ",                       # CD14+ Mono
      "FCGR3A", "MS4A7",                   # FCGR3A+ Mono
      "FCER1A", "CLEC10A",                # DC
      "PPBP", "PF4",                       # Platelet
      "FOXP3", "IL2RA",                    # Treg
      "PDCD1", "CTLA4",                    # Exhausted T
      "MKI67", "TOP2A"                     # Proliferating
    ),
    tumor = c(
      "EPCAM", "KRT8", "KRT18",           # 上皮/肿瘤
      "VIM", "ACTA2", "FAP",              # 间质/CAF
      "PECAM1", "VWF",                    # 内皮
      "CD3D", "CD8A", "CD4",              # T细胞
      "MS4A1", "CD79A",                   # B细胞
      "CD14", "CD68", "CD163",            # 髓系/巨噬
      "NCAM1", "NKG7",                    # NK
      "MKI67", "TOP2A"                    # 增殖
    ),
    brain = c(
      "RBFOX3", "SYT1",                   # 神经元
      "GFAP", "AQP4",                     # 星形胶质
      "OLIG2", "MBP", "PLP1",            # 少突胶质
      "AIF1", "CX3CR1",                   # 小胶质
      "CLDN5", "PECAM1",                  # 内皮
      "PDGFRA", "CSPG4"                   # OPC
    ),
    immune = c(
      "CD3D", "CD3E", "CD3G",             # T cell
      "CD4", "IL7R",                       # CD4 T
      "CD8A", "CD8B",                      # CD8 T
      "FOXP3", "IL2RA",                    # Treg
      "PDCD1", "CTLA4", "LAG3", "TIGIT", # Exhausted
      "MS4A1", "CD79A", "CD19",           # B cell
      "NCAM1", "NKG7", "GNLY",           # NK
      "CD14", "FCGR3A", "CD68",          # Mono/Macro
      "CD1C", "CLEC10A",                  # cDC
      "IL3RA", "LILRA4",                  # pDC
      "MZB1", "JCHAIN", "IGHG1",         # Plasma
      "MKI67"                             # Proliferating
    )
  )
  
  if (is.null(markers)) markers <- marker_db[[tissue]]
  # 过滤掉不存在的基因
  markers <- markers[markers %in% rownames(obj)]
  
  plots <- list()
  
  if (plot_type %in% c("dot", "all")) {
    p <- DotPlot(obj, features = markers) + RotatedAxis() +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))
    ggsave(file.path(output_dir, "dotplot_markers.png"), p, width = 12, height = 6, dpi = 300)
    plots$dot <- p
  }
  
  if (plot_type %in% c("feature", "all")) {
    p <- FeaturePlot(obj, features = markers, ncol = 4, min.cutoff = "q1", max.cutoff = "q99")
    ggsave(file.path(output_dir, "featureplot_markers.png"), p,
           width = 6 * min(4, ceiling(length(markers)/4)), height = 4 * ceiling(length(markers)/4), dpi = 200)
    plots$feature <- p
  }
  
  if (plot_type %in% c("vln", "all")) {
    p <- VlnPlot(obj, features = markers[1:min(12, length(markers))], ncol = 3, pt.size = 0)
    ggsave(file.path(output_dir, "vlnplot_markers.png"), p, width = 12, height = 8, dpi = 300)
    plots$vln <- p
  }
  
  cat("📁 Marker图已保存至:", output_dir, "\n")
  return(plots)
}

# ========== 使用示例 ==========
# obj <- manual_annotate(obj, c("0"="Naive CD4 T", "1"="B cell", "2"="CD14+ Mono"))
# obj <- autor_annotate_SingleR(obj)             ← 自动注释（需要联网下载参考数据）
# plots <- check_markers(obj, tissue = "pbmc")   ← PBMC数据一键出marker图
# plots <- check_markers(obj, tissue = "tumor")  ← 肿瘤数据
# plots <- check_markers(obj, markers = c("CD3D", "MS4A1", "CD14", "GNLY", "CD8A"))  ← 自定义marker
```

---

## 🔗 多样本整合

> 📖 **这段代码是干什么的？**
> 当你有多个样本（比如不同病人、不同处理条件）时，直接合并会产生**批次效应（batch effect）**——来自同一个实验批次的细胞会聚在一起，而不是按细胞类型聚在一起。整合的目的就是**去除这种技术批次差异，保留真实的生物学差异**。
>
> 🤔 **三种整合方法怎么选？**
> - **CCA（Canonical Correlation Analysis）**：Seurat经典方法，效果好但慢，样本数少时推荐
> - **RPCA（Reciprocal PCA）**：CCA的快速版，大数据集推荐
> - **Harmony**：独立的工具，速度最快，对大量样本效果很好，目前最流行
>
> 🤔 **Seurat v5 的整合变化**
> - v5 引入了 `IntegrateLayers()` 统一接口，替代了 v4 的 `FindIntegrationAnchors + IntegrateData` 两步
> - 新接口更简洁，参数更统一，推荐用新接口

```r
# ============================================================
# Seurat v5 多样本整合（IntegrateLayers封装）
# ============================================================
integrate_samples <- function(
    obj,
    split.by = "orig.ident",       # 按此列拆分样本
    method = "CCA",                # "CCA" / "RPCA" / "Harmony"
    norm.method = "LogNormalize",  # "LogNormalize" / "SCT"
    nfeatures = 2000,
    npcs = 30,
    dims = 1:30,
    resolution = 0.5,
    verbose = TRUE
) {
  library(Seurat)
  
  method_map <- list(
    CCA = CCAIntegration,
    RPCA = RPCAIntegration,
    Harmony = HarmonyIntegration
  )
  integration_fn <- method_map[[method]]
  if (is.null(integration_fn)) stop("method可选: CCA/RPCA/Harmony")
  
  # 拆分
  if (verbose) cat("🔹 拆分样本...\n")
  obj_list <- SplitObject(obj, split.by = split.by)
  
  # 预处理
  if (verbose) cat("🔹 各样本预处理...\n")
  if (norm.method == "SCT") {
    obj_list <- lapply(obj_list, function(x) {
      SCTransform(x, vst.flavor = "v2", verbose = FALSE)
    })
    features <- SelectIntegrationFeatures(object.list = obj_list, nfeatures = nfeatures)
    obj_list <- PrepSCTIntegration(object.list = obj_list, anchor.features = features)
  } else {
    obj_list <- lapply(obj_list, function(x) {
      x <- NormalizeData(x)
      x <- FindVariableFeatures(x, nfeatures = nfeatures)
    })
    features <- SelectIntegrationFeatures(object.list = obj_list)
  }
  
  # 合并
  if (verbose) cat("🔹 合并 + PCA...\n")
  merged <- merge(x = obj_list[[1]], y = obj_list[-1])
  merged <- ScaleData(merged, features = features)
  merged <- RunPCA(merged, features = features, npcs = npcs, verbose = FALSE)
  
  # 整合
  if (verbose) cat("🔹 IntegrateLayers (", method, ")...\n", sep = "")
  new_reduction <- paste0("integrated.", tolower(method))
  merged <- IntegrateLayers(
    merged,
    method = integration_fn,
    orig.reduction = "pca",
    new.reduction = new_reduction,
    verbose = FALSE
  )
  
  # 后续分析
  if (verbose) cat("🔹 UMAP + 聚类...\n")
  merged <- RunUMAP(merged, reduction = new_reduction, dims = dims, verbose = FALSE)
  merged <- FindNeighbors(merged, reduction = new_reduction, dims = dims)
  merged <- FindClusters(merged, resolution = resolution)
  
  if (verbose) cat("✅ 整合完成\n")
  return(merged)
}

# ============================================================
# Harmony 整合（独立封装，更灵活）
# ============================================================
harmony_integrate <- function(
    obj,
    group.by.vars = "orig.ident",   # 批次变量
    reduction = "pca",
    dims = 1:30,
    resolution = 0.5,
    plot = TRUE
) {
  if (!requireNamespace("harmony", quietly = TRUE)) {
    stop("请安装: install.packages('harmony')")
  }
  library(harmony); library(Seurat)
  
  obj <- RunHarmony(obj, group.by.vars = group.by.vars,
                    reduction = reduction, dims.use = dims)
  obj <- RunUMAP(obj, reduction = "harmony", dims = dims, verbose = FALSE)
  obj <- FindNeighbors(obj, reduction = "harmony", dims = dims)
  obj <- FindClusters(obj, resolution = resolution)
  
  if (plot) {
    library(patchwork)
    p1 <- DimPlot(obj, group.by = group.by.vars) + ggtitle("By Batch")
    p2 <- DimPlot(obj, label = TRUE) + ggtitle("By Cluster")
    print(p1 + p2)
  }
  return(obj)
}

# ============================================================
# 评估整合效果
# ============================================================
evaluate_integration <- function(
    obj,
    batch.col = "orig.ident",
    reduction = "umap"
) {
  library(Seurat); library(patchwork); library(ggplot2)
  
  p1 <- DimPlot(obj, reduction = reduction, group.by = batch.col) + ggtitle("By Batch")
  p2 <- DimPlot(obj, reduction = reduction, label = TRUE) + ggtitle("By Cluster")
  
  # 各cluster的批次分布
  batch_dist <- prop.table(table(obj$seurat_clusters, obj[[batch.col]][[1]]), 1)
  cat("📊 各Cluster批次分布:\n")
  print(round(batch_dist, 3))
  
  # 严重批次聚集检测
  for (i in 1:nrow(batch_dist)) {
    if (max(batch_dist[i, ]) > 0.9) {
      cat("⚠️ Cluster", rownames(batch_dist)[i],
          "批次严重聚集 (>90%):", colnames(batch_dist)[which.max(batch_dist[i,])], "\n")
    }
  }
  
  print(p1 + p2)
  return(batch_dist)
}

# ========== 使用示例 ==========
# obj <- integrate_samples(obj, method = "CCA")            ← CCA整合（样本少时推荐）
# obj <- integrate_samples(obj, method = "RPCA", norm.method = "SCT")  ← RPCA+SCT
# obj <- harmony_integrate(obj, group.by.vars = "batch")   ← Harmony整合（最快）
# evaluate_integration(obj)                                ← 评估整合效果
```

> ✅ **判断整合效果好不好？**
> - 整合好：UMAP图里来自不同样本的细胞混合在一起（按细胞类型聚），而不是分成孤立的团
> - 用 `evaluate_integration()` 看各cluster里不同批次的比例，理想情况下每个cluster里各批次都有分布

---

## 🧫 空间转录组

> 📖 **这段代码是干什么的？**
> 空间转录组技术（如10X Visium）能同时测量**基因表达量和细胞的空间位置**，让你知道不同基因在组织切片哪个部位表达。这比普通单细胞多了一个空间维度。
>
> 🤔 **为什么空间数据推荐用SCTransform？**
> - 空间数据的spots（检测点）之间测序深度差异比单细胞更大
> - SCTransform的负二项模型能更好地处理这种高变异数据

```r
# ============================================================
# 空间转录组一键分析
# ============================================================
spatial_pipeline <- function(
    data.dir = NULL,
    h5_file = "filtered_feature_bc_matrix.h5",
    assay = "Spatial",
    species = "human",
    npcs = 30,
    dims = 1:30,
    resolution = 0.5,
    features_to_plot = NULL,      # 空间表达可视化基因
    output_dir = "./spatial_output/"
) {
  library(Seurat); library(SeuratData); library(ggplot2)
  if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)
  
  # 加载数据
  if (!is.null(data.dir)) {
    obj <- Load10X_Spatial(data.dir = data.dir, filename = h5_file, assay = assay)
  } else {
    cat("📥 下载示例数据...\n")
    InstallData("stxBrain")
    obj <- LoadData("stxBrain", type = "anterior1")
  }
  
  # QC
  mt_pattern <- ifelse(species == "human", "^MT-", "^mt-")
  obj[["percent.mt"]] <- PercentageFeatureSet(obj, pattern = mt_pattern, assay = assay)
  
  # SCTransform（空间数据推荐）
  obj <- SCTransform(obj, assay = assay, vst.flavor = "v2", verbose = FALSE)
  
  # 降维聚类
  obj <- RunPCA(obj, verbose = FALSE)
  obj <- RunUMAP(obj, dims = 1:npcs, verbose = FALSE)
  obj <- FindNeighbors(obj, dims = 1:dims)
  obj <- FindClusters(obj, resolution = resolution)
  
  # 空间可视化
  p1 <- SpatialDimPlot(obj, label = TRUE, label.size = 3)
  ggsave(file.path(output_dir, "spatial_clusters.png"), p1, width = 10, height = 8, dpi = 300)
  
  # 基因空间表达
  if (!is.null(features_to_plot)) {
    features_to_plot <- features_to_plot[features_to_plot %in% rownames(obj)]
    p2 <- SpatialFeaturePlot(obj, features = features_to_plot)
    ggsave(file.path(output_dir, "spatial_features.png"), p2,
           width = 5 * length(features_to_plot), height = 5, dpi = 300)
  }
  
  cat("✅ 空间转录组分析完成\n")
  return(obj)
}

# ============================================================
# 空间数据 + 单细胞参考注释
# ============================================================
spatial_annotate <- function(
    spatial_obj,
    sc_ref,                   # 已注释的单细胞Seurat对象
    sc_celltype_col = "celltype",
    dims = 1:30
) {
  library(Seurat)
  
  anchors <- FindTransferAnchors(
    reference = sc_ref, query = spatial_obj,
    normalization.method = "SCT", dims = dims
  )
  predictions <- TransferData(
    anchorset = anchors,
    refdata = sc_ref[[sc_celltype_col]][[1]],
    weight.reduction = spatial_obj[["pca"]],
    dims = dims
  )
  spatial_obj <- AddMetaData(spatial_obj, metadata = predictions)
  
  # 可视化
  SpatialDimPlot(spatial_obj, group.by = "predicted.id", label = TRUE)
  
  cat("✅ 空间注释完成\n")
  return(spatial_obj)
}

# ========== 使用示例 ==========
# sp <- spatial_pipeline(data.dir = "./spatial/", features_to_plot = c("Hpca", "Ttr"))
# sp <- spatial_annotate(sp, sc_ref = pbmc_annotated)
```

---

## 🔀 WNN多模态分析

> 📖 **这段代码是干什么的？**
> WNN（Weighted Nearest Neighbor）是Seurat提供的**多模态数据整合**方法。当你的实验同时测量了多种数据类型时（比如CITE-seq同时测RNA和蛋白质，或Multiome同时测RNA和ATAC染色质可及性），WNN能把这两种信息整合起来，让聚类更准确。
>
> 🤔 **为什么ADT数据要用CLR归一化？**
> - ADT是蛋白质抗体数据，不像RNA那样稀疏，大部分基因不表达
> - CLR（Centered Log-Ratio）是专门针对成分数据设计的归一化方法，比普通log归一化更适合抗体数据
> - `margin = 2` 表示在细胞维度（列）上做归一化

```r
# ============================================================
# CITE-seq (RNA + ADT) WNN 分析
# ============================================================
wnn_citeseq <- function(
    obj,
    rna_assay = "RNA",
    adt_assay = "ADT",
    rna_dims = 1:30,
    adt_dims = 1:18,
    resolution = 0.8
) {
  library(Seurat)
  
  # RNA 处理
  DefaultAssay(obj) <- rna_assay
  obj <- NormalizeData(obj)
  obj <- FindVariableFeatures(obj)
  obj <- ScaleData(obj)
  obj <- RunPCA(obj, verbose = FALSE)
  
  # ADT 处理（必须用CLR）
  DefaultAssay(obj) <- adt_assay
  obj <- NormalizeData(obj, normalization.method = "CLR", margin = 2)
  obj <- ScaleData(obj)
  obj <- RunPCA(obj, reduction.name = "apca", verbose = FALSE)
  
  # WNN
  obj <- FindMultiModalNeighbors(
    obj,
    reduction.list = list("pca", "apca"),
    dims.list = list(rna_dims, adt_dims),
    modality.weight.name = c("RNA.weight", "ADT.weight")
  )
  
  obj <- RunUMAP(obj, nn.name = "weighted.nn", reduction.name = "wnn.umap", verbose = FALSE)
  obj <- FindClusters(obj, graph.name = "wsnn", algorithm = 3, resolution = resolution)
  
  # 对比单模态 vs WNN
  obj <- RunUMAP(obj, reduction = "pca", dims = rna_dims, reduction.name = "rna.umap", verbose = FALSE)
  obj <- RunUMAP(obj, reduction = "apca", dims = adt_dims, reduction.name = "adt.umap", verbose = FALSE)
  
  library(patchwork)
  p1 <- DimPlot(obj, reduction = "rna.umap", label = TRUE) + ggtitle("RNA Only")
  p2 <- DimPlot(obj, reduction = "adt.umap", label = TRUE) + ggtitle("ADT Only")
  p3 <- DimPlot(obj, reduction = "wnn.umap", label = TRUE) + ggtitle("WNN")
  print(p1 + p2 + p3)
  
  cat("✅ WNN分析完成\n")
  return(obj)
}

# ============================================================
# Multiome (RNA + ATAC) WNN 分析
# ============================================================
wnn_multiome <- function(
    obj,
    rna_dims = 1:30,
    atac_dims = 2:30,        # ATAC的LSI从第2维开始
    resolution = 0.8
) {
  library(Seurat); library(Signac)
  
  # RNA
  DefaultAssay(obj) <- "RNA"
  obj <- NormalizeData(obj)
  obj <- FindVariableFeatures(obj)
  obj <- ScaleData(obj)
  obj <- RunPCA(obj, verbose = FALSE)
  
  # ATAC
  DefaultAssay(obj) <- "ATAC"
  obj <- FindTopFeatures(obj, min.cutoff = "q0")
  obj <- RunSVD(obj, verbose = FALSE)  # LSI降维（ATAC专用，等价于PCA）
  
  # WNN
  obj <- FindMultiModalNeighbors(
    obj,
    reduction.list = list("pca", "lsi"),
    dims.list = list(rna_dims, atac_dims)
  )
  
  obj <- RunUMAP(obj, nn.name = "weighted.nn", reduction.name = "wnn.umap", verbose = FALSE)
  obj <- FindClusters(obj, graph.name = "wsnn", algorithm = 3, resolution = resolution)
  
  cat("✅ Multiome WNN完成\n")
  return(obj)
}

# ========== 使用示例 ==========
# obj <- wnn_citeseq(obj)    ← CITE-seq数据（RNA+蛋白）
# obj <- wnn_multiome(obj)   ← Multiome数据（RNA+ATAC）
```

> 🤔 **ATAC的LSI为什么从第2维开始（atac_dims = 2:30）？**
> - ATAC-seq数据的LSI第1个维度通常主要反映测序深度（技术噪音），不含生物学信息
> - 所以跳过第1维，从第2维开始使用，这是ATAC分析的标准做法

---

## 💾 百万级Sketch分析

> 📖 **这段代码是干什么的？**
> 当你的数据集有几十万甚至上百万个细胞时，直接加载到内存里根本放不下。**Sketch分析**是Seurat v5提供的解决方案：先智能抽样一小部分有代表性的细胞（比如5万个）做分析，然后把结果投影回全部细胞。
>
> 🤔 **为什么用BPCells？**
> - BPCells是一种"磁盘存储"格式，数据存在硬盘上，用到哪块加载哪块，不需要把所有数据加载到内存
> - 对于百万级细胞数据，这是唯一可行的方案
> - `as(obj[["RNA"]], "Assay5")` 这行把数据转换为BPCells格式

```r
# ============================================================
# Seurat v5 Sketch 分析（百万级细胞）
# ============================================================
sketch_analysis <- function(
    obj,
    n_sketch = 50000,          # 抽样细胞数
    npcs = 50,
    dims = 1:30,
    resolution = 0.5,
    method = "BPCells"         # "BPCells" / "regular"
) {
  library(Seurat)
  
  # BPCells on-disk 存储（大数据必须）
  if (method == "BPCells" && requireNamespace("BPCells", quietly = TRUE)) {
    library(BPCells)
    obj[["RNA"]] <- as(obj[["RNA"]], "Assay5")
    cat("✅ 已切换为BPCells on-disk模式\n")
  }
  
  # Sketch抽样（LeverScore是有代表性的智能抽样算法）
  cat("🔹 Sketch抽样 (n=", n_sketch, ")...\n", sep = "")
  obj <- SketchData(
    object = obj,
    ncells = n_sketch,
    method = "LeverScore",
    sketched.assay = "sketch"
  )
  
  # 在抽样数据上分析
  DefaultAssay(obj) <- "sketch"
  obj <- SCTransform(obj, vst.flavor = "v2", verbose = FALSE)
  obj <- RunPCA(obj, npcs = npcs, verbose = FALSE)
  obj <- RunUMAP(obj, dims = dims, verbose = FALSE)
  obj <- FindNeighbors(obj, dims = dims)
  obj <- FindClusters(obj, resolution = resolution)
  
  cat("✅ Sketch分析完成\n")
  return(obj)
}

# ============================================================
# 将Sketch结果投影回全量数据
# ============================================================
project_sketch_results <- function(
    obj,                   # Sketch分析后的对象
    full_obj               # 原始完整对象
) {
  library(Seurat)
  
  full_obj <- ProjectData(
    object = full_obj,
    assay = "RNA",
    full.assay = "RNA",
    sketched.assay = "sketch",
    reduction = "pca",
    dims = 1:30
  )
  
  cat("✅ 投影完成\n")
  return(full_obj)
}

# ========== 使用示例 ==========
# obj <- sketch_analysis(obj, n_sketch = 50000)
# full_obj <- project_sketch_results(obj, original_obj)
```

---

## 🧬 细胞周期评分与回归

> 📖 **这段代码是干什么的？**
> 细胞周期（G1期、S期、G2M期）会对基因表达产生很大影响。如果不处理，UMAP图上的细胞可能会因为细胞周期不同而分离，而不是因为细胞类型不同。这个函数帮你**评分细胞周期状态，并可选择去除其影响**。
>
> 🤔 **三种action有什么区别？**
> - `"score_only"`：只给每个细胞打分，不去除影响（如果你想研究细胞周期就用这个）
> - `"score_and_regress"`：完全去除S期和G2M期的影响，增殖细胞会和静止细胞聚在一起
> - `"regress_difference"`：去除细胞周期的效果，但**保留增殖细胞和非增殖细胞的区分**（更推荐）

```r
# ============================================================
# 细胞周期一键处理
# ============================================================
handle_cell_cycle <- function(
    obj,
    species = "human",          # "human" / "mouse"
    action = "score_and_regress", # "score_only" / "score_and_regress" / "regress_difference"
    s_genes = NULL,
    g2m_genes = NULL
) {
  library(Seurat)
  
  # 基因集（Seurat内置人类细胞周期基因）
  if (is.null(s_genes)) {
    s_genes <- cc.genes$s.genes
    g2m_genes <- cc.genes$g2m.genes
    if (species == "mouse") {
      # 转换为小鼠命名（首字母大写，其余小写）
      s_genes <- paste0(toupper(substr(tolower(s_genes), 1, 1)),
                        substr(tolower(s_genes), 2, nchar(s_genes)))
      g2m_genes <- paste0(toupper(substr(tolower(g2m_genes), 1, 1)),
                          substr(tolower(g2m_genes), 2, nchar(g2m_genes)))
    }
  }
  
  # 评分
  obj <- CellCycleScoring(obj, s.features = s_genes,
                          g2m.features = g2m_genes, set.ident = TRUE)
  cat("📊 细胞周期分布:\n")
  print(table(obj$Phase))
  
  # 回归
  if (action == "score_and_regress") {
    obj <- ScaleData(obj, vars.to.regress = c("S.Score", "G2M.Score"),
                     features = rownames(obj))
    cat("✅ 已回归S.Score + G2M.Score\n")
  } else if (action == "regress_difference") {
    obj$CC.Difference <- obj$S.Score - obj$G2M.Score
    obj <- ScaleData(obj, vars.to.regress = "CC.Difference",
                     features = rownames(obj))
    cat("✅ 已回归CC.Difference（保留增殖信号）\n")
  } else {
    cat("✅ 仅评分，未回归\n")
  }
  
  return(obj)
}
```

> ✅ **怎么用？**
> - 先跑 `obj <- handle_cell_cycle(obj, action = "score_only")` 看看数据里细胞周期分布
> - 如果G2M期细胞很多并影响聚类，再改成 `action = "regress_difference"` 去除影响

---

## 🎨 批量可视化出图

> 📖 **这段代码是干什么的？**
> 分析完成后，你需要出一套标准的图来展示结果。`batch_plot()` 帮你**一键生成所有标准图**（UMAP按cluster、按样本、QC小提琴图、DotPlot、FeaturePlot、热图等），全部自动保存到文件夹。`pretty_umap()` 是专门用于**发文章的高质量UMAP图**。
>
> 🤔 **为什么要封装成函数而不是逐个画图？**
> - 单细胞分析通常需要出几十张图，手写太麻烦
> - 封装成函数后，参数改一下就能批量重出所有图
> - `dpi = 300` 是期刊发表的标准分辨率要求

```r
# ============================================================
# 一键批量出图（分析完成后调用，自动保存所有标准图）
# ============================================================
batch_plot <- function(
    obj,
    markers = NULL,            # 基因向量
    tissue = "pbmc",           # 预设marker集
    celltype_col = "celltype", # 注释列名
    reduction = "umap",
    output_dir = "./figures/",
    dpi = 300,
    width_per_panel = 5
) {
  library(Seurat); library(patchwork); library(ggplot2)
  if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)
  
  # 默认marker
  if (is.null(markers)) {
    marker_db <- list(
      pbmc = c("IL7R","CCR7","S100A4","CD8A","MS4A1","CD79A",
               "CD14","LYZ","FCGR3A","GNLY","NKG7","FCER1A","PPBP"),
      tumor = c("EPCAM","VIM","ACTA2","PECAM1","CD3D","CD8A",
                "MS4A1","CD14","CD68","NKG7","MKI67","FOXP3"),
      brain = c("RBFOX3","GFAP","OLIG2","AIF1","CLDN5","PDGFRA","MBP"),
      immune = c("CD3D","CD4","CD8A","FOXP3","PDCD1","MS4A1",
                 "CD79A","NKG7","GNLY","CD14","FCGR3A","IL3RA","MKI67")
    )
    markers <- marker_db[[tissue]]
  }
  markers <- markers[markers %in% rownames(obj)]
  
  # 1. UMAP — 按cluster
  p1 <- DimPlot(obj, reduction = reduction, label = TRUE, pt.size = 0.3) + NoLegend()
  ggsave(file.path(output_dir, "01_umap_cluster.png"), p1, width = 8, height = 6, dpi = dpi)
  
  # 2. UMAP — 按celltype
  if (celltype_col %in% colnames(obj@meta.data)) {
    p2 <- DimPlot(obj, reduction = reduction, group.by = celltype_col,
                  label = TRUE, pt.size = 0.3) + NoLegend()
    ggsave(file.path(output_dir, "02_umap_celltype.png"), p2, width = 10, height = 6, dpi = dpi)
  }
  
  # 3. UMAP — 按样本
  if ("orig.ident" %in% colnames(obj@meta.data)) {
    p3 <- DimPlot(obj, reduction = reduction, group.by = "orig.ident")
    ggsave(file.path(output_dir, "03_umap_sample.png"), p3, width = 8, height = 6, dpi = dpi)
  }
  
  # 4. QC 小提琴图
  qc_feats <- intersect(c("nFeature_RNA", "nCount_RNA", "percent.mt"), colnames(obj@meta.data))
  if (length(qc_feats) > 0) {
    p4 <- VlnPlot(obj, features = qc_feats, ncol = length(qc_feats), pt.size = 0)
    ggsave(file.path(output_dir, "04_vln_qc.png"), p4,
           width = 4 * length(qc_feats), height = 5, dpi = dpi)
  }
  
  # 5. DotPlot
  p5 <- DotPlot(obj, features = markers) + RotatedAxis() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 8))
  ggsave(file.path(output_dir, "05_dotplot_markers.png"), p5, width = 12, height = 6, dpi = dpi)
  
  # 6. FeaturePlot
  n_col <- min(4, length(markers))
  p6 <- FeaturePlot(obj, features = markers, ncol = n_col, min.cutoff = "q1", max.cutoff = "q99")
  ggsave(file.path(output_dir, "06_featureplot_markers.png"), p6,
         width = width_per_panel * n_col,
         height = width_per_panel * ceiling(length(markers) / n_col),
         dpi = min(dpi, 200))
  
  # 7. Top marker热图
  if ("RNA_snn_res.0.5" %in% colnames(obj@meta.data)) {
    top10 <- FindAllMarkers(obj, only.pos = TRUE, min.pct = 0.25, logfc.threshold = 0.25) %>%
      group_by(cluster) %>% filter(avg_log2FC > 1) %>% slice_head(n = 10) %>% ungroup()
    p7 <- DoHeatmap(obj, features = top10$gene, size = 3) + NoLegend()
    ggsave(file.path(output_dir, "07_heatmap_top_markers.png"), p7, width = 14, height = 8, dpi = dpi)
  }
  
  # 8. 细胞周期（如果有）
  if ("Phase" %in% colnames(obj@meta.data)) {
    p8 <- DimPlot(obj, reduction = reduction, group.by = "Phase")
    ggsave(file.path(output_dir, "08_umap_cellcycle.png"), p8, width = 8, height = 6, dpi = dpi)
  }
  
  cat("📁 所有图片已保存至:", output_dir, "\n")
}

# ============================================================
# 自定义配色 UMAP（发文章用）
# ============================================================
pretty_umap <- function(
    obj,
    group.by = NULL,
    reduction = "umap",
    palette = "default",       # "default" / "nature" / "npg" / "lancet" / "igv"
    label = TRUE,
    title = "",
    font_size = 14,
    pt.size = 0.3,
    legend_ncol = NULL
) {
  library(Seurat); library(ggplot2)
  
  if (!is.null(group.by)) {
    p <- DimPlot(obj, reduction = reduction, group.by = group.by,
                 label = label, pt.size = pt.size)
  } else {
    p <- DimPlot(obj, reduction = reduction, label = label, pt.size = pt.size)
  }
  
  # 配色（ggsci提供各大期刊风格的配色方案）
  if (palette != "default" && requireNamespace("ggsci", quietly = TRUE)) {
    scale_fn <- switch(palette,
                       nature = ggsci::scale_color_npg(),
                       npg = ggsci::scale_color_npg(),       # Nature出版社配色
                       lancet = ggsci::scale_color_lancet(),  # Lancet配色
                       igv = ggsci::scale_color_igv(),        # IGV配色（颜色多）
                       jco = ggsci::scale_color_jco())
    if (!is.null(scale_fn)) p <- p + scale_fn
  }
  
  p <- p + theme_bw() +
    theme(plot.title = element_text(size = font_size, face = "bold"),
          axis.title = element_text(size = font_size),
          legend.text = element_text(size = font_size - 2),
          axis.text = element_text(size = font_size - 4)) +
    labs(title = title, x = paste0(toupper(reduction), " 1"), y = paste0(toupper(reduction), " 2"))
  
  if (!is.null(legend_ncol)) {
    p <- p + guides(color = guide_legend(ncol = legend_ncol, override.aes = list(size = 4)))
  }
  
  return(p)
}

# ========== 使用示例 ==========
# batch_plot(obj, tissue = "pbmc", output_dir = "./results/figures/")  ← 一键出所有标准图
# batch_plot(obj, markers = c("CD3D", "MS4A1", "CD14"), output_dir = "./figs/")
# p <- pretty_umap(obj, group.by = "celltype", palette = "npg", title = "PBMC3k")
# ggsave("umap_npg.png", p, width = 10, height = 7, dpi = 300)
```

---

## 💾 数据导出与保存

> 📖 **这段代码是干什么的？**
> 分析结束后需要保存各种结果，包括Seurat对象本身（方便以后继续分析）、元数据、UMAP坐标、cluster统计等。
>
> 🤔 **为什么要保存RDS格式而不是CSV？**
> - Seurat对象包含所有数据（表达矩阵、降维结果、聚类信息等），只有RDS格式能完整保存这个复杂的R对象
> - CSV只适合保存表格数据（比如元数据、marker列表）
> - 下次分析直接 `readRDS()` 加载，不需要重新跑所有流程

```r
# ============================================================
# 一键保存所有结果
# ============================================================
save_all_results <- function(
    obj,
    output_dir = "./results/",
    prefix = "scRNA"
) {
  if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)
  
  # 1. Seurat 对象（最重要！）
  saveRDS(obj, file.path(output_dir, paste0(prefix, "_seurat.rds")))
  cat("✅ Seurat对象已保存\n")
  
  # 2. 元数据（细胞信息：cluster、celltype、QC指标等）
  write.csv(obj@meta.data, file.path(output_dir, paste0(prefix, "_metadata.csv")))
  
  # 3. UMAP坐标（用于外部软件绘图）
  if ("umap" %in% names(obj@reductions)) {
    umap_df <- as.data.frame(Embeddings(obj, "umap"))
    umap_df$cell <- rownames(umap_df)
    write.csv(umap_df, file.path(output_dir, paste0(prefix, "_umap.csv")), row.names = FALSE)
  }
  
  # 4. 各cluster细胞数
  cluster_counts <- as.data.frame.table(table(Idents(obj)))
  colnames(cluster_counts) <- c("Cluster", "Count")
  write.csv(cluster_counts, file.path(output_dir, paste0(prefix, "_cluster_counts.csv")), row.names = FALSE)
  
  # 5. 高变基因
  write.csv(data.frame(Gene = VariableFeatures(obj)),
            file.path(output_dir, paste0(prefix, "_hvg.csv")), row.names = FALSE)
  
  # 6. PC 贡献率
  if ("pca" %in% names(obj@reductions)) {
    pc_var <- as.data.frame(Stdev(obj, "pca")^2 / sum(Stdev(obj, "pca")^2) * 100)
    colnames(pc_var) <- "Variance_Percent"
    pc_var$PC <- 1:nrow(pc_var)
    write.csv(pc_var, file.path(output_dir, paste0(prefix, "_pc_variance.csv")), row.names = FALSE)
  }
  
  cat("📁 所有结果已保存至:", output_dir, "\n")
}

# ============================================================
# 加载已保存的 Seurat 对象
# ============================================================
load_results <- function(path) {
  obj <- readRDS(path)
  cat("✅ 已加载:", path, "\n")
  cat("  基因数:", dim(obj)[1], "细胞数:", dim(obj)[2], "\n")
  cat("  降维:", paste(names(obj@reductions), collapse = ", "), "\n")
  cat("  meta.data列:", paste(colnames(obj@meta.data), collapse = ", "), "\n")
  return(obj)
}
```

---

## 🚀 一键全流程脚本

> 📖 **这段代码是干什么的？**
> 这是整个代码库的"终极Boss"——把上面所有步骤整合成一个函数，**只要调一行代码，从原始数据到出图全自动完成**。7个步骤：导入→QC→预处理→选PC→聚类→差异分析→注释。
>
> 🤔 **为什么最后才放这个？**
> - 因为它调用了上面定义的所有函数，所以必须先运行上面的代码定义好这些函数
> - **初学者建议**：先用 `run_full_pipeline("pbmc3k")` 跑一遍完整流程理解每步在干什么，再去调每个单独的函数
>
> 🤔 **参数怎么设？**
> - 最简单：`run_full_pipeline("pbmc3k")` 全用默认参数
> - 实际数据：改 `data_source`, `data.dir`, `species`, `output_dir`
> - 精调：根据QC结果调整 `nFeature_lower/upper`, `mt_upper`；根据Clustree图调整 `resolution`

```r
# ============================================================
# 🔥 一键全流程 — 复制改参数即跑
# ============================================================
run_full_pipeline <- function(
    # ===== 数据参数 =====
    data_source = "pbmc3k",     # "10x" / "h5" / "csv" / "pbmc3k" / "ifnb"
    data.dir = NULL,
    filename = NULL,
    species = "human",
    project_name = "scRNA",
    
    # ===== QC 参数 =====
    nFeature_lower = NULL,      # NULL自动
    nFeature_upper = NULL,
    mt_upper = NULL,
    auto_qc_threshold = TRUE,
    
    # ===== 预处理参数 =====
    norm.method = "LogNormalize", # "LogNormalize" / "SCT"
    nfeatures = 2000,
    npcs = 50,
    vars.to.regress = "percent.mt",
    
    # ===== 聚类参数 =====
    dims = 1:15,
    resolution = 0.5,
    algorithm = 4,              # 4=Leiden
    
    # ===== 注释参数 =====
    annotate = FALSE,
    cluster_to_celltype = NULL, # 手动注释映射
    
    # ===== 整合参数 =====
    integrate = FALSE,
    integration_method = "CCA", # "CCA" / "RPCA" / "Harmony"
    split.by = "orig.ident",
    
    # ===== 输出参数 =====
    output_dir = "./scRNA_results/",
    tissue = "pbmc",
    plot_dpi = 300
) {
  library(Seurat); library(dplyr); library(patchwork); library(ggplot2)
  
  cat("🧬 ========== 单细胞分析全流程 ==========\n")
  start_time <- Sys.time()
  
  # 1. 数据导入
  cat("\n📂 [1/7] 数据导入...\n")
  obj <- load_sc_data(data_source, data.dir = data.dir,
                      filename = filename, project = project_name, species = species)
  
  # 2. QC
  cat("\n🔬 [2/7] 质量控制...\n")
  obj <- auto_qc(obj, species = species,
                 nFeature_lower = nFeature_lower,
                 nFeature_upper = nFeature_upper,
                 mt_upper = mt_upper,
                 auto_threshold = auto_qc_threshold,
                 output_dir = file.path(output_dir, "qc/"))
  
  # 3. 预处理
  cat("\n⚙️ [3/7] 预处理...\n")
  obj <- standard_preprocess(obj, norm.method = norm.method,
                             nfeatures = nfeatures, npcs = npcs,
                             vars.to.regress = vars.to.regress)
  
  # 4. 选择PC
  cat("\n📊 [4/7] 选择PC数量...\n")
  n_pcs <- auto_select_pcs(obj, method = "elbow", max_pcs = npcs, plot = TRUE)
  dims_use <- 1:n_pcs
  
  # 5. 聚类
  cat("\n🎯 [5/7] 聚类...\n")
  obj <- auto_cluster(obj, dims = dims_use,
                      resolutions = c(0.2, 0.4, 0.6, resolution, 1.0, 1.2),
                      algorithm = algorithm,
                      output_dir = file.path(output_dir, "cluster/"))
  Idents(obj) <- paste0("RNA_snn_res.", resolution)
  
  # 6. 差异表达
  cat("\n📊 [6/7] 差异表达...\n")
  markers <- auto_marker_analysis(obj, output_dir = file.path(output_dir, "markers/"))
  obj@misc$markers <- markers
  
  # 7. 注释
  if (annotate && !is.null(cluster_to_celltype)) {
    cat("\n🏷️ [7/7] 细胞注释...\n")
    obj <- manual_annotate(obj, cluster_to_celltype)
  } else if (annotate) {
    cat("\n🏷️ [7/7] SingleR自动注释...\n")
    obj <- autor_annotate_SingleR(obj)
  } else {
    cat("\n⏭️ [7/7] 跳过注释\n")
  }
  
  # 整合（可选）
  if (integrate) {
    cat("\n🔗 整合样本...\n")
    obj <- integrate_samples(obj, split.by = split.by, method = integration_method)
  }
  
  # 批量出图
  cat("\n🎨 批量出图...\n")
  batch_plot(obj, tissue = tissue, output_dir = file.path(output_dir, "figures/"), dpi = plot_dpi)
  
  # 保存
  save_all_results(obj, output_dir = output_dir, prefix = project_name)
  
  # 汇总
  elapsed <- round(difftime(Sys.time(), start_time, units = "mins"), 1)
  cat("\n✅ ========== 分析完成 ==========\n")
  cat("  细胞数:", ncol(obj), "\n")
  cat("  基因数:", nrow(obj), "\n")
  cat("  Cluster数:", length(unique(Idents(obj))), "\n")
  cat("  耗时:", elapsed, "分钟\n")
  cat("  输出目录:", output_dir, "\n")
  
  return(obj)
}

# ========== 使用示例 ==========
# 最简单：PBMC3k一键跑完（初学者强烈推荐！）
# obj <- run_full_pipeline(data_source = "pbmc3k")
#
# 自定义10x数据：
# obj <- run_full_pipeline(
#   data_source = "10x",
#   data.dir = "./data/filtered_feature_bc_matrix/",
#   species = "human",
#   norm.method = "SCT",
#   resolution = 0.6,
#   annotate = TRUE,
#   cluster_to_celltype = c("0"="CD4 T", "1"="B cell", "2"="Mono"),
#   output_dir = "./my_analysis/"
# )
#
# 小鼠数据：
# obj <- run_full_pipeline(
#   data_source = "10x",
#   data.dir = "./mouse_data/",
#   species = "mouse",
#   mt_upper = 10,
#   tissue = "immune",
#   output_dir = "./mouse_analysis/"
# )
#
# 多样本整合：
# obj <- run_full_pipeline(
#   data_source = "ifnb",
#   integrate = TRUE,
#   integration_method = "Harmony",
#   split.by = "orig.ident"
# )
```

---

## 📋 函数速查表

### 核心封装函数

| 函数 | 用途 | 一行调用 |
|------|------|----------|
| `load_sc_data()` | 数据导入 | `load_sc_data("10x", data.dir="./data/")` |
| `load_multi_samples()` | 多样本加载 | `load_multi_samples(c(A="path/A", B="path/B"))` |
| `auto_qc()` | 自动QC+过滤 | `auto_qc(obj, species="human")` |
| `detect_doublets()` | Doublet检测 | `detect_doublets(obj)` |
| `standard_preprocess()` | 标准预处理 | `standard_preprocess(obj)` |
| `sctransform_pipeline()` | SCT流程 | `sctransform_pipeline(obj)` |
| `auto_select_pcs()` | 自动选PC | `auto_select_pcs(obj)` |
| `auto_cluster()` | 聚类+多分辨率 | `auto_cluster(obj, dims=1:15)` |
| `visualize_clusters()` | 聚类可视化 | `visualize_clusters(obj, res=0.5)` |
| `auto_marker_analysis()` | Marker分析 | `auto_marker_analysis(obj)` |
| `pairwise_de()` | 两组差异 | `pairwise_de(obj, "A", "B")` |
| `manual_annotate()` | 手动注释 | `manual_annotate(obj, c("0"="T"))` |
| `autor_annotate_SingleR()` | SingleR注释 | `autor_annotate_SingleR(obj)` |
| `check_markers()` | Marker可视化 | `check_markers(obj, tissue="pbmc")` |
| `integrate_samples()` | 多样本整合 | `integrate_samples(obj, method="CCA")` |
| `harmony_integrate()` | Harmony整合 | `harmony_integrate(obj)` |
| `evaluate_integration()` | 评估整合 | `evaluate_integration(obj)` |
| `spatial_pipeline()` | 空间转录组 | `spatial_pipeline(data.dir="./sp/")` |
| `spatial_annotate()` | 空间注释 | `spatial_annotate(sp, sc_ref)` |
| `wnn_citeseq()` | CITE-seq WNN | `wnn_citeseq(obj)` |
| `wnn_multiome()` | Multiome WNN | `wnn_multiome(obj)` |
| `sketch_analysis()` | 百万级分析 | `sketch_analysis(obj, n=50000)` |
| `handle_cell_cycle()` | 细胞周期 | `handle_cell_cycle(obj)` |
| `batch_plot()` | 批量出图 | `batch_plot(obj, tissue="pbmc")` |
| `pretty_umap()` | 发文级UMAP | `pretty_umap(obj, palette="npg")` |
| `save_all_results()` | 保存所有结果 | `save_all_results(obj)` |
| `run_full_pipeline()` | 一键全流程 | `run_full_pipeline("pbmc3k")` |

### Seurat v5 原生函数速查

```
# 数据
Read10X(data.dir) | Read10X_h5(filename) | CreateSeuratObject(counts)
merge(obj1, y=obj2, add.cell.ids)

# QC
PercentageFeatureSet(obj, pattern) | subset(obj, subset=...)

# 预处理
NormalizeData(obj) | SCTransform(obj, vst.flavor="v2")
FindVariableFeatures(obj, nfeatures=2000) | ScaleData(obj, vars.to.regress)

# 降维
RunPCA(obj, npcs) | RunUMAP(obj, dims) | RunTSNE(obj, dims)
ElbowPlot(obj) | DimHeatmap(obj, dims)

# 聚类
FindNeighbors(obj, dims) | FindClusters(obj, resolution)
Idents(obj) | RenameIdents(obj, new.ids)

# 差异
FindAllMarkers(obj, only.pos, test.use, min.pct)
FindMarkers(obj, ident.1, ident.2)

# 可视化
DimPlot() | FeaturePlot() | VlnPlot() | DotPlot() | DoHeatmap()

# 整合 v5
IntegrateLayers(obj, method, orig.reduction, new.reduction)
  method: CCAIntegration | RPCAIntegration | HarmonyIntegration
RunHarmony(obj, group.by.vars)

# WNN
FindMultiModalNeighbors(obj, reduction.list, dims.list)

# 空间
SpatialFeaturePlot() | SpatialDimPlot() | FindSpatialVariableFeatures()

# Sketch/BPCells
SketchData(obj, ncells) | ProjectData(obj)

# 细胞周期
CellCycleScoring(obj, s.features, g2m.features)

# 数据提取
obj[["RNA"]]$counts | obj[["RNA"]]$data | obj[["RNA"]]$scale.data
Embeddings(obj, "umap") | obj@meta.data

# 保存/加载
saveRDS(obj, file) | readRDS(file)
```

### v4 → v5 迁移

```
slot(obj, "counts")           → obj[["RNA"]]$counts
GetAssayData(obj, slot="data")→ obj[["RNA"]]$data
FindIntegrationAnchors()      → IntegrateLayers()
  + IntegrateData()
Assay()/SetAssay()            → [[ ]] 操作符
```

---

> 📌 **核心原则**：所有函数参数有默认值，复制改参数即跑。`run_full_pipeline()` 一行完成全流程。
> 遇到问题先看 `?函数名`，再查 [Seurat官网](https://satijalab.org/seurat/)。
