rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/圆环图&旭日图_ggplot2")

##绘图思路：
   #通过ggplot2绘制单组或多组条形图，然后变换坐标系即可获圆环图及多环图
   #绘制旭日图时需要调整x轴位置确定各个环的所在位置


###加载所需R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(formattable) # Create 'Formattable' Data Structures

##加载数据（随即编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")
head(df) 

###根据不同分组计算其值和及标签位置
##group1
#使用aggregate函数计算每个组的值和
data1 <- aggregate(value ~ group1, df, sum)
#计算相对丰度
data1$Rel <- data1$value/sum(data1$value)
#转换为百分比
data1$per <- percent (data1$Rel,1)
data1$group1 <- factor(data1$group1, levels = c("g1","g2","g3","g4","g5"))
#确定标签位置
data1$ymax<-cumsum(data1$Rel)
data1$ymin<-c(0,head(data1$ymax,n=-1))
data1$labelposition<-(data1$ymax + data1$ymin)/2

##group2
data2 <- aggregate(value ~ group2, df, sum)
data2$Rel <- data2$value/sum(data2$value)
data2$per <- percent (data2$Rel,1)
data2$group2 <- factor(data2$group2, levels = c("A","B","C"))
data2$ymax<-cumsum(data2$Rel)
data2$ymin<-c(0,head(data2$ymax,n=-1))
data2$labelposition<-(data2$ymax + data2$ymin)/2

##group3
data3 <- aggregate(value ~ group3, df, sum)
data3$Rel <- data3$value/sum(data3$value)
data3$per <- percent (data3$Rel,1)
data3$group3 <- factor(data3$group3, levels = c("G1","G2"))
data3$ymax<-cumsum(data3$Rel)
data3$ymin<-c(0,head(data3$ymax,n=-1))
data3$labelposition<-(data3$ymax + data3$ymin)/2

#########绘制圆环图#############
p1 <- ggplot(data1,aes(ymax=ymax,ymin=ymin,
                xmax=3,xmin=2))+
  #通过方块先绘制柱状堆积图
  geom_rect(aes(fill=group1))+
  #添加标签
  geom_text(x=2.5,aes(y=labelposition,label=paste0(group1,"\n(",per,")")),size=4, color = "black")+
  #通过拉大x轴范围实现环图绘制
  xlim(1,3)+
  #转换为极坐标
  coord_polar(theta="y")+
  theme_void()+
  theme(legend.position = "none")+
  #自定义颜色
  scale_fill_manual(values = c("#ffaaaa", "#ffc2e5","#ebffac","#c1f1fc","#00c7f2"))
p1
##在环图中间增加空白间隔
p2 <- p1+ylim(0,1.1)
p2


###########绘制双环图################
p3 <- ggplot()+
  #通过方块先绘制第一层饼图
  geom_rect(data=data2,aes(ymax=ymax,ymin=ymin,
                      xmax=2,xmin=0,#x轴0-2绘制第一层
                      fill=group2),
            color="white",linewidth=1)+
  #绘制第二层圆环图
  geom_rect(data=data1,aes(ymax=ymax,ymin=ymin,
                      xmax=3.5,xmin=2,#x轴2-3.5绘制第二层
                      fill=group1),
            color="white",linewidth=1,alpha=0.4)+
  #添加第一层标签
  geom_text(data=data2,aes(x=1,#标签在x=1的位置上，确保在0-2中间
                           y=labelposition,
                           label=paste0(group2,"\n(",per,")")),
            size=4, color = "black")+
  # #添加第二层标签
  geom_text(data=data1,aes(x=2.75,#标签在x=2.75的位置上，确保在2-3.5中间
                           y=labelposition,
                           label=paste0(group1,"\n(",per,")")),
            size=3, color = "black")+
  #通过拉大x轴范围实现环图绘制
  xlim(0,3.5)+
  #转换为极坐标
  coord_polar(theta="y")+
  theme_void()+
  theme(legend.position = "none")+
  #自定义颜色,建议将内外环对应的组颜色设置为一致
  scale_fill_manual(values = c("A"="#ffc168","B"="#2dde98","C"="#1cc7d0",
                               "g1"="#ffc168","g2"="#ffc168","g3"="#2dde98",
                               "g4"="#1cc7d0","g5"="#1cc7d0"))
p3

##在环图中间增加空白间隔
p4 <- p3+ylim(0,1.1)
p4


###########绘制三环旭日图################
p5 <- ggplot()+
  #通过方块先绘制第一层饼图
  geom_rect(data=data3,aes(ymax=ymax,ymin=ymin,
                           xmax=2,xmin=0,#x轴0-2绘制第一层
                           fill=group3),
            color="white",linewidth=1)+
  #绘制第二层圆环图
  geom_rect(data=data2,aes(ymax=ymax,ymin=ymin,
                           xmax=3.5,xmin=2,#x轴2-3.5绘制第二层
                           fill=group2),
            color="white",linewidth=1,alpha=0.6)+
  #绘制第三层圆环图
  geom_rect(data=data1,aes(ymax=ymax,ymin=ymin,
                           xmax=5,xmin=3.5,#x轴3.5-5绘制第三层
                           fill=group1),
            color="white",linewidth=1,alpha=0.3)+
  #添加第一层标签
  geom_text(data=data3,aes(x=1,#标签在x=1的位置上，确保在0-2中间
                           y=labelposition,
                           label=paste0(group3,"\n(",per,")")),
            size=3.5, color = "black")+
  ##添加第二层标签
  geom_text(data=data2,aes(x=2.75,#标签在x=2.75的位置上，确保在2-3.5中间
                           y=labelposition,
                           label=paste0(group2,"\n(",per,")")),
            size=3, color = "black")+
  ##添加第三层标签
  geom_text(data=data1,aes(x=4.25,#标签在x=4.25的位置上，确保在3.5-5中间
                           y=labelposition,
                           label=paste0(group1,"\n(",per,")")),
            size=3, color = "black")+
  #通过拉大x轴范围实现环图绘制
  xlim(0,5)+
  #转换为极坐标
  coord_polar(theta="y")+
  theme_void()+
  theme(legend.position = "none")+
  #自定义颜色,建议将内外环对应的组颜色设置为一致
  scale_fill_manual(values = c("G1"="#ff4e00","G2"="#01cd74",
                               "A"="#ff4e00","B"="#ff4e00","C"="#01cd74",
                               "g1"="#ff4e00","g2"="#ff4e00","g3"="#ff4e00",
                               "g4"="#01cd74","g5"="#01cd74"))
p5
##在环图中间增加空白间隔
p6 <- p5+ylim(0,1.1)
p6

###拼图
library(patchwork)
(p1+p3+p5)/(p2+p4+p6)
