# WGCNA共表达网络模块识别与可视化

  expr_file <- ifelse(interactive(), readline("表达矩阵CSV(行=基因,列=样本) [expression.csv]: "), "expression.csv")
  soft_power <- ifelse(interactive(), readline("软阈值幂次(0=自动) [0]: "), "0")
  min_module_size <- ifelse(interactive(), readline("最小模块大小 [30]: "), "30")
  output_dir <- ifelse(interactive(), readline("输出目录 [wgcna_results]: "), "wgcna_results")
  library(WGCNA); options(stringsAsFactors=FALSE)
  dat <- as.data.frame(t(read.csv(expr_file, row.names=1)))
  gsg <- goodSamplesGenes(dat, verbose=0)
  if(!gsg$allOK) dat <- dat[gsg$goodSamples, gsg$goodGenes]
  pv <- as.numeric(soft_power)
  if(pv == 0){ sft <- pickSoftThreshold(dat, verbose=0); pv <- ifelse(is.na(sft$powerEstimate), 6, sft$powerEstimate) }
  adj <- adjacency(dat, power=pv)
  TOM <- TOMsimilarity(adj); dissTOM <- 1 - TOM
  gtree <- hclust(as.dist(dissTOM), method="average")
  mods <- cutreeDynamic(dendro=gtree, deepSplit=2, pamRespectsDendro=FALSE,
                        minClusterSize=as.numeric(min_module_size))
  mcols <- labels2colors(mods)
  dir.create(output_dir, showWarnings=FALSE, recursive=TRUE)
  write.csv(data.frame(Gene=colnames(dat), Module=mcols),
            file.path(output_dir, "module_assignments.csv"), row.names=FALSE)
  cat("WGCNA完成, 模块数:", length(unique(mcols)), "\n")

