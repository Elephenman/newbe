#设置工作环境
rm(list=ls())
setwd("D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\环状柱形图")

#加载相关R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggthemes) # Extra Themes, Scales and Geoms for 'ggplot2'
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization
#加载数据
df <- read.table("data1.txt",header = T, check.names = F)
#配色
col <- colorRampPalette(brewer.pal(9,"Set1"))(7)
#背景色
color <- colorRampPalette(brewer.pal(11,"BrBG"))(30)
#绘图
ggplot(df, aes(x = sample, y = value, fill = sample)) +
  geom_bar(stat = "identity", color = "white",
           lwd = 1, show.legend = FALSE,width = 0.6)+
  geom_text(aes(y=value+5,label=value,color=sample))+
  scale_fill_manual(values = col)+
  scale_color_manual(values = col)+
  theme_pander()+
  coord_polar()+
  theme(axis.text.y = element_blank(),
        axis.ticks.y =element_blank(),
        axis.text.x = element_text(color='black',size=15),
        legend.position = "none",
        panel.grid.major.x = element_blank())+
  labs(y=NULL,x=NULL)
#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

###根据分组不同进行着色
#绘图
ggplot(df, aes(x = sample, y = value, fill = group)) +
  geom_bar(stat = "identity", color = "white",
           lwd = 1, show.legend = T,width = 0.6)+
  geom_text(aes(y=value+5,label=value,color=group),show.legend = F)+
  scale_fill_manual(values = col)+
  scale_color_manual(values = col)+
  theme_pander()+
  coord_polar()+
  theme(axis.text.y = element_blank(),
        axis.ticks.y =element_blank(),
        axis.text.x = element_text(color='black',size=15),
        legend.position = "right",
        panel.grid.major.x = element_blank())+
  labs(y=NULL,x=NULL)
#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)
