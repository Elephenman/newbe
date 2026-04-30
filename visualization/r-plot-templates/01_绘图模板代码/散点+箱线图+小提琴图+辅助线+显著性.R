rm(list=ls())#clear Global Environment
#设置工作目录
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点+箱线图+小提琴图+辅助线+显著性")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggsignif) # Significance Brackets for 'ggplot2'
library(gghalves) # Compose Half-Half Plots Using Your Favourite Geoms
#加载数据
df <- read.table("data.txt",header = 1)
#将分组信息转变为factor类型数据
df$group <- factor(df$group,levels = c("A","B","C","D"))

##绘图
ggplot(df,aes(group,value,fill=group))+
  #半小提琴
  geom_half_violin(position = position_nudge(x=0.25),side = "r",width=0.8,color=NA)+
  #箱线图
  geom_boxplot(width=0.4,size=1.2,outlier.color =NA)+
  #散点图
  geom_jitter(aes(fill=group),shape=21,size=2.5,width=0.2)+
  #水平辅助线
  geom_hline(yintercept = 0, linetype = 2, color = "red",linewidth=1)+
  geom_hline(yintercept = 80, linetype = 2, color = "red",linewidth=1)+
  #显著性
  geom_signif(comparisons = list(c("A","B"),
                                 c("A","C"),
                                 c("C","D")),
              map_signif_level = T, 
              test = t.test, 
              y_position = c(100,120,130),
              tip_length = c(0,0,0,0,0,0),
              size=1,color="black",textsize = 7)+
  #y轴范围
  scale_y_continuous(limits = c(-20,140),breaks = c(0,40,80,120))+
  #主题
  theme_bw()+
  theme(panel.grid = element_blank(),
        panel.border = element_rect(size = 1),
        axis.text.x = element_text(color = "black", size = 13),
        axis.text.y = element_text(color = "black",size = 13),
        legend.position = "none",
        axis.ticks = element_line(color="black",linewidth = 1))+
  #标题设置
  labs(x=NULL,y=NULL)+
  #颜色
  scale_fill_manual(values = c("#5cc3e8","#ffdb00","#79ceb8","#e95f5c"))

