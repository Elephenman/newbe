#!/usr/bin/env Rscript
# 单细胞marker基因批量查找
suppressPackageStartupMessages({
  if (!require(Seurat)) { cat("需要Seurat\n"); quit(status=1) }
  library(ggplot2)
})

get_input <- function(p, d=NULL) {
  v <- readline(prompt=paste0(p, " [默认: ", d, "]: "))
  if (v == "" || is.null(v)) return(d); return(v)
}

cat("============================================================\n")
cat("  Marker基因查找\n")
cat("============================================================\n\n")

obj_path <- get_input("Seurat对象路径(rds)", "seurat.rds")
method <- get_input("查找方法(FindAllMarkers/cosg)", "FindAllMarkers")
logfc_threshold <- as.numeric(get_input("logFC阈值", "0.25"))
min_pct <- as.numeric(get_input("min.pct", "0.1"))
top_n <- as.integer(get_input("每cluster取topN", "10"))
make_heatmap <- get_input("是否出热图(yes/no)", "yes")
make_dotplot <- get_input("是否出dot plot(yes/no)", "yes")

obj <- readRDS(obj_path)
Idents(obj) <- "seurat_clusters"

if (method == "FindAllMarkers") {
  markers <- FindAllMarkers(obj, only.pos = TRUE, min.pct = min_pct,
                             logfc.threshold = logfc_threshold)
} else if (method == "cosg") {
  if (!require(cosg)) { cat("需要cosg\n"); markers <- FindAllMarkers(obj, only.pos=TRUE); }
  else { markers <- cosg::cosg(obj, only.pos = TRUE, min.pct = min_pct) }
}

# 每cluster取topN
# Handle Seurat v4 (avg_log2FC) and v5 (avg_log2FC) column names
fc_col <- intersect(c("avg_log2FC", "avg_log", "logFC"), colnames(markers))[1]
if (is.na(fc_col)) fc_col <- colnames(markers)[3]  # fallback to 3rd column
top_markers <- markers %>% group_by(cluster) %>% slice_max(order_by = !!sym(fc_col), n = top_n)

# 保存
write.csv(markers, "all_markers.csv", row.names = FALSE)
write.csv(top_markers, "top_markers.csv", row.names = FALSE)
cat("所有marker: all_markers.csv\n")
cat("Top markers: top_markers.csv\n")

# 热图
if (make_heatmap == "yes") {
  top_genes <- unique(top_markers$gene)
  if (length(top_genes) <= 50) {
    p <- DoHeatmap(obj, features = top_genes, size = 3)
    ggsave("marker_heatmap.png", p, width=12, height=8, dpi=300)
    cat("热图: marker_heatmap.png\n")
  } else {
    cat("基因数太多，热图省略\n")
  }
}

# Dot plot
if (make_dotplot == "yes") {
  top_genes <- unique(top_markers$gene[1:min(20, length(unique(top_markers$gene)))])
  p <- DotPlot(obj, features = top_genes) + RotatedAxis()
  ggsave("marker_dotplot.png", p, width=10, height=6, dpi=300)
  cat("Dot plot: marker_dotplot.png\n")
}

cat("Marker查找完成\n")
cat("  方法:", method, "\n")
cat("  总marker数:", nrow(markers), "\n")
cat("  每cluster topN:", top_n, "\n")