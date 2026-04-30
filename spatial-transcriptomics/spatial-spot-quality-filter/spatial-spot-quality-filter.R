# 空间spot质量过滤
library(Seurat)
library(ggplot2)

get_input <- function(prompt, default) {
  val <- readline(prompt=paste0(prompt, " [默认: ", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat(paste(rep("=", 60), collapse=""), "\n")
cat("  🔬 空间Spot质量过滤器\n")
cat(paste(rep("=", 60), collapse=""), "\n")

rds_file <- get_input("空间Seurat对象路径", "spatial_obj.rds")
min_nf <- as.integer(get_input("最小nFeature_RNA", "200"))
max_nf <- as.integer(get_input("最大nFeature_RNA", "8000"))
max_mt <- as.numeric(get_input("最大线粒体比例", "20"))
output_file <- get_input("过滤后对象路径", "filtered_spatial.rds")

obj <- readRDS(rds_file)
cat(paste0("\n✅ 加载对象: ", ncol(obj), " spots\n"))

obj[["percent.mt"]] <- PercentageFeatureSet(obj, pattern="^MT-|^mt-")

cat(paste0("  nFeature范围: ", min(obj$nFeature_RNA), "-", max(obj$nFeature_RNA), "\n"))
cat(paste0("  percent.mt范围: ", round(min(obj$percent.mt),1), "-", round(max(obj$percent.mt),1), "\n"))

obj <- subset(obj, subset=nFeature_RNA > min_nf & nFeature_RNA < max_nf & percent.mt < max_mt)

cat(paste0("\n✅ 过滤完成: ", ncol(obj), " spots保留\n"))

saveRDS(obj, output_file)
cat(paste0("📄 过滤后对象: ", output_file, "\n"))