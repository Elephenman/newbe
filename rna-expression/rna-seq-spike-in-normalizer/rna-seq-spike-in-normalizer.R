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
cat("  RNA-seq ERCC Spike-in标准化\n")
print_separator()

count_file <- get_input("count矩阵文件路径", "counts.csv")
spike_file <- get_input("ERCC spike-in信息文件路径", "ercc_mix.csv")
output_file <- get_input("标准化结果路径", "spike_normalized.tsv")
plot_out <- get_input("校准图路径", "spike_calibration.png")
target_ercc_total <- as.numeric(get_input("目标ERCC总counts", "1000000"))

count_df <- read.csv(count_file, row.names=1)
spike_df <- read.csv(spike_file)

spike_genes <- spike_df$ERCC_ID
ercc_counts <- count_df[rownames(count_df) %in% spike_genes, ]
gene_counts <- count_df[!rownames(count_df) %in% spike_genes, ]

cat(paste0("\n加载完成: ", nrow(gene_counts), " 基因, ", nrow(ercc_counts), " ERCC\n"))

# Compute observed ERCC total per sample
ercc_total <- colSums(ercc_counts)

# Compute scaling factor = target_ERCC_total / observed_ERCC_total
scaling_factor <- target_ercc_total / ercc_total

# Normalize gene counts by multiplying with scaling factor
normalized <- sweep(gene_counts, 2, scaling_factor, "*")

write.table(normalized, output_file, sep="\t", quote=FALSE)

calibration <- data.frame(
  Sample=colnames(ercc_counts),
  ERCC_Total=ercc_total,
  Scaling_Factor=scaling_factor,
  Normalized_ERCC_Target=target_ercc_total
)

p <- ggplot(calibration, aes(x=Sample, y=Scaling_Factor)) +
  geom_bar(stat="identity", fill="steelblue") +
  geom_hline(yintercept=1, linetype="dashed", color="red") +
  labs(title="ERCC Normalization Scaling Factors", x="Sample", y="Scaling Factor") +
  theme_bw() +
  theme(axis.text.x = element_text(angle=45, hjust=1))

ggsave(plot_out, p, width=8, height=6)

cat(paste0("\n标准化完成\n"))
cat(paste0("  输出: ", output_file, "\n"))
cat(paste0("  校准图: ", plot_out, "\n"))
cat(paste0("  目标ERCC总counts: ", target_ercc_total, "\n"))
