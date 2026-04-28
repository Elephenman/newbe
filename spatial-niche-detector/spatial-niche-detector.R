# 空间转录组生态位(Niche)检测与可视化

  rds_file <- ifelse(interactive(), readline("Seurat空间对象RDS路径 [spatial.rds]: "), "spatial.rds")
  output_plot <- ifelse(interactive(), readline("输出图片路径 [niche_plot.png]: "), "niche_plot.png")
  n_niches <- ifelse(interactive(), readline("Niche数量 [4]: "), "4")
  library(Seurat)
  obj <- readRDS(rds_file)
  obj <- FindNeighbors(obj, graph="spatial")
  obj <- FindClusters(obj, resolution=0.5, graph="spatial")
  p <- SpatialDimPlot(obj, group.by="seurat_clusters", label=TRUE)
  ggsave(output_plot, p, width=8, height=8, dpi=150)
  cat("Niche检测完成:", output_plot, "\n")

