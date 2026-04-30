rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点+分组+置信圈+质心连线")

##加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(dplyr) # A Grammar of Data Manipulation

##加载数据——iris数据集
# data(iris)
df <- read.table("iris.txt", header = 1, check.names = F, sep = "\t")


##绘制基础散点图并根据分组着色
p <- ggplot(iris,aes(Sepal.Length,Sepal.Width))+
  geom_point(aes(color=Species))+
  theme_bw()
p

##添加置信圈
p1 <- p+stat_ellipse(aes(fill=Species,color=Species),
                     geom = "polygon", 
                     level = 0.95,#置信度95%
                     linetype=1,linewidth=0.6,alpha=0.2)
p1

##添加质心连线
#按照分组计算均值(质心点)：
mean <- aggregate(df[,1:2], by=list(df$Species), mean)
colnames(mean)[1] <- "Species"
#合并结果
df1 <- merge(df, mean, by = 'Species') #按分组合并均值列
df1
#绘图
p2 <- p1+geom_segment(data = df1, aes(x = Sepal.Length.y, y = Sepal.Width.y,
                                      xend = Sepal.Length.x, yend = Sepal.Width.x, color = Species),
                      alpha = 0.6, show.legend = FALSE)
p2


###个性化绘图模板
##散点
plot1 <- ggplot(iris,aes(Sepal.Length,Sepal.Width))+
  #散点
  geom_point(aes(fill = Species), 
             size = 3, shape = 21, color = "black")+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(size = 10),
        axis.title = element_text(color = "black", size = 12))+
  scale_fill_manual(values = c("#46bc99","#f68d42","#5ec6f2"))

##散点+质心连线
plot2 <- ggplot(iris,aes(Sepal.Length,Sepal.Width))+
  #质心连线
  geom_segment(data = df1, aes(x = Sepal.Length.y, y = Sepal.Width.y,
                               xend = Sepal.Length.x, yend = Sepal.Width.x, 
                               color = Species),
               alpha = 0.8, linewidth = 1, show.legend = FALSE)+
  #散点
  geom_point(aes(fill = Species), 
             size = 3, shape = 21, color = "black")+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(size = 10),
        axis.title = element_text(color = "black", size = 12))+
  scale_color_manual(values = c("#46bc99","#f68d42","#5ec6f2"))+
  scale_fill_manual(values = c("#46bc99","#f68d42","#5ec6f2"))

##散点+置信圈
plot3 <- ggplot(iris,aes(Sepal.Length,Sepal.Width))+
  #散点
  geom_point(aes(fill = Species), 
             size = 3, shape = 21, color = "black")+
  #置信圈
  stat_ellipse(aes(fill=Species,color=Species),
               geom = "polygon", 
               level = 0.95,#置信度95%
               linetype=1,linewidth=0.6,alpha=0.2)+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(size = 10),
        axis.title = element_text(color = "black", size = 12))+
  scale_color_manual(values = c("#46bc99","#f68d42","#5ec6f2"))+
  scale_fill_manual(values = c("#46bc99","#f68d42","#5ec6f2"))

##散点+质心连线+置信圈
plot4 <- ggplot(iris,aes(Sepal.Length,Sepal.Width))+
  #质心连线
  geom_segment(data = df1, aes(x = Sepal.Length.y, y = Sepal.Width.y,
                               xend = Sepal.Length.x, yend = Sepal.Width.x, 
                               color = Species),
               alpha = 0.8, linewidth = 1, show.legend = FALSE)+
  #散点
  geom_point(aes(fill = Species), 
             size = 3, shape = 21, color = "black")+
  #置信圈
  stat_ellipse(aes(fill=Species,color=Species),
               geom = "polygon", 
               level = 0.95,#置信度95%
               linetype=1,linewidth=0.6,alpha=0.2)+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(size = 10),
        axis.title = element_text(color = "black", size = 12))+
  scale_color_manual(values = c("#46bc99","#f68d42","#5ec6f2"))+
  scale_fill_manual(values = c("#46bc99","#f68d42","#5ec6f2"))

##拼图
library(patchwork)
(plot1+plot2)/(plot3+plot4)

