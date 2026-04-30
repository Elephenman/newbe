#!/usr/bin/env Rscript
# 单细胞RNA velocity分析流程包装

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat("============================================================\n")
cat("  RNA Velocity分析\n")
cat("============================================================\n\n")

loom_file <- get_input("Velocyto loom文件路径", "velocyto.loom")
rds_file <- get_input("Seurat对象RDS路径", "seurat_obj.rds")
output_dir <- get_input("输出目录", "velocity_results")

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
if (!requireNamespace("velocyto.R", quietly=TRUE)) {
  cat("[ERROR] 需要velocyto.R包: devtools::install_github('velocyto-team/velocyto.R')\n")
  quit(status=1)
}

library(Seurat)
library(velocyto.R)

if (!file.exists(rds_file)) { cat("[ERROR] RDS文件不存在\n"); quit(status=1) }
if (!file.exists(loom_file)) { cat("[ERROR] loom文件不存在\n"); quit(status=1) }

dir.create(output_dir, showWarnings=FALSE, recursive=TRUE)

cat("[Processing] 加载数据...\n")
obj <- readRDS(rds_file)
ldat <- read.loom.matrices(loom_file)

emat <- ldat$spliced
nmat <- ldat$unspliced

# Intersect cells
cell.ids <- intersect(colnames(emat), colnames(obj))
if (length(cell.ids) == 0) {
  cat("[ERROR] loom和Seurat对象无共同细胞\n")
  quit(status=1)
}

emat <- emat[, cell.ids]
nmat <- nmat[, cell.ids]
cat("[Processing] 共同细胞:", length(cell.ids), "\n")

# Check UMAP exists
if (!"umap" %in% names(obj@reductions)) {
  cat("[ERROR] 未找到UMAP，请先运行RunUMAP\n")
  quit(status=1)
}

cat("[Processing] 计算RNA velocity...\n")
rvel <- gene.relative.velocity.estimates(emat, nmat, deltaT=1, k=20, fit.quantile=0.02)

cat("[Processing] 可视化...\n")
pdf(file.path(output_dir, "velocity.pdf"), width=8, height=8)
show.velocity.on.embedding.cor(Embeddings(obj, "umap")[cell.ids, ],
                                rvel, n=200, scale="sqrt", cex=0.8, arrow.scale=5)
dev.off()

# Also save PNG
png(file.path(output_dir, "velocity.png"), width=2000, height=2000, res=150)
show.velocity.on.embedding.cor(Embeddings(obj, "umap")[cell.ids, ],
                                rvel, n=200, scale="sqrt", cex=0.8, arrow.scale=5)
dev.off()

# Save velocity object
saveRDS(rvel, file.path(output_dir, "velocity.rds"))

cat("\n============================================================\n")
cat("  RESULTS SUMMARY\n")
cat("============================================================\n")
cat("  Cells analyzed:", length(cell.ids), "\n")
cat("  Output dir:   ", output_dir, "\n")
cat("============================================================\n\n")
cat("[Done] RNA velocity analysis completed!\n")
