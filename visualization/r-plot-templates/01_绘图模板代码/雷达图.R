rm(list = ls())

#数据——生成绘图数据
set.seed(12)
df <- data.frame(
  group=LETTERS[1:5],
  V1=sample(1:50, 5, replace = FALSE),
  V2=sample(20:50, 5, replace = FALSE),
  V3=sample(1:50, 5, replace = FALSE),
  V4=sample(30:50, 5, replace = FALSE),
  V5=sample(10:50, 5, replace = FALSE))
rownames(df)<-df$group#修改行名
df<-df[-1]#删除多余行
df <- rbind(rep(50,5) , rep(0,5) , df)#加入限定雷达图极限值范围

#安装包
# install.packages("fmsb")
#加载包
library(fmsb) # Functions for Medical Statistics Book with some Demographic Data
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization 
####绘图
#背景色
color <- colorRampPalette(brewer.pal(11,"PuOr"))(30)
#填充色建议大家使用一些浅色系的颜色，不然容易覆盖底部的图
radarchart(df,#数据
           pcol=rainbow(5),#多边形特征：线的颜色
           # pfcol=rainbow(5),#多边形特征：填充色
           plwd=2,#多边形特征：线宽
           plty=2,#多边形特征：线形
           cglcol='grey',#网格特征:网格颜色
           cglty=1,#网格特征:网格线形
           axistype=1,#坐标轴类型
           axislabcol='red',#网格特征:轴颜色
           caxislabels=seq(0,50,5),#网格特征:轴范围
           cglwd=0.8,#网格特征:网格线宽
           vlcex=0.8)#组标签大小
#添加图例
legend(x=1.2, y=1.2, legend = rownames(df[-c(1,2),]), 
       bty = "n", pch=20 , col=rainbow(5) , 
       text.col = "black", cex=1.2, pt.cex=3)
#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

#加入填充色
col<- rainbow(5)
colors_in <- alpha(col,0.1)
#绘图
radarchart(df,#数据
           pcol=rainbow(5),#多边形特征：线的颜色
           pfcol=colors_in,#多边形特征：填充色
           plwd=1.5,#多边形特征：线宽
           plty=2,#多边形特征：线形
           cglcol='grey70',#网格特征:网格颜色
           cglty=1,#网格特征:网格线形
           axistype=1,#坐标轴类型
           axislabcol='red',#网格特征:轴颜色
           caxislabels=seq(0,50,5),#网格特征:轴范围
           cglwd=0.8,#网格特征:网格线宽
           vlcex=0.8)#组标签大小
#添加图例
legend(x=1.2, y=1.2, legend = rownames(df[-c(1,2),]), 
       bty = "n", pch=20 , col=rainbow(5) , 
       text.col = "black", cex=1.2, pt.cex=3)

#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)
#参考：https://r-graph-gallery.com/143-spider-chart-with-saveral-individuals.html

