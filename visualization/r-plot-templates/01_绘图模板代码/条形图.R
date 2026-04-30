#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/条形图")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics

#加载数据
df <- read.table("data.txt",header = T, check.names = F)

#绘图
col <- c("#d91481","#e7524e","#f8a250","#f9f05f","#4ea363","#7bc8f6","#5193f4","#ae77e8")
ggplot(df,aes(samples,value,fill=group))+
  geom_bar(stat="summary",fun=mean,position="dodge")+
  theme_classic()+
  theme(axis.text.x=element_blank(),
        axis.text.y=element_text(color='black',size=9),
        axis.ticks.x = element_blank(),
        legend.text = element_text(color='black',size=12),
        legend.title = element_blank(),
        legend.background = element_blank(),
        legend.position = c(0.5,0.9),
        axis.title = element_text(color='black',size=12))+
  scale_y_continuous(expand = c(0, 0), limit = c(0, 100))+
  scale_x_continuous(expand = c(0, 0.5), limit = c(0, 125))+
  scale_fill_manual(values = col)+
  labs(x="Genome assembly",y="Number of duplicated \nprotein-coding genes")+
  guides(fill = guide_legend(nrow = 1))

