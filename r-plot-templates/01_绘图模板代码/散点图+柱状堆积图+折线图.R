rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点图+柱状堆积图+折线图')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggpmisc) # Miscellaneous Extensions to 'ggplot2'
library(ggalt) # Extra Coordinate Systems, 'Geoms', Statistical Transformations,Scales and Fonts for 'ggplot2' 
#读取数据
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)
df2 <- read.table(file="data2.txt",sep="\t",header=T,check.names=FALSE)
df3 <- read.table(file="data3.txt",sep="\t",header=T,check.names=FALSE)
######绘图#######
##散点图
#绘图
p <- ggplot(df,aes(x,y))+
  geom_point(shape=21,size=3,alpha=0.5,fill="#be0027")+
  #添加回归曲线并添加置信区间
  geom_smooth(method = "lm", se=T, 
              formula = y ~ x,
              linetype=1,alpha=0.5,color="#00c7f2")+
  #添加回归方程
  stat_poly_eq(formula = y ~ x, 
               aes(label = paste(after_stat(eq.label),
                                             after_stat(rr.label),sep = "~~~")), parse = TRUE,
               color="blue") +
  theme_bw()+
  theme(panel.grid=element_blank())+
  labs(x=NULL,y=NULL)
p

###柱状堆积图+折线图
#构建颜色
col2 <- c("#ffed00","#ff0092","#c2ff00","#00c7f2")
p1<-ggplot()+
  geom_col(df2, mapping=aes(x = sample,y=value,fill = group),
           position = 'stack', width = 0.6)+
  geom_line(df3,mapping=aes(x = sample,y=value,group=1),linewidth=1,color="black",linetype=3)+
  geom_point(df3,mapping=aes(x = sample,y=value),shape=21,color="black",fill= "#db3552",size=3)+
  scale_y_continuous(expand = c(0,0),limits = c(0,210))+
  labs(x="Samples",y="Relative Abundance(%)",
       fill=NULL)+
  guides(fill=guide_legend(keywidth = 1, keyheight = 1))+
  theme_bw()+
  theme(legend.position = c(0.04, .93),
        legend.justification = c(0.05, 0.5),
        legend.direction = 'horizontal',
        axis.title.x=element_text(size=12),
        axis.title.y=element_text(size=12,angle=90),
        axis.text.y=element_text(size=10,color = "black"),
        axis.text.x=element_text(size=10,color = "black"),
        panel.grid=element_blank())+
  scale_fill_manual(values = col2)
p1

####组合图
p1 + annotation_custom(grob=ggplotGrob(p),ymin = 70, ymax = 205, xmin=4.2, xmax=8.5)


