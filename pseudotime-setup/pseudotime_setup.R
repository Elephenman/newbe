#!/usr/bin/env Rscript
# 拟时序分析启动器(Monocle3/Slingshot)
get_input <- function(p,d=NULL){v=readline(paste0(p," [默认: ",d,"]: "));if(v==""||is.null(v))return(d);return(v)}
cat("============================================================\n")
cat("  🔄 拟时序分析启动器\n")
cat("============================================================\n\n")
obj_path <- get_input("Seurat对象路径(rds)","seurat.rds")
root <- get_input("root定义(cluster号/基因名)","3")
method <- get_input("轨迹方法(monocle3/slingshot)","monocle3")

obj <- readRDS(obj_path)
suppressPackageStartupMessages({
  if (method == "monocle3") {
    if (!require(monocle3)) { cat("需要monocle3\n"); quit(status=1) }
    cds <- as.cell_data_set(obj)
    cds <- learn_graph(cds)
    root_cells <- colnames(cds)[cds@clusters$UMAP$partitions == root | obj@meta.data$seurat_clusters == root]
    cds <- order_cells(cds, root_cells = root_cells[1])
    p <- plot_cells(cds, color_cells_by = "pseudotime")
    ggsave("pseudotime_monocle3.png", p, width=10, height=8, dpi=300)
    write.csv(data.frame(cell=colnames(cds), pseudotime=monocle3::pseudotime(cds)), "pseudotime_coords.csv", row.names=FALSE)
  } else {
    if (!require(slingshot)) { cat("需要slingshot\n"); quit(status=1) }
    rd <- obj@reductions$UMAP@cell.embeddings
    cl <- obj@meta.data$seurat_clusters
    sce <- slingshot::slingshot(rd, clusterLabels=cl, start.clus=root)
    p <- plot(rd, col=slingshot::slingPseudotime(sce), pch=16)
    png("pseudotime_slingshot.png", width=800, height=600)
    print(p); dev.off()
    write.csv(data.frame(cell=rownames(rd), pseudotime=slingshot::slingPseudotime(sce)), "pseudotime_coords.csv", row.names=FALSE)
  }
})
cat("✅ 拟时序分析完成\n")