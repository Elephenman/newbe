#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/双向柱状图")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics

#加载数据
df <- read.table("data.txt",header = T,sep='\t')
df$group <- factor(df$group,levels = c("HPRC.EAS","CPC"))
df$sample <- factor(df$sample,levels = c("OR4K2","OR4K1","GRPIN2","OR9G1","SULT1A3","OR4Q3",
                                         "PDPR","CYP2D6","PRAMEF18"))
#数据处理——将其中一组的数据转换为负值
df$value <- ifelse(df$group=="HPRC.EAS",-df$value,df$value)
#颜色
col <- c("#f89f68","#4b84b3")
#绘图
ggplot(df,aes(sample,value,fill=group))+
  #柱状图
  geom_col(width = 0.8)+
  #坐标转换
  coord_flip()+
  #自定义颜色
  scale_fill_manual(values = col)+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.x = element_text(color = "black", size = 13),
        axis.text.y = element_text(color = "black",size = 14,face = "italic"),
        axis.title = element_text(color = "black",size = 16),
        legend.position = "top",
        legend.title = element_blank(),
        legend.text = element_text(color = "black",size = 15))+
  #标题设置
  labs(x=NULL,y="CNV Frequency")+
  #y轴范围设置
  scale_y_continuous(breaks = seq(-1, 1, 0.5), 
                     labels = as.character(abs(seq(-1, 1, 0.5))),
                     limits = c(-1, 1))
