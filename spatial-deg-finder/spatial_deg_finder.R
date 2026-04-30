# 空间转录组差异表达基因发现
# 使用Seurat的FindSpatialVariableFeatures或DE分析

cat("=", rep("-", 59), "\n", sep="")
cat("  空间转录组差异表达基因发现\n")
cat("=", rep("-", 59), "\n", sep="")
cat("\n")

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

spatial_rds  <- get_input("空间Seurat对象RDS路径", "spatial.rds")
method       <- get_input("方法(SpatialDE/FindMarkers/FindSpatialVariableFeatures)", "FindSpatialVariableFeatures")
group_col    <- get_input("分组列名(用于FindMarkers)", "region")
group1       <- get_input("组1", "region1")
group2       <- get_input("组2", "region2")
output_csv   <- get_input("输出CSV路径", "spatial_deg.csv")
output_plot  <- get_input("输出图片路径", "spatial_deg_volcano.png")

cat("\nRDS:    ", spatial_rds, "\n")
cat("Method: ", method, "\n")
cat("Output: ", output_csv, "\n\n")

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
library(Seurat)
library(ggplot2)

if (!file.exists(spatial_rds)) { cat("[ERROR] RDS文件不存在\n"); quit(status=1) }

obj <- readRDS(spatial_rds)
cat("[Processing] 加载对象:", ncol(obj), "spots\n")

if (method == "FindSpatialVariableFeatures") {
  cat("[Processing] 寻找空间变异基因...\n")
  obj <- FindSpatialVariableFeatures(obj, selection.method="moransi")
  svf <- SpatialVariability(obj)[1:min(100, nrow(SpatialVariability(obj))), ]
  results <- data.frame(
    Gene=rownames(svf),
    SpatialVariability=svf[,1]
  )
  results <- results[order(-results$SpatialVariability), ]

} else if (method == "FindMarkers") {
  cat("[Processing] 差异分析:", group1, "vs", group2, "\n")
  if (!(group_col %in% colnames(obj@meta.data))) {
    cat("[ERROR] 分组列不存在:", group_col, "\n"); quit(status=1)
  }
  Idents(obj) <- group_col
  markers <- FindMarkers(obj, ident.1=group1, ident.2=group2,
                          min.pct=0.1, logfc.threshold=0.25)
  results <- data.frame(
    Gene=rownames(markers),
    avg_log2FC=markers$avg_log2FC,
    p_val=markers$p_val,
    p_val_adj=markers$p_val_adj,
    pct.1=markers$pct.1,
    pct.2=markers$pct.2
  )
  results <- results[order(results$p_val_adj), ]

} else if (method == "SpatialDE") {
  if (!requireNamespace("SpatialDE", quietly=TRUE)) {
    cat("[ERROR] SpatialDE未安装\n"); quit(status=1)
  }
  cat("[Processing] SpatialDE分析...\n")
  coords <- GetTissueCoordinates(obj)
  expr <- as.matrix(GetAssayData(obj, slot="data"))
  results <- SpatialDE::run(expr, as.data.frame(coords))
  results <- results[order(results$qvalue), ]
}

write.csv(results, output_csv, row.names=FALSE)

# Volcano plot for FindMarkers
if (method == "FindMarkers" && nrow(results) > 0) {
  results$significance <- ifelse(results$p_val_adj < 0.05 & abs(results$avg_log2FC) > 0.5,
                                  "Significant", "NS")
  p <- ggplot(results, aes(x=avg_log2FC, y=-log10(p_val_adj), color=significance)) +
    geom_point(size=0.5, alpha=0.7) +
    scale_color_manual(values=c("gray", "red")) +
    theme_bw() +
    labs(title="Spatial DEG Volcano", x="avg_log2FC", y="-log10(p_adj)")
  ggsave(output_plot, p, width=8, height=6, dpi=300)
}

cat("\n", "=", rep("-", 59), "\n", sep="")
cat("  RESULTS SUMMARY\n")
cat("=", rep("-", 59), "\n", sep="")
cat("  Method:     ", method, "\n")
cat("  DEGs found: ", nrow(results), "\n")
cat("  Output:     ", output_csv, "\n")
cat("=", rep("-", 59), "\n\n", sep="")
cat("[Done] spatial_deg_finder completed!\n")
