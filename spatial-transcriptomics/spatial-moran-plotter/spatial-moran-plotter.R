#!/usr/bin/env Rscript
# 计算空间基因表达的Moran's I自相关统计量

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat("============================================================\n")
cat("  空间Moran's I自相关分析\n")
cat("============================================================\n\n")

rds_file <- get_input("Seurat空间对象RDS路径", "spatial.rds")
genes <- get_input("目标基因(逗号分隔,留空=自动选择)", "")
output_file <- get_input("输出CSV路径", "moran_results.csv")
output_plot <- get_input("输出散点图路径", "moran_plot.png")
k_neighbors <- as.integer(get_input("K近邻数", "6"))

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
if (!requireNamespace("spdep", quietly=TRUE)) { cat("需要spdep\n"); quit(status=1) }
library(Seurat)
library(spdep)

if (!file.exists(rds_file)) { cat("[ERROR] RDS文件不存在\n"); quit(status=1) }

obj <- readRDS(rds_file)

# Select genes
if (genes == "") {
  gl <- VariableFeatures(obj)[1:min(20, length(VariableFeatures(obj)))]
} else {
  gl <- strsplit(genes, ",")[[1]]
}

gl <- gl[gl %in% rownames(obj)]
if (length(gl) == 0) { cat("[ERROR] 无有效基因\n"); quit(status=1) }

cat("[Processing] 分析", length(gl), "个基因的Moran's I...\n")

# Build spatial weights
coords <- GetTissueCoordinates(obj)
nb <- knn2nb(knearneigh(as.matrix(coords), k=min(k_neighbors, nrow(coords)-1)))
lw <- nb2listw(nb, style="W")

# Calculate Moran's I for each gene
results <- data.frame(Gene=character(), Moran_I=numeric(), p_value=numeric(),
                       Expectation=numeric(), stringsAsFactors=FALSE)

for (g in gl) {
  expr <- GetAssayData(obj, slot="data")[g, ]
  if (var(expr) == 0) next
  tryCatch({
    mi <- moran.test(as.numeric(expr), lw)
    results <- rbind(results, data.frame(
      Gene=g,
      Moran_I=round(mi$estimate[1], 4),
      p_value=mi$p.value,
      Expectation=round(mi$estimate[2], 4)
    ))
  }, error=function(e) {
    cat("  [WARN]", g, "Moran test failed\n")
  })
}

# Sort by Moran's I
results <- results[order(-results$Moran_I), ]
write.csv(results, output_file, row.names=FALSE)

# Plot
if (nrow(results) > 0) {
  library(ggplot2)
  results$Significant <- ifelse(results$p_value < 0.05, "Yes", "No")

  p <- ggplot(results, aes(x=reorder(Gene, Moran_I), y=Moran_I, fill=Significant)) +
    geom_bar(stat="identity") +
    coord_flip() +
    scale_fill_manual(values=c("No"="#8491B4", "Yes"="#E64B35")) +
    theme_bw() +
    labs(title="Moran's I Spatial Autocorrelation",
         x="Gene", y="Moran's I", fill="p < 0.05")

  ggsave(output_plot, p, width=10, height=max(6, nrow(results)*0.4), dpi=300)
}

cat("\n============================================================\n")
cat("  RESULTS SUMMARY\n")
cat("============================================================\n")
cat("  Genes tested:  ", length(gl), "\n")
cat("  Results:       ", nrow(results), "\n")
if (nrow(results) > 0) {
  cat("  Top Moran's I: ", results$Gene[1], "(", results$Moran_I[1], ")\n")
  cat("  Significant:   ", sum(results$p_value < 0.05), "\n")
}
cat("  Output:        ", output_file, "\n")
cat("============================================================\n\n")
cat("[Done] spatial-moran-plotter completed!\n")
