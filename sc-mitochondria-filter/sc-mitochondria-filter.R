# 根据线粒体基因比例过滤单细胞低质量细胞

  rds_file <- ifelse(interactive(), readline("Seurat对象RDS路径 [seurat_obj.rds]: "), "seurat_obj.rds")
  output_rds <- ifelse(interactive(), readline("过滤后RDS路径 [filtered.rds]: "), "filtered.rds")
  mt_threshold <- ifelse(interactive(), readline("线粒体百分比阈值 [20]: "), "20")
  min_features <- ifelse(interactive(), readline("最低feature数 [200]: "), "200")
  max_features <- ifelse(interactive(), readline("最高feature数 [6000]: "), "6000")
  library(Seurat)
  obj <- readRDS(rds_file)
  if(!"percent.mt" %in% colnames(obj@meta.data))
    obj[["percent.mt"]] <- PercentageFeatureSet(obj, pattern="^MT-|^mt-")
  before <- ncol(obj)
  obj <- subset(obj, subset=nFeature_RNA > as.numeric(min_features) &
                          nFeature_RNA < as.numeric(max_features) &
                          percent.mt < as.numeric(mt_threshold))
  saveRDS(obj, output_rds)
  cat("过滤:", before, "->", ncol(obj), "cells\n")

