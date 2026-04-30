#!/usr/bin/env Rscript
# 空间转录组生态位(Niche)检测与可视化

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat("============================================================\n")
cat("  空间Niche检测\n")
cat("============================================================\n\n")

rds_file <- get_input("Seurat空间对象RDS路径", "spatial.rds")
output_plot <- get_input("输出图片路径", "niche_plot.png")
n_niches <- as.integer(get_input("Niche数量(0=自动)", "4"))
resolution <- as.numeric(get_input("聚类分辨率", "0.5"))
use_spatial <- get_input("使用空间图(yes/no)", "yes")

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
library(Seurat)

if (!file.exists(rds_file)) { cat("[ERROR] RDS文件不存在\n"); quit(status=1) }

obj <- readRDS(rds_file)
cat("[Processing] 加载对象:", ncol(obj), "spots\n")

# Build spatial neighbors
cat("[Processing] 构建空间邻域图...\n")

if (use_spatial == "yes") {
  # Use spatial graph for clustering
  obj <- FindNeighbors(obj, graph="spatial", verbose=FALSE)
  obj <- FindClusters(obj, resolution=resolution, graph="spatial", verbose=FALSE)
} else {
  # Use PCA-based graph
  obj <- FindNeighbors(obj, dims=1:30, verbose=FALSE)
  obj <- FindClusters(obj, resolution=resolution, verbose=FALSE)
}

n_found <- length(unique(obj$seurat_clusters))
cat("[Processing] 检测到", n_found, "个niche\n")

# If user specified n_niches, adjust resolution
if (n_niches > 0 && n_found != n_niches) {
  cat("[Processing] 调整分辨率以匹配目标niche数...\n")
  for (res_try in seq(0.1, 2.0, by=0.1)) {
    obj_tmp <- FindClusters(obj, resolution=res_try,
                            graph=ifelse(use_spatial=="yes", "spatial", "RNA_snn"),
                            verbose=FALSE)
    n_tmp <- length(unique(obj_tmp$seurat_clusters))
    if (n_tmp >= n_niches) {
      obj$niche <- obj_tmp$seurat_clusters
      cat("  Resolution:", res_try, "->", n_tmp, "niches\n")
      break
    }
  }
  if (!("niche" %in% colnames(obj@meta.data))) {
    obj$niche <- obj$seurat_clusters
  }
} else {
  obj$niche <- obj$seurat_clusters
}

# Visualization
cat("[Processing] 生成可视化...\n")

# Spatial plot
p1 <- SpatialDimPlot(obj, group.by="niche", label=TRUE, label.size=3)

# UMAP plot if available
if ("umap" %in% names(obj@reductions)) {
  p2 <- DimPlot(obj, group.by="niche", label=TRUE)
  library(ggplot2)
  combined <- p1 + p2
  ggsave(output_plot, combined, width=16, height=8, dpi=150)
} else {
  ggsave(output_plot, p1, width=8, height=8, dpi=150)
}

# Save niche statistics
niche_stats <- as.data.frame(table(obj$niche))
colnames(niche_stats) <- c("Niche", "N_spots")
write.csv(niche_stats, gsub("\\.png$", "_stats.csv", output_plot), row.names=FALSE)

cat("\n============================================================\n")
cat("  RESULTS SUMMARY\n")
cat("============================================================\n")
cat("  Niches detected:", length(unique(obj$niche)), "\n")
cat("  Niche distribution:\n")
print(table(obj$niche))
cat("  Output:        ", output_plot, "\n")
cat("============================================================\n\n")
cat("[Done] spatial-niche-detector completed!\n")
