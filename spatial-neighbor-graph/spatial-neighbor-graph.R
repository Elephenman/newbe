# 空间邻域图构建与可视化

  rds_file <- ifelse(interactive(), readline("Seurat空间对象RDS路径 [spatial.rds]: "), "spatial.rds")
  output_plot <- ifelse(interactive(), readline("输出图片路径 [neighbor_graph.png]: "), "neighbor_graph.png")
  k_neighbors <- ifelse(interactive(), readline("K近邻数 [6]: "), "6")
  library(Seurat); library(igraph)
  obj <- readRDS(rds_file)
  coords <- GetTissueCoordinates(obj)
  knn <- knearneigh(as.matrix(coords), k=as.integer(k_neighbors))
  nb <- knn2nb(knn)
  g <- graph_from_adj_list(nb, mode="undirected")
  pdf(output_plot, width=10, height=10)
  plot(g, vertex.size=0.5, vertex.label=NA, edge.color="gray80",
       layout=as.matrix(coords), main="Spatial Neighbor Graph")
  dev.off()
  cat("邻域图:", output_plot, "\n")

