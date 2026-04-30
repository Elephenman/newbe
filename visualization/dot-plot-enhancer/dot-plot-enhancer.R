# 点图增强版
library(ggplot2)
library(dplyr)

get_input <- function(prompt, default) {
  val <- readline(prompt=paste0(prompt, " [默认: ", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat(paste(rep("=", 60), collapse=""), "\n")
cat("  🎨 点图增强版\n")
cat(paste(rep("=", 60), collapse=""), "\n")

input_file <- get_input("数据文件路径(CSV)", "dotplot_data.csv")
x_col <- get_input("X轴列名", "pathway")
y_col <- get_input("Y轴列名", "gene")
size_col <- get_input("点大小映射列名", "gene_count")
color_col <- get_input("点颜色映射列名", "pvalue")
plot_out <- get_input("输出图片路径", "enhanced_dotplot.png")

df <- read.csv(input_file)
cat(paste0("\n✅ 加载数据: ", nrow(df), " 行\n"))

p <- ggplot(df, aes_string(x=x_col, y=y_col, size=size_col, color=color_col)) +
  geom_point() +
  scale_size_continuous(range=c(1, 10), name=size_col) +
  scale_color_gradient2(low="#C44E52", mid="white", high="#4C72B0",
                         midpoint=median(df[[color_col]]), name=color_col) +
  theme_bw() +
  theme(axis.text.x=element_text(angle=45, hjust=1)) +
  labs(title="Enhanced Dot Plot", x=x_col, y=y_col)

ggsave(plot_out, p, width=10, height=8, dpi=200)
cat(paste0("\n✅ 点图已保存: ", plot_out, "\n"))