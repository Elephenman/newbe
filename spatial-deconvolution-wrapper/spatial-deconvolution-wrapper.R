# 空间转录组细胞类型反卷积(SPOTlight)

  spatial_rds <- ifelse(interactive(), readline("空间Seurat对象RDS [spatial.rds]: "), "spatial.rds")
  sc_rds <- ifelse(interactive(), readline("单细胞参考Seurat对象RDS [reference.rds]: "), "reference.rds")
  output_rds <- ifelse(interactive(), readline("反卷积结果RDS路径 [deconv.rds]: "), "deconv.rds")
  library(Seurat); library(SPOTlight)
  spatial <- readRDS(spatial_rds)
  sc_ref <- readRDS(sc_rds)
  Idents(sc_ref) <- "cell_type"
  markers <- FindAllMarkers(sc_ref, only.pos=TRUE, min.pct=0.25, logfc.threshold=0.25)
  spotlight <- spotlight_deconvolution(seurat_sc=sc_ref, seurat_sp=spatial,
    markers=markers, cluster_id="cell_type", n_samples=5000)
  saveRDS(spotlight, output_rds)
  cat("反卷积完成:", output_rds, "\n")

