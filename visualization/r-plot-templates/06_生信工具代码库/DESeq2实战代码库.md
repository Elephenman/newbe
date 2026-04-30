---
tags:
  - DESeq2
  - 差异表达
  - RNA-seq
  - 实战代码
  - 一键运行
aliases:
  - DESeq2代码库
  - 差异分析速查
  - 转录组实战宝典
created: 2026-04-20
updated: 2026-04-20
version: DESeq2 1.42+
description: RNA-seq差异表达分析实战代码库，从原始计数到发文图表，封装函数+完整流程，改参数即跑
---

# 🧬 DESeq2 实战代码库

> **定位**：复制→改参数→直接跑。覆盖 RNA-seq 差异分析全流程，从计数矩阵到发文级火山图/热图/富集分析。
> 基于 **DESeq2 最新版**，含 lfcShrink、多重比较矫正、复杂数据设计、独立过滤等高级用法。

---

## 📑 快速导航

| 需求 | 跳转 |
|------|------|
| 环境安装 | [[#📦 环境安装]] |
| 一键全流程 | [[#🚀 一键全流程]] |
| 数据准备与导入 | [[#📂 数据准备与导入]] |
| DESeq2 核心流程 | [[#⚙️ DESeq2 核心流程]] |
| lfcShrink 缩折 | [[#📉 lfcShrink 缩折变化]] |
| 多组比较 | [[#🔄 多组比较与复杂设计]] |
| 结果提取与筛选 | [[#📊 结果提取与筛选]] |
| 可视化全套 | [[#🎨 可视化全套]] |
| 质量诊断 | [[#🔍 质量诊断]] |
| 高级用法 | [[#🧪 高级用法]] |
| 常见问题速查 | [[#❓ 常见问题速查]] |
| 函数速查表 | [[#📋 函数速查表]] |

---

## 📦 环境安装

```r
# ============================================================
# DESeq2 + 依赖包安装
# ============================================================
install_if_missing <- function(pkgs, bio = FALSE) {
  for (pkg in pkgs) {
    if (!requireNamespace(pkg, quietly = TRUE)) {
      cat("安装:", pkg, "\n")
      if (bio) BiocManager::install(pkg, ask = FALSE, update = FALSE)
      else install.packages(pkg)
    } else {
      cat("✅", pkg, as.character(packageVersion(pkg)), "\n")
    }
  }
}

if (!requireNamespace("BiocManager")) install.packages("BiocManager")

# 核心
install_if_missing(c("DESeq2", "apeglm", "ashr"), bio = TRUE)

# 上游数据处理
install_if_missing(c("tximport", "tximeta", "GenomicFeatures", "Rsamtools"), bio = TRUE)

# 下游分析
install_if_missing(c("clusterProfiler", "org.Hs.eg.db", "org.Mm.eg.db",
                      "DOSE", "enrichplot", "pathview"), bio = TRUE)

# 可视化
install_if_missing(c("ggplot2", "ggrepel", "ggsci", "patchwork",
                      "pheatmap", "ComplexHeatmap", "RColorBrewer",
                      "VennDiagram", "UpSetR"))

# 数据处理
install_if_missing(c("tidyverse", "janitor", "broom"))

# 加载核心包
library(DESeq2)
library(tidyverse)
library(ggrepel)
library(ggsci)
library(patchwork)
```

---

## 🚀 一键全流程

```r
# ============================================================
# run_deseq2 —— 一键完成 DESeq2 全流程
# ============================================================
run_deseq2 <- function(count_file = NULL,
                        sample_file = NULL,
                        count_mat = NULL,
                        sample_info = NULL,
                        gene_col = 1,         # 基因名列位置
                        design_formula = "~ condition",
                        ref_level = NULL,      # 参考水平
                        contrasts = "auto",    # "auto" | list(c("cond","A","B"))
                        fc_cutoff = 1,
                        padj_cutoff = 0.05,
                        lfc_shrink = TRUE,
                        cook_filter = TRUE,
                        independent_filter = TRUE,
                        top_n_label = 15,
                        save_dir = "deseq2_results",
                        species = "human") {
  
  cat("🚀 DESeq2 分析流程启动\n")
  dir.create(save_dir, showWarnings = FALSE, recursive = TRUE)
  
  # ---- 1. 读取数据 ----
  cat("📂 数据读取...\n")
  if (is.null(count_mat)) {
    count_df <- readr::read_csv(count_file, show_col_types = FALSE)
    count_mat <- count_df %>% column_to_rownames(gene_col) %>% as.matrix()
  }
  if (is.null(sample_info)) {
    sample_info <- readr::read_csv(sample_file, show_col_types = FALSE)
  }
  
  # 确保列名一致
  common_samples <- intersect(colnames(count_mat), sample_info[[1]])
  count_mat <- count_mat[, common_samples]
  sample_info <- sample_info %>% filter(.[[1]] %in% common_samples)
  rownames(sample_info) <- sample_info[[1]]
  sample_info <- sample_info[common_samples, ]
  
  cat("  基因数:", nrow(count_mat), " 样本数:", ncol(count_mat), "\n")
  
  # ---- 2. 预过滤 ----
  cat("🔧 预过滤...\n")
  keep <- rowSums(count_mat >= 10) >= ncol(count_mat) * 0.1
  count_mat <- count_mat[keep, ]
  cat("  保留基因:", nrow(count_mat), "\n")
  
  # ---- 3. 创建 DESeq2 对象 ----
  cat("⚙️ 创建 DESeqDataSet...\n")
  dds <- DESeqDataSetFromMatrix(
    countData = count_mat,
    colData = sample_info,
    design = as.formula(design_formula)
  )
  
  # 设置参考水平
  if (!is.null(ref_level)) {
    for (var_name in names(ref_level)) {
      dds[[var_name]] <- relevel(factor(dds[[var_name]]), ref = ref_level[[var_name]])
    }
  }
  
  # ---- 4. 运行 DESeq2 ----
  cat("🧬 运行 DESeq2...\n")
  dds <- DESeq(dds)
  
  # ---- 5. 确定比较组 ----
  design_vars <- all.vars(as.formula(design_formula))
  main_var <- design_vars[1]
  groups <- unique(as.character(sample_info[[main_var]]))
  
  if (identical(contrasts, "auto")) {
    if (length(groups) == 2) {
      contrasts <- list(c(main_var, groups[2], groups[1]))
    } else {
      ref <- if (!is.null(ref_level)) ref_level[[main_var]] else groups[1]
      contrasts <- purrr::map(setdiff(groups, ref), ~ c(main_var, .x, ref))
    }
  }
  
  # ---- 6. 逐对比较 ----
  all_results <- list()
  for (contrast in contrasts) {
    comp_name <- paste(contrast[2], "vs", contrast[3])
    cat("  📊", comp_name, "\n")
    
    res <- results(dds, contrast = contrast, alpha = padj_cutoff,
                   cooksCutoff = if (cook_filter) Inf else FALSE,
                   independentFiltering = independent_filter)
    
    # LFC 缩折
    if (lfc_shrink) {
      tryCatch({
        res <- lfcShrink(dds, contrast = contrast, res = res, type = "apeglm")
      }, error = function(e) {
        cat("    ⚠️ apeglm失败，使用normal\n")
        res <<- lfcShrink(dds, contrast = contrast, res = res, type = "normal")
      })
    }
    
    res_df <- as.data.frame(res) %>% rownames_to_column("gene")
    res_df <- res_df %>%
      mutate(
        direction = case_when(
          log2FoldChange > fc_cutoff & padj < padj_cutoff ~ "Up",
          log2FoldChange < -fc_cutoff & padj < padj_cutoff ~ "Down",
          TRUE ~ "NS"
        ),
        comparison = comp_name
      )
    
    # 火山图
    p_volcano <- deseq2_volcano(res_df, fc_col = "log2FoldChange", pval_col = "padj",
                                 gene_col = "gene", fc_cut = fc_cutoff,
                                 padj_cut = padj_cutoff, top_n = top_n_label,
                                 title = comp_name)
    ggsave(file.path(save_dir, paste0("volcano_", gsub(" ", "_", comp_name), ".png")),
           p_volcano, width = 8, height = 6, dpi = 300)
    
    all_results[[comp_name]] <- res_df
  }
  
  # ---- 7. 合并结果 ----
  combined <- bind_rows(all_results, .id = "comparison")
  write_csv(combined, file.path(save_dir, "all_DEG_results.csv"))
  
  # ---- 8. QC诊断图 ----
  cat("🎨 生成诊断图...\n")
  
  # 样本距离热图
  vsd <- vst(dds, blind = FALSE)
  p_dist <- deseq2_sample_distance(vsd)
  ggsave(file.path(save_dir, "sample_distance_heatmap.png"), p_dist, width = 8, height = 7, dpi = 300)
  
  # PCA
  p_pca <- deseq2_pca(vsd, intgroup = main_var)
  ggsave(file.path(save_dir, "PCA_plot.png"), p_pca, width = 7, height = 6, dpi = 300)
  
  # ---- 9. Top基因热图 ----
  sig_genes <- combined %>%
    filter(direction != "NS") %>%
    group_by(gene) %>%
    slice(1) %>%
    ungroup() %>%
    slice_max(abs(log2FoldChange), n = 30) %>%
    pull(gene)
  
  if (length(sig_genes) > 0) {
    p_heat <- deseq2_heatmap(vsd, genes = sig_genes, group_col = main_var)
    ggsave(file.path(save_dir, "top_DEG_heatmap.png"), p_heat, width = 10, height = 8, dpi = 300)
  }
  
  # ---- 10. 汇总 ----
  summary <- combined %>%
    group_by(comparison, direction) %>%
    summarise(n = n(), .groups = "drop") %>%
    filter(direction != "NS") %>%
    pivot_wider(names_from = direction, values_from = n, values_fill = 0)
  
  cat("\n✅ 分析完成！结果保存在:", save_dir, "\n")
  print(as.data.frame(summary))
  
  # 保存 RDS
  saveRDS(dds, file.path(save_dir, "dds_object.rds"))
  saveRDS(vsd, file.path(save_dir, "vsd_object.rds"))
  
  invisible(list(
    dds = dds, vsd = vsd, results = all_results,
    combined = combined, summary = summary
  ))
}

# 使用示例：
# res <- run_deseq2(count_file = "counts.csv", sample_file = "samples.csv",
#                    design_formula = "~ condition", ref_level = list(condition = "Control"))
```

---

## 📂 数据准备与导入

### 1. 计数矩阵格式

```r
# ============================================================
# 标准计数矩阵格式
# ============================================================
# 行 = 基因，列 = 样本
#         sample1  sample2  sample3  sample4
# GENE1       23       45       12       67
# GENE2        0        5        2        8
# GENE3      456      789      234      567

# 读取
count_mat <- readr::read_csv("counts.csv", show_col_types = FALSE) %>%
  column_to_rownames("gene_id") %>%   # 第一列是基因名
  as.matrix()

# 或从 featureCounts 输出读取
read_featurecounts <- function(file) {
  df <- read.delim(file, comment.char = "#", check.names = FALSE)
  # 去除前5列注释列，保留计数
  counts <- df %>%
    select(Geneid, starts_with("Aligned")) %>%
    column_to_rownames("Geneid") %>%
    as.matrix()
  # 清理列名
  colnames(counts) <- basename(colnames(counts)) %>%
    stringr::str_remove("\\.bam$") %>%
    stringr::str_remove("_Aligned.*")
  counts
}

# ============================================================
# 样本信息格式
# ============================================================
# sample_id  condition  batch  patient
# sample1    Control    B1     P001
# sample2    Treat      B1     P001
# sample3    Control    B2     P002
# sample4    Treat      B2     P002

sample_info <- readr::read_csv("samples.csv", show_col_types = FALSE)
# 确保 sample_id 与 count_mat 列名一致
rownames(sample_info) <- sample_info[[1]]
```

### 2. 从 Salmon/Kallisto 导入

```r
# ============================================================
# tximport —— 从转录本定量到基因水平
# ============================================================
library(tximport)
library(GenomicFeatures)

# 构建 TxDb（只需要做一次）
txdb <- makeTxDbFromGFF("annotation.gtf", format = "gtf")
tx2gene <- select(txdb, keys(txdb, "GENEID"), "TXNAME", "GENEID")

# Salmon 输出
salmon_files <- list.files("./salmon_output/", pattern = "quant.sf$",
                           full.names = TRUE, recursive = TRUE)
names(salmon_files) <- basename(dirname(salmon_files))

txi_salmon <- tximport(salmon_files, type = "salmon", tx2gene = tx2gene,
                        countsFromAbundance = "lengthScaledTPM")

# Kallisto 输出
kallisto_files <- list.files("./kallisto_output/", pattern = "abundance.tsv$",
                              full.names = TRUE, recursive = TRUE)
names(kallisto_files) <- basename(dirname(kallisto_files))

txi_kallisto <- tximport(kallisto_files, type = "kallisto", tx2gene = tx2gene,
                          countsFromAbundance = "lengthScaledTPM")

# 直接用 txi 对象创建 DESeq2 对象
dds <- DESeqDataSetFromTximport(txi_salmon, sample_info, ~ condition)
```

### 3. 数据预处理检查

```r
# ============================================================
# 数据质量预检
# ============================================================
precheck_counts <- function(count_mat, sample_info) {
  cat("=== 计数矩阵概览 ===\n")
  cat("基因数:", nrow(count_mat), "\n")
  cat("样本数:", ncol(count_mat), "\n")
  
  # 全零基因
  zero_genes <- sum(rowSums(count_mat) == 0)
  cat("全零基因:", zero_genes, "\n")
  
  # 低表达基因
  low_genes <- sum(rowSums(count_mat >= 10) < ncol(count_mat) * 0.1)
  cat("低表达基因(<10%样本≥10计数):", low_genes, "\n")
  
  # 样本深度
  cat("\n=== 样本测序深度 ===\n")
  lib_sizes <- colSums(count_mat)
  cat("最小:", format(min(lib_sizes), big.mark = ","), "\n")
  cat("最大:", format(max(lib_sizes), big.mark = ","), "\n")
  cat("中位:", format(median(lib_sizes), big.mark = ","), "\n")
  cat("变异系数:", round(cv(lib_sizes), 3), "\n")
  
  # 异常样本检测（MAD法）
  log_lib <- log10(lib_sizes)
  med <- median(log_lib)
  mad_val <- mad(log_lib)
  outliers <- names(log_lib)[abs(log_lib - med) > 3 * mad_val]
  if (length(outliers) > 0) {
    cat("\n⚠️ 可能的异常样本:", paste(outliers, collapse = ", "), "\n")
  } else {
    cat("\n✅ 未检测到异常样本\n")
  }
  
  # 样本相关性
  cat("\n=== 样本间相关性 ===\n")
  log_counts <- log2(count_mat + 1)
  cor_mat <- cor(log_counts, method = "spearman")
  cat("Spearman中位数:", round(median(cor_mat[lower.tri(cor_mat)]), 3), "\n")
  
  invisible(list(lib_sizes = lib_sizes, outliers = outliers, cor_mat = cor_mat))
}
```

---

## ⚙️ DESeq2 核心流程

### 1. 创建 DESeqDataSet

```r
# ============================================================
# DESeqDataSetFromMatrix —— 从计数矩阵创建
# ============================================================
dds <- DESeqDataSetFromMatrix(
  countData = count_mat,    # 计数矩阵（整数）
  colData = sample_info,    # 样本信息 data.frame
  design = ~ condition      # 设计公式
)

# 设置参考水平（对照组）
dds$condition <- relevel(factor(dds$condition), ref = "Control")

# ============================================================
# 预过滤（推荐，减少内存加速计算）
# ============================================================
# 保留在至少一些样本中有足够计数的基因
keep <- rowSums(counts(dds) >= 10) >= ncol(dds) * 0.1
dds <- dds[keep, ]
# 更宽松的过滤：
# keep <- rowSums(counts(dds)) >= 10

# ============================================================
# 运行 DESeq() —— 三步合一
# ============================================================
dds <- DESeq(dds)
# 等价于依次运行：
# dds <- estimateSizeFactors(dds)    # 大小因子归一化
# dds <- estimateDispersions(dds)     # 离散度估计
# dds <- nbinomWaldTest(dds)          # 负二项Wald检验

# 查看结果
resultsNames(dds)   # 可用的比较名称
```

### 2. 复杂实验设计

```r
# ============================================================
# 含 batch 效应的设计
# ============================================================
dds <- DESeqDataSetFromMatrix(count_mat, sample_info, ~ batch + condition)
# 注意：感兴趣的变量放最后！

# ============================================================
# 配对设计
# ============================================================
dds <- DESeqDataSetFromMatrix(count_mat, sample_info, ~ patient + condition)

# ============================================================
# 交互效应
# ============================================================
dds <- DESeqDataSetFromMatrix(count_mat, sample_info, ~ condition + time + condition:time)
# 简写：~ condition * time

# ============================================================
# 多因素设计
# ============================================================
dds <- DESeqDataSetFromMatrix(count_mat, sample_info, ~ batch + sex + age + condition)

# ============================================================
# 查看设计矩阵
# ============================================================
model.matrix(design(dds), colData(dds))
```

---

## 📉 lfcShrink 缩折变化

```r
# ============================================================
# lfcShrink —— 缩折 log2FC（强烈推荐！）
# ============================================================
# 为什么用：低表达基因的 log2FC 估计方差大，缩折后更稳健
# 适用于排序和可视化，不建议用于基因筛选（筛选用原始结果）

# 方法一：apeglm（推荐，最稳健）
res_shrunk <- lfcShrink(dds, coef = "condition_Treat_vs_Control", type = "apeglm")

# 方法二：ashr（多组比较推荐）
res_shrunk <- lfcShrink(dds, coef = "condition_Treat_vs_Control", type = "ashr")

# 方法三：normal（传统方法，需要 contrast）
res_shrunk <- lfcShrink(dds, contrast = c("condition", "Treat", "Control"), type = "normal")

# 注意：
# - apeglm 和 ashr 需要 coef（系数名），从 resultsNames(dds) 获取
# - normal 需要 contrast
# - apeglm 最稳健，但对极端 log2FC 可能缩折过多
# - 火山图推荐用缩折后的 log2FC，更准确

# 查看可用系数名
resultsNames(dds)
```

---

## 🔄 多组比较与复杂设计

### 1. 两两比较

```r
# ============================================================
# 手动指定比较
# ============================================================

# 方法一：用 contrast 向量
res <- results(dds, contrast = c("condition", "Treat_A", "Control"))

# 方法二：用 coef 系数名
res <- results(dds, coef = "condition_Treat_A_vs_Control")

# 方法三：用 name（等价于 coef）
res <- results(dds, name = "condition_Treat_A_vs_Control")

# ============================================================
# 批量两两比较
# ============================================================
all_pairwise <- function(dds, variable, ref = NULL) {
  groups <- unique(as.character(colData(dds)[[variable]]))
  if (is.null(ref)) ref <- groups[1]
  
  comparisons <- purrr::map(setdiff(groups, ref), ~ c(variable, .x, ref))
  
  purrr::imap_dfr(comparisons, function(comp, i) {
    res <- results(dds, contrast = comp)
    as.data.frame(res) %>%
      rownames_to_column("gene") %>%
      mutate(comparison = paste(comp[2], "vs", comp[3]))
  })
}
```

### 2. 交互效应检验

```r
# ============================================================
# 交互效应 —— 检验条件×时间的交互
# ============================================================
dds <- DESeqDataSetFromMatrix(count_mat, sample_info, ~ condition + time + condition:time)
dds <- DESeq(dds)

# 查看交互效应的系数
resultsNames(dds)
# [1] "Intercept" ...
#     "conditionTreat.timePost"  ← 交互效应项

# 提取交互效应
res_interaction <- results(dds, name = "conditionTreat.timePost")

# 在 Treat 组中比较 time Post vs Pre
res_treat_time <- results(dds, contrast = list(
  "time_Post_vs_Pre",
  "conditionTreat.timePost"
))

# ============================================================
# likelihood ratio test (LRT) —— 检验多个系数的联合显著性
# ============================================================
dds_lrt <- DESeq(dds, test = "LRT", reduced = ~ condition)
# full: ~ condition + time + condition:time
# reduced: ~ condition
# LRT 检验的是 time 和 interaction 项是否联合显著

res_lrt <- results(dds_lrt)
# LRT 结果没有 log2FC，只有统计显著性
```

---

## 📊 结果提取与筛选

```r
# ============================================================
# results() 参数详解
# ============================================================
res <- results(dds,
  contrast = c("condition", "Treat", "Control"),
  alpha = 0.05,              # FDR 阈值
  lfcThreshold = 0,          # log2FC 阈值（用于检验而非筛选）
  altHypothesis = "greaterAbs",  # "greaterAbs" | "lessAbs" | "greater" | "less"
  cooksCutoff = TRUE,        # Cook's distance 过滤
  independentFiltering = TRUE, # 独立过滤（推荐开启）
  pAdjustMethod = "BH"       # 多重比较矫正方法
)

# ============================================================
# 结果列含义
# ============================================================
# baseMean        → 所有样本的平均表达量（归一化后）
# log2FoldChange  → log2倍变化
# lfcSE           → log2FC 标准误
# stat            → Wald 统计量
# pvalue          → 原始p值
# padj            → 校正后p值（BH法）

# ============================================================
# 筛选差异基因
# ============================================================
# 方法一：直接筛选
sig_genes <- res %>%
  as.data.frame() %>%
  rownames_to_column("gene") %>%
  filter(padj < 0.05 & abs(log2FoldChange) > 1)

# 方法二：使用 results() 内置筛选
res <- results(dds, alpha = 0.05, lfcThreshold = 1, altHypothesis = "greaterAbs")
# 这会在统计检验层面考虑 log2FC 阈值

# 方法三：分上调/下调
up_genes <- sig_genes %>% filter(log2FoldChange > 0)
down_genes <- sig_genes %>% filter(log2FoldChange < 0)

# ============================================================
# 提取特定基因的结果
# ============================================================
# 单个基因
res["TP53", ]

# 多个基因
genes_of_interest <- c("TP53", "BRCA1", "EGFR", "MYC")
res[genes_of_interest, ]

# ============================================================
# 排序
# ============================================================
# 按p值排序
res_ordered <- res[order(res$padj), ]

# 按 log2FC 绝对值排序
res_ordered <- res[order(abs(res$log2FoldChange), decreasing = TRUE), ]

# ============================================================
# 导出
# ============================================================
res_df <- as.data.frame(res) %>% rownames_to_column("gene")
readr::write_csv(res_df, "DEG_results.csv")
```

---

## 🎨 可视化全套

### 1. 火山图

```r
# ============================================================
# deseq2_volcano —— 标准发文级火山图
# ============================================================
deseq2_volcano <- function(res_df,
                            fc_col = "log2FoldChange",
                            pval_col = "padj",
                            gene_col = "gene",
                            fc_cut = 1,
                            padj_cut = 0.05,
                            top_n = 15,
                            highlight_genes = NULL,
                            title = "Volcano Plot",
                            palette = c("#2166AC", "#BEBEBE", "#B2182B")) {
  
  df <- res_df %>%
    filter(!is.na(!!sym(pval_col))) %>%
    mutate(
      sig = case_when(
        !!sym(fc_col) > fc_cut & !!sym(pval_col) < padj_cut ~ "Up",
        !!sym(fc_col) < -fc_cut & !!sym(pval_col) < padj_cut ~ "Down",
        TRUE ~ "NS"
      ),
      nlog10p = -log10(!!sym(pval_col))
    )
  
  # 自动标注 top 基因
  label_df <- df %>%
    filter(sig != "NS") %>%
    group_by(sig) %>%
    slice_max(order_by = nlog10p, n = top_n) %>%
    ungroup()
  
  if (!is.null(highlight_genes)) {
    label_df <- df %>% filter(!!sym(gene_col) %in% highlight_genes)
  }
  
  ggplot(df, aes(x = !!sym(fc_col), y = nlog10p, color = sig)) +
    geom_point(size = 0.6, alpha = 0.4) +
    geom_point(data = filter(df, sig != "NS"), size = 1, alpha = 0.7) +
    ggrepel::geom_text_repel(
      data = label_df, aes(label = !!sym(gene_col)),
      size = 2.5, max.overlaps = 25, color = "black",
      segment.color = "grey60", segment.size = 0.2
    ) +
    geom_hline(yintercept = -log10(padj_cut), linetype = "dashed", color = "grey50", linewidth = 0.3) +
    geom_vline(xintercept = c(-fc_cut, fc_cut), linetype = "dashed", color = "grey50", linewidth = 0.3) +
    scale_color_manual(values = c(Down = palette[1], NS = palette[2], Up = palette[3])) +
    labs(title = title,
         x = expression(log[2]~Fold~Change),
         y = expression(-log[10](P[adj])),
         color = "") +
    theme_bw() +
    theme(
      plot.title = element_text(hjust = 0.5, face = "bold"),
      panel.grid.minor = element_blank(),
      legend.position = "bottom"
    )
}
```

### 2. MA 图

```r
# ============================================================
# deseq2_ma —— MA 图
# ============================================================
deseq2_ma <- function(dds, contrast = NULL, alpha = 0.05,
                       main = "MA Plot") {
  res <- results(dds, contrast = contrast, alpha = alpha)
  res_df <- as.data.frame(res) %>% rownames_to_column("gene")
  
  res_df %>%
    mutate(sig = padj < alpha) %>%
    ggplot(aes(x = log10(baseMean + 1), y = log2FoldChange, color = sig)) +
    geom_point(size = 0.4, alpha = 0.4) +
    scale_color_manual(values = c("grey70", "red3"), labels = c("NS", "Sig")) +
    geom_hline(yintercept = 0, linetype = "dashed", color = "blue", linewidth = 0.3) +
    labs(title = main, x = expression(log[10]~Mean), y = expression(log[2]~FC)) +
    theme_bw() +
    theme(legend.position = "bottom", plot.title = element_text(hjust = 0.5))
}
```

### 3. 样本距离热图

```r
# ============================================================
# deseq2_sample_distance —— 样本聚类热图
# ============================================================
deseq2_sample_distance <- function(vsd, intgroup = "condition") {
  library(pheatmap)
  
  dist_mat <- dist(t(assay(vsd)))
  mat <- as.matrix(dist_mat)
  rownames(mat) <- colData(vsd)[[intgroup]]
  colnames(mat) <- colData(vsd)[[intgroup]]
  
  pheatmap(mat,
    clustering_distance_rows = dist_mat,
    clustering_distance_cols = dist_mat,
    main = "Sample Distance Matrix",
    display_numbers = TRUE,
    number_format = "%.2f",
    fontsize_number = 8
  )
}
```

### 4. PCA 图

```r
# ============================================================
# deseq2_pca —— 发文级 PCA 图
# ============================================================
deseq2_pca <- function(vsd, intgroup = "condition", ntop = 500,
                        palette = "npg", label_samples = FALSE) {
  
  pca_data <- plotPCA(vsd, intgroup = intgroup, ntop = ntop, returnData = TRUE)
  percent_var <- attr(pca_data, "percentVar")
  
  p <- ggplot(pca_data, aes(x = PC1, y = PC2, color = !!sym(intgroup))) +
    geom_point(size = 3, alpha = 0.8) +
    stat_ellipse(level = 0.95, linewidth = 0.8) +
    labs(
      x = paste0("PC1: ", round(percent_var[1], 1), "% variance"),
      y = paste0("PC2: ", round(percent_var[2], 1), "% variance"),
      title = "PCA Plot"
    ) +
    theme_bw() +
    theme(plot.title = element_text(hjust = 0.5, face = "bold"))
  
  if (palette == "npg") p <- p + scale_color_npg()
  else if (palette == "aaas") p <- p + scale_color_aaas()
  else if (palette == "lancet") p <- p + scale_color_lancet()
  
  if (label_samples) {
    p <- p + ggrepel::geom_text_repel(aes(label = name), size = 2.5, max.overlaps = 20)
  }
  
  p
}
```

### 5. 表达热图

```r
# ============================================================
# deseq2_heatmap —— Top DEGs 热图
# ============================================================
deseq2_heatmap <- function(vsd, genes = NULL, res_df = NULL,
                            n_top = 30, group_col = "condition",
                            cluster_rows = TRUE, cluster_cols = TRUE,
                            show_rownames = TRUE) {
  library(pheatmap)
  
  # 确定基因列表
  if (is.null(genes) && !is.null(res_df)) {
    genes <- res_df %>%
      filter(padj < 0.05) %>%
      slice_max(abs(log2FoldChange), n = n_top) %>%
      pull(gene)
  }
  
  if (length(genes) == 0) stop("没有可用的差异基因")
  
  mat <- assay(vsd)[genes, ]
  mat <- mat - rowMeans(mat)  # 中心化
  
  # 注释
  annotation_col <- as.data.frame(colData(vsd)[group_col])
  colnames(annotation_col) <- group_col
  
  ann_colors <- list()
  n_groups <- length(unique(annotation_col[[group_col]]))
  ann_colors[[group_col]] <- ggsci::pal_npg("nrc")(n_groups) %>%
    setNames(unique(annotation_col[[group_col]]))
  
  pheatmap(mat,
    annotation_col = annotation_col,
    annotation_colors = ann_colors,
    cluster_rows = cluster_rows,
    cluster_cols = cluster_cols,
    show_rownames = show_rownames,
    show_colnames = TRUE,
    fontsize_row = 7,
    fontsize_col = 8,
    scale = "row",
    color = colorRampPalette(c("navy", "white", "firebrick3"))(100),
    main = paste0("Top ", length(genes), " DEGs")
  )
}
```

### 6. 基因表达图

```r
# ============================================================
# deseq2_gene_plot —— 单基因/多基因表达图
# ============================================================
deseq2_gene_plot <- function(dds, genes, intgroup = "condition",
                              plot_type = "boxplot") {
  
  vsd <- vst(dds, blind = FALSE)
  
  for (gene in genes) {
    if (!gene %in% rownames(dds)) {
      cat("⚠️", gene, "不在数据中\n")
      next
    }
    
    df <- data.frame(
      expression = assay(vsd)[gene, ],
      group = colData(vsd)[[intgroup]]
    )
    
    p <- switch(plot_type,
      boxplot = ggplot(df, aes(x = group, y = expression, fill = group)) +
        geom_boxplot(width = 0.6, outlier.shape = NA) +
        geom_jitter(width = 0.15, size = 1.5, alpha = 0.6) +
        ggpubr::stat_compare_means(method = "wilcox.test") +
        scale_fill_npg() +
        labs(title = gene, y = "VST expression") +
        theme_bw(),
      
      violin = ggplot(df, aes(x = group, y = expression, fill = group)) +
        geom_violin(alpha = 0.5, width = 0.8) +
        geom_boxplot(width = 0.15, outlier.size = 0.5) +
        ggpubr::stat_compare_means(method = "wilcox.test") +
        scale_fill_npg() +
        labs(title = gene, y = "VST expression") +
        theme_bw(),
      
      bar = ggplot(df, aes(x = group, y = expression, fill = group)) +
        geom_bar(stat = "summary", fun = "mean", width = 0.6) +
        geom_errorbar(stat = "summary", fun.data = mean_se, width = 0.2) +
        geom_jitter(size = 1.5, alpha = 0.5) +
        scale_fill_npg() +
        labs(title = gene, y = "VST expression (mean ± SE)") +
        theme_bw()
    )
    
    print(p)
  }
}

# 使用: deseq2_gene_plot(dds, c("TP53", "BRCA1", "EGFR"), plot_type = "violin")
```

### 7. Count 图

```r
# ============================================================
# plotCounts —— DESeq2 内置计数图
# ============================================================
# 单基因
plotCounts(dds, gene = "TP53", intgroup = "condition")

# 封装版
deseq2_count_plot <- function(dds, gene, intgroup = "condition") {
  data <- plotCounts(dds, gene = gene, intgroup = intgroup, returnData = TRUE)
  ggplot(data, aes(x = !!sym(intgroup), y = count, fill = !!sym(intgroup))) +
    geom_boxplot(width = 0.5, outlier.shape = NA) +
    geom_jitter(width = 0.1, size = 2, alpha = 0.7) +
    scale_y_log10() +
    scale_fill_npg() +
    labs(title = gene, y = "Count (log10 scale)") +
    theme_bw()
}
```

---

## 🔍 质量诊断

```r
# ============================================================
# deseq2_qc_report —— 生成全套 QC 报告
# ============================================================
deseq2_qc_report <- function(dds, intgroup = "condition", save_dir = "qc_report") {
  dir.create(save_dir, showWarnings = FALSE)
  
  vsd <- vst(dds, blind = FALSE)
  
  # 1. 离散度图
  png(file.path(save_dir, "dispersion_plot.png"), width = 800, height = 600)
  plotDispEsts(dds)
  dev.off()
  
  # 2. Cook's distance
  png(file.path(save_dir, "cooks_distance.png"), width = 1000, height = 600)
  par(mfrow = c(1, 2))
  plot(dds, "cooks")
  dev.off()
  
  # 3. 样本距离
  dist_mat <- dist(t(assay(vsd)))
  p_dist <- deseq2_sample_distance(vsd, intgroup)
  png(file.path(save_dir, "sample_distance.png"), width = 800, height = 700)
  print(p_dist)
  dev.off()
  
  # 4. PCA
  p_pca <- deseq2_pca(vsd, intgroup)
  ggsave(file.path(save_dir, "PCA.png"), p_pca, width = 7, height = 6, dpi = 300)
  
  # 5. 大小因子
  sf <- sizeFactors(dds)
  cat("=== 大小因子 ===\n")
  print(round(sf, 3))
  cat("\n大小因子变异系数:", round(sd(sf) / mean(sf), 3), "\n")
  
  # 6. 样本深度
  cat("\n=== 样本深度 ===\n")
  lib_sizes <- colSums(counts(dds))
  print(round(lib_sizes / 1e6, 2))
  
  cat("\n✅ QC 报告已保存至:", save_dir, "\n")
}
```

---

## 🧪 高级用法

### 1. VST vs rlog

```r
# ============================================================
# 降维变换选择
# ============================================================

# VST（方差稳定变换）—— 推荐用于大数据集
vsd <- vst(dds, blind = FALSE)        # blind=FALSE: 考虑设计
vsd <- vst(dds, blind = TRUE)         # blind=TRUE: 不考虑设计（QC时推荐）

# rlog（正则化log变换）—— 小数据集更平滑
rld <- rlog(dds, blind = FALSE)        # 慢但更稳健

# 提取变换后的矩阵
vst_mat <- assay(vsd)
rlog_mat <- assay(rld)

# 选择建议：
# 样本数 > 30 → vst（快）
# 样本数 < 10 → rlog（更稳健）
# 一般情况 → vst 够用
```

### 2. 独立过滤

```r
# ============================================================
# 独立过滤（independentFiltering）
# ============================================================
# 默认开启，基于平均表达量过滤低表达基因
# 过滤阈值自动选择，使发现差异基因数最大化

# 查看过滤阈值
metadata(res)$filterThreshold
# 查看过滤通过率
metadata(res)$filterNumRej

# 关闭独立过滤
res_no_filter <- results(dds, independentFiltering = FALSE)
# 一般不推荐关闭
```

### 3. Cook's Distance 异常值

```r
# ============================================================
# Cook's Distance 异常值检测与处理
# ============================================================

# 查看被 Cook's distance 过滤的基因
res_cooks_off <- results(dds, cooksCutoff = FALSE)
n_filtered <- sum(is.na(res$padj) & !is.na(res_cooks_off$padj))
cat("被 Cook's 过滤的基因:", n_filtered, "\n")

# 查看具体哪些基因
cooks_genes <- which(is.na(res$padj) & !is.na(res_cooks_off$padj))
head(rownames(res)[cooks_genes])

# 关闭 Cook's 过滤（不推荐，除非明确需要）
res <- results(dds, cooksCutoff = FALSE)

# 手动检查 Cook's 距离
cooks_mat <- assays(dds)[["cooks"]]
max_cooks <- apply(cooks_mat, 1, max)
hist(max_cooks, breaks = 50, main = "Max Cook's Distance per Gene")
```

### 4. 并行加速

```r
# ============================================================
# 大数据集并行计算
# ============================================================
library(BiocParallel)

# 注册并行后端
register(MulticoreParam(8))     # Linux/Mac
register(SnowParam(8))          # Windows

# 在 DESeq() 中启用并行
dds <- DESeq(dds, parallel = TRUE)

# results() 也支持并行
res <- results(dds, parallel = TRUE)
```

### 5. 从已有对象继续分析

```r
# ============================================================
# 保存与恢复
# ============================================================
# 保存
saveRDS(dds, "dds_object.rds")
saveRDS(vsd, "vsd_object.rds")

# 加载
dds <- readRDS("dds_object.rds")

# 添加新的比较（不需要重新运行 DESeq）
res_new <- results(dds, contrast = c("condition", "NewGroup", "Control"))
```

---

## ❓ 常见问题速查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 全部 padj = NA | 低表达基因太多 | 降低过滤阈值或用 `independentFiltering=FALSE` |
| log2FC 异常大 | 低表达基因 | 使用 `lfcShrink(type="apeglm")` |
| 样本聚类异常 | batch效应 | 在 design 中加入 batch 变量 |
| 差异基因为0 | 样本量不足 | 增加重复数或放宽阈值 |
| 计数矩阵有负值 | 输入了FPKM/TPM | DESeq2 需要原始整数计数 |
| Error: less than 2 samples | 重复不够 | 每组至少2个样本 |
| "model matrix not full rank" | 设计矩阵共线性 | 检查 colData，移除冗余变量 |
| 运行太慢 | 基因数太多 | 预过滤 + 并行计算 |
| VST 失败 | 样本太少 | 改用 `rlog()` |

---

## 📋 函数速查表

### 封装函数速查

| 函数 | 用途 | 调用示例 |
|------|------|----------|
| `run_deseq2()` | 一键全流程 | `run_deseq2("counts.csv","samples.csv")` |
| `precheck_counts()` | 数据预检 | `precheck_counts(mat, info)` |
| `read_featurecounts()` | 读取featureCounts | `read_featurecounts("counts.txt")` |
| `deseq2_volcano()` | 火山图 | `deseq2_volcano(df, fc_col="log2FoldChange")` |
| `deseq2_ma()` | MA图 | `deseq2_ma(dds)` |
| `deseq2_pca()` | PCA图 | `deseq2_pca(vsd, "condition")` |
| `deseq2_sample_distance()` | 样本距离热图 | `deseq2_sample_distance(vsd)` |
| `deseq2_heatmap()` | Top DEGs热图 | `deseq2_heatmap(vsd, genes=top30)` |
| `deseq2_gene_plot()` | 基因表达图 | `deseq2_gene_plot(dds, c("TP53"))` |
| `deseq2_count_plot()` | 计数图 | `deseq2_count_plot(dds, "TP53")` |
| `deseq2_qc_report()` | QC报告 | `deseq2_qc_report(dds)` |
| `all_pairwise()` | 批量两两比较 | `all_pairwise(dds, "condition")` |

### DESeq2 核心函数速查

```
# 创建对象
DESeqDataSetFromMatrix(countData, colData, design)
DESeqDataSetFromTximport(txi, colData, design)

# 分析
DESeq(dds)                        # 运行全部
estimateSizeFactors(dds)           # 大小因子
estimateDispersions(dds)           # 离散度
nbinomWaldTest(dds)                # Wald检验

# 变换
vst(dds, blind)                    # VST
rlog(dds, blind)                   # rlog
lfcShrink(dds, coef, type)         # LFC缩折

# 结果
results(dds, contrast, coef, alpha)
resultsNames(dds)                  # 可用比较名

# 可视化
plotPCA(vsd, intgroup)             # PCA
plotDispEsts(dds)                  # 离散度
plotCounts(dds, gene, intgroup)    # 计数图

# 信息提取
counts(dds, normalized=TRUE)       # 归一化计数
assay(vsd)                         # VST矩阵
sizeFactors(dds)                   # 大小因子
colData(dds)                       # 样本信息
mcols(res)                         # 结果列说明
```

---

> 📌 **核心原则**：原始计数输入 → DESeq2 自动归一化 → lfcShrink 缩折 → padj 筛选 → 火山图/热图出图。
> 一行运行：`run_deseq2("counts.csv", "samples.csv")` 完成全流程。
