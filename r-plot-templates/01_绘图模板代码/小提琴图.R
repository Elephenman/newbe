rm(list=ls())#clear Global Environment
setwd('D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\小提琴图')#设置工作目录

#安装包
# install.packages("ggplot2")
# install.packages("ggpubr")
# install.packages("ggsignif")
# install.packages("tidyverse")
# install.packages("ggprism")
# install.packages("vioplot")
#加载包
library(ggplot2)#绘图包
library(ggpubr)#基于ggplot2的可视化包，主要用于绘制符合出版要求的图形
library(ggsignif)#用于P值计算和显著性标记
library(tidyverse)#数据预处理
library(ggprism)#提供了GraphPad prism风格的主题和颜色，主要用于美化我们的图形
library(vioplot)#小提琴图绘制包
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization
#准备数据
# df <- read.table("data.txt",header = T,  check.names = F)
#自己随机编写的数据
df <- data.frame(
  A_1 = c(2,5,6,5,4,8,6,3,8,9),
  A_2 = c(5,8,6,3,4,7,9,3,6,4),
  B_1 = c(15,10,5,18,12,13,16,14,10,9),
  B_2 = c(25,20,23,15,14,24,20,22,25,26),
  C_1 = c(1,3,6,5,2,3,6,2,4,1),
  C_2 = c(7,8,9,6,7,8,9,6,7,10)
)
#预览数据
head(df)
#使用tidyverse包对数据进行处理
df <- df %>% 
  gather(key = 'samples',value = 'values') #gather()函数可以把多列数据合并成一列数据

#添加分组信息
df$group = rep(c("A","B","C"), each = 20)
head(df)#预览数据

###############绘图###############
###1、使用vioplot包进行绘制
??vioplot#查看具体参数

vioplot(values~samples, data = df, 
        main = "vioplot", # 设置标题
        col=c("#000000", "#be0027", "#cf8d2e","#e4e932","#2c9f45","#371777"),# 设置小提琴颜色
        xlab="Samples", ylab="values") 
#具体大家可以在参数中进行设置

###2、基于ggplot2包进行绘制，也是我们主要讲的
#基本绘图
p1 <- ggplot(df, aes(x=samples, y=values, fill=samples)) + 
  geom_violin()

p1

#添加箱线图及均值点
p2<-p1+geom_boxplot(alpha=1,outlier.size=0, size=0.3, width=0.2,fill="white")+
  stat_summary(fun="mean",geom="point",shape=21, size=2,fill="blue")
p2

#自定义颜色
col=c("#000000", "#be0027", "#cf8d2e","#e4e932","#2c9f45","#371777")
p3<-p2+scale_fill_manual(values = col)
p3

#分面
p4<-p3+facet_grid(~group,scales = 'free')
p4
  
##显著性标记
p5<-p1+geom_signif(comparisons = list(c("A_1","A_2"),
                                      c("B_1","B_2"),
                                      c("C_1","C_2")),# 设置需要比较的组
                   map_signif_level = T, #是否使用星号显示
                   test = t.test, ##计算方法
                   size=0.8,color="black")
p5

#结合ggprism包进行个性化设置
p <- ggplot(df, aes(x=samples, y=values, fill=group))+#指定数据
  geom_violin(trim = T,position = position_dodge(width = 0.1), scale = 'width')+#绘制小提琴图函数
  geom_boxplot(alpha=1,outlier.size=0, size=0.3, width=0.2,fill="white")+#添加箱线图
  stat_summary(fun="mean",geom="point",shape=21, size=2,fill="blue")+#均值点
  labs(x="Samples",y=NULL)+#标题
  # geom_jitter(width = 0.2,size=2,pch=20,color="black")+#添加抖动点
  theme_prism(palette = "flames",
              base_fontface = "plain", # 字体样式，可选 bold, plain, italic
              base_family = "serif", # 字体格式，可选 serif, sans, mono, Arial等
              base_size = 16,  # 图形的字体大小
              base_line_size = 0.8, # 坐标轴的粗细
              axis_text_angle = 45)+ # 可选值有 0，45，90，270
  scale_fill_prism(palette = "flames")+
  geom_signif(comparisons = list(c("A_1","A_2"),#显著性
                                 c("B_1","B_2"),
                                 c("C_1","C_2")),# 设置需要比较的组
              map_signif_level = T, #是否使用星号显示
              test = "t.test", ##计算方法
              tip_length = c(c(0.01,0.01),
                             c(0.01,0.01),
                             c(0.01,0.01)),#横线下方的竖线设置
              size=0.8,color="black")
p


#背景色
color <- colorRampPalette(brewer.pal(11,"BrBG"))(30)
#配色
col <- colorRampPalette(brewer.pal(9,"Set1"))(6)
####绘图模板
ggplot(df, aes(x=samples, y=values, fill=samples))+#指定数据
  geom_violin(trim = T,position = position_dodge(width = 0.1), scale = 'width')+#绘制小提琴图函数
  geom_boxplot(alpha=1,outlier.size=0, size=0.3, width=0.2,fill="white")+#添加箱线图
  stat_summary(fun="mean",geom="point",shape=21, size=2,fill="blue")+#均值点
  labs(x=NULL,y=NULL)+#标题
  theme_bw()+
  theme(panel.grid = element_blank(), #背景
        axis.line=element_line(),#坐标轴的线设为显示
        legend.position="none",#图例位置
        axis.text=element_text(color='#003b64',size=12),
        legend.text = element_text(color='#003b64',size=12),
        axis.title= element_text(size=12),
        axis.text.x=element_text(angle = 45,vjust = 1,hjust = 1))+
  scale_fill_manual(values = col)+
  geom_signif(comparisons = list(c("A_1","A_2"),#显著性
                                 c("B_1","B_2"),
                                 c("C_1","C_2")),# 设置需要比较的组
              map_signif_level = T, #是否使用星号显示
              test = "t.test", ##计算方法
              tip_length = c(c(0.01,0.01),
                             c(0.01,0.01),
                             c(0.01,0.01)),#横线下方的竖线设置
              size=0.8,color="black")

#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)
