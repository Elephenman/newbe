#!/usr/bin/env Rscript
# -*- coding: utf-8 -*-
# 表达矩阵→聚类热图

get_input <- function(prompt, default = NULL) {
  val <- readline(prompt = paste0(prompt, " [默认: ", default, "]: "))
  if (val == "" || is.null(val)) return(default)
  return(val)
}

cat("============================================================\n")
cat("  🔥 表达矩阵聚类热图\n")
cat("============================================================\n\n")

csv_path <- get_input("表达矩阵CSV路径(行=基因,列=样本)", "expression.csv")
log_transform <- get_input("是否log2转换(yes/no)", "yes")
cluster_method <- get_input("聚类方法(hierarchical/kmeans)", "hierarchical")
top_n <- get_input("取topN高变异基因", "500")
color_scheme <- get_input("配色(Nature/Cell/BlueRed)", "Nature")

suppressPackageStartupMessages({
  library(ggplot2)
  if (!require(pheatmap)) { cat("需要pheatmap\n"); quit(status=1) }
})

mat <- as.matrix(read.csv(csv_path, row.names = 1))
if (log_transform == "yes" || log_transform == "y") {
  mat <- log2(mat + 1)
}

# 取topN高变异基因
gene_vars <- apply(mat, 1, var)
top_idx <- order(gene_vars, decreasing = TRUE)[1:min(as.integer(top_n), nrow(mat))]
mat_sub <- mat[top_idx, ]

# 配色
colors <- list(
  Nature = c("#3C5488", "#FFFFFF", "#E64B35"),
  Cell = c("#003366", "#FFFFFF", "#CC0000"),
  BlueRed = c("#0000FF", "#FFFFFF", "#FF0000")
)
pal <- colorRampPalette(colors[[color_scheme]])(100)

out_path <- paste0(tools::file_path_sans_ext(csv_path), "_heatmap.png")
if (cluster_method == "kmeans") {
  pheatmap(mat_sub, color = pal, scale = "row",
           kmeans_k = min(10, nrow(mat_sub) %/% 5),
           filename = out_path, width = 12, height = 10, dpi = 300)
} else {
  pheatmap(mat_sub, color = pal, scale = "row",
           clustering_method = cluster_method,
           filename = out_path, width = 12, height = 10, dpi = 300)
}

cat("✅ 热图已保存:", out_path, "\n")
cat("   基因数:", nrow(mat_sub), "  样本数:", ncol(mat_sub), "\n")