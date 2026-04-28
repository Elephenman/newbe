# FeaturePlot批量生成器
library(Seurat)
library(ggplot2)

get_input <- function(prompt, default) {
  val <- readline(prompt=paste0(prompt, " [默认: ", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat(paste(rep("=", 60), collapse=""), "\n")
cat("  🔬 FeaturePlot批量生成器\n")
cat(paste(rep("=", 60), collapse=""), "\n")

rds_file <- get_input("Seurat对象路径", "seurat_obj.rds")
gene_file <- get_input("基因列表文件路径", "genes.txt")
reduction <- get_input("降维方法(umap/tsne)", "umap")
output_dir <- get_input("输出目录", "feature_plots")

dir.create(output_dir, showWarnings=FALSE)

obj <- readRDS(rds_file)
genes <- readLines(gene_file)
genes <- genes[genes != ""]
cat(paste0("\n✅ 加载对象: ", ncol(obj), " cells, ", length(genes), " 基因\n"))

expr_genes <- genes[genes %in% rownames(obj)]
missing <- genes[!(genes %in% rownames(obj))]
if (length(missing) > 0) {
  cat(paste0("  ⚠️ 缺失基因: ", paste(missing, collapse=","), "\n"))
}

for (gene in expr_genes) {
  p <- FeaturePlot(obj, features=gene, reduction=reduction, min.cutoff="q1", max.cutoff="q99")
  pdf_path <- file.path(output_dir, paste0(gene, "_featureplot.pdf"))
  ggsave(pdf_path, p, width=6, height=5)
  png_path <- file.path(output_dir, paste0(gene, "_featureplot.png"))
  ggsave(png_path, p, width=6, height=5, dpi=150)
}

cat(paste0("\n✅ 完成: ", length(expr_genes), " FeaturePlots\n"))
cat(paste0("  输出目录: ", output_dir, "\n"))