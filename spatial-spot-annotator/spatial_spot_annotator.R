#!/usr/bin/env Rscript
# 空间转录组spot自动注释
suppressPackageStartupMessages({
  if (!require(Seurat)) { cat("需要Seurat\n"); quit(status=1) }
  library(ggplot2)
})

get_input <- function(p, d=NULL) {
  v <- readline(prompt=paste0(p, " [默认: ", d, "]: "))
  if (v == "" || is.null(v)) return(d); return(v)
}

cat("============================================================\n")
cat("  空间转录组spot注释\n")
cat("============================================================\n\n")

spatial_path <- get_input("空间Seurat对象路径(rds)", "spatial.rds")
ref_path <- get_input("参考Seurat对象路径(含注释)", "annotated.rds")
method <- get_input("注释方法(transfer/marker)", "transfer")
make_plot <- get_input("是否出空间图(yes/no)", "yes")

spatial <- readRDS(spatial_path)
ref <- readRDS(ref_path)

if (method == "transfer") {
  # TransferData annotation
  # Use appropriate reduction: check for PCA in spatial object
  reduction_method <- "rpca"
  if (!"pca" %in% names(spatial@reductions)) {
    cat("[WARN] spatial对象无PCA，运行PCA...\n")
    spatial <- ScaleData(spatial, verbose=FALSE)
    spatial <- RunPCA(spatial, verbose=FALSE)
  }

  anchors <- FindTransferAnchors(reference = ref, query = spatial,
                                  features = VariableFeatures(ref),
                                  reduction.method = reduction_method)
  predictions <- TransferData(anchorset = anchors, refdata = ref$celltype,
                               weight.reduction = spatial[["pca"]])
  spatial <- AddMetaData(spatial, metadata = predictions)
  spatial$predicted_celltype <- predictions$predicted.id
  
  cat("注释完成:\n")
  cat("  方法: TransferData\n")
  cat("  注释分布:\n")
  print(table(spatial$predicted_celltype))
} else {
  # Marker基因匹配
  cat("请提供marker基因文件(markers.csv: celltype,gene1,gene2,...)\n")
  marker_file <- get_input("marker基因文件路径", "markers.csv")
  markers <- read.csv(marker_file)
  
  for (i in 1:nrow(markers)) {
    celltype <- markers[i, 1]
    gene_list <- as.character(markers[i, 2:length(markers[i])])
    gene_list <- gene_list[gene_list != "" & !is.na(gene_list)]
    matched <- gene_list[gene_list %in% rownames(spatial)]
    
    if (length(matched) >= 3) {
      scores <- rowMeans(spatial[matched, ]@assays$Spatial@data)
      spatial[[paste0("score_", celltype)]] <- scores
    }
    cat(celltype, ": matched", length(matched), "markers\n")
  }
  
  # 基于最高评分分配类型
  score_cols <- grep("^score_", colnames(spatial@meta.data), value = TRUE)
  if (length(score_cols) > 0) {
    max_scores <- apply(spatial@meta.data[, score_cols], 1, which.max)
    spatial$predicted_celltype <- gsub("score_", "", score_cols[max_scores])
  }
}

if (make_plot == "yes") {
  p <- SpatialDimPlot(spatial, group.by = "predicted_celltype")
  ggsave("spatial_annotation.png", p, width=10, height=8, dpi=300)
  cat("空间注释图: spatial_annotation.png\n")
}

saveRDS(spatial, "spatial_annotated.rds")
cat("注释对象: spatial_annotated.rds\n")