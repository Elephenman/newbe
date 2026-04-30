# 多拟时序方法结果对比+一致性评估
# 比较不同轨迹推断方法(Monocle3/Slingshot等)的拟时序结果

cat("=", rep("-", 59), "\n", sep="")
cat("  多拟时序方法结果对比+一致性评估\n")
cat("=", rep("-", 59), "\n", sep="")
cat("\n")

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

rds_file     <- get_input("Seurat对象RDS路径(含拟时序)", "seurat.rds")
pt_cols      <- get_input("拟时序列名(逗号分隔,如 pseudotime_monocle,pseudotime_slingshot)", "pseudotime_monocle,pseudotime_slingshot")
output_file  <- get_input("输出CSV路径", "trajectory_comparison.csv")
output_plot  <- get_input("输出对比图路径", "trajectory_comparison.png")

cat("\nRDS:     ", rds_file, "\n")
cat("PT cols: ", pt_cols, "\n")
cat("Output:  ", output_file, "\n\n")

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
library(Seurat)
library(ggplot2)

if (!file.exists(rds_file)) { cat("[ERROR] RDS文件不存在\n"); quit(status=1) }

obj <- readRDS(rds_file)
meta <- obj@meta.data

pt_list <- strsplit(pt_cols, ",")[[1]]
pt_list <- pt_list[pt_list %in% colnames(meta)]

if (length(pt_list) < 2) {
  cat("[ERROR] 需要至少2个拟时序列，找到:", length(pt_list), "\n")
  quit(status=1)
}

cat("[Processing] 比较", length(pt_list), "个拟时序结果...\n")

# Pairwise Spearman correlation
cor_results <- data.frame()
for (i in 1:(length(pt_list)-1)) {
  for (j in (i+1):length(pt_list)) {
    col1 <- pt_list[i]; col2 <- pt_list[j]
    valid <- !is.na(meta[[col1]]) & !is.na(meta[[col2]])
    if (sum(valid) < 10) next
    sp <- cor(meta[[col1]][valid], meta[[col2]][valid], method="spearman")
    pe <- cor(meta[[col1]][valid], meta[[col2]][valid], method="pearson")
    cor_results <- rbind(cor_results, data.frame(
      Method1=col1, Method2=col2,
      Spearman=round(sp, 4), Pearson=round(pe, 4),
      N_cells=sum(valid)
    ))
    cat("  ", col1, "vs", col2, ":", round(sp, 3), "(Spearman)\n")
  }
}

write.csv(cor_results, output_file, row.names=FALSE)

# Scatter plot comparison
if (length(pt_list) >= 2) {
  df <- data.frame(UMAP_1=Embeddings(obj, "umap")[,1],
                   UMAP_2=Embeddings(obj, "umap")[,2])
  for (col in pt_list) {
    df[[col]] <- meta[[col]]
  }

  plots <- lapply(pt_list, function(col) {
    ggplot(df, aes(x=UMAP_1, y=UMAP_2, color=.data[[col]])) +
      geom_point(size=0.5, alpha=0.7) +
      scale_color_viridis_c(na.value="gray80") +
      theme_bw() + labs(title=col, color="Pseudotime") + NoLegend()
  })

  combined <- patchwork::wrap_plots(plots, ncol=min(3, length(plots)))
  ggsave(output_plot, combined, width=6*min(3, length(plots)), height=5, dpi=300)
}

cat("\n", "=", rep("-", 59), "\n", sep="")
cat("  RESULTS SUMMARY\n")
cat("=", rep("-", 59), "\n", sep="")
cat("  Methods compared: ", length(pt_list), "\n")
cat("  Pairwise comparisons:", nrow(cor_results), "\n")
cat("  Output: ", output_file, "\n")
cat("=", rep("-", 59), "\n\n", sep="")
cat("[Done] sc_trajectory_comparer completed!\n")
