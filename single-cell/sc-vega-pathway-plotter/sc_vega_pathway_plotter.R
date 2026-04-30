# 单细胞通路活性小提琴图+统计
# 使用Seurat的AddModuleScore计算通路活性，绘制小提琴图

cat("=", rep("-", 59), "\n", sep="")
cat("  单细胞通路活性小提琴图+统计\n")
cat("=", rep("-", 59), "\n", sep="")
cat("\n")

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

rds_file     <- get_input("Seurat对象RDS路径", "seurat.rds")
pathway_file <- get_input("通路基因集文件(CSV: pathway,gene1;gene2;...)", "pathways.csv")
group_col    <- get_input("分组列名", "seurat_clusters")
output_plot  <- get_input("输出图片路径", "pathway_violin.png")
output_csv   <- get_input("输出统计CSV", "pathway_stats.csv")

cat("\nRDS:      ", rds_file, "\n")
cat("Pathways: ", pathway_file, "\n")
cat("Group:    ", group_col, "\n")
cat("Output:   ", output_plot, "\n\n")

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
library(Seurat)
library(ggplot2)

if (!file.exists(rds_file)) { cat("[ERROR] RDS文件不存在\n"); quit(status=1) }
if (!file.exists(pathway_file)) { cat("[ERROR] 通路文件不存在\n"); quit(status=1) }

obj <- readRDS(rds_file)

# Parse pathway file
pw_df <- read.csv(pathway_file, stringsAsFactors=FALSE, header=FALSE)
colnames(pw_df) <- c("pathway", "genes")

pathway_list <- list()
for (i in 1:nrow(pw_df)) {
  pw_name <- pw_df$pathway[i]
  gene_str <- pw_df$genes[i]
  genes <- unique(strsplit(gene_str, "[;|,]")[[1]])
  genes <- genes[genes != "" & !is.na(genes)]
  pathway_list[[pw_name]] <- genes
}

cat("[Processing] 计算", length(pathway_list), "个通路评分...\n")

# Add module scores
for (pw_name in names(pathway_list)) {
  genes <- pathway_list[[pw_name]]
  genes_present <- genes[genes %in% rownames(obj)]
  if (length(genes_present) < 3) {
    cat("  [WARN]", pw_name, "only", length(genes_present), "genes found\n")
    next
  }
  obj <- AddModuleScore(obj, features=list(genes_present),
                        name=pw_name, ctrl=min(5, length(genes_present)))
  cat("  Scored:", pw_name, "(", length(genes_present), "genes)\n")
}

# Identify score columns
score_cols <- grep("^[A-Za-z].*\\d$", colnames(obj@meta.data), value=TRUE)
# Match back to pathway names
score_map <- list()
for (pw_name in names(pathway_list)) {
  matches <- grep(paste0("^", pw_name), score_cols, value=TRUE)
  if (length(matches) > 0) score_map[[pw_name]] <- matches[1]
}

# Validate group column
if (!(group_col %in% colnames(obj@meta.data))) {
  cat("[ERROR] 分组列不存在:", group_col, "\n")
  quit(status=1)
}

# Statistics
stats_df <- data.frame()
for (pw_name in names(score_map)) {
  col <- score_map[[pw_name]]
  for (grp in unique(obj@meta.data[[group_col]])) {
    vals <- obj@meta.data[obj@meta.data[[group_col]] == grp, col]
    stats_df <- rbind(stats_df, data.frame(
      Pathway=pw_name, Group=grp,
      Mean=round(mean(vals, na.rm=TRUE), 4),
      Median=round(median(vals, na.rm=TRUE), 4),
      SD=round(sd(vals, na.rm=TRUE), 4),
      N=sum(!is.na(vals))
    ))
  }
}
write.csv(stats_df, output_csv, row.names=FALSE)

# Violin plot
if (length(score_map) > 0) {
  # Melt for plotting
  plot_df <- obj@meta.data[, c(group_col, unlist(score_map)), drop=FALSE]
  colnames(plot_df)[2:ncol(plot_df)] <- names(score_map)

  library_df <- reshape2::melt(plot_df, id.vars=group_col,
                                variable.name="Pathway", value.name="Score")

  p <- ggplot(library_df, aes(x=.data[[group_col]], y=Score, fill=.data[[group_col]])) +
    geom_violin(alpha=0.7, scale="width") +
    geom_boxplot(width=0.1, outlier.size=0.3) +
    facet_wrap(~Pathway, scales="free_y") +
    theme_bw() +
    labs(title="Pathway Activity Scores", x=group_col, y="Module Score") +
    theme(axis.text.x=element_text(angle=45, hjust=1))

  n_pathways <- length(score_map)
  ggsave(output_plot, p, width=max(8, n_pathways*3), height=max(6, n_pathways*2), dpi=300)
}

cat("\n", "=", rep("-", 59), "\n", sep="")
cat("  RESULTS SUMMARY\n")
cat("=", rep("-", 59), "\n", sep="")
cat("  Pathways scored:", length(score_map), "\n")
cat("  Stats CSV:     ", output_csv, "\n")
cat("  Violin plot:   ", output_plot, "\n")
cat("=", rep("-", 59), "\n\n", sep="")
cat("[Done] sc_vega_pathway_plotter completed!\n")
