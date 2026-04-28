# 按条件提取单细胞子集并保存为新Seurat对象

  rds_file <- ifelse(interactive(), readline("Seurat对象RDS路径 [seurat_obj.rds]: "), "seurat_obj.rds")
  output_rds <- ifelse(interactive(), readline("子集RDS输出路径 [subset.rds]: "), "subset.rds")
  subset_col <- ifelse(interactive(), readline("筛选列名 [seurat_clusters]: "), "seurat_clusters")
  subset_val <- ifelse(interactive(), readline("筛选值(逗号分隔) [0,1,2]: "), "0,1,2")
  library(Seurat)
  obj <- readRDS(rds_file)
  vals <- strsplit(subset_val, ",")[[1]]
  if(subset_col %in% colnames(obj@meta.data)){
    cells <- WhichCells(obj, expression = .data[[subset_col]] %in% vals)
  } else {
    cells <- colnames(obj); cat("警告: 列", subset_col, "不存在\n")
  }
  sub_obj <- subset(obj, cells=cells)
  saveRDS(sub_obj, output_rds)
  cat("子集提取:", ncol(obj), "->", ncol(sub_obj), "cells\n")

