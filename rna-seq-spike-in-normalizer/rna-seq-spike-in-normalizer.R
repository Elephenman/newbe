# RNA-seq ERCC spike-in标准化
library(ggplot2)
library(dplyr)

get_input <- function(prompt, default) {
  val <- readline(prompt=paste0(prompt, " [默认: ", default, "]: "))
  if (val == "") return(default) else return(val)
}

print_separator <- function() {
  cat(paste(rep("=", 60), collapse=""), "\n")
}

print_separator()
cat("  📊 RNA-seq ERCC Spike-in标准化\n")
print_separator()

count_file <- get_input("count矩阵文件路径", "counts.csv")
spike_file <- get_input("ERCC spike-in信息文件路径", "ercc_mix.csv")
output_file <- get_input("标准化结果路径", "spike_normalized.tsv")
plot_out <- get_input("校准图路径", "spike_calibration.png")

count_df <- read.csv(count_file, row.names=1)
spike_df <- read.csv(spike_file)

spike_genes <- spike_df$ERCC_ID
ercc_counts <- count_df[rownames(count_df) %in% spike_genes, ]
gene_counts <- count_df[!rownames(count_df) %in% spike_genes, ]

cat(paste0("\n✅ 加载完成: ", nrow(gene_counts), " 基因, ", nrow(ercc_counts), " ERCC\n"))

ercc_total <- colSums(ercc_counts)
gene_total <- colSums(gene_counts)
scaling_factor <- ercc_total / gene_total

normalized <- sweep(gene_counts, 2, scaling_factor, "/")

write.table(normalized, output_file, sep="\t", quote=FALSE)

calibration <- data.frame(
  Sample=colnames(ercc_counts),
  ERCC_Total=ercc_total,
  Gene_Total=gene_total,
  Scaling_Factor=scaling_factor
)

p <- ggplot(calibration, aes(x=Gene_Total, y=ERCC_Total)) +
  geom_point(size=3) +
  geom_smooth(method="lm", se=TRUE) +
  labs(title="ERCC Calibration Curve", x="Gene Counts", y="ERCC Counts") +
  theme_bw()

ggsave(plot_out, p, width=8, height=6)

cat(paste0("\n✅ 标准化完成\n"))
cat(paste0("  输出: ", output_file, "\n"))
cat(paste0("  校准图: ", plot_out, "\n"))