#!/usr/bin/env Rscript
# Seurat质控一键流水线
suppressPackageStartupMessages({
  if (!require(Seurat)) { cat("需要Seurat\n"); quit(status=1) }
  library(ggplot2)
})

get_input <- function(prompt, default = NULL) {
  val <- readline(prompt = paste0(prompt, " [默认: ", default, "]: "))
  if (val == "" || is.null(val)) return(default); return(val)
}

cat("============================================================\n")
cat("  🧬 Seurat质控流水线\n")
cat("============================================================\n\n")

data_path <- get_input("数据路径(10X目录/h5/matrix.csv)", "data/")
species <- get_input("物种(human/mouse)", "human")
nfeature_min <- as.integer(get_input("nFeature最小值", "200"))
nfeature_max <- as.integer(get_input("nFeature最大值", "5000"))
mito_max <- as.integer(get_input("mito%上限", "20"))
make_plots <- get_input("是否出QC图(yes/no)", "yes")

# 加载数据
if (dir.exists(data_path)) {
  obj <- Read10X(data.path = data_path)
} else if (grepl(".h5", data_path)) {
  obj <- Read10X_h5(data_path)
} else {
  obj <- as.matrix(read.csv(data_path, row.names = 1))
}

seurat <- CreateSeuratObject(counts = obj, project = "QC")
mito_pattern <- if (species == "human") "^MT-" else "^mt-"
seurat[["percent.mt"]] <- PercentageFeatureSet(seurat, pattern = mito_pattern)

cat("原始细胞数:", ncol(seurat), "\n")
cat("原始基因数:", nrow(seurat), "\n")
cat("mito%均值:", mean(seurat$percent.mt), "\n")

# 过滤
seurat <- subset(seurat, subset = nFeature_RNA > nfeature_min & nFeature_RNA < nfeature_max & percent.mt < mito_max)
cat("过滤后细胞数:", ncol(seurat), "\n")

# QC图
if (make_plots == "yes") {
  p1 <- VlnPlot(seurat, features = c("nFeature_RNA", "nCount_RNA", "percent.mt"), ncol = 3)
  p2 <- FeatureScatter(seurat, feature1 = "nCount_RNA", feature2 = "percent.mt")
  p3 <- FeatureScatter(seurat, feature1 = "nCount_RNA", feature2 = "nFeature_RNA")

  ggsave("seurat_qc_violin.png", p1, width = 12, height = 6, dpi = 300)
  combined_scatter <- p2 + p3
  ggsave("seurat_qc_scatter.png", combined_scatter, width = 10, height = 5, dpi = 300)
  cat("✅ QC图已保存\n")
}

# 保存对象
saveRDS(seurat, "seurat_qc_filtered.rds")
cat("✅ Seurat质控完成: seurat_qc_filtered.rds\n")