#!/usr/bin/env Rscript
# 单细胞doublet检测+过滤
suppressPackageStartupMessages(library(Seurat))
get_input <- function(p,d=NULL){v=readline(paste0(p," [默认: ",d,"]: "));if(v==""||is.null(v))return(d);return(v)}
cat("============================================================\n")
cat("  🔍 Doublet检测\n")
cat("============================================================\n\n")
obj_path <- get_input("Seurat对象路径(rds)","seurat.rds")
method <- get_input("检测方法(DoubletFinder/scDblFinder)","scDblFinder")
rate <- as.numeric(get_input("预期doublet率(%)","5"))
auto_remove <- get_input("是否自动移除(yes/no)","yes")

obj <- readRDS(obj_path)
if (method == "scDblFinder") {
  suppressPackageStartupMessages(if (!require(scDblFinder)) { cat("需要scDblFinder\n"); quit(status=1) })
  sce <- as.SingleCellExperiment(obj)
  sce <- scDblFinder(sce, dbr = rate/100)
  obj$doublet <- sce$scDblFinder.class
} else {
  suppressPackageSeparatorMessages(if (!require(DoubletFinder)) { cat("需要DoubletFinder\n"); quit(status=1) })
  obj <- NormalizeData(obj); obj <- FindVariableFeatures(obj); obj <- ScaleData(obj); obj <- RunPCA(obj)
  sweep.res.list <- paramSweep_v3(obj, PCs=1:10, sct=FALSE)
  sweep.stats <- summarizeSweep(sweep.res.list, GT=FALSE)
  pk <- find.pK(sweep.stats)
  homotypic.prop <- modelHomotypic(obj$seurat_clusters)
  nExp_poi <- round(rate/100 * ncol(obj) * (1-homotypic.prop))
  obj <- doubletFinder_v3(obj, PCs=1:10, pN=0.25, pK=pk$mode_pk, nExp=nExp_poi)
  obj$doublet <- obj$DF.classifications_0.25_pk_mode_pk_nExp
}
dbl_count <- sum(obj$doublet=="Doublet")
cat("检测到doublet:", dbl_count, "(", round(dbl_count/ncol(obj)*100,1), "%)\n")
if (auto_remove=="yes") {
  obj <- subset(obj, subset=doublet=="Singlet")
  cat("移除后细胞数:", ncol(obj), "\n")
}
saveRDS(obj, "seurat_doublet_filtered.rds")
cat("✅ Doublet检测完成\n")