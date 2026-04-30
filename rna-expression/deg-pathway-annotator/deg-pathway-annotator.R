# 将DEG结果自动注释到KEGG/GO通路并生成富集报告

  deg_file <- ifelse(interactive(), readline("DEG结果CSV路径(含gene/log2FC/padj) [deg_results.csv]: "), "deg_results.csv")
  organism <- ifelse(interactive(), readline("物种(hsa/mmu) [hsa]: "), "hsa")
  pvalue_cutoff <- ifelse(interactive(), readline("P值阈值 [0.05]: "), "0.05")
  qvalue_cutoff <- ifelse(interactive(), readline("q值阈值 [0.2]: "), "0.2")
  output_dir <- ifelse(interactive(), readline("输出目录 [pathway_results]: "), "pathway_results")
  library(clusterProfiler); library(org.Hs.eg.db)
  deg <- read.csv(deg_file, stringsAsFactors=FALSE)
  genes <- deg$gene
  ego <- enrichGO(gene=genes, OrgDb=org.Hs.eg.db, keyType="SYMBOL",
                  ont="BP", pAdjustMethod="BH",
                  pvalueCutoff=as.numeric(pvalue_cutoff),
                  qvalueCutoff=as.numeric(qvalue_cutoff))
  eid <- bitr(genes, fromType="SYMBOL", toType="ENTREZID", OrgDb=org.Hs.eg.db)
  kk <- enrichKEGG(gene=eid$ENTREZID, organism=organism,
                   pvalueCutoff=as.numeric(pvalue_cutoff),
                   qvalueCutoff=as.numeric(qvalue_cutoff))
  dir.create(output_dir, showWarnings=FALSE, recursive=TRUE)
  write.csv(as.data.frame(ego), file.path(output_dir,"GO_enrichment.csv"), row.names=FALSE)
  write.csv(as.data.frame(kk), file.path(output_dir,"KEGG_enrichment.csv"), row.names=FALSE)
  cat("通路注释完成:", output_dir, "\n")

