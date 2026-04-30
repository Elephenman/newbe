#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/分组直方图")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggpubr)
#加载数据
df <- read.table("data.txt",header = T,sep='\t')
df$group <- factor(df$group,levels = c("Sal","Coca","Ket","LSD","MDMA"))
df$sample <- factor(df$sample,levels = c("48 h","2 wk"))

#绘图
col <- c("#000000","#575757","#c53a8e","#e79600","#a42422")
col2 <- c("#767475","#000000","#872860","#f0b75b","#c97c7b")
ggplot(df,aes(sample,value))+
  geom_bar(aes(fill=group),color="black",stat="summary",fun=mean,position="dodge",size=1)+
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0,linewidth=1)+
  geom_point(aes(color=group),shape=21,size=4,stroke=1.5)+
  geom_hline(yintercept = 0, linetype = 1, color = "black", size = 1)+
  facet_grid(~group,scales = 'free_x',space = "free")+
  scale_color_manual(values = col2)+
  scale_fill_manual(values = col)+
  theme_classic()+
  theme(axis.line = element_line(size = 1),
        axis.text.x = element_text(color = "black", angle = 90,vjust = 0.5,hjust = 1,size = 15),
        axis.text.y = element_text(color = "black",size = 15),
        axis.ticks = element_line(color = "black",size = 1),
        legend.position = "none",
        strip.background = element_blank(),
        strip.text = element_text(color = "black",size = 18))+
  labs(x=NULL,y=NULL)
