# Forest图绘制器
library(ggplot2)
library(dplyr)

get_input <- function(prompt, default) {
  val <- readline(prompt=paste0(prompt, " [默认: ", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat(paste(rep("=", 60), collapse=""), "\n")
cat("  🎨 Forest图绘制器\n")
cat(paste(rep("=", 60), collapse=""), "\n")

input_file <- get_input("数据文件路径(CSV)", "forest_data.csv")
label_col <- get_input("标签列名", "feature")
effect_col <- get_input("效应量列名", "odds_ratio")
ci_low <- get_input("CI下限列名", "ci_low")
ci_high <- get_input("CI上限列名", "ci_high")
plot_out <- get_input("输出图片路径", "forest_plot.png")

df <- read.csv(input_file)
cat(paste0("\n✅ 加载数据: ", nrow(df), " 行\n"))

df$order <- nrow(df):1

p <- ggplot(df, aes_string(x=effect_col, y="order")) +
  geom_point(size=3, color="#4C72B0") +
  geom_errorbarh(aes_string(xmin=ci_low, xmax=ci_high), height=0.3, color="#4C72B0") +
  geom_vline(xintercept=1, linetype="dashed", color="red") +
  scale_y_continuous(breaks=df$order, labels=df[[label_col]]) +
  labs(x=effect_col, y="", title="Forest Plot") +
  theme_bw() +
  theme(panel.grid.major.y=element_line(color="grey90"))

ggsave(plot_out, p, width=8, height=max(6, nrow(df)*0.4), dpi=200)
cat(paste0("\n✅ Forest图已保存: ", plot_out, "\n"))