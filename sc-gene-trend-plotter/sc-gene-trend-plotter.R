#!/usr/bin/env Rscript
# 单细胞基因沿伪时间趋势图

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat("============================================================\n")
cat("  基因沿伪时间趋势图\n")
cat("============================================================\n\n")

rds_file <- get_input("Seurat对象RDS路径(含伪时间)", "seurat_obj.rds")
genes <- get_input("目标基因(逗号分隔,留空=自动选择)", "")
pseudotime_col <- get_input("伪时间列名", "pseudotime")
output_plot <- get_input("输出图片路径", "gene_trend.png")
smooth_method <- get_input("平滑方法(loess/gam)", "loess")

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
library(Seurat)
library(ggplot2)

if (!file.exists(rds_file)) { cat("[ERROR] RDS文件不存在\n"); quit(status=1) }

obj <- readRDS(rds_file)

if (!(pseudotime_col %in% colnames(obj@meta.data))) {
  cat("[ERROR] 伪时间列不存在:", pseudotime_col, "\n")
  cat("  可用列:", paste(colnames(obj@meta.data), collapse=", "), "\n")
  quit(status=1)
}

# Select genes
if (genes == "") {
  gl <- VariableFeatures(obj)[1:min(6, length(VariableFeatures(obj)))]
} else {
  gl <- strsplit(genes, ",")[[1]]
}

# Filter to genes in object
gl <- gl[gl %in% rownames(obj)]
if (length(gl) == 0) {
  cat("[ERROR] 无有效基因\n"); quit(status=1)
}
cat("[Processing] 绘制", length(gl), "个基因趋势...\n")

pt <- obj@meta.data[[pseudotime_col]]

# Build data frame
df_list <- lapply(gl, function(g) {
  expr <- GetAssayData(obj, slot="data")[g, ]
  data.frame(Gene=g, Pseudotime=pt, Expression=as.numeric(expr))
})
df <- do.call(rbind, df_list)

# Plot
if (smooth_method == "gam" && requireNamespace("mgcv", quietly=TRUE)) {
  p <- ggplot(df, aes(x=Pseudotime, y=Expression)) +
    geom_point(aes(color=Gene), size=0.3, alpha=0.3) +
    stat_smooth(aes(color=Gene), method="gam",
                formula=y~s(x, bs="cs"), se=FALSE) +
    theme_bw() + labs(title="Gene Trends along Pseudotime (GAM)")
} else {
  p <- ggplot(df, aes(x=Pseudotime, y=Expression)) +
    geom_point(aes(color=Gene), size=0.3, alpha=0.3) +
    geom_smooth(aes(color=Gene), method="loess", se=FALSE, span=0.5) +
    theme_bw() + labs(title="Gene Trends along Pseudotime (LOESS)")
}

ggsave(output_plot, p, width=10, height=6, dpi=150)
cat("趋势图:", output_plot, "\n")
cat("[Done] sc-gene-trend-plotter completed!\n")
