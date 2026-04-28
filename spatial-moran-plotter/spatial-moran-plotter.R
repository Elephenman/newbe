# 计算空间基因表达的Moran's I自相关统计量

  rds_file <- ifelse(interactive(), readline("Seurat空间对象RDS路径 [spatial.rds]: "), "spatial.rds")
  genes <- ifelse(interactive(), readline("目标基因(逗号分隔) []: "), "")
  output_file <- ifelse(interactive(), readline("输出CSV路径 [moran_results.csv]: "), "moran_results.csv")
  library(Seurat); library(spdep)
  obj <- readRDS(rds_file)
  gl <- if(genes=="") VariableFeatures(obj)[1:min(20, length(VariableFeatures(obj)))] else strsplit(genes,",")[[1]]
  results <- data.frame(Gene=character(), Moran_I=numeric(), p_value=numeric(), stringsAsFactors=FALSE)
  coords <- GetTissueCoordinates(obj)
  nb <- knn2nb(knearneigh(as.matrix(coords), k=6))
  lw <- nb2listw(nb, style="W")
  for(g in gl){
    expr <- GetAssayData(obj, slot="data")[g,]
    if(var(expr) == 0) next
    mi <- moran.test(as.numeric(expr), lw)
    results <- rbind(results, data.frame(Gene=g, Moran_I=mi$estimate[1], p_value=mi$p.value))
  }
  write.csv(results, output_file, row.names=FALSE)
  cat("Moran I完成:", nrow(results), "genes\n")

