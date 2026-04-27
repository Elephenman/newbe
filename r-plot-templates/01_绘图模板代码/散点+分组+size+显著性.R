rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点+分组+size+显著性")

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(rstatix) # Pipe-Friendly Framework for Basic Statistical Tests

#加载绘图数据（随机编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F)
df$group1 <- factor(df$group1, levels = c("One", "Two", "Three"))
df$group2 <- factor(df$group2, levels = c("1", "2", "3","4", "5", "6"))
df$group3 <- factor(df$group3, levels = c("A", "B"))

#计算显著性
p <- df[df$group1 == "Two", ] %>% 
  wilcox_test(Score ~ group3) %>%
  adjust_pvalue()
p

# # A tibble: 1 × 8
# .y.   group1 group2    n1    n2 statistic        p    p.adj
# <chr> <chr>  <chr>  <int> <int>     <dbl>    <dbl>    <dbl>
#   1 Score A      B         13     9       113 0.000271 0.000271

#绘图
ggplot(df)+
  #散点图
  geom_point(aes(x = group2, y = Score, 
                 color = group3, size = Count))+
  #设置分面
  facet_grid(~group1,
             switch='x')+#switch='x'可将标签位置由顶部移至底部，当switch='y'时，可将位于右边的分面标签移至左边
  #主题设置
  theme_bw()+
  theme(axis.text.x = element_blank(),
        axis.text.y = element_text(color = "black", size = 12),
        axis.title = element_text(color = "black", size = 14),
        axis.ticks.x = element_blank(),
        strip.background = element_blank(),
        strip.text = element_text(color = "black", size = 12),
        panel.grid = element_blank())+
  #调整size范围
  scale_size_continuous(range = c(2, 7), breaks = c(1,3,6))+
  #颜色
  scale_color_manual(values = c("#ff4e00","#01cd74"))+
  #y轴范围及刻度设置
  scale_y_continuous(breaks = c(0,1,2,3,4,5,6,7))+
  #图例
  guides(color=guide_legend(override.aes = list(size=4,alpha=1)))+
  labs(x = NULL, color = NULL)+
  #手动添加显著性
  geom_segment(df[df$group1 == "Two", ], mapping = aes(x = 2, xend = 5, y = 7.5, yend = 7.5),
               color = "black", linewidth = 0.6)+
  geom_text(df[df$group1 == "Two", ], mapping = aes(x = 3.5, y = 8, label = 'p < 0.001'), size =4.5, color="black")


