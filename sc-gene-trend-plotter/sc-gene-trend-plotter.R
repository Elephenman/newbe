# 单细胞基因沿伪时间趋势图

  rds_file <- ifelse(interactive(), readline("Seurat对象RDS路径(含伪时间) [seurat_obj.rds]: "), "seurat_obj.rds")
  genes <- ifelse(interactive(), readline("目标基因(逗号分隔) []: "), "")
  pseudotime_col <- ifelse(interactive(), readline("伪时间列名 [pseudotime]: "), "pseudotime")
  output_plot <- ifelse(interactive(), readline("输出图片路径 [gene_trend.png]: "), "gene_trend.png")
  library(Seurat); library(ggplot2)
  obj <- readRDS(rds_file)
  gl <- if(genes=="") VariableFeatures(obj)[1:min(6, length(VariableFeatures(obj)))] else strsplit(genes,",")[[1]]
  if(!(pseudotime_col %in% colnames(obj@meta.data))){ cat("未找到:", pseudotime_col, "\n"); return(invisible(NULL)) }
  pt <- obj@meta.data[[pseudotime_col]]
  df_list <- lapply(gl, function(g){
    expr <- GetAssayData(obj, slot="data")[g,]
    data.frame(Gene=g, Pseudotime=pt, Expression=as.numeric(expr))
  })
  df <- do.call(rbind, df_list)
  p <- ggplot(df, aes(x=Pseudotime, y=Expression)) + geom_smooth(aes(color=Gene), se=FALSE) +
    theme_bw() + labs(title="Gene Trends along Pseudotime")
  ggsave(output_plot, p, width=10, height=6, dpi=150)
  cat("趋势图:", output_plot, "\n")

