---
tags:
  - clusterProfiler
  - 富集分析
  - GO
  - KEGG
  - GSEA
  - 实战代码
  - 一键运行
aliases:
  - clusterProfiler代码库
  - 富集分析速查
  - GO/KEGG实战宝典
  - GSEA代码库
created: 2026-04-20
updated: 2026-04-20
version: clusterProfiler 4.10+
description: 功能富集分析实战代码库，GO/KEGG/GSEA全覆盖，封装函数+发文级可视化，改参数即跑
---

# 🔬 clusterProfiler 实战代码库

> **定位**：复制→改参数→直接跑。覆盖功能富集分析全流程：ORA（过表达分析）+ GSEA（基因集富集），从基因列表到发文级图表。
> 基于 **clusterProfiler 4.10+**，含 enrichGO/enrichKEGG/gseGO/gseKEGG + 十余种可视化 + 多组比较。

---

## 📑 快速导航

| 需求 | 跳转 |
|------|------|
| 环境安装 | [[#📦 环境安装]] |
| 一键全流程 | [[#🚀 一键全流程]] |
| 基因ID转换 | [[#🔄 基因ID转换]] |
| GO富集分析 | [[#📊 GO 富集分析]] |
| KEGG富集分析 | [[#🧬 KEGG 富集分析]] |
| GSEA分析 | [[#📈 GSEA 分析]] |
| 其他数据库 | [[#🗄️ 其他数据库富集]] |
| 可视化全套 | [[#🎨 可视化全套]] |
| 多组比较 | [[#🔄 多组比较富集]] |
| 生信实战封装 | [[#🧪 生信实战封装]] |
| 常见问题速查 | [[#❓ 常见问题速查]] |
| 函数速查表 | [[#📋 函数速查表]] |

---

## 📦 环境安装

```r
# ============================================================
# clusterProfiler 生态安装
# ============================================================
if (!requireNamespace("BiocManager")) install.packages("BiocManager")

# 核心包
BiocManager::install(c(
  "clusterProfiler",     # 富集分析核心
  "enrichplot",          # 可视化
  "DOSE",                # 语义相似度
  "AnnotationDbi"        # 注释基础
))

# 物种注释包
BiocManager::install(c(
  "org.Hs.eg.db",        # 人类
  "org.Mm.eg.db",        # 小鼠
  "org.Rn.eg.db",        # 大鼠
  "org.Dm.eg.db",        # 果蝇
  "org.Ce.eg.db"         # 线虫
))

# KEGG 相关
BiocManager::install(c(
  "KEGGREST",
  "pathview"             # KEGG通路图标注
))

# 其他富集数据库
BiocManager::install(c(
  "ReactomePA",          # Reactome通路
  "msigdbr",             # MSigDB基因集
  "GSVA",                # GSVA分析
  "enrichTF"             # 转录因子富集
))

# 可视化增强
install.packages(c("ggupset", "ggnewscale", "ggforce"))

# 加载核心包
library(clusterProfiler)
library(enrichplot)
library(DOSE)
library(org.Hs.eg.db)
library(ggplot2)
```

---

## 🚀 一键全流程

```r
# ============================================================
# run_enrichment —— 一键完成 GO + KEGG + GSEA 全套富集
# ============================================================
run_enrichment <- function(gene_list = NULL,
                            gene_df = NULL,
                            gene_col = "gene",
                            fc_col = "log2FoldChange",
                            padj_col = "padj",
                            fc_cutoff = 1,
                            padj_cutoff = 0.05,
                            species = "human",
                            ont = "BP",
                            pvalue_cutoff = 0.05,
                            qvalue_cutoff = 0.2,
                            top_n = 20,
                            save_dir = "enrichment_results") {
  
  cat("🔬 富集分析流程启动\n")
  dir.create(save_dir, showWarnings = FALSE, recursive = TRUE)
  
  # 确定物种参数
  org_db <- switch(species,
    human = "org.Hs.eg.db",
    mouse = "org.Mm.eg.db",
    rat   = "org.Rn.eg.db",
    fly   = "org.Dm.eg.db",
    worm  = "org.Ce.eg.db",
    stop("不支持的物种: ", species)
  )
  kegg_org <- switch(species,
    human = "hsa", mouse = "mmu", rat = "rno",
    fly = "dme", worm = "cel",
    stop("不支持的物种: ", species)
  )
  
  library(org_db, character.only = TRUE)
  
  # ---- 1. 准备基因列表 ----
  cat("🔄 基因ID转换...\n")
  
  if (!is.null(gene_df)) {
    # 从 DESeq2 结果中提取
    sig_genes <- gene_df %>%
      filter(!!sym(padj_col) < padj_cutoff & abs(!!sym(fc_col)) > fc_cutoff) %>%
      pull(!!sym(gene_col))
    
    # GSEA 需要的排序列表
    ranked_genes <- gene_df %>%
      filter(!is.na(!!sym(padj_col))) %>%
      arrange(desc(!!sym(fc_col))) %>%
      select(gene = !!sym(gene_col), log2FoldChange = !!sym(fc_col))
  } else {
    sig_genes <- gene_list
    ranked_genes <- NULL
  }
  
  cat("  显著基因数:", length(sig_genes), "\n")
  
  # SYMBOL → ENTREZID
  ids <- bitr(sig_genes, fromType = "SYMBOL", toType = "ENTREZID",
              OrgDb = org_db)
  entrez_ids <- ids$ENTREZID
  cat("  成功转换:", nrow(ids), "/", length(sig_genes), "\n")
  
  # GSEA 的排序列表
  if (!is.null(ranked_genes)) {
    gsea_ids <- bitr(ranked_genes$gene, fromType = "SYMBOL", toType = "ENTREZID",
                     OrgDb = org_db)
    ranked_list <- ranked_genes %>%
      inner_join(gsea_ids, by = c("gene" = "SYMBOL")) %>%
      arrange(desc(log2FoldChange)) %>%
      deframe()
    names(ranked_list) <- gsea_ids$ENTREZID[match(names(ranked_list), gsea_ids$ENTREZID)]
  }
  
  # ---- 2. GO 富集 ----
  cat("\n📊 GO 富集分析...\n")
  go_bp <- enrichGO(gene = entrez_ids, OrgDb = org_db, ont = "BP",
                     pvalueCutoff = pvalue_cutoff, qvalueCutoff = qvalue_cutoff,
                     readable = TRUE)
  go_mf <- enrichGO(gene = entrez_ids, OrgDb = org_db, ont = "MF",
                     pvalueCutoff = pvalue_cutoff, qvalueCutoff = qvalue_cutoff,
                     readable = TRUE)
  go_cc <- enrichGO(gene = entrez_ids, OrgDb = org_db, ont = "CC",
                     pvalueCutoff = pvalue_cutoff, qvalueCutoff = qvalue_cutoff,
                     readable = TRUE)
  
  cat("  BP:", nrow(as.data.frame(go_bp)), "terms\n")
  cat("  MF:", nrow(as.data.frame(go_mf)), "terms\n")
  cat("  CC:", nrow(as.data.frame(go_cc)), "terms\n")
  
  # GO 可视化
  if (nrow(as.data.frame(go_bp)) > 0) {
    p <- enrich_plot_bar(go_bp, top_n = top_n, title = "GO Biological Process")
    ggsave(file.path(save_dir, "GO_BP_barplot.png"), p, width = 10, height = 8, dpi = 300)
    
    p <- enrich_plot_dot(go_bp, top_n = top_n, title = "GO Biological Process")
    ggsave(file.path(save_dir, "GO_BP_dotplot.png"), p, width = 10, height = 8, dpi = 300)
  }
  
  # ---- 3. KEGG 富集 ----
  cat("\n🧬 KEGG 富集分析...\n")
  kegg <- enrichKEGG(gene = entrez_ids, organism = kegg_org,
                      pvalueCutoff = pvalue_cutoff, qvalueCutoff = qvalue_cutoff)
  
  cat("  KEGG:", nrow(as.data.frame(kegg)), "pathways\n")
  
  if (nrow(as.data.frame(kegg)) > 0) {
    kegg <- setReadable(kegg, OrgDb = org_db, keyType = "ENTREZID")
    
    p <- enrich_plot_dot(kegg, top_n = top_n, title = "KEGG Pathway")
    ggsave(file.path(save_dir, "KEGG_dotplot.png"), p, width = 10, height = 8, dpi = 300)
  }
  
  # ---- 4. GSEA ----
  if (!is.null(ranked_list) && length(ranked_list) > 100) {
    cat("\n📈 GSEA 分析...\n")
    
    gsea_go <- gseGO(geneList = ranked_list, OrgDb = org_db, ont = ont,
                      pvalueCutoff = pvalue_cutoff, verbose = FALSE)
    
    gsea_kegg <- gseKEGG(geneList = ranked_list, organism = kegg_org,
                          pvalueCutoff = pvalue_cutoff, verbose = FALSE)
    
    cat("  GSEA-GO:", nrow(as.data.frame(gsea_go)), "terms\n")
    cat("  GSEA-KEGG:", nrow(as.data.frame(gsea_kegg)), "pathways\n")
    
    if (nrow(as.data.frame(gsea_go)) > 0) {
      gsea_go <- setReadable(gsea_go, OrgDb = org_db, keyType = "ENTREZID")
      p <- enrich_plot_gsea(gsea_go, top_n = 5)
      ggsave(file.path(save_dir, "GSEA_GO_ridge.png"), p, width = 10, height = 6, dpi = 300)
    }
    
    if (nrow(as.data.frame(gsea_kegg)) > 0) {
      gsea_kegg <- setReadable(gsea_kegg, OrgDb = org_db, keyType = "ENTREZID")
      p <- enrich_plot_gsea(gsea_kegg, top_n = 5)
      ggsave(file.path(save_dir, "GSEA_KEGG_ridge.png"), p, width = 10, height = 6, dpi = 300)
    }
  }
  
  # ---- 5. 保存 ----
  cat("\n💾 保存结果...\n")
  if (nrow(as.data.frame(go_bp)) > 0) write_csv(as.data.frame(go_bp), file.path(save_dir, "GO_BP_results.csv"))
  if (nrow(as.data.frame(go_mf)) > 0) write_csv(as.data.frame(go_mf), file.path(save_dir, "GO_MF_results.csv"))
  if (nrow(as.data.frame(go_cc)) > 0) write_csv(as.data.frame(go_cc), file.path(save_dir, "GO_CC_results.csv"))
  if (nrow(as.data.frame(kegg)) > 0) write_csv(as.data.frame(kegg), file.path(save_dir, "KEGG_results.csv"))
  if (exists("gsea_go") && nrow(as.data.frame(gsea_go)) > 0) write_csv(as.data.frame(gsea_go), file.path(save_dir, "GSEA_GO_results.csv"))
  if (exists("gsea_kegg") && nrow(as.data.frame(gsea_kegg)) > 0) write_csv(as.data.frame(gsea_kegg), file.path(save_dir, "GSEA_KEGG_results.csv"))
  
  cat("\n✅ 富集分析完成！结果保存在:", save_dir, "\n")
  
  invisible(list(
    go_bp = go_bp, go_mf = go_mf, go_cc = go_cc,
    kegg = kegg,
    gsea_go = if (exists("gsea_go")) gsea_go else NULL,
    gsea_kegg = if (exists("gsea_kegg")) gsea_kegg else NULL
  ))
}

# 使用示例：
# results <- run_enrichment(gene_df = deg_results, species = "human")
```

---

## 🔄 基因ID转换

```r
# ============================================================
# bitr —— 基因ID类型转换（最常用）
# ============================================================

# SYMBOL → ENTREZID
ids <- bitr(c("TP53", "BRCA1", "EGFR", "MYC"),
            fromType = "SYMBOL",
            toType = "ENTREZID",
            OrgDb = org.Hs.eg.db)

# SYMBOL → 多种ID
ids_multi <- bitr(c("TP53", "BRCA1"),
                   fromType = "SYMBOL",
                   toType = c("ENTREZID", "ENSEMBL", "GENENAME"),
                   OrgDb = org.Hs.eg.db)

# ENTREZID → SYMBOL
ids_back <- bitr(ids$ENTREZID,
                  fromType = "ENTREZID",
                  toType = "SYMBOL",
                  OrgDb = org.Hs.eg.db)

# ============================================================
# bitr_kegg —— KEGG 专用转换
# ============================================================
kegg_ids <- bitr_kegg(c("TP53", "BRCA1"),
                       fromType = "kegg",
                       toType = "ncbi-geneid",
                       organism = "hsa")

# ============================================================
# 批量ID转换封装
# ============================================================
auto_id_convert <- function(genes, from = "SYMBOL", to = "ENTREZID",
                             species = "human", drop_unmapped = TRUE) {
  org_db <- switch(species,
    human = org.Hs.eg.db, mouse = org.Mm.eg.db,
    rat = org.Rn.eg.db, stop("不支持的物种"))
  
  result <- bitr(genes, fromType = from, toType = to, OrgDb = org_db)
  
  n_unmapped <- length(genes) - nrow(result)
  if (n_unmapped > 0) {
    cat("⚠️", n_unmapped, "个基因未匹配\n")
    unmapped <- setdiff(genes, result[[from]])
    if (!drop_unmapped) cat("  未匹配:", paste(head(unmapped, 10), collapse = ", "), "\n")
  }
  
  result
}

# ============================================================
# setReadable —— 结果中 ENTREZID 转回 SYMBOL
# ============================================================
# enrichGO 结果默认就是可读的（readable=TRUE）
# enrichKEGG 结果需要手动转换
kegg_result <- setReadable(kegg_result, OrgDb = org.Hs.eg.db, keyType = "ENTREZID")
# 转换后 geneID 列显示 SYMBOL 而非 ENTREZID
```

---

## 📊 GO 富集分析

### 1. 三大本体

```r
# ============================================================
# GO 三大本体（Ontology）
# ============================================================
# BP (Biological Process) — 生物过程 → 最常用
#   例：cell proliferation, immune response, apoptosis
# MF (Molecular Function) — 分子功能
#   例：protein binding, kinase activity, DNA binding
# CC (Cellular Component) — 细胞组分
#   例：nucleus, plasma membrane, cytoskeleton

# 基因列表（ENTREZID）
gene_entrez <- c("7157", "672", "1956", "4609", "7422")  # TP53, BRCA1, EGFR...

# ============================================================
# enrichGO —— GO 过表达分析
# ============================================================
go_bp <- enrichGO(
  gene         = gene_entrez,           # 基因列表（ENTREZID）
  OrgDb        = org.Hs.eg.db,          # 注释数据库
  keyType      = "ENTREZID",            # 输入基因类型
  ont          = "BP",                  # 本体类型
  pvalueCutoff = 0.05,                  # p值阈值
  qvalueCutoff = 0.2,                   # q值阈值
  minGSSize    = 10,                    # 基因集最小大小
  maxGSSize    = 500,                   # 基因集最大大小
  readable     = TRUE,                  # 自动转SYMBOL
  pool         = FALSE                  # 是否合并三大本体
)

# MF 和 CC
go_mf <- enrichGO(gene = gene_entrez, OrgDb = org.Hs.eg.db, ont = "MF", readable = TRUE)
go_cc <- enrichGO(gene = gene_entrez, OrgDb = org.Hs.eg.db, ont = "CC", readable = TRUE)

# ============================================================
# 一次性分析三大本体
# ============================================================
go_all <- enrichGO(gene = gene_entrez, OrgDb = org.Hs.eg.db,
                    ont = "BP", readable = TRUE)  # 分别运行再合并
# 或用 pool = TRUE（不推荐，混合解释困难）

# 查看结果
head(as.data.frame(go_bp))
# ID  Description  GeneRatio  BgRatio  pvalue  p.adjust  qvalue  geneID  Count
```

### 2. GO 结果解读

```r
# ============================================================
# 结果列含义
# ============================================================
# ID          → GO term ID (如 GO:0006915)
# Description → GO term 描述 (如 "apoptotic process")
# GeneRatio   → 输入基因中属于该term的比例 (如 "15/200")
# BgRatio     → 背景基因中属于该term的比例 (如 "250/20000")
# pvalue      → Fisher精确检验p值
# p.adjust    → BH校正后p值
# qvalue      → q值
# geneID      → 属于该term的输入基因列表
# Count       → 属于该term的输入基因数

# 富集比 = (Count/输入基因总数) / (BgCount/背景基因总数)
# 富集比 > 1 且 p.adjust < 0.05 → 显著富集

# 提取特定信息
go_bp@result %>% filter(p.adjust < 0.01 & Count >= 5)
```

---

## 🧬 KEGG 富集分析

```r
# ============================================================
# enrichKEGG —— KEGG 通路富集
# ============================================================
kegg <- enrichKEGG(
  gene         = gene_entrez,           # ENTREZID
  organism     = "hsa",                 # 物种代码
  keyType      = "kegg",                # 基因ID类型
  pvalueCutoff = 0.05,
  qvalueCutoff = 0.2,
  minGSSize    = 10,
  maxGSSize    = 500,
  use_internal_data = FALSE             # 用在线数据（推荐）
)

# 常见物种代码：
# hsa = 人类    mmu = 小鼠    rno = 大鼠
# dme = 果蝇    cel = 线虫    dre = 斑马鱼
# bta = 牛      ssc = 猪      gga = 鸡

# 转为可读
kegg <- setReadable(kegg, OrgDb = org.Hs.eg.db, keyType = "ENTREZID")

# ============================================================
# KEGG 通路图标注（pathview）
# ============================================================
library(pathview)

# 单通路标注
pathview(gene.data = ranked_list,          # log2FC 排序列表
         pathway.id = "hsa04110",          # Cell cycle
         species = "hsa",
         out.suffix = "treatment")

# 批量标注 top 通路
top_kegg <- head(kegg@result$ID, 5)
for (pid in top_kegg) {
  pathview(gene.data = ranked_list, pathway.id = pid,
           species = "hsa", out.suffix = "treatment")
}

# ============================================================
# browseKEGG —— 在浏览器中查看
# ============================================================
browseKEGG(kegg, "hsa04110")
```

---

## 📈 GSEA 分析

### 1. 准备排序列表

```r
# ============================================================
# 基因排序列表 —— GSEA 的输入
# ============================================================

# 从 DESeq2 结果生成
library(DESeq2)
res_df <- as.data.frame(res) %>% rownames_to_column("gene")

# SYMBOL → ENTREZID 并排序
ids <- bitr(res_df$gene, fromType = "SYMBOL", toType = "ENTREZID",
            OrgDb = org.Hs.eg.db)

ranked_list <- res_df %>%
  inner_join(ids, by = c("gene" = "SYMBOL")) %>%
  filter(!is.na(log2FoldChange)) %>%
  arrange(desc(log2FoldChange)) %>%
  select(ENTREZID, log2FoldChange) %>%
  deframe()

# 检查排序
head(ranked_list)    # 应该从大到小
tail(ranked_list)    # 应该是负值

# 去除重复和NA
ranked_list <- ranked_list[!duplicated(names(ranked_list))]
ranked_list <- ranked_list[!is.na(ranked_list)]
ranked_list <- sort(ranked_list, decreasing = TRUE)
```

### 2. GSEA 核心函数

```r
# ============================================================
# gseGO —— GSEA-GO 分析
# ============================================================
gsea_go <- gseGO(
  geneList     = ranked_list,            # 排序列表
  OrgDb        = org.Hs.eg.db,
  ont          = "BP",
  minGSSize    = 10,
  maxGSSize    = 500,
  pvalueCutoff = 0.05,
  verbose      = FALSE
)

# ============================================================
# gseKEGG —— GSEA-KEGG 分析
# ============================================================
gsea_kegg <- gseKEGG(
  geneList     = ranked_list,
  organism     = "hsa",
  minGSSize    = 10,
  maxGSSize    = 500,
  pvalueCutoff = 0.05,
  verbose      = FALSE
)

# 转为可读
gsea_kegg <- setReadable(gsea_kegg, OrgDb = org.Hs.eg.db, keyType = "ENTREZID")

# ============================================================
# GSEA vs ORA 对比
# ============================================================
# ORA（enrichGO/enrichKEGG）：
#   输入：显著差异基因列表（二值：显著/不显著）
#   优点：简单直观
#   缺点：丢失幅度信息，阈值敏感
#
# GSEA（gseGO/gseKEGG）：
#   输入：全部基因的排序列表（连续值）
#   优点：不需要阈值，利用全部信息，检测温和变化
#   缺点：计算慢，解读稍复杂
#
# 建议：两种都做！ORA看强信号，GSEA看弱信号

# ============================================================
# GSEA 结果解读
# ============================================================
# NES (Normalized Enrichment Score) → 标准化富集分数
#   NES > 0 → 通路在排序列表顶部富集（上调相关）
#   NES < 0 → 通路在排序列表底部富集（下调相关）
# |NES| > 1 → 有生物学意义
# p.adjust < 0.25 → 显著（GSEA阈值通常比ORA宽松）
```

---

## 🗄️ 其他数据库富集

```r
# ============================================================
# ReactomePA —— Reactome 通路富集
# ============================================================
library(ReactomePA)

reactome <- enrichPathway(
  gene = gene_entrez,
  organism = "human",
  pvalueCutoff = 0.05,
  qvalueCutoff = 0.2,
  readable = TRUE
)

# GSEA 版本
gsea_reactome <- gsePathway(
  geneList = ranked_list,
  organism = "human",
  pvalueCutoff = 0.05,
  verbose = FALSE
)

# ============================================================
# MSigDB 基因集富集
# ============================================================
library(msigdbr)

# 查看可用基因集
msigdbr_collections()

# 获取 Hallmark 基因集
hallmark_genesets <- msigdbr(species = "Homo sapiens", category = "H")

# 转为 GSEA 可用格式
hallmark_list <- split(hallmark_genesets$gene_symbol, hallmark_genesets$gs_name)

# 用 clusterProfiler 的 GSEA
gsea_hallmark <- GSEA(
  geneList = ranked_list,
  TERM2GENE = hallmark_genesets %>% select(gs_name, gene_symbol),
  pvalueCutoff = 0.05,
  verbose = FALSE
)

# C2 (Curated) 基因集
c2_genesets <- msigdbr(species = "Homo sapiens", category = "C2")

# C7 (Immunologic) 基因集
c7_genesets <- msigdbr(species = "Homo sapiens", category = "C7")

# ============================================================
# DO —— 疾病本体富集
# ============================================================
library(DOSE)

do_enrich <- enrichDO(
  gene = gene_entrez,
  ont = "DO",
  pvalueCutoff = 0.05,
  qvalueCutoff = 0.2,
  readable = TRUE
)

# NCG (Network of Cancer Genes)
ncg_enrich <- enrichNCG(gene = gene_entrez, pvalueCutoff = 0.05)

# ============================================================
# 自定义基因集富集
# ============================================================
# TERM2GENE 格式：term_name, gene_id
custom_terms <- data.frame(
  term = c("CellDeath", "CellDeath", "CellDeath", "Immune", "Immune"),
  gene = c("TP53", "BAX", "CASP3", "CD8A", "PDCD1")
)

custom_enrich <- enricher(
  gene = gene_entrez,
  TERM2GENE = custom_terms,
  pvalueCutoff = 0.05,
  qvalueCutoff = 0.2
)

# GSEA 版本
custom_gsea <- GSEA(
  geneList = ranked_list,
  TERM2GENE = custom_terms,
  pvalueCutoff = 0.05,
  verbose = FALSE
)
```

---

## 🎨 可视化全套

### 1. 柱状图

```r
# ============================================================
# enrich_plot_bar —— 富集柱状图
# ============================================================
enrich_plot_bar <- function(enrich_result, top_n = 20, showCategory = NULL,
                             title = NULL, font_size = 10) {
  if (is.null(showCategory)) showCategory <- top_n
  
  barplot(enrich_result, showCategory = showCategory,
          font.size = font_size) +
    labs(title = title) +
    scale_fill_continuous(low = "red", high = "blue", name = "p.adjust") +
    theme(plot.title = element_text(hjust = 0.5, face = "bold", size = 14))
}

# 使用: enrich_plot_bar(go_bp, top_n = 15, title = "GO BP")
```

### 2. 气泡图

```r
# ============================================================
# enrich_plot_dot —— 富集气泡图（推荐！信息最丰富）
# ============================================================
enrich_plot_dot <- function(enrich_result, top_n = 20, showCategory = NULL,
                             title = NULL, font_size = 9) {
  if (is.null(showCategory)) showCategory <- top_n
  
  dotplot(enrich_result, showCategory = showCategory,
          font.size = font_size) +
    labs(title = title) +
    theme(plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
          axis.text.y = element_text(size = font_size))
}
```

### 3. 基因概念网络图

```r
# ============================================================
# cnetplot —— 基因-Term 网络图
# ============================================================

# 基础
cnetplot(go_bp, showCategory = 5)

# 带 fold change
cnetplot(go_bp, showCategory = 5,
         foldChange = ranked_list,          # 颜色表示log2FC
         circular = FALSE,                  # 非圆形布局
         colorEdge = TRUE)                  # 边按term着色

# 圆形布局
cnetplot(go_bp, showCategory = 5, circular = TRUE, foldChange = ranked_list)
```

### 4. 富集通路关系图

```r
# ============================================================
# emapplot —— 富集 Term 间关系图
# ============================================================
emapplot(go_bp, showCategory = 20)

# 带 pie 显示基因比例
emapplot(go_bp, showCategory = 20,
         pie = "count",                     # 按基因数
         pie_scale = 1.2)                   # pie 大小
```

### 5. GSEA 经典图

```r
# ============================================================
# gseaplot —— GSEA 单通路图
# ============================================================

# 经典三面板图
gseaplot(gsea_go, geneSetID = 1)                    # 第1个通路
gseaplot(gsea_go, geneSetID = "GO:0006915")         # 指定GO ID
gseaplot2(gsea_go, geneSetID = 1:3)                 # 多通路叠加

# ============================================================
# enrich_plot_gsea —— GSEA Ridge Plot（推荐！）
# ============================================================
enrich_plot_gsea <- function(gsea_result, top_n = 5, title = "GSEA") {
  ridgeplot(gsea_result, showCategory = top_n) +
    labs(title = title) +
    theme(plot.title = element_text(hjust = 0.5, face = "bold"))
}

# ============================================================
# gseaplot2 —— 多通路对比
# ============================================================
# 显示前5个上调和下调通路
top_up <- gsea_go@result %>% filter(NES > 0) %>% slice_head(n = 3) %>% pull(ID)
top_down <- gsea_go@result %>% filter(NES < 0) %>% slice_head(n = 3) %>% pull(ID)

gseaplot2(gsea_go, geneSetID = c(top_up, top_down),
          subplots = 1:3)   # 1=running score, 2=position, 3=原始分布
```

### 6. UpSet 图

```r
# ============================================================
# upsetplot —— 多 Term 间基因重叠
# ============================================================
upsetplot(go_bp, showCategory = 20)

# 简化版
upsetplot(go_bp, n = 10)
```

### 7. 热图

```r
# ============================================================
# enrichplot::heatplot —— 基因-Term 热图
# ============================================================
heatplot(go_bp, showCategory = 10, foldChange = ranked_list)
```

### 8. 树图

```r
# ============================================================
# treeplot —— GO 层级关系树图
# ============================================================
treeplot(go_bp, showCategory = 30)
```

### 9. 发文级组合图

```r
# ============================================================
# enrich_combined_plot —— 发文级组合图
# ============================================================
enrich_combined_plot <- function(go_result, kegg_result,
                                  ranked_list = NULL, top_n = 10) {
  
  p1 <- dotplot(go_result, showCategory = top_n) + ggtitle("GO BP") + theme(plot.title = element_text(hjust = 0.5, face = "bold"))
  p2 <- dotplot(kegg_result, showCategory = top_n) + ggtitle("KEGG") + theme(plot.title = element_text(hjust = 0.5, face = "bold"))
  p3 <- emapplot(go_result, showCategory = 15) + ggtitle("GO Network")
  
  if (!is.null(ranked_list)) {
    p4 <- cnetplot(go_result, showCategory = 5, foldChange = ranked_list, circular = FALSE)
    combined <- (p1 | p2) / (p3 | p4) + plot_annotation(tag_levels = "A")
  } else {
    combined <- (p1 | p2) / p3 + plot_annotation(tag_levels = "A")
  }
  
  combined
}

# 使用：enrich_combined_plot(go_bp, kegg, ranked_list)
```

---

## 🔄 多组比较富集

```r
# ============================================================
# compareCluster —— 多组富集比较
# ============================================================

# 准备数据：每个cluster/组的基因列表
# 格式：data.frame，两列（基因 + 分组标记）
cluster_genes <- bind_rows(
  tibble(gene = up_genes, cluster = "Up"),
  tibble(gene = down_genes, cluster = "Down")
)

# 转换ID
ids <- bitr(cluster_genes$gene, fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)
cluster_genes <- cluster_genes %>% inner_join(ids, by = c("gene" = "SYMBOL"))

# 多组比较
cc <- compareCluster(
  ENTREZID ~ cluster,
  data = cluster_genes,
  fun = "enrichGO",
  OrgDb = org.Hs.eg.db,
  ont = "BP",
  pvalueCutoff = 0.05
)

# 可视化
dotplot(cc, showCategory = 10) + ggtitle("Up vs Down DEGs")
dotplot(cc, showCategory = 10, by = "geneRatio")   # 按基因比例排序

# ============================================================
# 多个cluster的marker基因比较
# ============================================================
# 从 Seurat FindAllMarkers 结果
cluster_list <- split(pbmc.markers$gene, pbmc.markers$cluster)

# 转换ID
cluster_df <- purrr::imap_dfr(cluster_list, ~ tibble(ENTREZID = bitr(.x, fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)$ENTREZID, cluster = .y))

cc_seurat <- compareCluster(
  ENTREZID ~ cluster,
  data = cluster_df,
  fun = "enrichGO",
  OrgDb = org.Hs.eg.db,
  ont = "BP",
  pvalueCutoff = 0.05
)

dotplot(cc_seurat, showCategory = 5) + ggtitle("Cluster Enrichment")
```

---

## 🧪 生信实战封装

### 1. 简化冗余 GO Terms

```r
# ============================================================
# simplify —— 去除GO冗余term
# ============================================================
go_simplified <- simplify(go_bp, cutoff = 0.7, by = "p.adjust", select_fun = min)
# cutoff: 语义相似度阈值，0.7表示相似度>0.7的term会被合并
# by: 用哪个指标选择代表性term
# select_fun: 选择最小（最显著）的

# 对比
cat("原始:", nrow(as.data.frame(go_bp)), "terms\n")
cat("简化:", nrow(as.data.frame(go_simplified)), "terms\n")
```

### 2. 上调/下调分别富集

```r
# ============================================================
# split_enrichment —— 按上调/下调分别富集
# ============================================================
split_enrichment <- function(res_df, gene_col = "gene", fc_col = "log2FoldChange",
                              padj_col = "padj", fc_cutoff = 1, padj_cutoff = 0.05,
                              species = "human", ont = "BP") {
  
  org_db <- switch(species, human = org.Hs.eg.db, mouse = org.Mm.eg.db)
  library(org_db, character.only = TRUE)
  
  up_genes <- res_df %>% filter(!!sym(fc_col) > fc_cutoff & !!sym(padj_col) < padj_cutoff) %>% pull(!!sym(gene_col))
  down_genes <- res_df %>% filter(!!sym(fc_col) < -fc_cutoff & !!sym(padj_col) < padj_cutoff) %>% pull(!!sym(gene_col))
  
  up_ids <- bitr(up_genes, "SYMBOL", "ENTREZID", org_db)$ENTREZID
  down_ids <- bitr(down_genes, "SYMBOL", "ENTREZID", org_db)$ENTREZID
  
  up_go <- enrichGO(up_ids, OrgDb = org_db, ont = ont, readable = TRUE, pvalueCutoff = 0.05)
  down_go <- enrichGO(down_ids, OrgDb = org_db, ont = ont, readable = TRUE, pvalueCutoff = 0.05)
  
  up_kegg <- tryCatch(enrichKEGG(up_ids, organism = switch(species, human="hsa", mouse="mmu")), error = function(e) NULL)
  down_kegg <- tryCatch(enrichKEGG(down_ids, organism = switch(species, human="hsa", mouse="mmu")), error = function(e) NULL)
  
  cat("上调基因:", length(up_genes), "→ GO:", nrow(as.data.frame(up_go)), "terms\n")
  cat("下调基因:", length(down_genes), "→ GO:", nrow(as.data.frame(down_go)), "terms\n")
  
  list(up_go = up_go, down_go = down_go, up_kegg = up_kegg, down_kegg = down_kegg)
}
```

### 3. 自动出图+保存

```r
# ============================================================
# auto_enrich_plots —— 自动出全套富集图
# ============================================================
auto_enrich_plots <- function(enrich_result, ranked_list = NULL,
                               name = "enrichment", save_dir = ".",
                               top_n = 15) {
  dir.create(save_dir, showWarnings = FALSE, recursive = TRUE)
  
  df <- as.data.frame(enrich_result)
  if (nrow(df) == 0) { cat("⚠️ 无显著富集结果\n"); return(NULL) }
  
  # 气泡图
  p <- dotplot(enrich_result, showCategory = top_n)
  ggsave(file.path(save_dir, paste0(name, "_dotplot.png")), p, width = 10, height = 8, dpi = 300)
  
  # 柱状图
  p <- barplot(enrich_result, showCategory = top_n)
  ggsave(file.path(save_dir, paste0(name, "_barplot.png")), p, width = 10, height = 8, dpi = 300)
  
  # 网络图
  tryCatch({
    p <- cnetplot(enrich_result, showCategory = 5, foldChange = ranked_list, circular = FALSE)
    ggsave(file.path(save_dir, paste0(name, "_cnetplot.png")), p, width = 12, height = 10, dpi = 300)
  }, error = function(e) cat("  cnetplot 失败\n"))
  
  # 关系图
  tryCatch({
    p <- emapplot(enrich_result, showCategory = 15)
    ggsave(file.path(save_dir, paste0(name, "_emapplot.png")), p, width = 12, height = 10, dpi = 300)
  }, error = function(e) cat("  emapplot 失败\n"))
  
  # 热图
  tryCatch({
    p <- heatplot(enrich_result, showCategory = 10, foldChange = ranked_list)
    ggsave(file.path(save_dir, paste0(name, "_heatplot.png")), p, width = 12, height = 8, dpi = 300)
  }, error = function(e) cat("  heatplot 失败\n"))
  
  # GSEA 特有
  if (inherits(enrich_result, "gseaResult")) {
    tryCatch({
      p <- ridgeplot(enrich_result, showCategory = 10)
      ggsave(file.path(save_dir, paste0(name, "_ridgeplot.png")), p, width = 10, height = 8, dpi = 300)
    }, error = function(e) cat("  ridgeplot 失败\n"))
    
    tryCatch({
      p <- gseaplot2(enrich_result, geneSetID = 1:3)
      ggsave(file.path(save_dir, paste0(name, "_gseaplot.png")), p, width = 10, height = 6, dpi = 300)
    }, error = function(e) cat("  gseaplot 失败\n"))
  }
  
  cat("✅ 图表已保存至:", save_dir, "\n")
}
```

---

## ❓ 常见问题速查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 全部 padj = NA | 输入基因太少或背景不匹配 | 增加基因数，检查ID类型 |
| KEGG 报错连接失败 | 网络问题 | 重试或用 `use_internal_data=TRUE` |
| GO 结果太多 | 阈值太宽松 | 降低 `pvalueCutoff`，用 `simplify()` 去冗余 |
| GSEA 结果太少 | 排序列表不对 | 确认降序排列，检查ENTREZID转换 |
| geneRatio 和 BgRatio 含义 | — | "15/200" = 输入200基因中15个属于该term |
| SYMBOL 输入报错 | enrichGO 需要 ENTREZID | 先用 `bitr()` 转换，或 `keyType="SYMBOL"` |
| 小鼠KEGG分析报错 | organism参数错误 | 用 `"mmu"` 不是 `"mouse"` |
| pathview 生成空图 | 基因ID不匹配 | 确保用 ENTREZID 的排序列表 |
| 可视化报错 "not enough terms" | 结果太少 | 放宽阈值或增加输入基因 |

---

## 📋 函数速查表

### 封装函数速查

| 函数 | 用途 | 调用示例 |
|------|------|----------|
| `run_enrichment()` | 一键全流程 | `run_enrichment(gene_df=deg, species="human")` |
| `auto_id_convert()` | 基因ID转换 | `auto_id_convert(genes, to="ENTREZID")` |
| `enrich_plot_bar()` | 柱状图 | `enrich_plot_bar(go_bp, top_n=15)` |
| `enrich_plot_dot()` | 气泡图 | `enrich_plot_dot(go_bp, top_n=15)` |
| `enrich_plot_gsea()` | GSEA ridge | `enrich_plot_gsea(gsea_go)` |
| `enrich_combined_plot()` | 组合图 | `enrich_combined_plot(go_bp, kegg)` |
| `split_enrichment()` | 上调/下调分别富集 | `split_enrichment(res_df)` |
| `auto_enrich_plots()` | 自动出图 | `auto_enrich_plots(go_bp, name="GO_BP")` |

### clusterProfiler 核心函数速查

```
# ORA（过表达分析）
enrichGO(gene, OrgDb, ont, pvalueCutoff)       # GO富集
enrichKEGG(gene, organism, pvalueCutoff)         # KEGG富集
enrichPathway(gene, organism)                     # Reactome富集
enrichDO(gene, ont)                               # 疾病本体
enricher(gene, TERM2GENE)                         # 自定义基因集

# GSEA（基因集富集）
gseGO(geneList, OrgDb, ont)                       # GSEA-GO
gseKEGG(geneList, organism)                       # GSEA-KEGG
gsePathway(geneList, organism)                    # GSEA-Reactome
GSEA(geneList, TERM2GENE)                         # GSEA自定义

# 多组比较
compareCluster(gene~cluster, fun="enrichGO")      # 多组比较

# 简化
simplify(go_result, cutoff=0.7)                   # 去冗余

# ID转换
bitr(genes, fromType, toType, OrgDb)              # 基因ID转换
setReadable(result, OrgDb, keyType)               # 结果转可读

# 可视化
dotplot()   barplot()   cnetplot()   emapplot()
heatplot()  upsetplot() treeplot()   ridgeplot()
gseaplot()  gseaplot2()
```

---

> 📌 **核心原则**：SYMBOL→bitr→ENTREZID→enrich→simplify→dotplot。ORA看强信号，GSEA看弱信号，两种都做。
> 一行运行：`run_enrichment(gene_df = deg_results, species = "human")` 完成 GO+KEGG+GSEA 全套。
