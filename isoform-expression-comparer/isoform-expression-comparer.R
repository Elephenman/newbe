# 比较同一基因不同亚型的表达量差异并可视化

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat("============================================================\n")
cat("  Isoform Expression Comparer\n")
cat("============================================================\n\n")

expression_file <- get_input("亚型表达矩阵CSV (rows=transcripts, cols=samples)", "isoform_exp.csv")
gene_id <- get_input("目标基因ID (或搜索模式)", "BRCA1")
output_plot <- get_input("输出图片路径", "isoform_compare.png")
stat_test <- get_input("统计检验(wilcox/t.test/kruskal)", "wilcox")

suppressPackageStartupMessages({
  library(ggplot2)
  library(reshape2)
})

# 读取数据
if (!file.exists(expression_file)) {
  cat("[ERROR] File not found:", expression_file, "\n")
  cat("Expected format: CSV with row names as transcript IDs\n")
  quit(status=1)
}

dat <- read.csv(expression_file, row.names=1, check.names=FALSE)

# 搜索匹配的转录本
tgt <- grep(gene_id, rownames(dat), value=TRUE, ignore.case=TRUE)
if (length(tgt) == 0) {
  cat("[WARN] No transcripts found matching:", gene_id, "\n")
  cat("Available transcripts (first 20):\n")
  cat(paste(head(rownames(dat), 20), collapse="\n"), "\n")
  quit(status=0)
}

cat("[Processing] Found", length(tgt), "transcripts matching", gene_id, "\n")

# 准备数据
sub <- dat[tgt, , drop=FALSE]
sub$Transcript <- rownames(sub)
m <- melt(sub, id.vars="Transcript", variable.name="Sample", value.name="Expression")

# 绘制箱线图+散点
p <- ggplot(m, aes(x=Transcript, y=Expression, fill=Transcript)) +
  geom_boxplot(alpha=0.7, outlier.shape=NA) +
  geom_jitter(width=0.2, alpha=0.5, size=1) +
  theme_bw() +
  labs(title=paste("Isoform Expression:", gene_id),
       x="Transcript", y="Expression Level") +
  theme(axis.text.x=element_text(angle=45, hjust=1)) +
  scale_fill_brewer(palette="Set2")

ggsave(output_plot, p, width=10, height=7, dpi=150)
cat("[Done] Isoform comparison plot:", output_plot, "\n")

# 统计检验
if (length(tgt) >= 2) {
  cat("\n--- Statistical Tests ---\n")
  for (i in 1:(length(tgt)-1)) {
    for (j in (i+1):length(tgt)) {
      t1 <- as.numeric(dat[tgt[i],])
      t2 <- as.numeric(dat[tgt[j],])
      t1 <- t1[!is.na(t1)]
      t2 <- t2[!is.na(t2)]

      if (length(t1) >= 3 && length(t2) >= 3) {
        if (stat_test == "t.test") {
          res <- t.test(t1, t2)
          cat(sprintf("  %s vs %s: t=%.3f, p=%.4f\n", tgt[i], tgt[j], res$statistic, res$p.value))
        } else {
          res <- wilcox.test(t1, t2)
          cat(sprintf("  %s vs %s: W=%.1f, p=%.4f\n", tgt[i], tgt[j], res$statistic, res$p.value))
        }
      }
    }
  }
}

# 保存比较数据
out_csv <- sub("\\.png$", "_data.csv", output_plot)
write.csv(m, out_csv, row.names=FALSE)
cat("[Done] Comparison data:", out_csv, "\n")
