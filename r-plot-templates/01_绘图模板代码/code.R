rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/柱状图+散点图+误差线+显著性+截断")
#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggsignif) # Significance Brackets for 'ggplot2'
library(ggpubr) # 'ggplot2' Based Publication Ready Plots
library(ggbreak) # Set Axis Break for 'ggplot2'
# 加载示例数据
data <- read.table("data.txt",check.names = T,header = 1)
data$group <- factor(data$group,levels = c("OT-II","OT-I"))
##绘图
ggplot(data,aes(sample,value))+
  #误差线
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.15,size=1)+
  #柱状图
  geom_bar(aes(fill=group),color="black",stat="summary",fun=mean,position="dodge",size=0.5)+
  #散点图
  geom_jitter(color="black",size = 2.5,width = 0.2,alpha=0.9)+
  #显著性
  geom_signif(comparisons = list(c("IM","TC")),
              map_signif_level=T, 
              tip_length=0, 
              y_position = 1200, 
              size=1, 
              test = "t.test")+
  #分面
  facet_wrap(~group)+
  #颜色
  scale_fill_manual(values = c("#009700","#fa3f3f"))+
  #主题设置
  theme_classic()+
  theme(axis.line = element_line(size = 1),
        axis.text.x = element_text(color = "black", angle = 90,vjust = 0.5,hjust = 1,size = 15),
        axis.text.y = element_text(color = "black",size = 15),
        axis.ticks = element_line(color = "black",size = 1),
        legend.position = "none",
        strip.background = element_blank(),
        strip.text = element_text(color = "black",size = 16),
        axis.title = element_text(color = "black",size = 18))+
  #轴标题
  labs(x=NULL,y="cells per"~mm^2)+
  #y轴截断
  scale_y_break(c(10,45),
                scales=1.2, 
                ticklabels=c(50,100),
                space=0.2)+
  scale_y_break(c(100,600),
                scales=2.5, 
                ticklabels=c(600,800,1200),
                space=0.2)



