rm(list=ls())#clear Global Environment
#设置工作目录
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/热图+显著性+间隔+注释+柱状图")

##加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
#加载绘图数据
data1 <- read.table("data1.txt",sep="\t",header = T,check.names = F)
data2 <- read.table("data2.txt",sep="\t",header = T,check.names = F)

##数据清洗与转换
#为方便后续添加方框，需要将x和y轴转变成数值型，这里我们添加一列数据
data1$Y <- c(1,2,3,4)
data2$Y <- c(1,2,3,4)
#将数据转变成长格式
df1 <- melt(data1,id.vars = c("group","Y"))
#为方便后续添加方框，需要将x和y轴转变成数值型，这里我们添加一列数据
df1$X <- rep(1:9, each = 4)
#添加一个分组，方便后续进行间隔添加
df1$gap <- rep(c(1,2,3),times = c(4,4,28))

##绘制基本热图
p1 <- ggplot(df1, aes(X, Y)) +
  #添加圆周围的方框
  geom_rect(aes(xmin = X-0.5, xmax = X+0.5, ymin = Y-0.5, ymax = Y+0.5), color = "grey40",fill="white") +
  #绘制散点图，这里先将其中符合要求的点进行绘制
  geom_point(aes(size= ifelse(value > 0, value, 0),color=ifelse(value > 0, value, 0)))+
  #颜色
  scale_color_continuous(low = "white", high = "#23589e") +
  #将不符合要求的点使用固定大小和颜色的点显示
  geom_point(data = df1[df1$value == 0, ], shape = 21, size = 1, color = "black",fill="grey50")+
  #为图中不显著的数据添加NS标记
  geom_text(data = subset(df1, value > 0 & value < 0.5),
            aes(label = "NS"), size=4,color="#92461f",vjust=-0.1)+
  #自定义X轴和Y轴的标签
  scale_x_continuous(position = "top",breaks = c(1:9), labels = c("Overall transm.", "CosteaPl_2017_DEU", "BritolL_2016",
                                                 "Guinea-Bissau", "PasolliE_2018_MDG","PehrssonE_2016_PER",
                                                 "PehrssonE_2016_SLV","Ghana","Tanzania")) +
  scale_y_continuous(breaks = c(1:4), labels = data1$group)+
  #主题设置
  theme_void()+
  theme(axis.text.x = element_text(angle = 45,hjust = 0,vjust = 0,size=10,color="black"),
        axis.text.y = element_text(color="black",size=10,vjust = 0,hjust = 1))+
  #标题
  labs(x=NULL,y=NULL,color="SGB transmissibility")+
  guides(size = "none")+#去除size的图例
  #设置散点的显示范围
  scale_size_continuous(range = c(1,8))+
  #通过分面形式为图形添加间隔
  facet_grid(~gap,scales = 'free',space = "free")+
  theme(strip.text = element_blank())+
  #添加最下方的矩形注释
  geom_rect(data = df1[df1$gap == 2, ], aes(xmin = 1.5, xmax = 2.5, ymin = -Inf, ymax = 0.3),
            fill = "#6c3417")+
  geom_rect(data = df1[df1$gap == 3, ], aes(xmin = 2.5, xmax = 9.5, ymin = -Inf, ymax = 0.3),
            fill = "#68a030")
p1

#绘制柱状图
p2 <- ggplot(data2,aes(Y,value))+
  geom_col(fill="#b2b2b2",width = 0.8)+
  theme_classic()+
  theme(axis.text.x = element_text(color = "black",size=12),
        axis.ticks.x = element_line(color = "black",linewidth=0.8),
        axis.line.x = element_line(color = "black",linewidth=0.8),
        axis.text.y=element_blank(),
        axis.ticks.y=element_blank(),
        axis.line.y = element_blank(),
        plot.title = element_text(color="black",hjust = 0.5,size=15),
        plot.background = element_blank())+
  coord_flip()+#旋转图形
  labs(x=NULL,y=NULL,title = "Prevalence(%)")+
  scale_y_continuous(expand = c(0,0))
p2

###拼接图形
p1%>%aplot::insert_right(p2,width = 0.2)

###最后使用AI或者PS调整图形细节即可

