rm(list=ls())#clear Global Environment
setwd('D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\气泡图')#设置工作路径

#安装包
# install.packages("ggplot2")
# install.packages("ggprism")
#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggprism) # A 'ggplot2' Extension Inspired by 'GraphPad Prism'
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization
#读取数据
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)

######绘图#######
#1、基本绘图
p1<-ggplot(df,aes(A,B,fill=C))+
  geom_point(aes(size=D,color=C))
p1

#自定义颜色
col<-c("#000000", "#be0027", "#cf8d2e","#e4e932","#2c9f45")
p2<-p1+scale_color_manual(values=col)
p2

#调整气泡相对大小
p3<-p2+scale_size_continuous(range = c(0.5, 15))
p3

#更换数据显示为不同气泡图
p4<-ggplot(df,aes(C,B,fill=A))+
  geom_point(aes(size=D,color=A))+
  scale_size_continuous(range = c(0.5, 15))
p4

#气泡形状
p5<-ggplot(df,aes(A,B,color=C,size=D,fill=C))+
  geom_point(color="black",shape=22)#设置形状
p5


#结合ggprism包进行个性化设置
ggplot(df,aes(A,B,#数据
              color=C,#根据C列的数据填充颜色
              size=D,#气泡大小根据D列数据
              fill=C))+#根据C列数据填充颜色
  geom_point(color="black",#气泡边框色
             shape=21)+#形状
  scale_size_continuous(range = c(0.5, 15))+#气泡的相对大小
  theme_prism(palette = "flames",
              base_fontface = "plain", # 字体样式，可选 bold, plain, italic
              base_family = "serif", # 字体格式，可选 serif, sans, mono, Arial等
              base_size = 16,  # 图形的字体大小
              base_line_size = 0.8, # 坐标轴的粗细
              axis_text_angle = 45)+ # 可选值有 0，45，90，270
  scale_fill_prism(palette = "candy_bright")+#填充色
  labs(title = "Chart", # 定义主标题
       subtitle = "XXXXXXX", # 定义子标题
       x = "XXXXX", # 定义x轴文本
       y = "XXXXX")# 定义y轴文本



###绘图模板
ggplot(df,aes(A,B,color=C,size=D,fill=C))+#色
  geom_point(color="black",#气泡边框色
             shape=21,alpha=0.9)+#形状
  scale_size_continuous(range = c(1, 15))+#气泡的相对大小
  theme_bw()+
  theme(panel.grid = element_blank(), #背景
        axis.line=element_line(),#坐标轴的线设为显示
        axis.text=element_text(color='black',size=12),
        legend.text = element_text(color='black',size=12),
        axis.title= element_text(size=12),
        axis.text.x=element_text(vjust = 1,hjust = 1),
        legend.key = element_blank())+
  scale_fill_manual(values=c("#34a186","#f9cb45","#b5182b","#4cb1c4","#ab96d2"))+#指定颜色
  labs(x = NULL, # 定义x轴文本
       y = NULL)# 定义y轴文本

#背景色
color <- colorRampPalette(brewer.pal(11,"BrBG"))(30)
#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

