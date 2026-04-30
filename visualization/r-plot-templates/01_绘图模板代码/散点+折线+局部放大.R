rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点+折线+局部放大")
#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2)
#加载数据
data <- read.table("data.txt",header = T)
data2 <- data[1:15,]
#生成绘图数据
df <- melt(data,id.vars = "time")
df2 <- melt(data2,id.vars = "time")
#准备配色
col <- c("black", "#c3c0d4",
              "yellow","blue",
              "red","green","#2072A8")

#绘图
p1 <- ggplot(df,aes(time,value,color=variable))+
  geom_line(linewidth=0.5)+
  geom_point(size=1)+
  theme_bw()+
  theme(legend.position = "none",
        axis.title.x=element_text(size=12),
        axis.title.y=element_text(size=12,angle=90),
        axis.text=element_text(size=12,color = "black"),
        panel.grid=element_blank())+
  scale_color_manual(values = col)+
  labs(x="Time(s)")
p1
#绘制子图形
p2 <- ggplot(df2,aes(time,value,color=variable))+
  geom_line(linewidth=0.5)+
  geom_point(size=1)+
  theme_bw()+
  theme(legend.position = c(0.9,0.65),
        legend.title = element_blank(),
        legend.background = element_blank(),
        legend.key.height = unit(0.5, "cm"),
        axis.title.x=element_text(size=12),
        axis.title.y=element_text(size=12,angle=90),
        axis.text=element_text(size=12,color = "black"),
        panel.grid=element_blank(),
        panel.background = element_blank(),
        plot.background = element_blank())+
  scale_color_manual(values = col)+
  labs(x="Time(s)")+
  scale_x_continuous(breaks = seq(0, 30, len = 6))
p2

#组合图形
p1 + annotation_custom(grob=ggplotGrob(p2),ymin = 15, ymax = 100, xmin=35, xmax=100)

##修饰
p1+geom_rect(xmin = -2, xmax = 22, ymin = 0, ymax = 102,
             fill = "transparent", color = "#00bce4", linetype = "dashed",linewidth=0.8)+
  geom_segment(aes(x = 22, y = 60, xend = 35, yend = 60),
               arrow = arrow(length = unit(0.3, "cm"),type="closed"),
               color = "#00bce4",linewidth=0.8)+
  annotation_custom(grob=ggplotGrob(p2),ymin = 15, ymax = 100, xmin=35, xmax=100)

