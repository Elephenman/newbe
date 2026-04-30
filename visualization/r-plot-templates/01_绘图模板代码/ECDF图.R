# ECDF图,即经验累积密度函数，通过图可以看出低于特定数值个体百分比
rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/ECDF图")

##加载所需R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(tidyverse) # Easily Install and Load the 'Tidyverse'

##加载数据（随即编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")
head(df)

##简单绘制其中一组的ECDF图
df %>% filter(group=="group1") %>%
  ggplot(aes(x=value)) +
  stat_ecdf(linewidth=1)

##按照分组进行绘制
df %>% 
  ggplot(aes(x=value,col=group)) +
  ##绘制ecdf图的主要函数stat_ecdf()
  stat_ecdf(linewidth=0.6)+
  scale_color_manual(values = c("#00b2a9","#a626aa","#6639b7","#aea400","#ff6319"))+
  labs(title = "ECDF plot")+
  theme_bw()+
  theme(panel.grid = element_blank(),
        legend.position = c(0.9,0.3),
        plot.title = element_text(hjust = 0.5),
        axis.text = element_text(size = 10),
        axis.title = element_text(size=14, color = "black"))
