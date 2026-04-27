#!/usr/bin/env Rscript
# 单细胞自动注释辅助
suppressPackageStartupMessages(library(Seurat))
get_input <- function(p,d=NULL){v=readline(paste0(p," [默认: ",d,"]: "));if(v==""||is.null(v))return(d);return(v)}
cat("============================================================\n")
cat("  🔬 细胞类型自动注释\n")
cat("============================================================\n\n")
obj_path <- get_input("Seurat对象路径(rds)","seurat.rds")
marker_file <- get_input("标记基因文件(细胞类型→基因,CSV)","markers.csv")
threshold <- as.integer(get_input("最少匹配N个marker",3))
make_plot <- get_input("是否出UMAP标注图(yes/no)","yes")

obj <- readRDS(obj_path)
markers <- read.csv(marker_file)
annotations <- rep("Unannotated", ncol(obj))

for (i in 1:nrow(markers)) {
  celltype <- markers[i,1]; gene_list <- as.character(markers[i,2:length(markers[i])])
  gene_list <- gene_list[gene_list != "" & !is.na(gene_list)]
  matched <- gene_list[gene_list %in% rownames(obj)]
  if (length(matched) >= threshold) {
    scores <- rowMeans(obj[matched, ]@assays$RNA@data)
    annotations[scores > 0] <- celltype
  }
  cat(celltype, ": matched", length(matched), "markers\n")
}
obj$celltype_annotated <- annotations
if (make_plot == "yes") {
  p <- DimPlot(obj, group.by = "celltype_annotated")
  ggsave("celltype_annotation.png", p, width=10, height=8, dpi=300)
}
saveRDS(obj, "seurat_annotated.rds")
cat("✅ 注释完成: seurat_annotated.rds\n")
cat("   未注释比例:", sum(annotations=="Unannotated")/length(annotations)*100, "%\n")