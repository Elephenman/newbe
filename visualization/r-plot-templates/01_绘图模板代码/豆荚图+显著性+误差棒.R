#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/豆荚图+显著性+误差棒")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(dplyr) # A Grammar of Data Manipulation
library(gghalves) # Compose Half-Half Plots Using Your Favourite Geoms

##构造数据
df <- read.table("data.txt",header = T, check.names = F)

# 分组计算显著性
df %>%
  group_by(Group, Period) %>%
  summarise(p_value = t.test(value[G == "CG"], value[G == "EG"])$p.value)->df1

###绘图
##groupA组
ggplot(df)+
  #绘制CG组的图
  geom_half_violin(data=df[df$Group=="groupA"&df$G=="CG",],
                   aes(Period, value,fill=G),
                   side = "l",#绘制左边小提琴
                   width=0.8,#控制宽度
                   alpha=0.7,
                   color=NA)+#边缘颜色设置
  #添加CG组的均值点
  stat_summary(data=df[df$Group=="groupA"&df$G=="CG",],
               aes(Period, value),
               position = position_nudge(x=-0.1),#控制均值点的位置
               fun = "mean", geom = "point",size=2)+
  #添加CG组的误差棒
  stat_summary(data=df[df$Group=="groupA"&df$G=="CG",],
               aes(Period, value),
               position = position_nudge(x=-0.1),#控制误差棒的位置
               color="grey10",fun.data = "mean_cl_normal",
               geom = "errorbar",
               width = 0.05,size=0.8) +
  #绘制EG组的图
  geom_half_violin(data=df[df$Group=="groupA"&df$G=="EG",],
                   aes(Period, value,fill=G),
                   side = "r",#绘制右边小提琴
                   width=0.8,alpha=0.7,
                   color=NA)+
  #添加EG组的均值点
  stat_summary(data=df[df$Group=="groupA"&df$G=="EG",],
               aes(Period, value),position = position_nudge(x=0.1),
               fun = "mean", geom = "point",size=2)+
  #添加EG组的误差棒
  stat_summary(data=df[df$Group=="groupA"&df$G=="EG",],
               aes(Period, value),position = position_nudge(x=0.1),
               color="grey10",fun.data = "mean_cl_normal",
               geom = "errorbar",
               width = 0.05,size=0.8)+
  ##手动添加误差
  annotate("text", x = 1 , y = 128,label = "ns", size= 5,color = "black")+
  annotate("text", x = 2 , y = 150,label = "***", size= 5,color = "black")+
  #主题相关设置
  labs(y="This is y-axis",x=NULL,fill=NULL,title = "groupA")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 25, vjust = 1, hjust = 1,size = 11),
        axis.text.y = element_text(size = 11),
        axis.title = element_text(size = 13),
        legend.position = c(0.9,0.2),
        legend.background = element_blank())+
  #颜色设置
  scale_fill_manual(values = c("#ff4e00","#01cd74"))->p1
p1


##groupB组
ggplot(df)+
  #绘制CG组的图
  geom_half_violin(data=df[df$Group=="groupB"&df$G=="CG",],
                   aes(Period, value,fill=G),
                   side = "l",#绘制左边小提琴
                   width=0.8,#控制宽度
                   alpha=0.7,
                   color=NA)+#边缘颜色设置
  #添加CG组的均值点
  stat_summary(data=df[df$Group=="groupB"&df$G=="CG",],
               aes(Period, value),
               position = position_nudge(x=-0.1),#控制均值点的位置
               fun = "mean", geom = "point",size=2)+
  #添加CG组的误差棒
  stat_summary(data=df[df$Group=="groupB"&df$G=="CG",],
               aes(Period, value),
               position = position_nudge(x=-0.1),#控制误差棒的位置
               color="grey10",fun.data = "mean_cl_normal",
               geom = "errorbar",
               width = 0.05,size=0.8) +
  #绘制EG组的图
  geom_half_violin(data=df[df$Group=="groupB"&df$G=="EG",],
                   aes(Period, value,fill=G),
                   side = "r",#绘制右边小提琴
                   width=0.8,alpha=0.7,
                   color=NA)+
  #添加EG组的均值点
  stat_summary(data=df[df$Group=="groupB"&df$G=="EG",],
               aes(Period, value),position = position_nudge(x=0.1),
               fun = "mean", geom = "point",size=2)+
  #添加EG组的误差棒
  stat_summary(data=df[df$Group=="groupB"&df$G=="EG",],
               aes(Period, value),position = position_nudge(x=0.1),
               color="grey10",fun.data = "mean_cl_normal",
               geom = "errorbar",
               width = 0.05,size=0.8)+
  ##手动添加误差
  annotate("text", x = 1 , y = 115,label = "ns", size= 5,color = "black")+
  annotate("text", x = 2 , y = 130,label = "***", size= 5,color = "black")+
  #主题相关设置
  labs(y="This is y-axis",x=NULL,fill=NULL,title = "groupB")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 25, vjust = 1, hjust = 1,size = 11),
        axis.text.y = element_text(size = 11),
        axis.title = element_text(size = 13),
        legend.position = c(0.9,0.2),
        legend.background = element_blank())+
  #颜色设置
  scale_fill_manual(values = c("#ff4e00","#01cd74"))->p2
p2

##拼图
library(patchwork)
p1+p2