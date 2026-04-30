###科研后花园####
####@wzs#####

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/云雨图')#设置工作目录

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(tidyverse) # Easily Install and Load the 'Tidyverse'
library(ggsignif) # Significance Brackets for 'ggplot2'
library(gghalves) # Compose Half-Half Plots Using Your Favourite Geoms

#这里使用我自己随机编写的数据
df <- data.frame(
  A = c(2,5,6,5,4,8,6,3,8,9),
  B = c(15,10,5,18,12,13,16,14,10,9),
  C = c(1,3,6,5,2,3,6,2,4,1),
  D = c(20,15,14,16,10,22,18,10,11,12)
)
#预览数据
head(df)

#使用tidyverse包对数据进行处理
df <- df %>% 
  gather(key = 'group',value = 'values')#gather()函数可以把多列数据合并成一列数据
head(df)#预览数据

#绘图
df$group <- factor(df$group,levels = c("A","B","C","D"))
p<-ggplot(df,aes(group,values,color=group))+#指定数据及坐标数据
  geom_half_violin(position = position_nudge(x = 0),side=1.5,size=1.2)+
  stat_boxplot(geom = "errorbar", width=0.1, size=1.2)+#添加误差线,注意位置，放到最后则这条先不会被箱体覆盖
  geom_boxplot(position="dodge",width=0.8,size=1.2)+#绘制箱线图函数
  geom_signif(comparisons = list(c("A","B"),
                                 c("A","D")),# 设置需要比较的组
              map_signif_level = T, #是否使用星号显示
              test = t.test, ##计算方法
              y_position = c(24,26),#图中横线位置设置
              tip_length = c(c(0.7,0.3),
                             c(0.7,0.2)),#横线下方的竖线设置
              size=1,color="#007fbd")+
  geom_jitter(alpha=0.3,width = 0.3,size=3)+#添加抖动点
  theme_bw()+
  theme(legend.position = 'none',#去除图例
        panel.grid = element_blank(),
        axis.text.x = element_text(angle = 45,vjust = 1,hjust = 1,size = 12),
        axis.text.y = element_text(size = 12))+
  scale_y_continuous(limits = c(0,28))+
  scale_color_manual(values=c("#3be8b0","#1aafd0","#6a67ce","#fc636b"))
p



