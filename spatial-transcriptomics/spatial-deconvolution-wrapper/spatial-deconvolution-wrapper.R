#!/usr/bin/env Rscript
# 空间转录组细胞类型反卷积(SPOTlight)

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat("============================================================\n")
cat("  空间转录组反卷积(SPOTlight)\n")
cat("============================================================\n\n")

spatial_rds <- get_input("空间Seurat对象RDS", "spatial.rds")
sc_rds <- get_input("单细胞参考Seurat对象RDS", "reference.rds")
output_rds <- get_input("反卷积结果RDS路径", "deconv.rds")
celltype_col <- get_input("细胞类型列名", "cell_type")

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
if (!requireNamespace("SPOTlight", quietly=TRUE)) {
  cat("[ERROR] 需要SPOTlight包\n"); quit(status=1)
}

library(Seurat)
library(SPOTlight)

if (!file.exists(spatial_rds)) { cat("[ERROR] 空间RDS不存在\n"); quit(status=1) }
if (!file.exists(sc_rds)) { cat("[ERROR] 单细胞RDS不存在\n"); quit(status=1) }

spatial <- readRDS(spatial_rds)
sc_ref <- readRDS(sc_rds)

cat("[Processing] 空间对象:", ncol(spatial), "spots\n")
cat("[Processing] 参考对象:", ncol(sc_ref), "cells\n")

if (!(celltype_col %in% colnames(sc_ref@meta.data))) {
  cat("[ERROR] 细胞类型列不存在:", celltype_col, "\n")
  quit(status=1)
}

Idents(sc_ref) <- celltype_col

cat("[Processing] 查找marker基因...\n")
markers <- FindAllMarkers(sc_ref, only.pos=TRUE, min.pct=0.25, logfc.threshold=0.25)

cat("[Processing] 运行SPOTlight反卷积...\n")
spotlight <- spotlight_deconvolution(
  seurat_sc = sc_ref,
  seurat_sp = spatial,
  markers = markers,
  cluster_id = celltype_col,
  n_samples = 5000
)

saveRDS(spotlight, output_rds)

# Visualization
if ("umap" %in% names(spatial@reductions)) {
  # Add deconvolution results to spatial object
  # SPOTlight returns a matrix of proportions
  if (is.list(spotlight) && "prop" %in% names(spotlight)) {
    prop_mat <- spotlight$prop
    for (ct in colnames(prop_mat)) {
      spatial[[paste0("prop_", ct)]] <- prop_mat[, ct]
    }
    # Plot top cell types
    top_cts <- colnames(prop_mat)[order(colSums(prop_mat), decreasing=TRUE)][1:min(6, ncol(prop_mat))]
    p <- SpatialFeaturePlot(spatial, features=paste0("prop_", top_cts))
    ggsave("deconvolution_proportions.png", p, width=14, height=10, dpi=300)
    cat("反卷积比例图: deconvolution_proportions.png\n")
  }
}

cat("\n============================================================\n")
cat("  RESULTS SUMMARY\n")
cat("============================================================\n")
cat("  Spots:         ", ncol(spatial), "\n")
cat("  Cell types:    ", length(unique(sc_ref@meta.data[[celltype_col]])), "\n")
cat("  Output RDS:    ", output_rds, "\n")
cat("============================================================\n\n")
cat("[Done] Spatial deconvolution completed!\n")
