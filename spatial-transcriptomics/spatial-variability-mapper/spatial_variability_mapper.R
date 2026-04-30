# 空间基因表达变异度可视化
# 计算基因的空间变异系数，可视化空间表达模式

cat("=", rep("-", 59), "\n", sep="")
cat("  空间基因表达变异度可视化\n")
cat("=", rep("-", 59), "\n", sep="")
cat("\n")

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

spatial_rds  <- get_input("空间Seurat对象RDS路径", "spatial.rds")
genes        <- get_input("目标基因(逗号分隔,留空=自动选择)", "")
output_dir   <- get_input("输出目录", "spatial_variability")
top_n        <- as.integer(get_input("展示topN基因", "9"))

cat("\nRDS:    ", spatial_rds, "\n")
cat("Output: ", output_dir, "\n")
cat("TopN:   ", top_n, "\n\n")

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
library(Seurat)
library(ggplot2)

if (!file.exists(spatial_rds)) { cat("[ERROR] RDS文件不存在\n"); quit(status=1) }

obj <- readRDS(spatial_rds)
dir.create(output_dir, showWarnings=FALSE, recursive=TRUE)

# Select genes
if (genes != "") {
  gene_list <- strsplit(genes, ",")[[1]]
} else {
  # Auto-select: most variable genes
  obj <- FindSpatialVariableFeatures(obj, selection.method="moransi")
  gene_list <- VariableFeatures(obj)[1:min(top_n, length(VariableFeatures(obj)))]
}

# Filter to genes present in the object
gene_list <- gene_list[gene_list %in% rownames(obj)]
if (length(gene_list) == 0) {
  cat("[ERROR] 无有效基因\n"); quit(status=1)
}

cat("[Processing] 可视化", length(gene_list), "个基因的空间表达...\n")

# Calculate variability metrics
var_stats <- data.frame()
for (gene in gene_list) {
  expr <- GetAssayData(obj, slot="data")[gene, ]
  cv <- sd(expr) / mean(expr)  # coefficient of variation
  var_stats <- rbind(var_stats, data.frame(Gene=gene, CV=cv, Mean=mean(expr), SD=sd(expr)))
}
var_stats <- var_stats[order(-var_stats$CV), ]
write.csv(var_stats, file.path(output_dir, "variability_stats.csv"), row.names=FALSE)

# Spatial feature plots
for (i in seq(1, length(gene_list), by=9)) {
  batch <- gene_list[i:min(i+8, length(gene_list))]
  p <- SpatialFeaturePlot(obj, features=batch)
  ggsave(file.path(output_dir, paste0("spatial_expr_", ceiling(i/9), ".png")),
         p, width=min(4*length(batch), 20), height=4*ceiling(length(batch)/3), dpi=300)
}

# Variability barplot
p <- ggplot(var_stats, aes(x=reorder(Gene, CV), y=CV)) +
  geom_bar(stat="identity", fill="#3C5488") +
  coord_flip() +
  theme_bw() +
  labs(title="Spatial Expression Variability (CV)", x="Gene", y="Coefficient of Variation")
ggsave(file.path(output_dir, "variability_barplot.png"), p, width=8, height=6, dpi=300)

cat("\n", "=", rep("-", 59), "\n", sep="")
cat("  RESULTS SUMMARY\n")
cat("=", rep("-", 59), "\n", sep="")
cat("  Genes analyzed:  ", length(gene_list), "\n")
cat("  Output dir:      ", output_dir, "\n")
cat("  Stats CSV:       variability_stats.csv\n")
cat("=", rep("-", 59), "\n\n", sep="")
cat("[Done] spatial_variability_mapper completed!\n")
