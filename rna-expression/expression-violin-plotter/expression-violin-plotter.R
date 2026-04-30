# 绘制多基因/多样本表达量小提琴图

  expression_file <- ifelse(interactive(), readline("表达矩阵CSV [expression.csv]: "), "expression.csv")
  genes <- ifelse(interactive(), readline("目标基因(逗号分隔) []: "), "")
  output_plot <- ifelse(interactive(), readline("输出图片路径 [violin_plot.png]: "), "violin_plot.png")
  group_file <- ifelse(interactive(), readline("分组CSV(样本,组) []: "), "")
  library(ggplot2); library(reshape2)
  dat <- read.csv(expression_file, row.names=1)
  gl <- if(genes=="") names(sort(apply(dat,1,var,na.rm=TRUE),decreasing=TRUE))[1:min(10,nrow(dat))] else strsplit(genes,",")[[1]]
  gl <- intersect(gl, rownames(dat))
  sub <- dat[gl,,drop=FALSE]; sub$Gene <- rownames(sub)
  m <- melt(sub, id.vars="Gene", variable.name="Sample", value.name="Expression")
  if(group_file != ""){
    grp <- read.csv(group_file); m <- merge(m, grp, by.x="Sample", by.y=1)
    p <- ggplot(m, aes(x=Gene, y=Expression, fill=Group)) + geom_violin(alpha=0.7, position=position_dodge(0.9))
  } else {
    p <- ggplot(m, aes(x=Gene, y=Expression, fill=Gene)) + geom_violin(alpha=0.7)
  }
  p <- p + theme_bw() + theme(axis.text.x=element_text(angle=45, hjust=1)) + labs(title="Expression Violin")
  ggsave(output_plot, p, width=10, height=6, dpi=150)
  cat("小提琴图:", output_plot, "\n")

