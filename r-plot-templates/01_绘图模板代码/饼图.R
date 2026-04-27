rm(list=ls())

#数据——随机生成
df<-data.frame(
  group=c('A', 'B', 'C', 'D', 'E'),
  value=c(55,75,20,60,100))

###使用pie()函数绘制
col<-rainbow(5)
pie(df$value, #扇形数值大小
    labels = df$group, #各扇形面积标签
    radius = 0.9,#饼图半径
    main = 'Pie',#标题
    clockwise = FALSE, #饼图各个切片是否按顺时针做出分割
    col = col)#自定义颜色
legend("topright", df$group, cex = 0.8,fill = col)#图例

pie(df$value, #扇形数值大小
    labels = df$group, #各扇形面积标签
    radius = 0.9,#饼图半径
    main = 'Pie',#标题
    clockwise = FALSE, #饼图各个切片是否按顺时针做出分割
    density = 20, # 设置阴影线密度
    angle = 45,#设置阴影线角度
    col = rainbow(5))#自定义颜色

###ggplot2包绘制
library(ggplot2)
ggplot(df, aes(x="", y = value, fill = group))+#数据
  geom_bar(width = 1, stat = "identity",color="white")+#绘制柱状图
  coord_polar('y')+#变为极坐标
  theme_void()+#主题
  scale_fill_manual(values=rainbow(5))+#自定义颜色
  geom_text(aes(y = sum(value)-cumsum(value)+value/2,
                    label = scales::percent(value/sum(value))), size=4.5)#标签
  

###ggstatsplot包绘制饼图
#以数据集mtcars为例
df1<-mtcars
library(ggstatsplot)
ggpiestats(df1, 'vs', #数据
           direction = 1, #方向，通过1和-1调整
           title = "Pie",#标题
           factor.levels = df1$vs,#标签
           slice.label = 'percentage',#标签类型，percentage/counts/both
           perc.k = 2,#百分数小数位数
           results.subtitle = F) #标题是否显示统计结果


###pie3D()函数绘制3D饼图
library(plotrix)
col<-rainbow(5)
pie3D(df$value, #数据
      labels = df$group, #标签
      theta = pi/5, 
      labelcex=1.2, #标签大小
      main = "3D pie",#标题
      explode = 0.1, #各扇形间隔
      height = 0.08,#各扇形高度
      radius = 1,#半径，0~1
      col = rainbow(5))#颜色
legend("topright", df$group, cex = 0.8,fill = col)#图例

###ggpubr包绘制
library(ggpubr)
ggpie(df, "value", #数据
      label = "group",#标签
      lab.pos = 'in',#标签位置
      lab.font = c(5, 'white'),#标签大小及颜色
      fill = "group", #填充
      color = "grey",#间隔颜色
      palette = rainbow(5))#填充颜色

###fan.plot()函数绘制扇形
library(plotrix)
col<-rainbow(5)
fan.plot(df$value,#绘图数据
         radius=1,#半径
         col=col,#填充颜色
         labels=df$group,#标签
         label.radius=1.1,#标签距扇形的距离
         align="left",#扇形对齐的位置
         main="Fan plot")#标题
legend("right", df$group, cex = 0.9,fill = col)#图例
# 参考：各函数帮助文档
