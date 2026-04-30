#!/usr/bin/env Rscript
# -*- coding: utf-8 -*-
# GO/KEGG富集分析一键流水线

get_input <- function(prompt, default = NULL) {
  val <- readline(prompt = paste0(prompt, " [默认: ", default, "]: "))
  if (val == "" || is.null(val)) return(default)
  return(val)
}

cat("============================================================\n")
cat("  🎯 GO/KEGG富集分析流水线\n")
cat("============================================================\n\n")

gene_file <- get_input("基因列表文件路径(每行一个基因)", "genes.txt")
species <- get_input("物种(human/mouse/yeast/zebrafish)", "human")
enrich_type <- get_input("富集类型(GO/KEGG/both)", "both")
padj_cutoff <- get_input("padj阈值", "0.05")
plot_type <- get_input("图片类型(dot/bar)", "dot")

suppressPackageStartupMessages({
  if (!require(clusterProfiler)) { cat("需要clusterProfiler\n"); quit(status=1) }
  library(org.Hs.eg.db)  # 默认human，后续可切换
  library(enrichplot)
  library(ggplot2)
})

genes <- readLines(gene_file)
genes <- trimws(genes)
genes <- genes[genes != ""]
cat("读取基因数:", length(genes), "\n")

# 基因ID转换
org_db <- switch(species,
  human = "org.Hs.eg.db", mouse = "org.Mm.eg.db",
  yeast = "org.Sc.sgd.db", zebrafish = "org.Dr.eg.db",
  "org.Hs.eg.db")
library(org_db, character.only = TRUE)

gene_map <- bitr(genes, fromType = "SYMBOL", toType = c("ENTREZID", "ENSEMBL"),
                  OrgDb = org_db)
entrez_ids <- gene_map$ENTREZID

# GO富集
if (enrich_type == "GO" || enrich_type == "both") {
  ego <- enrichGO(gene = entrez_ids, OrgDb = org_db,
                   ont = "ALL", pAdjustMethod = "BH",
                   pvalueCutoff = 0.05, qvalueCutoff = as.numeric(padj_cutoff))
  
  out_go <- paste0(tools::file_path_sans_ext(gene_file), "_GO_enrichment.csv")
  write.csv(as.data.frame(ego), out_go, row.names = FALSE)
  cat("✅ GO富集结果:", out_go, "\n")
  cat("   显著GO条目数:", nrow(as.data.frame(ego)), "\n")
  
  # 绘图
  go_plot <- paste0(tools::file_path_sans_ext(gene_file), "_GO_plot.png")
  if (plot_type == "dot") {
    p <- dotplot(ego, showCategory = 20) + ggtitle("GO Enrichment")
  } else {
    p <- barplot(ego, showCategory = 20) + ggtitle("GO Enrichment")
  }
  ggsave(go_plot, p, width = 10, height = 8, dpi = 300)
  cat("✅ GO图已保存:", go_plot, "\n")
}

# KEGG富集
if (enrich_type == "KEGG" || enrich_type == "both") {
  kegg_org <- switch(species, human = "hsa", mouse = "mmu", yeast = "sce", zebrafish = "dre", "hsa")
  ekegg <- enrichKEGG(gene = entrez_ids, organism = kegg_org,
                       pvalueCutoff = 0.05, qvalueCutoff = as.numeric(padj_cutoff))
  
  out_kegg <- paste0(tools::file_path_sans_ext(gene_file), "_KEGG_enrichment.csv")
  write.csv(as.data.frame(ekegg), out_kegg, row.names = FALSE)
  cat("✅ KEGG富集结果:", out_kegg, "\n")
  
  kegg_plot <- paste0(tools::file_path_sans_ext(gene_file), "_KEGG_plot.png")
  if (plot_type == "dot") {
    p <- dotplot(ekegg, showCategory = 20) + ggtitle("KEGG Enrichment")
  } else {
    p <- barplot(ekegg, showCategory = 20) + ggtitle("KEGG Enrichment")
  }
  ggsave(kegg_plot, p, width = 10, height = 8, dpi = 300)
  cat("✅ KEGG图已保存:", kegg_plot, "\n")
}

cat("\n✅ 富集分析流水线完成！\n")