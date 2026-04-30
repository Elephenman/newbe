#!/usr/bin/env Rscript
# 按条件提取单细胞子集并保存为新Seurat对象

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat("============================================================\n")
cat("  单细胞子集提取\n")
cat("============================================================\n\n")

rds_file <- get_input("Seurat对象RDS路径", "seurat_obj.rds")
output_rds <- get_input("子集RDS输出路径", "subset.rds")
subset_col <- get_input("筛选列名", "seurat_clusters")
subset_val <- get_input("筛选值(逗号分隔)", "0,1,2")
keep_reductions <- get_input("保留降维结果(yes/no)", "yes")

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
library(Seurat)

if (!file.exists(rds_file)) { cat("[ERROR] RDS文件不存在\n"); quit(status=1) }

obj <- readRDS(rds_file)
vals <- strsplit(subset_val, ",")[[1]]

cat("[Processing] 原始对象:", ncol(obj), "cells\n")

if (subset_col %in% colnames(obj@meta.data)) {
  # Get the column values as character for matching
  col_vals <- as.character(obj@meta.data[[subset_col]])
  cells <- colnames(obj)[col_vals %in% vals]
  cat("[Processing] 匹配", length(cells), "cells\n")
} else {
  cat("[WARN] 列", subset_col, "不存在，返回完整对象\n")
  cells <- colnames(obj)
}

# Subset
sub_obj <- subset(obj, cells=cells)

# Optionally re-run PCA/UMAP on subset
if (ncol(sub_obj) > 50) {
  cat("[Processing] 重新计算PCA/UMAP...\n")
  sub_obj <- ScaleData(sub_obj, verbose=FALSE)
  sub_obj <- RunPCA(sub_obj, verbose=FALSE)
  sub_obj <- RunUMAP(sub_obj, dims=1:min(30, ncol(sub_obj@reductions$pca)), verbose=FALSE)
}

saveRDS(sub_obj, output_rds)

cat("\n============================================================\n")
cat("  RESULTS SUMMARY\n")
cat("============================================================\n")
cat("  Before: ", ncol(obj), "cells\n")
cat("  After:  ", ncol(sub_obj), "cells\n")
cat("  Filter: ", subset_col, "in {", paste(vals, collapse=","), "}\n")
cat("  Output: ", output_rds, "\n")
cat("============================================================\n\n")
cat("[Done] sc-subset-extractor completed!\n")
