rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点图+拟合曲线+边际组合图形')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggpmisc) # Miscellaneous Extensions to 'ggplot2'
library(ggpubr) # 'ggplot2' Based Publication Ready Plots
library(gghalves) # Compose Half-Half Plots Using Your Favourite Geoms

#读取数据——以Chiplot绘图平台数据为例
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)

#自定义颜色
col<-c("#0099e5")

###绘图
#散点图
p1 <- ggplot(df,aes(x,y,fill=group))+
  geom_point(shape=21,size=3,alpha=0.5)+
  #添加回归曲线并添加置信区间
  geom_smooth(method = "lm",aes(color=group), se=T, 
              formula = y ~ x,
              linetype=1,alpha=0.5)+
  #计算R值和p值
  stat_cor(color=col,method = "pearson",label.x = 0.2, label.y = 8.5,size=4)+
  #添加回归方程
  stat_poly_eq(formula = y ~ x, 
               aes(color=group,label = paste(after_stat(eq.label),
                                             sep = "~~~")), parse = TRUE) +
  #颜色
  scale_fill_manual(values = col)+
  scale_color_manual(values = col)+
  #主题设置
  theme_bw()+
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='black',size=12),
        axis.title = element_text(color='black',size=14),
        legend.position = "none")+
  #标题设置
  labs(x="The title of x",y="The title of y")
p1

###添加边际组合图形——散点+箱线图+半小提琴
#小提示：这里可以以group作为X轴输入，但是由于X轴范围过大，故更换为固定数值1，大家可以试试
# 右边边际图
p2 <- ggplot(df,aes(1,y))+
  #半小提琴图
  geom_half_violin(fill="#00d1b2",position = position_nudge(x=0.26),side = "r",width=0.5,color=NA)+
  #箱线图
  geom_boxplot(fill="#ff4c4c",width=0.1,size=1.2,outlier.color =NA,position = position_nudge(x=0.2))+
  #散点图
  geom_jitter(fill="#0099e5",shape=21,size=3,width=0.12,alpha=0.5)+
  theme_void()+
  theme(legend.position = "none")
p2
#顶部边际图
p3 <- ggplot(df,aes(1,x))+
  geom_half_violin(fill="#00d1b2",position = position_nudge(x=0.26),side = "r",width=0.5,color=NA)+
  geom_boxplot(fill="#ff4c4c",width=0.1,size=1.2,outlier.color =NA,position = position_nudge(x=0.2))+
  geom_jitter(fill="#0099e5",shape=21,size=3,width=0.12,alpha=0.5)+
  theme_void()+
  theme(legend.position = "none")+
  coord_flip()
p3

#组合图形——基于aplot包进行组合
library(aplot) # Decorate a 'ggplot' with Associated Information
p1%>%insert_top(p3,height = 0.4)%>%
  insert_right(p2,width = 0.4)
