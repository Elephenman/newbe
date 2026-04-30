#设置工作环境
rm(list=ls())
setwd("D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\环状柱形图")

#加载R包
library(tidyverse)
library(reshape2)
library(ggplot2)
library(ggprism)

#加载数据
df <- read.table("data.txt",header = T, check.names = F)
#转换数据
data=melt(df)
data$G<-rep(c("T","F","H"), each = 24)
data_label <- data
data_label$ID <- as.numeric(rownames(data_label))

#####绘图————无分组情况
#计算标签角度
number_of_bar <- nrow(data_label)
angle <-  90 - 360 * (data_label$ID-0.5) /number_of_bar
data_label$hjust<-ifelse(angle < -90, 1, 0)
data_label$angle<-ifelse(angle < -90, angle+180, angle)

#绘图
p1 <- ggplot(data_label, aes(x=ID, y=value))+
  geom_bar(stat="identity", fill="blue", alpha=0.7) +
  ylim(-75,75) +#y轴范围，控制内圆大小与条形大小
  theme_minimal() +#主题
  theme(axis.text = element_blank(),
        axis.title = element_blank(),
        panel.grid = element_blank(),
        plot.margin = unit(rep(-1,4), "cm")) +#调整边缘以使得标签不会被截断
  coord_polar(start = 0) +#极坐标
  geom_text(data=data_label, aes(x=ID, y=value+10, label=variable, hjust=hjust), 
            color="black", fontface="bold",alpha=0.6, size=2.5, 
            angle= data_label$angle, inherit.aes = F) #标签

p1

#####绘图————添加分组并增加分组间隔
#调整柱子显示顺序
data_label = data_label %>% arrange(G, value)
#设置分组间的空白间隔
data_label$G<-as.factor(data_label$G)
number_empty_bar <- 3
to_add <- data.frame(matrix(NA, number_empty_bar*nlevels(as.factor(data_label$G)), ncol(data_label)) )
colnames(to_add) <- colnames(data_label)
to_add$G <- rep(levels(data_label$G), each=number_empty_bar)
data_label <- rbind(data_label, to_add)
data_label <- data_label %>% arrange(G)
data_label$ID <- seq(1, nrow(data_label))
##标签设置
number_of_bar <- nrow(data_label)
angle <-  90 - 360 * (data_label$ID-0.5) /number_of_bar
data_label$hjust<-ifelse(angle < -90, 1, 0)
data_label$angle<-ifelse(angle < -90, angle+180, angle)
#绘图
p2 <- ggplot(data_label, aes(x=ID, y=value, fill=G)) +
  geom_bar(stat="identity", alpha=0.5) +
  ylim(-75,75) +
  theme_minimal() +
  theme(legend.position = "none",
        axis.text = element_blank(),
        axis.title = element_blank(),
        panel.grid = element_blank(),
        plot.margin = unit(rep(-1,4), "cm")) +
  coord_polar() + #极坐标
  geom_text(data=data_label, aes(x=ID, y=value+10, label=variable, hjust=hjust), 
            color="black", fontface="bold",alpha=0.6, size=2.5, 
            angle= angle, inherit.aes = F)+#标签
  scale_fill_prism(palette = "candy_bright")#使用ggprism包修改颜色

p2
####添加分组标签
#创建标签数据及位置
base_data <- data_label %>% 
  group_by(G) %>% 
  summarize(start=min(ID), end=max(ID) - number_empty_bar) %>% 
  rowwise() %>% 
  mutate(title=mean(c(start, end)))
#绘图
p2+geom_segment(data=base_data, aes(x = start, y = -5, xend = end, yend = -5),
                color = "red", alpha=0.8, size=0.8 , inherit.aes = F)+#添加分组线
  geom_text(data=base_data, aes(x = title, y = -18, label=G), 
            hjust=c(1,1,0), colour = "black", alpha=0.8, size=4, 
            fontface="bold", inherit.aes = F)#分组标签

#参考:https://r-graph-gallery.com/297-circular-barplot-with-groups.html
