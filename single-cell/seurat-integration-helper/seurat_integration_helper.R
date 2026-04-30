# Seurat多样本整合辅助+批次校正评估
# 使用CCA/RPCA进行多样本整合，评估批次效应校正效果

cat("=", rep("-", 59), "\n", sep="")
cat("  Seurat多样本整合辅助+批次校正评估\n")
cat("=", rep("-", 59), "\n", sep="")
cat("\n")

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

input_dir    <- get_input("RDS文件目录(每个样本一个.rds)", "samples/")
batch_col    <- get_input("批次列名", "sample")
method       <- get_input("整合方法(CCA/RPCA)", "CCA")
output_rds   <- get_input("整合后RDS路径", "integrated.rds")
output_dir   <- get_input("输出目录", "integration_results")

cat("\nInput:   ", input_dir, "\n")
cat("Batch:   ", batch_col, "\n")
cat("Method:  ", method, "\n")
cat("Output:  ", output_rds, "\n\n")

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
library(Seurat)
library(ggplot2)

dir.create(output_dir, showWarnings=FALSE, recursive=TRUE)

# Load all RDS files
rds_files <- list.files(input_dir, pattern="\\.rds$", full.names=TRUE)
if (length(rds_files) == 0) {
  cat("[ERROR] 目录中无RDS文件:", input_dir, "\n")
  quit(status=1)
}
cat("[Processing] 找到", length(rds_files), "个样本\n")

obj_list <- lapply(rds_files, function(f) {
  obj <- readRDS(f)
  sample_name <- gsub("\\.rds$", "", basename(f))
  obj$sample <- sample_name
  obj <- NormalizeData(obj, verbose=FALSE)
  obj <- FindVariableFeatures(obj, selection.method="vst", nfeatures=2000, verbose=FALSE)
  cat("  Loaded:", sample_name, "-", ncol(obj), "cells\n")
  return(obj)
})

# Integration
cat("[Processing] 整合样本...\n")
n_anchors <- ifelse(method == "RPCA", 30, 5)
reduction_method <- ifelse(method == "RPCA", "rpca", "cca")

anchors <- FindIntegrationAnchors(object.list=obj_list,
                                   anchor.features=2000,
                                   reduction=reduction_method)
integrated <- IntegrateData(anchorset=anchors)

# Standard workflow
integrated <- ScaleData(integrated, verbose=FALSE)
integrated <- RunPCA(integrated, verbose=FALSE)
integrated <- RunUMAP(integrated, dims=1:30, verbose=FALSE)

# Before/after comparison: run UMAP on unintegrated data too
DefaultAssay(integrated) <- "RNA"
integrated <- ScaleData(integrated, verbose=FALSE)
integrated <- RunPCA(integrated, verbose=FALSE)
integrated <- RunUMAP(integrated, reduction="pca", dims=1:30,
                       reduction.name="umap.unintegrated", verbose=FALSE)

# Plot comparison
p1 <- DimPlot(integrated, group.by=batch_col, reduction="umap.unintegrated") +
      ggtitle("Before Integration") + NoLegend()
p2 <- DimPlot(integrated, group.by=batch_col, reduction="umap") +
      ggtitle("After Integration") + NoLegend()

ggsave(file.path(output_dir, "integration_comparison.png"),
       p1 + p2, width=14, height=6, dpi=300)

DefaultAssay(integrated) <- "integrated"

# Save
saveRDS(integrated, output_rds)

cat("\n", "=", rep("-", 59), "\n", sep="")
cat("  RESULTS SUMMARY\n")
cat("=", rep("-", 59), "\n", sep="")
cat("  Samples integrated:", length(rds_files), "\n")
cat("  Method:           ", method, "\n")
cat("  Total cells:      ", ncol(integrated), "\n")
cat("  Output RDS:       ", output_rds, "\n")
cat("  Output dir:       ", output_dir, "\n")
cat("=", rep("-", 59), "\n\n", sep="")
cat("[Done] seurat_integration_helper completed!\n")
