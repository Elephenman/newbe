#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/条形图+黑白色填充+条纹+显著性")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(ggpubr) # 'ggplot2' Based Publication Ready Plots

#加载数据
df <- read.table("data.txt",header = T, check.names = F)
#转换数据
data=melt(df)
data$G<-rep(c("T","F","H"), each = 24)

#基础绘图
p1 <- ggplot(data,aes(G,value))+
  #绘制条形图
  geom_bar(aes(fill=G),color='grey50', stat="summary",
           fun=mean,position="dodge", linewidth = 0.8)+ 
  #误差棒
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.2, linewidth = 0.8)+
  labs(x=NULL,y=NULL)+
  #颜色
  scale_fill_manual(values = c("#4c4c4c","#6f6f6f","#ffffff"))+
  #显著性
  geom_signif(comparisons = list(c("F","H"),
                                 c("H","T"),
                                 c("F","T")),
              map_signif_level = T, 
              test = "t.test",
              textsize = 6,
              y_position = c(50,55,60),
              tip_length = c(0,0,0),
              size=0.8,color="black")+
  scale_y_continuous(expand = c(0,0), limits = c(0,70), breaks = c(0,10,20,30,40,50,60))+
  # 主题相关设置
  theme_classic()+
  theme(axis.text = element_text(size = 14),
        legend.position = "none",
        axis.line = element_line(linewidth = 0.8))
p1

###添加花纹——需要借助ggpattern包
#安装并加载ggpattern包
# remotes::install_github("coolbutuseless/ggpattern")
library(ggpattern)
p2 <- ggplot(data,aes(G,value))+
  #利用ggpattern包中的geom_bar_pattern函数绘制条形图
  geom_bar_pattern(aes(fill=G,pattern=G),color='grey50', stat="summary",
                   fun=mean,position="dodge", linewidth = 0.8,
                   pattern_color = "black",
                   pattern_size = 0.5,
                   pattern_spacing = 0.03)+ 
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.2, linewidth = 0.8)+
  labs(x=NULL,y=NULL)+
  scale_fill_manual(values = c("#4c4c4c","#6f6f6f","#ffffff"))+
  geom_signif(comparisons = list(c("F","H"),
                                 c("H","T"),
                                 c("F","T")),
              map_signif_level = T, 
              test = "t.test",
              textsize = 6,
              y_position = c(50,55,60),
              tip_length = c(0,0,0),
              size=0.8,color="black")+
  scale_y_continuous(expand = c(0,0), limits = c(0,70), breaks = c(0,10,20,30,40,50,60))+
  theme_classic()+
  theme(axis.text = element_text(size = 14),
        legend.position = "none",
        axis.line = element_line(linewidth = 0.8))
p2

##去除填充色
p3 <- ggplot(data,aes(G,value))+
  geom_bar_pattern(aes(pattern=G),
                   color='grey50', fill = "white",stat="summary",
                   fun=mean,position="dodge", linewidth = 0.8,
                   pattern_color = "white",
                   pattern_fill = "black",
                   pattern_size = 0.5,
                   pattern_spacing = 0.05)+ 
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.2, linewidth = 0.8)+
  labs(x=NULL,y=NULL)+
  geom_signif(comparisons = list(c("F","H"),
                                 c("H","T"),
                                 c("F","T")),
              map_signif_level = T, 
              test = "t.test",
              textsize = 6,
              y_position = c(50,55,60),
              tip_length = c(0,0,0),
              size=0.8,color="black")+
  scale_y_continuous(expand = c(0,0), limits = c(0,70), breaks = c(0,10,20,30,40,50,60))+
  theme_classic()+
  theme(axis.text = element_text(size = 14),
        legend.position = "none",
        axis.line = element_line(linewidth = 0.8))
p3

##根据分组添加条纹
p4 <- ggplot(data,aes(G,value))+
  geom_bar_pattern(aes(pattern_type = G),
                   color='grey50', fill = "white",stat="summary",
                   fun=mean,position="dodge", linewidth = 0.8,
                   pattern = 'polygon_tiling',#'stripe' (default), 'crosshatch', 'point', 'circle', 'none'
                   pattern_key_scale_factor = 1.2,
                   pattern_fill = "white",
                   pattern_color = "black"
                   )+ 
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.2, linewidth = 0.8)+
  labs(x=NULL,y=NULL)+
  geom_signif(comparisons = list(c("F","H"),
                                 c("H","T"),
                                 c("F","T")),
              map_signif_level = T, 
              test = "t.test",
              textsize = 6,
              y_position = c(50,55,60),
              tip_length = c(0,0,0),
              size=0.8,color="black")+
  scale_y_continuous(expand = c(0,0), limits = c(0,70), breaks = c(0,10,20,30,40,50,60))+
  theme_classic()+
  theme(axis.text = element_text(size = 14),
        legend.position = "none",
        axis.line = element_line(linewidth = 0.8))+
  scale_pattern_type_manual(values = c("hexagonal", "rhombille",
                                       "pythagorean"))
p4

####拓展
p5 <- ggplot(data,aes(G,value))+
  geom_bar_pattern(aes(pattern_angle = G),
                   stat="summary",
                   fun=mean,position="dodge", linewidth = 0.8,
                   pattern         = 'placeholder',
                   pattern_type    = 'kitten',
                   fill            = 'white', 
                   colour          = 'black',
                   pattern_spacing = 0.025
  )+ 
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.2, linewidth = 0.8)+
  labs(x=NULL,y=NULL)+
  geom_signif(comparisons = list(c("F","H"),
                                 c("H","T"),
                                 c("F","T")),
              map_signif_level = T, 
              test = "t.test",
              textsize = 6,
              y_position = c(50,55,60),
              tip_length = c(0,0,0),
              size=0.8,color="black")+
  scale_y_continuous(expand = c(0,0), limits = c(0,70), breaks = c(0,10,20,30,40,50,60))+
  theme_classic()+
  theme(axis.text = element_text(size = 14),
        legend.position = "none",
        axis.line = element_line(linewidth = 0.8))
p5

p6 <- ggplot(data,aes(G,value))+
  geom_bar_pattern(aes(pattern_fill = G),
                   stat="summary",color='grey50', fill = "white",
                   fun=mean,position="dodge", linewidth = 0.8,
                   pattern       = 'plasma'
  )+ 
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.2, linewidth = 0.8)+
  labs(x=NULL,y=NULL)+
  geom_signif(comparisons = list(c("F","H"),
                                 c("H","T"),
                                 c("F","T")),
              map_signif_level = T, 
              test = "t.test",
              textsize = 6,
              y_position = c(50,55,60),
              tip_length = c(0,0,0),
              size=0.8,color="black")+
  scale_y_continuous(expand = c(0,0), limits = c(0,70), breaks = c(0,10,20,30,40,50,60))+
  theme_classic()+
  theme(axis.text = element_text(size = 14),
        legend.position = "none",
        axis.line = element_line(linewidth = 0.8))
p6

####拼图
(p1+p2+p3)/(p4+p5+p6)
