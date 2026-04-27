#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/柱状图+散点图+折线图")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(tidyr) # Tidy Messy Data
library(dplyr) # A Grammar of Data Manipulation
library(ggsignif) # Significance Brackets for 'ggplot2'

#数据——ggplot自带的ToothGrowth数据
df <- ToothGrowth
df$dose <- as.factor(df$dose)
data <- df
#计算均值及标准差
df1 <- data%>% group_by(dose)%>%
  summarise(mean= mean(len), sd= sd(len))
#绘图
ggplot()+ 
  #柱状图绘制
  geom_bar(df1,mapping=aes(x=dose,y=mean), fill = "white",
           size = 1.5,color = c("#d20962","#f47721","#7ac143"),position="dodge",
           stat="identity",width = 0.6)+
  #误差线
  geom_errorbar(df1,mapping=aes(x = dose,ymin = mean-sd, ymax = mean+sd),
                width = 0.3,color = c("#d20962","#f47721","#7ac143"), size=1.5)+
  #散点图
  geom_jitter(df, mapping=aes(x=dose,y=len,fill = dose,color = dose,shape = dose),
              size = 2.5,width = 0.2,alpha=0.9)+ 
  #折线图
  geom_line(df1,mapping=aes(x=dose,y=mean,group=1),
            size=1,color="#00aee6")+
  #为折线图添加数据点
  geom_point(df1,mapping=aes(x=dose,y=mean),color="black",size=3,shape=8)+
  #自定义颜色
  scale_color_manual(values = c("#d20962","#f47721","#7ac143"))+ 
  #显著性
  geom_signif(df,mapping=aes(x=dose,y=len), 
              comparisons = list(c("0.5", "1"),
                                 c("1","2"),
                                 c("0.5","2")),
              map_signif_level=T, 
              tip_length=c(0,0,0,0,0,0), 
              y_position = c(35,40,45), 
              size=1, textsize = 7, 
              test = "t.test")+
  #y轴范围
  scale_y_continuous(expand = c(0, 0), limit = c(0, 50))+
  #主题设置
  theme_classic(base_line_size = 1)+
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='black',size=13,face = "bold"),
        axis.title.y = element_text(color='black',size=15,face = "bold"),
        legend.text = element_text(color='black',size=13,face = "bold"),
        legend.title = element_blank(),
        legend.position = "none")+
  #轴标题
  labs(x=NULL,y="Value")



