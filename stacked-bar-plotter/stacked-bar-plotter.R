# 堆叠条形图绘制器
library(ggplot2)
library(dplyr)

get_input <- function(prompt, default) {
  val <- readline(prompt=paste0(prompt, " [默认: ", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat(paste(rep("=", 60), collapse=""), "\n")
cat("  🎨 堆叠条形图绘制器\n")
cat(paste(rep("=", 60), collapse=""), "\n")

input_file <- get_input("数据文件路径(CSV)", "proportion_data.csv")
group_col <- get_input("分组列名", "sample")
category_col <- get_input("类别列名", "cell_type")
value_col <- get_input("数值列名(比例)", "percentage")
plot_out <- get_input("输出图片路径", "stacked_barplot.png")

df <- read.csv(input_file)
cat(paste0("\n✅ 加载数据: ", nrow(df), " 行\n"))

categories <- unique(df[[category_col]])
n_cat <- length(categories)

colors <- c("#4C72B0","#DD8452","#55A868","#C44E52","#8C8C8C",
            "#CCB974","#64B5CD","#E5AE38","#A2D9CE","#FF6F61")[1:min(n_cat, 10)]

p <- ggplot(df, aes_string(x=group_col, y=value_col, fill=category_col)) +
  geom_bar(stat="identity", position="stack", width=0.7) +
  scale_fill_manual(values=colors) +
  theme_bw() +
  theme(axis.text.x=element_text(angle=45, hjust=1)) +
  labs(title="Stacked Bar Plot", x=group_col, y=value_col, fill=category_col)

ggsave(plot_out, p, width=10, height=6, dpi=200)
cat(paste0("\n✅ 堆叠条形图已保存: ", plot_out, "\n"))