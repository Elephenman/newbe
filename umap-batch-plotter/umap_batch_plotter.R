#!/usr/bin/env Rscript
# UMAP按多维度批量分色绘图
suppressPackageStartupMessages(library(Seurat))
get_input <- function(p,d=NULL){v=readline(paste0(p," [默认: ",d,"]: "));if(v==""||is.null(v))return(d);return(v)}
cat("============================================================\n")
cat("  🎨 UMAP批量绘图\n")
cat("============================================================\n\n")
obj_path <- get_input("Seurat对象路径(rds)","seurat.rds")
dims <- get_input("分组维度列表(逗号分隔)","cluster,celltype,sample")
combo <- get_input("是否组合大图(yes/no)","yes")
palette <- get_input("配色方案(Set2/Paired/Nature)","Set2")
obj <- readRDS(obj_path)
dims_list <- strsplit(dims, ",")[[1]]
for (d in dims_list) {
  if (!(d %in% colnames(obj@meta.data))) { cat("⚠",d,"不存在\n"); continue }
  p <- DimPlot(obj, group.by=d, cols=palette)
  ggsave(paste0("UMAP_",d,".png"), p, width=8, height=6, dpi=300)
  cat("✅ UMAP_",d,".png\n")
}
if (combo=="yes" && length(dims_list)>1) {
  plots <- lapply(dims_list, function(d) DimPlot(obj, group.by=d)+NoLegend())
  combined <- CombinePlots(plots, ncol=2)
  ggsave("UMAP_combined.png", combined, width=14, height=10, dpi=300)
  cat("✅ 组合图: UMAP_combined.png\n")
}