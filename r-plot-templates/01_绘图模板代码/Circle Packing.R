rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/Circle Packing')#设置工作路径
#加载R包
library(packcircles) # Circle Packing
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics

#加载数据
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)

#根据数据集生成圆心和半径
df1 <- circleProgressiveLayout(df$size, sizetype='area')
#合并数据集
data = cbind(df, df1)
df1$group <- df$group
#验证圆的面积和数值大小是否成正比
plot(data$radius^2, data$size)
# 生成50条直线用于绘制圆
data1 <- circleLayoutVertices(df1, #数据
                               npoints=50,#为每个圆生成的顶点数。
                               idcol=4,#圆标识符的可选索引或列名。
                               sizetype = "radius")#The type of size values: either "radius" (default) or "area". May be abbreviated.
data1$G <- rep(1:150,each=51)#由于设置的id列存在重复，绘图时会出现排列错乱现象，所以需要添加一列数据用于直线排列位置标识
ggplot() +
  geom_point(data=data,aes(x,y,size=size),color = "black")+
  scale_size(range = c(1,10))+
  geom_polygon(data = data1, 
               aes(x, y, group = G,
                   fill=as.factor(id)),
               color = "white") +#通过绘制大量的直线来填充这个圆
  scale_fill_manual(values = c("#d20962","#f47721","#7ac143","#00a78e","#00bce4","#7d3f98")) +
  theme_void() + 
  theme(legend.position="right") +
  labs(fill="Group")+#图例标题
  coord_equal()#保证x，y尺度大小相同

#参考：https://www.cnblogs.com/tecdat/p/15839746.html
