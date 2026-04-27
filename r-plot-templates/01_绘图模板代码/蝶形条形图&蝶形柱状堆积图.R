#########微信公众号：科研后花园
######推文题目：跟着Nature Genetics学绘图——蝶形条形图与柱状堆积图的绘制！！！

##清除环境并设置工作目录
rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/蝶形条形图&蝶形柱状堆积图")

##加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(aplot) # Decorate a 'ggplot' with Associated Information
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package

##加载数据（随机编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")

##确定排序
df$sample <- factor(df$sample,levels = c("OR4K2","OR4K1","GRPIN2","OR9G1","SULT1A3","OR4Q3",
                                          "PDPR","CYP2D6","PRAMEF18"))

##绘制蝶形条形图
#绘制蝶形条形图右半边
p1 <- ggplot(df[df$group=="group1",],#指定绘制的数据
             aes(sample, value1))+
  #绘制条形图
  geom_col(aes(fill = Fill))+
  #添加数字标注
  geom_text(aes(y = value1+3, label = value1))+
  #转置x轴与y轴
  coord_flip()+
  #调整y轴范围及显示刻度
  scale_y_continuous(expand = c(0,0),
                     limits = c(0,90),
                     breaks = seq(0, 90, 10))+
  #设置副标题
  labs(subtitle = "group1")+
  #设置主题
  theme_void()+
  theme(axis.text.y = element_text(size = 12, vjust = 0.5),
        axis.text.x = element_text(size = 10),
        plot.subtitle = element_text(hjust = 0, size = 14),
        legend.position = "none")+
  #自定义颜色
  scale_fill_manual(values = c("#9cc63a","#5bc1ec","#fa7a1b","#ffde7b"))
p1
#绘制蝶形条形图左半边
p2 <- ggplot(df[df$group=="group2",], aes(sample, -value1))+
  geom_col(aes(fill = Fill))+
  geom_text(aes(y = -value1-4, label = value1))+
  coord_flip()+
  scale_y_continuous(expand = c(0,0),
                     limits = c(-90,0),
                     breaks = seq(-90, 0, 10),
                     #需要单独对左半边标签进行设置
                     labels = as.character(abs(seq(-90, 0, 10))))+
  labs(subtitle = "group2")+
  theme_void()+
  theme(axis.text.x = element_text(size = 10),
        plot.subtitle = element_text(hjust = 1, size = 14),
        legend.position = "none")+
  scale_fill_manual(values = c("#9cc63a","#5bc1ec","#fa7a1b","#ffde7b"))
p2
#组合图形
p1%>%insert_left(p2, width = 1)


####绘制蝶形柱状堆积图
###将宽数据转变为长数据
df2 <- melt(df, id.vars = c("sample","group"), 
            measure.vars = c('value5','value4','value3',
                             'value2','value1'))
df2$group <- factor(df2$group,levels = c("group1","group2"))
df2$sample <- factor(df2$sample,levels = c("OR4K2","OR4K1","GRPIN2","OR9G1","SULT1A3","OR4Q3",
                                          "PDPR","CYP2D6","PRAMEF18"))

#绘制蝶形柱状堆积图右半边
p3 <- ggplot(df2[df2$group=="group1",],#指定绘制的数据
             aes(sample, value))+
  #绘制柱状堆积图
  geom_col(aes(fill = variable))+
  #转置x轴与y轴
  coord_flip()+
  #调整y轴范围及显示刻度
  scale_y_continuous(expand = c(0,0),
                     limits = c(0,480),
                     breaks = seq(0, 450, 50))+
  #设置副标题
  labs(subtitle = "group1")+
  #设置主题
  theme_void()+
  theme(axis.text.y = element_text(size = 12, vjust = 0.5),
        axis.text.x = element_text(size = 10),
        plot.subtitle = element_text(hjust = 0, size = 14),
        legend.position = "none")+
  #自定义颜色
  scale_fill_manual(values = c("#9cc63a","#5bc1ec","#fa7a1b","#ffde7b","#ff6b6b"))
p3
#绘制蝶形柱状堆积图左半边
p4 <- ggplot(df2[df2$group=="group2",],#指定绘制的数据
             aes(sample, -value))+
  #绘制柱状堆积图
  geom_col(aes(fill = variable))+
  #转置x轴与y轴
  coord_flip()+
  #调整y轴范围及显示刻度
  scale_y_continuous(expand = c(0,0),
                     limits = c(-480,0),
                     breaks = seq(-450, 0, 50),
                     #需要单独对左半边标签进行设置
                     labels = as.character(abs(seq(-450, 0, 50))))+
  #设置副标题
  labs(subtitle = "group2")+
  #设置主题
  theme_void()+
  theme(axis.text.x = element_text(size = 10),
        plot.subtitle = element_text(hjust = 1, size = 14),
        legend.position = "none")+
  #自定义颜色
  scale_fill_manual(values = c("#9cc63a","#5bc1ec","#fa7a1b","#ffde7b","#ff6b6b"))
p4
#组合图形
p3%>%insert_left(p4, width = 1)
