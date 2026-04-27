#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/点+误差棒")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
#构造数据
df <- read.table("data2.txt",header = T, check.names = F)
data=melt(df)
#误差棒这里我们随机编写，无实际意义
data$er=data$value/10
#绘图
ggplot(data,aes(variable,value))+
  geom_point(aes(color=variable),size=3)+
  facet_wrap(~ group, ncol =3)+
  geom_errorbar(aes(ymin = value-er, ymax = value+er,color=variable),
                width = 0.2,position = position_dodge(width = 0.8),cex=1.2)+ #添加误差棒
  labs(x="",y=NULL)+#去除轴标题
  theme_bw()+#主题
  theme(panel.grid=element_blank(),
        axis.text.y=element_text(color='black',size=10),
        axis.text.x=element_blank(),
        axis.ticks.x = element_blank(),
        legend.text = element_text(color='black',size=12),
        legend.title = element_text(color='red',size=13),
        strip.background.x = element_rect(fill = "#0081b4", color = "black"))+
  scale_y_continuous(expand = c(0, 0), limit = c(5, 23))+#去除网格线
  scale_color_manual(values=c("#004a77","#00adee","#ff8100","red"))

