#!/usr/bin/env Rscript
# 空间邻域图构建与可视化

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat("============================================================\n")
cat("  空间邻域图构建\n")
cat("============================================================\n\n")

rds_file <- get_input("Seurat空间对象RDS路径", "spatial.rds")
output_plot <- get_input("输出图片路径(PDF)", "neighbor_graph.pdf")
k_neighbors <- as.integer(get_input("K近邻数", "6"))

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
library(Seurat)

if (!file.exists(rds_file)) { cat("[ERROR] RDS文件不存在\n"); quit(status=1) }

obj <- readRDS(rds_file)
coords <- GetTissueCoordinates(obj)

cat("[Processing] 构建KNN邻域图 (k=", k_neighbors, ")...\n", sep="")

# Build KNN
k_use <- min(k_neighbors, nrow(coords)-1)
knn <- knearneigh(as.matrix(coords), k=k_use)
nb <- knn2nb(knn)

# Build igraph object
if (!requireNamespace("igraph", quietly=TRUE)) { cat("需要igraph\n"); quit(status=1) }
library(igraph)

g <- graph_from_adj_list(nb, mode="undirected")

# Color by cluster if available
vertex_colors <- "steelblue"
if ("seurat_clusters" %in% colnames(obj@meta.data)) {
  clusters <- as.factor(obj$seurat_clusters)
  n_clusters <- nlevels(clusters)
  palette <- rainbow(n_clusters)
  vertex_colors <- palette[as.integer(clusters)]
}

cat("[Processing] 绘制邻域图...\n")

pdf(output_plot, width=10, height=10)
plot(g, vertex.size=0.5, vertex.label=NA, vertex.color=vertex_colors,
     edge.color="gray80", edge.width=0.3,
     layout=as.matrix(coords), main="Spatial Neighbor Graph")
dev.off()

# Also save adjacency list
adj_file <- gsub("\\.pdf$", "_adjacency.csv", output_plot)
edges <- as_edgelist(g)
write.csv(edges, adj_file, row.names=FALSE, col.names=c("From", "To"))

cat("\n============================================================\n")
cat("  RESULTS SUMMARY\n")
cat("============================================================\n")
cat("  Spots:       ", nrow(coords), "\n")
cat("  K:           ", k_use, "\n")
cat("  Edges:       ", ecount(g), "\n")
cat("  Output:      ", output_plot, "\n")
cat("  Adjacency:   ", adj_file, "\n")
cat("============================================================\n\n")
cat("[Done] spatial-neighbor-graph completed!\n")
