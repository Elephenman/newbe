#!/usr/bin/env Rscript
# 可视化单细胞双细胞检测结果(UMAP标注+分布统计)

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat("============================================================\n")
cat("  双细胞检测结果可视化\n")
cat("============================================================\n\n")

rds_file <- get_input("Seurat对象RDS路径", "seurat_obj.rds")
output_plot <- get_input("输出图片路径", "doublet_viz.png")
doublet_col <- get_input("双细胞注释列名(数值或分类)", "doublet_score")

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
library(Seurat)
library(ggplot2)

if (!file.exists(rds_file)) { cat("[ERROR] RDS文件不存在\n"); quit(status=1) }

obj <- readRDS(rds_file)

if (!(doublet_col %in% colnames(obj@meta.data))) {
  cat("[ERROR] 列不存在:", doublet_col, "\n")
  cat("  可用列:", paste(colnames(obj@meta.data), collapse=", "), "\n")
  quit(status=1)
}

df <- obj@meta.data

# Check if UMAP exists
if (!"umap" %in% names(obj@reductions)) {
  cat("[ERROR] 未找到UMAP，请先运行RunUMAP\n")
  quit(status=1)
}

df$UMAP_1 <- Embeddings(obj, "umap")[,1]
df$UMAP_2 <- Embeddings(obj, "umap")[,2]

# Determine if doublet_col is numeric or categorical
is_numeric <- is.numeric(df[[doublet_col]])

if (is_numeric) {
  # Numeric score: gradient coloring
  p <- ggplot(df, aes(x=UMAP_1, y=UMAP_2, color=.data[[doublet_col]])) +
    geom_point(size=0.5, alpha=0.7) +
    scale_color_viridis_c(name=doublet_col) +
    theme_bw() + labs(title="Doublet Score Visualization")
} else {
  # Categorical: discrete coloring
  p <- ggplot(df, aes(x=UMAP_1, y=UMAP_2, color=.data[[doublet_col]])) +
    geom_point(size=0.5, alpha=0.7) +
    scale_color_manual(values=c("singlet"="#4DBBD5", "doublet"="#E64B35",
                                 "Singlet"="#4DBBD5", "Doublet"="#E64B35")) +
    theme_bw() + labs(title="Doublet Classification Visualization")
}

ggsave(output_plot, p, width=8, height=6, dpi=150)

# Statistics
cat("\n双细胞统计:\n")
if (is_numeric) {
  cat("  Score分布:\n")
  cat("    Min: ", min(df[[doublet_col]], na.rm=TRUE), "\n")
  cat("    Median:", median(df[[doublet_col]], na.rm=TRUE), "\n")
  cat("    Max: ", max(df[[doublet_col]], na.rm=TRUE), "\n")
} else {
  cat("  分类统计:\n")
  print(table(df[[doublet_col]]))
}

cat("\n双细胞可视化:", output_plot, "\n")
cat("[Done] sc-doublet-visualizer completed!\n")
