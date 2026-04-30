rm(list = ls())

#安装R包
# install.packages("ggbump")
# install.packages("ggplot2")
# install.packages("ggprism")
#加载R包
library(ggbump)
library(ggplot2)
library(ggprism)
library(dplyr)
#数据——随机生成
#注：要保证X轴和Y轴为数值型数据，否则无法绘制
df<-data.frame(
  x=rep(1:6,4),
  y=c(10,12,14,12,14,16, 12,14,12,10,12,12, 14,16,10,14,16,10, 16,10,16,16,10,14),
  z=c(rep('g1',6),rep('g2',6),rep('g3',6),rep('g4',6)))
head(df)

#绘图
ggplot(df, aes(x = x, y = y, color = z)) +#数据
  geom_bump(size = 1.2)+#基本凹凸图绘制
  geom_point(size = 10)+#添加节点
  scale_color_prism(palette = 'candy_bright')+#自定义颜色
  theme_void() +#主题
  geom_text(data = df,
            aes(x = x, label = z),
            size = 4, color='white')+#添加标签
  theme(legend.position = "none")#去除图例


#参考：https://r-charts.com/ranking/ggbump/