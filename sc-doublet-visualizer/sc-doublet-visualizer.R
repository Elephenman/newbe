# 可视化单细胞双细胞检测结果(UMAP标注+分布统计)

  rds_file <- ifelse(interactive(), readline("Seurat对象RDS路径 [seurat_obj.rds]: "), "seurat_obj.rds")
  output_plot <- ifelse(interactive(), readline("输出图片路径 [doublet_viz.png]: "), "doublet_viz.png")
  doublet_col <- ifelse(interactive(), readline("双细胞注释列名 [doublet_score]: "), "doublet_score")
  library(Seurat); library(ggplot2)
  obj <- readRDS(rds_file)
  if(!(doublet_col %in% colnames(obj@meta.data))){ cat("未找到:", doublet_col, "\n"); return(invisible(NULL)) }
  df <- obj@meta.data
  df$UMAP_1 <- Embeddings(obj, "umap")[,1]
  df$UMAP_2 <- Embeddings(obj, "umap")[,2]
  p <- ggplot(df, aes(x=UMAP_1, y=UMAP_2, color=.data[[doublet_col]])) +
    geom_point(size=0.5, alpha=0.7) + theme_bw() + labs(title="Doublet Visualization")
  ggsave(output_plot, p, width=8, height=6, dpi=150)
  cat("双细胞可视化:", output_plot, "\n")

