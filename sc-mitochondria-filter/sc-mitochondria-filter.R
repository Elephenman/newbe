#!/usr/bin/env Rscript
# 根据线粒体基因比例过滤单细胞低质量细胞

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat("============================================================\n")
cat("  单细胞线粒体过滤\n")
cat("============================================================\n\n")

rds_file <- get_input("Seurat对象RDS路径", "seurat_obj.rds")
output_rds <- get_input("过滤后RDS路径", "filtered.rds")
mt_threshold <- as.numeric(get_input("线粒体百分比阈值", "20"))
min_features <- as.integer(get_input("最低feature数", "200"))
max_features <- as.integer(get_input("最高feature数", "6000"))

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
library(Seurat)

if (!file.exists(rds_file)) { cat("[ERROR] RDS文件不存在\n"); quit(status=1) }

obj <- readRDS(rds_file)
cat("[Processing] 加载对象:", ncol(obj), "cells\n")

# Calculate percent.mt if not present
if (!"percent.mt" %in% colnames(obj@meta.data)) {
  cat("[Processing] 计算线粒体基因比例...\n")
  obj[["percent.mt"]] <- PercentageFeatureSet(obj, pattern="^MT-|^mt-")
}

# Print before stats
cat("\n过滤前统计:\n")
cat("  细胞数:       ", ncol(obj), "\n")
cat("  nFeature_RNA: ", median(obj$nFeature_RNA), "(median)\n")
cat("  percent.mt:   ", round(median(obj$percent.mt), 2), "%(median)\n")

# Filter
before <- ncol(obj)
obj <- subset(obj, subset = nFeature_RNA > min_features &
                         nFeature_RNA < max_features &
                         percent.mt < mt_threshold)

cat("\n过滤后统计:\n")
cat("  细胞数:       ", ncol(obj), "\n")
cat("  保留率:       ", round(ncol(obj)/before*100, 1), "%\n")

# QC plots
tryCatch({
  library(ggplot2)
  p <- VlnPlot(obj, features=c("nFeature_RNA", "nCount_RNA", "percent.mt"), ncol=3)
  ggsave("mt_filter_violin.png", p, width=12, height=5, dpi=150)
  cat("  QC图: mt_filter_violin.png\n")
}, error=function(e) {})

saveRDS(obj, output_rds)

cat("\n============================================================\n")
cat("  RESULTS SUMMARY\n")
cat("============================================================\n")
cat("  Before:       ", before, "cells\n")
cat("  After:        ", ncol(obj), "cells\n")
cat("  Filtered:     ", before - ncol(obj), "cells\n")
cat("  MT threshold: ", mt_threshold, "%\n")
cat("  Output:       ", output_rds, "\n")
cat("============================================================\n\n")
cat("[Done] sc-mitochondria-filter completed!\n")
