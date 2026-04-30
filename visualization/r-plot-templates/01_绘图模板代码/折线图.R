rm(list=ls())
#设置工作环境
setwd("D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\折线图")

#安装包
# install.packages("ggplot2")
# install.packages("reshape2")
# install.packages("ggprism")
# install.packages("ggalt")
#加载包
library(ggplot2)
library(reshape2)
library(ggprism)
library(ggalt)
#生成作图数据
df <- data.frame(
  y1=c(2,5,6,7,8,6,7,10,4),
  y2=c(10,12,14,15,10,12,13,9,10),
  y3=c(7,8,9,6,4,8,9,3,6)
)
#转换数据
data=melt(df)
data$x<-rep(c(1,2,3,4,5,6,7,8,9))
#修改列名
colnames(data)=c("group","y","x")
####绘图
#基础绘图
p1<-ggplot(data, aes(x, y, group=group, color=group, shape=group,linetype=group))+
  geom_point(size=3)+
  geom_line(size=1)
p1
#修改线形
p1+scale_linetype_manual(values = c(y1 = 4, y2 = 1, y3 = 3))
#自定义颜色
p1+scale_color_manual(values = c('#ec1c24','#fdbd10','#0066b2'))
#自定义节点形状
p1+scale_shape_manual(values = c(17,18,19))
#修改主题
p1+theme_bw()
#修改图例
p1+theme(legend.title = element_blank(),#图例标题去除
      legend.text = element_text(family = 'serif'),#字体
      legend.position = c(0.05,0.9),#位置
      legend.direction = "vertical")#水平或垂直
#使得折线图曲线平滑
ggplot(data, aes(x, y, group=group, color=group, shape=group))+
  geom_point(size=3)+
  geom_xspline(spline_shape = -0.3,size=1)

###个性化绘图
ggplot(data, aes(x, y, group=group, color=group, shape=group,linetype=group))+
  geom_point(size=3)+#散点
  geom_xspline(spline_shape = -0.3,size=1)+#曲线平滑
  scale_color_manual(values = c('#ec1c24','#fdbd10','#0066b2'))+#自定义颜色
  theme_prism(palette = "candy_soft",#主题设置
              base_fontface = "plain", 
              base_family = "serif", 
              base_size = 16,  
              base_line_size = 0.8, 
              axis_text_angle = 45)+
  theme(legend.title = element_blank(),#图例标题去除
        legend.text = element_text(family = 'serif'),#字体
        legend.position = c(0.9,0.9),#位置
        legend.direction = "vertical")+#水平或垂直
  labs(title = "XXX", # 定义主标题
       subtitle = "XXXXXXX", # 定义子标题
       x = "XXXXX", # 定义x轴文本
       y = "XXXXX")# 定义y轴文本
