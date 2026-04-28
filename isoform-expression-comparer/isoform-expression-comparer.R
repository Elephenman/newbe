# 比较同一基因不同亚型的表达量差异并可视化

  expression_file <- ifelse(interactive(), readline("亚型表达矩阵CSV [isoform_exp.csv]: "), "isoform_exp.csv")
  gene_id <- ifelse(interactive(), readline("目标基因ID [BRCA1]: "), "BRCA1")
  output_plot <- ifelse(interactive(), readline("输出图片路径 [isoform_compare.png]: "), "isoform_compare.png")
  library(ggplot2); library(reshape2)
  dat <- read.csv(expression_file, row.names=1)
  tgt <- grep(gene_id, rownames(dat), value=TRUE)
  if(length(tgt)==0){ cat("未找到:", gene_id, "\n"); return(invisible(NULL)) }
  sub <- dat[tgt,,drop=FALSE]; sub$Transcript <- rownames(sub)
  m <- melt(sub, id.vars="Transcript", variable.name="Sample", value.name="Expression")
  p <- ggplot(m, aes(x=Transcript, y=Expression, fill=Transcript)) +
    geom_boxplot(alpha=0.7) + theme_bw() + labs(title=paste("Isoform:", gene_id)) +
    theme(axis.text.x=element_text(angle=45, hjust=1))
  ggsave(output_plot, p, width=8, height=6, dpi=150)
  cat("亚型比较图:", output_plot, "\n")

