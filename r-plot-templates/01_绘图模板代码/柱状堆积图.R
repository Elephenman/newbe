rm(list=ls())#clear Global Environment
#安装包
# install.packages("ggplot2")
# install.packages("ggprism")
# install.packages("reshape")
# install.packages("ggalluvial")
#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape) # Flexibly Reshape Data
library(ggalluvial) # Alluvial Plots in 'ggplot2'
library(ggprism) # A 'ggplot2' Extension Inspired by 'GraphPad Prism'

# 构造数据
df<-data.frame(samples=c('a','b','c','d','e'),
               A=c(0.3,0.25,0.1,0.2,0.15),
               B=c(0.6,0.1,0.05,0.2,0.05),
               C=c(0.4,0.2,0.1,0.15,0.15),
               D=c(0.1,0.2,0.3,0.3,0.1),
               E=c(0.3,0.25,0.1,0.2,0.15),
               F=c(0.6,0.1,0.05,0.2,0.05),
               G=c(0.4,0.2,0.1,0.15,0.15),
               H=c(0.1,0.2,0.3,0.3,0.1),
               I=c(0.3,0.25,0.1,0.2,0.15),
               J=c(0.6,0.1,0.05,0.2,0.05),
               K=c(0.4,0.2,0.1,0.15,0.15),
               L=c(0.1,0.2,0.3,0.3,0.1))
# 变量格式转换,宽数据转化为长数据,方便后续作图
df1 <- melt(df,id.vars = 'samples')
names(df1)[1:2] <- c("group","X")  #修改列名

#绘图
p1 <- ggplot(df1, aes( x = X,y=100 * value,fill = group,
                 stratum = group, alluvium = group))+
  geom_stratum(width = 0.9, color='white')+
  # geom_flow(alpha = 0.3,width = 0.5)+
  geom_alluvium(alpha = 0.3,#透明度
                width = 0.9,#宽度
                color='white',#间隔颜色
                size = 1,#间隔宽度
                curve_type = "linear")+#曲线形状，有linear、cubic、quintic、sine、arctangent、sigmoid几种类型可供调整
  scale_y_continuous(expand = c(0,0))+# 调整y轴属性，使柱子与X轴坐标接触
  labs(x=NULL,y="Relative Abundance(%)",#设置X轴和Y轴的名称以及添加标题
       fill="group")+
  scale_fill_prism(palette = "summer")+#使用ggprism包修改颜色
  theme_light()+
  theme(legend.position = 'none')+
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='#333c41',size=12),
        legend.text = element_text(color='#333c41',size=12))
p1

p2 <- ggplot(df1, aes( x = X,y=100 * value,fill = group,
                       stratum = group, alluvium = group))+
  geom_alluvium(curve_type = "sine",#曲线形状，有linear、cubic、quintic、sine、arctangent、sigmoid几种类型可供调整
                alpha=1)+
  scale_y_continuous(expand = c(0,0))+# 调整y轴属性，使柱子与X轴坐标接触
  labs(x=NULL,y=NULL,#设置X轴和Y轴的名称以及添加标题
       fill="group")+
  scale_fill_prism(palette = "summer")+#使用ggprism包修改颜色
  theme_minimal()+
  theme(legend.position = 'right')+
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='#333c41',size=12),
        legend.text = element_text(color='#333c41',size=12),
        axis.text.y = element_blank())
p2
#拼图
cowplot::plot_grid(p1,p2,ncol = 2)
