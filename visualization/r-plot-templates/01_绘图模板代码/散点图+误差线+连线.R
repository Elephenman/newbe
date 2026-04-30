###科研后花园####
####@wzs#####

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/箱线图+散点图')#设置工作目录

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(tidyverse) # Easily Install and Load the 'Tidyverse'
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization
#这里使用我自己随机编写的数据
df <- data.frame(
  A = c(2,5,6,5,4,8,6,3,8,9),
  B = c(15,10,5,18,12,13,16,14,10,9),
  C = c(1,3,6,5,2,3,6,2,4,1),
  D = c(20,15,14,16,10,22,18,10,11,12),
  E = c(2,5,6,5,4,8,6,3,8,9),
  F = c(15,10,5,18,12,13,16,14,10,9),
  G = c(1,3,6,5,2,3,6,2,4,1),
  H = c(20,15,14,16,10,22,18,10,11,12),
  I = c(2,5,6,5,4,8,6,3,8,9)
)
#预览数据
head(df)

#使用tidyverse包对数据进行处理
df <- df %>% 
  gather(key = 'group',value = 'values')#gather()函数可以把多列数据合并成一列数据
head(df)#预览数据

#绘图
col = c("#ffa500","#00858a","#006400","#87ceeb","#e8d9c5","#00ff7f","#e5ad21","#ff7f50","#be92e6")
ggplot(df,aes(group,values)) +
  geom_dotplot(binaxis = "y",fill = "lightgray", dotsize = 0.9,
               stackdir = "center",position = position_dodge(1)) + 
  stat_summary(aes(color=group),fun.data = "mean_cl_normal",
               geom = "errorbar",
               width = 0.1,size=1) +
  stat_summary(fun = "mean", geom = "line",group=1,size=0.8,color="red")+
  stat_summary(aes(color=group),fun = "mean", geom = "point",size=5)+
  theme_bw()+
  theme(axis.text.x = element_text(color = "black", angle = 45,vjust = 1,hjust = 1,size = 12),
        axis.text.y = element_text(color = "black",size = 12),
        axis.title.y = element_text(color = "black",size = 14),
        legend.position = "none",
        panel.grid = element_blank())+
  labs(x=NULL,y="Temperature (℃)")+
  scale_color_manual(values = col)

#构建背景色
color1 <- colorRampPalette(brewer.pal(11,"PiYG"))(30)
#添加背景
grid.raster(alpha(color1, 0.1), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)
