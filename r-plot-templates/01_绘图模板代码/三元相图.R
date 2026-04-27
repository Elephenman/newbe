rm(list = ls())
setwd("D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\三元相图")

#安装R包
# install.packages("ggtern")
#加载R包
library(ggtern) # An Extension to 'ggplot2', for the Creation of Ternary Diagrams
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualizatio
# 加载数据
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)
# 创建分组信息数据集
df$group <-  rep(c("T", "D", "L", "K"),each = 20)
#计算3个样本的平均值定义点的大小
df$size <- (apply(df[2:4], 1, mean))

#配色
col <- colorRampPalette(brewer.pal(11,"Set1"))(4)
#背景色
color <- colorRampPalette(brewer.pal(11,"PuOr"))(30)
#绘图
ggtern(data=df,aes(x=A,y=B,z=C))+ #X,Y,Z轴分别代表的变量
  geom_mask()+# 显示超出边界的点
  geom_point(aes(size=size,#以散点图形式呈现，大小是size
                 color=group),#颜色映射的为group变量
             alpha=0.8)+#透明度
  scale_colour_manual(values = col)+#自定义颜色
  guides(color = guide_legend(override.aes = list(size = 4)))+#改变颜色映射图例符号大小
  theme_classic()+#主题
  labs(title = "Ternary plot")+#标题
  theme(axis.line=element_line(linetype=1,color="grey",size=1),#坐标轴粗细、类型及颜色设置
    plot.title = element_text(size=15,hjust = 0.5)) #标题大小和位置
#添加背景
grid.raster(alpha(color, 0.1), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)


