# 聚类分辨率自动优化
library(Seurat)

get_input <- function(prompt, default) {
  val <- readline(prompt=paste0(prompt, " [默认: ", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat(paste(rep("=", 60), collapse=""), "\n")
cat("  🔬 聚类分辨率优化器\n")
cat(paste(rep("=", 60), collapse=""), "\n")

rds_file <- get_input("Seurat对象路径", "seurat_obj.rds")
min_res <- as.numeric(get_input("最小分辨率", "0.1"))
max_res <- as.numeric(get_input("最大分辨率", "2.0"))
step <- as.numeric(get_input("分辨率步长", "0.1"))
output_file <- get_input("优化结果路径", "resolution_optimization.tsv")

obj <- readRDS(rds_file)
cat(paste0("\n✅ 加载Seurat对象: ", ncol(obj), " cells\n"))

resolutions <- seq(min_res, max_res, by=step)
results <- data.frame()

for (res in resolutions) {
  obj <- FindClusters(obj, resolution=res, verbose=FALSE)
  n_clusters <- length(unique(Idents(obj)))
  avg_size <- mean(table(Idents(obj)))
  min_size <- min(table(Idents(obj)))
  stability <- 1 - (min_size / avg_size)
  
  results <- rbind(results, data.frame(
    Resolution=res, N_Clusters=n_clusters,
    Avg_Cluster_Size=avg_size, Min_Cluster_Size=min_size,
    Stability_Score=stability
  ))
}

optimal <- results[which.max(results$Stability_Score), ]
cat(paste0("\n✅ 最优分辨率: ", optimal$Resolution, "\n"))
cat(paste0("  聚类数: ", optimal$N_Clusters, "\n"))
cat(paste0("  稳定性评分: ", round(optimal$Stability_Score, 3), "\n"))

write.table(results, output_file, sep="\t", quote=FALSE, row.names=FALSE)
cat(paste0("📄 结果: ", output_file, "\n"))