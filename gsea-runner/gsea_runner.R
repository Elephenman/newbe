#!/usr/bin/env Rscript
# -*- coding: utf-8 -*-
# GSEA分析一键运行

get_input <- function(prompt, default = NULL) {
  val <- readline(prompt = paste0(prompt, " [默认: ", default, "]: "))
  if (val == "" || is.null(val)) return(default)
  return(val)
}

cat("============================================================\n")
cat("  🌊 GSEA分析一键运行\n")
cat("============================================================\n\n")

mat_path <- get_input("表达矩阵路径(行=基因,列=样本)", "expression.csv")
group_file <- get_input("分组标签文件(样本名+分组,逗号分隔)", "groups.txt")
gene_set <- get_input("基因集(KEGG/Reactome/custom)", "KEGG")
p_cutoff <- get_input("pvalue阈值", "0.05")
species <- get_input("物种(human/mouse)", "human")

suppressPackageStartupMessages({
  if (!require(fgsea)) { cat("需要fgsea\n"); quit(status=1) }
  library(ggplot2)
})

mat <- as.matrix(read.csv(mat_path, row.names = 1))
groups <- read.csv(group_file, header = FALSE)
group_vec <- setNames(groups$V2, groups$V1)

# 计算ranked list (t-test)
ranked <- sapply(rownames(mat), function(g) {
  g1 <- mat[g, names(group_vec[group_vec == unique(group_vec)[1]])]
  g2 <- mat[g, names(group_vec[group_vec == unique(group_vec)[2]])]
  if (length(g1) < 2 || length(g2) < 2) return(0)
  t.test(g1, g2)$statistic
})
ranked_list <- sort(ranked, decreasing = TRUE)

# 基因集
kegg_org <- if(species == "human") "hsa" else "mmu"
if (gene_set == "KEGG") {
  if (!require(clusterProfiler)) { cat("需要clusterProfiler\n"); quit(status=1) }
  pathways <- gseKEGG(geneList = ranked_list, organism = kegg_org)
} else if (gene_set == "Reactome") {
  if (!require(ReactomePA)) { cat("需要ReactomePA\n"); quit(status=1) }
  pathways <- gsePathway(geneList = ranked_list)
} else {
  pathways <- fgsea(pathways = readLines("custom_pathways.gmt"), stats = ranked_list)
}

out_path <- paste0(tools::file_path_sans_ext(mat_path), "_GSEA.csv")
write.csv(as.data.frame(pathways), out_path, row.names = FALSE)
cat("✅ GSEA结果:", out_path, "\n")
cat("   显著通路数:", nrow(as.data.frame(pathways)), "\n")