# 空间区域边界检测
library(Seurat)

get_input <- function(prompt, default) {
  val <- readline(prompt=paste0(prompt, " [默认: ", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat(paste(rep("=", 60), collapse=""), "\n")
cat("  🔬 空间区域边界检测器\n")
cat(paste(rep("=", 60), collapse=""), "\n")

rds_file <- get_input("空间Seurat对象路径", "spatial_obj.rds")
n_zones <- as.integer(get_input("预期区域数", "3"))
method <- get_input("边界检测方法(kmeans/spatial)", "kmeans")
output_file <- get_input("边界结果路径", "zone_boundaries.tsv")

obj <- readRDS(rds_file)
cat(paste0("\n✅ 加载对象: ", ncol(obj), " spots\n"))

coords <- GetTissueCoordinates(obj)
expr <- GetAssayData(obj, slot="data")

pca_coords <- prcomp(t(as.matrix(expr)), scale.=TRUE)$x[, 1:10]

if (method == "kmeans") {
  km <- kmeans(pca_coords, centers=n_zones)
  zones <- km$cluster
} else {
  km <- kmeans(coords[, 1:2], centers=n_zones)
  zones <- km$cluster
}

obj$zone <- as.factor(zones)

results <- data.frame(
  Cell=colnames(obj),
  X=coords[,1], Y=coords[,2],
  Zone=zones
)

write.table(results, output_file, sep="\t", quote=FALSE, row.names=FALSE)

cat(paste0("\n✅ 边界检测完成\n"))
for (z in 1:n_zones) {
  cat(paste0("  Zone ", z, ": ", sum(zones==z), " spots\n"))
}
cat(paste0("📄 结果: ", output_file, "\n"))