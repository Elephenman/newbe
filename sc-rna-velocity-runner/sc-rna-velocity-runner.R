# 单细胞RNA velocity分析流程包装

  loom_file <- ifelse(interactive(), readline("Velocyto loom文件路径 [velocyto.loom]: "), "velocyto.loom")
  rds_file <- ifelse(interactive(), readline("Seurat对象RDS路径 [seurat_obj.rds]: "), "seurat_obj.rds")
  output_dir <- ifelse(interactive(), readline("输出目录 [velocity_results]: "), "velocity_results")
  library(Seurat); library(velocyto.R)
  obj <- readRDS(rds_file)
  ldat <- read.loom.matrices(loom_file)
  emat <- ldat$spliced; nmat <- ldat$unspliced
  cell.ids <- intersect(colnames(emat), colnames(obj))
  emat <- emat[,cell.ids]; nmat <- nmat[,cell.ids]
  rvel <- gene.relative.velocity.estimates(emat, nmat, deltaT=1, k=20, fit.quantile=0.02)
  dir.create(output_dir, showWarnings=FALSE, recursive=TRUE)
  pdf(file.path(output_dir, "velocity.pdf"), width=8, height=8)
  show.velocity.on.embedding.cor(Embeddings(obj, "umap"), rvel, n=200, scale="sqrt", cex=0.8, arrow.scale=5)
  dev.off()
  cat("RNA velocity完成:", output_dir, "\n")

