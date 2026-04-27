rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/柱状图+散点+配对连线+显著性")
#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggsignif) # Significance Brackets for 'ggplot2'
library(ggpubr) # 'ggplot2' Based Publication Ready Plots

#加载数据
df <- read.table("data.txt",header = 1,check.names = F,sep = "\t")
df$group1 <- factor(df$group1,levels = c("mCherry","hM3Dq","Cherry","M3Dq"))
df$group2 <- factor(df$group2,levels = c("Saline","CNO"))
#绘图
ggplot(df,aes(group2,value))+
  #误差线
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.15,size=0.8)+
  #柱状图
  geom_bar(aes(fill=group3),color="black",stat="summary",fun=mean,position="dodge",width = 0.7)+
  #配对连线
  geom_line(aes(group=paired),color="grey30",linewidth=0.8)+
  #散点
  geom_point(fill="black",size=3,color="grey",shape=21)+
  #分面
  facet_grid(~group1,scales = 'free_x',space = "free")+
  #显著性
  geom_signif(comparisons = list(c("Saline","CNO")),
              map_signif_level=T, y_position = 170, 
              tip_length = c(c(0.05,0.05),c(0.05,0.05)),
              size=1, textsize = 6, test = "t.test")+
  #y轴范围
  scale_y_continuous(limits = c(0,200),expand = c(0,0))+
  #主题
  theme_classic()+
  theme(legend.position = "none",
        strip.background = element_blank(),
        strip.text = element_text(color = "black",size = 16),
        axis.text.x = element_text(color = "black", angle = 90,vjust = 0.5,hjust = 1,size = 15),
        axis.text.y = element_text(color = "black",size = 15),
        axis.line = element_line(size = 1),
        axis.ticks = element_line(color = "black",size = 1),
        axis.title = element_text(color = "black",size = 18),
        axis.ticks.length.x = unit(0.2, "cm"))+
  #轴标题
  labs(x=NULL,y="Investigation duration (s)")+
  #颜色
  scale_fill_manual(values = c("#84bd00","#efdf00","#fe5000","#e4002b",
                               "#da1884","#a51890","#0077c8","#008eaa"))
