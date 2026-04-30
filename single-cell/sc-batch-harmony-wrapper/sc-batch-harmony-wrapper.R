# Harmony批次校正包装
library(Seurat)
library(harmony)

get_input <- function(prompt, default) {
  val <- readline(prompt=paste0(prompt, " [默认: ", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat(paste(rep("=", 60), collapse=""), "\n")
cat("  🔬 Harmony批次校正器\n")
cat(paste(rep("=", 60), collapse=""), "\n")

rds_file <- get_input("Seurat对象路径", "seurat_obj.rds")
batch_key <- get_input("批次变量列名", "batch")
theta <- as.numeric(get_input("Harmony theta参数", "2"))
output_file <- get_input("校正后对象路径", "harmony_corrected.rds")

obj <- readRDS(rds_file)
cat(paste0("\n✅ 加载对象: ", ncol(obj), " cells\n"))

obj <- RunPCA(obj, verbose=FALSE)
obj <- RunHarmony(obj, group.by.vars=batch_key, theta=theta)
obj <- RunUMAP(obj, reduction="harmony", dims=1:30, verbose=FALSE)
obj <- FindNeighbors(obj, reduction="harmony", dims=1:30)
obj <- FindClusters(obj, resolution=0.5)

n_batch <- length(unique(obj[[batch_key]]))
cat(paste0("\n✅ Harmony校正完成\n"))
cat(paste0("  批次数: ", n_batch, "\n"))
cat(paste0("  聚类数: ", length(unique(Idents(obj))), "\n"))

saveRDS(obj, output_file)
cat(paste0("📄 校正后对象: ", output_file, "\n"))