# Gene expression boxplot batch generation + statistical tests
# Interactive R script - all parameters via readline()

cat("=", rep("-", 59), "\n", sep="")
cat("  Gene expression boxplot + statistical tests\n")
cat("=", rep("-", 59), "\n", sep="")
cat("\n")

# === Input Parameters ===
get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

expression_file <- get_input("Expression matrix CSV (rows=genes, cols=samples)", "expression.csv")
genes_input     <- get_input("Target genes (comma-separated, or 'auto' for top variable)", "auto")
group_file      <- get_input("Group file CSV (sample,group)", "groups.csv")
output_plot     <- get_input("Output plot path", "expression_boxplot.png")
test_method     <- get_input("Statistical test (wilcox/t.test/anova)", "wilcox")

cat("\nExpression: ", expression_file, "\n")
cat("Groups:     ", group_file, "\n")
cat("Output:     ", output_plot, "\n\n")

# === Validate and Load ===
suppressPackageStartupMessages({
  library(ggplot2)
  library(reshape2)
})

if (!file.exists(expression_file)) {
  cat("[ERROR] Expression file not found:", expression_file, "\n")
  quit(status=1)
}
if (!file.exists(group_file)) {
  cat("[ERROR] Group file not found:", group_file, "\n")
  quit(status=1)
}

cat("[Processing] Loading data...\n")
expr <- read.csv(expression_file, row.names=1, check.names=FALSE)
groups <- read.csv(group_file, stringsAsFactors=FALSE)
colnames(groups)[1:2] <- c("Sample", "Group")

# Select genes
if (genes_input == "auto") {
  gene_vars <- apply(expr, 1, var, na.rm=TRUE)
  gl <- names(sort(gene_vars, decreasing=TRUE))[1:min(10, nrow(expr))]
} else {
  gl <- trimws(strsplit(genes_input, ",")[[1]])
}
gl <- intersect(gl, rownames(expr))

if (length(gl) == 0) {
  cat("[ERROR] No target genes found in expression matrix\n")
  quit(status=1)
}

cat("[Processing]", length(gl), "genes selected\n")

# Prepare data for plotting
sub_expr <- expr[gl, , drop=FALSE]
sub_expr$Gene <- rownames(sub_expr)
m <- melt(sub_expr, id.vars="Gene", variable.name="Sample", value.name="Expression")
m <- merge(m, groups, by.x="Sample", by.y="Sample")

# Statistical tests
cat("[Processing] Running statistical tests...\n")
test_results <- data.frame(Gene=character(), pvalue=numeric(), method=character(), stringsAsFactors=FALSE)
for (g in gl) {
  g_data <- m[m$Gene == g, ]
  group_levels <- unique(g_data$Group)
  if (length(group_levels) == 2) {
    g1 <- g_data$Expression[g_data$Group == group_levels[1]]
    g2 <- g_data$Expression[g_data$Group == group_levels[2]]
    if (test_method == "t.test") {
      res <- t.test(g1, g2)
    } else {
      res <- wilcox.test(g1, g2)
    }
    test_results <- rbind(test_results, data.frame(Gene=g, pvalue=res$p.value, method=test_method))
  } else if (length(group_levels) > 2) {
    res <- aov(Expression ~ Group, data=g_data)
    pval <- summary(res)[[1]][["Pr(>F)"]][1]
    test_results <- rbind(test_results, data.frame(Gene=g, pvalue=pval, method="anova"))
  }
}
test_results$padj <- p.adjust(test_results$pvalue, method="BH")
test_results$significance <- ifelse(test_results$padj < 0.05, "*", "ns")

# Generate plot
p <- ggplot(m, aes(x=Gene, y=Expression, fill=Group)) +
  geom_boxplot(alpha=0.7, outlier.size=0.5) +
  theme_bw() +
  theme(axis.text.x=element_text(angle=45, hjust=1)) +
  labs(title="Gene Expression by Group", y="Expression", x="Gene") +
  scale_fill_brewer(palette="Set2")

ggsave(output_plot, p, width=max(8, length(gl)), height=6, dpi=300)

# Save test results
test_file <- sub("\\.png$", "_stats.csv", output_plot)
write.csv(test_results, test_file, row.names=FALSE)

# === Summary Report ===
sig_count <- sum(test_results$padj < 0.05, na.rm=TRUE)
cat("\n", "=", rep("-", 59), "\n", sep="")
cat("  RESULTS SUMMARY\n")
cat("=", rep("-", 59), "\n", sep="")
cat("  Genes tested:    ", length(gl), "\n")
cat("  Significant:     ", sig_count, " (padj < 0.05)\n")
cat("  Plot:            ", output_plot, "\n")
cat("  Test results:    ", test_file, "\n")
cat("=", rep("-", 59), "\n\n", sep="")
cat("[Done] expression_boxplot_maker completed!\n")
