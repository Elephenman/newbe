# 单细胞聚类稳定性评估+分辨率优化
# 对Seurat对象在不同分辨率下重复聚类，评估稳定性

cat("=", rep("-", 59), "\n", sep="")
cat("  单细胞聚类稳定性评估+分辨率优化\n")
cat("=", rep("-", 59), "\n", sep="")
cat("\n")

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

rds_file     <- get_input("Seurat对象RDS路径(含PCA)", "seurat.rds")
output_dir   <- get_input("输出目录", "stability_results")
resolutions  <- get_input("分辨率列表(逗号分隔)", "0.2,0.4,0.6,0.8,1.0,1.2")
n_repeats    <- as.integer(get_input("重复次数", "3"))
n_pcs        <- as.integer(get_input("使用PC数", "30"))

cat("\nRDS:     ", rds_file, "\n")
cat("Output:  ", output_dir, "\n")
cat("Res:     ", resolutions, "\n")
cat("Repeats: ", n_repeats, "\n")
cat("PCs:     ", n_pcs, "\n\n")

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
library(Seurat)
library(ggplot2)

dir.create(output_dir, showWarnings=FALSE, recursive=TRUE)

obj <- readRDS(rds_file)
res_list <- as.numeric(strsplit(resolutions, ",")[[1]])

cat("[Processing] 评估聚类稳定性...\n")

# Run clustering at each resolution
stability_results <- data.frame()
ari_matrix_list <- list()

for (res in res_list) {
  cat("  Resolution:", res, "\n")

  # Multiple repeats with slightly different PC subsets to test stability
  clusterings <- list()
  for (rep_i in 1:n_repeats) {
    # Use slightly different PC combinations for each repeat
    pc_use <- min(n_pcs, ncol(obj@reductions$pca))
    if (n_repeats > 1 && rep_i > 1) {
      # Subsample PCs slightly for stability testing
      pc_subset <- sample(1:pc_use, max(pc_use - 2, 5))
      pc_subset <- sort(pc_subset)
    } else {
      pc_subset <- 1:pc_use
    }

    obj_tmp <- FindNeighbors(obj, dims=pc_subset, verbose=FALSE)
    obj_tmp <- FindClusters(obj_tmp, resolution=res, verbose=FALSE)
    clusterings[[rep_i]] <- obj_tmp$seurat_clusters
  }

  # Calculate pairwise ARI between repeats
  if (requireNamespace("mclust", quietly=TRUE)) {
    ari_vals <- c()
    for (i in 1:(length(clusterings)-1)) {
      for (j in (i+1):length(clusterings)) {
        ari <- mclust::adjustedRandIndex(as.integer(clusterings[[i]]),
                                          as.integer(clusterings[[j]]))
        ari_vals <- c(ari_vals, ari)
      }
    }
    mean_ari <- mean(ari_vals)
  } else {
    # Simple agreement rate as fallback
    mean_ari <- NA
    cat("    [WARN] mclust未安装，跳过ARI计算\n")
  }

  n_clusters <- length(unique(clusterings[[1]]))

  stability_results <- rbind(stability_results, data.frame(
    Resolution=res,
    N_Clusters=n_clusters,
    Mean_ARI=mean_ari
  ))
}

# Save results
write.csv(stability_results, file.path(output_dir, "stability_results.csv"), row.names=FALSE)

# Plot
if (nrow(stability_results) > 1) {
  p <- ggplot(stability_results, aes(x=Resolution, y=N_Clusters)) +
    geom_line(color="#3C5488", linewidth=1) +
    geom_point(color="#E64B35", size=3) +
    theme_bw() +
    labs(title="Clusters vs Resolution", x="Resolution", y="Number of Clusters")
  ggsave(file.path(output_dir, "resolution_clusters.png"), p, width=8, height=6, dpi=300)

  if (!all(is.na(stability_results$Mean_ARI))) {
    p2 <- ggplot(stability_results, aes(x=Resolution, y=Mean_ARI)) +
      geom_line(color="#00A087", linewidth=1) +
      geom_point(color="#E64B35", size=3) +
      theme_bw() +
      labs(title="Clustering Stability (ARI)", x="Resolution", y="Mean ARI") +
      ylim(0, 1)
    ggsave(file.path(output_dir, "stability_ari.png"), p2, width=8, height=6, dpi=300)
  }
}

# Recommendation
if (!all(is.na(stability_results$Mean_ARI))) {
  best_res <- stability_results$Resolution[which.max(stability_results$Mean_ARI)]
  cat("\n推荐分辨率:", best_res, "(ARI最高)\n")
} else {
  cat("\n无法推荐(ARI未计算)\n")
}

cat("\n", "=", rep("-", 59), "\n", sep="")
cat("  RESULTS SUMMARY\n")
cat("=", rep("-", 59), "\n", sep="")
cat("  Resolutions tested:", length(res_list), "\n")
cat("  Results saved to:  ", output_dir, "\n")
cat("=", rep("-", 59), "\n\n", sep="")
cat("[Done] sc_cluster_stability_checker completed!\n")
