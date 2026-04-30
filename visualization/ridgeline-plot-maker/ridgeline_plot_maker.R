# Ridgeline山脊图（多组分布对比）
# 读取包含分组和数值列的数据，生成山脊图

cat("=", rep("-", 59), "\n", sep="")
cat("  Ridgeline山脊图（多组分布对比）\n")
cat("=", rep("-", 59), "\n", sep="")
cat("\n")

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

input_file    <- get_input("输入数据文件(CSV/TSV)", "data.csv")
output_file   <- get_input("输出图片路径", "ridgeline_plot.png")
group_col     <- get_input("分组列名", "group")
value_col     <- get_input("数值列名", "value")
title         <- get_input("图表标题", "Ridgeline Plot")

cat("\nInput:  ", input_file, "\n")
cat("Output: ", output_file, "\n")
cat("Group:  ", group_col, "\n")
cat("Value:  ", value_col, "\n\n")

# Check required packages
if (!requireNamespace("ggplot2", quietly=TRUE)) { cat("需要ggplot2\n"); quit(status=1) }
if (!requireNamespace("ggridges", quietly=TRUE)) { cat("需要ggridges\n"); quit(status=1) }

# Read data
if (!file.exists(input_file)) {
  cat("[ERROR] 文件不存在:", input_file, "\n")
  quit(status=1)
}

if (grepl("\\.tsv$", input_file) || grepl("\\.tab$", input_file)) {
  data <- read.table(input_file, header=TRUE, sep="\t", stringsAsFactors=FALSE)
} else {
  data <- read.csv(input_file, stringsAsFactors=FALSE)
}

cat("[Processing]", nrow(data), "records loaded\n")

# Validate columns
if (!(group_col %in% colnames(data))) {
  cat("[ERROR] 分组列不存在:", group_col, "\n")
  cat("  可用列:", paste(colnames(data), collapse=", "), "\n")
  quit(status=1)
}
if (!(value_col %in% colnames(data))) {
  cat("[ERROR] 数值列不存在:", value_col, "\n")
  cat("  可用列:", paste(colnames(data), collapse=", "), "\n")
  quit(status=1)
}

# Ensure group is factor and sort
data[[group_col]] <- factor(data[[group_col]])
data[[value_col]] <- as.numeric(data[[value_col]])
data <- data[!is.na(data[[value_col]]), ]

cat("[Processing]", length(unique(data[[group_col]])), "groups\n")

# Generate ridgeline plot
library(ggplot2)
library(ggridges)

p <- ggplot(data, aes(x=.data[[value_col]], y=.data[[group_col]], fill=.data[[group_col]])) +
  geom_density_ridges(alpha=0.7, scale=1.2) +
  theme_ridges() +
  labs(title=title, x=value_col, y=group_col) +
  theme(legend.position="none")

ggsave(output_file, p, width=10, height=max(6, length(unique(data[[group_col]])) * 0.8), dpi=300)

cat("\n", "=", rep("-", 59), "\n", sep="")
cat("  RESULTS SUMMARY\n")
cat("=", rep("-", 59), "\n", sep="")
cat("  Groups:       ", length(unique(data[[group_col]])), "\n")
cat("  Records:      ", nrow(data), "\n")
cat("  Output:       ", output_file, "\n")
cat("=", rep("-", 59), "\n\n", sep="")
cat("[Done] ridgeline_plot_maker completed!\n")
