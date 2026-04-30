rm(list = ls())
# 生成数据或者自己导入数据
# df <- read.table("xxx.txt",header = T, row.names = 1, check.names = F)
df <- data.frame(x=LETTERS[1:10],y=sample(10:20,10))

#加载数据包
library(ggplot2)
library(tidyverse)
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization
# 先做柱形图，然后再用极坐标
ggplot(df,aes(x=x,y=y))+
  geom_col(aes(fill=x),show.legend = F)+
  coord_polar()

#通过构造正余弦函数使得极坐标的圆弧成为花瓣状
x<-1:180
y<-sin(10*x*pi/180)

df1<-data.frame(x1=x,y1=abs(y),var=gl(10,18,labels = LETTERS[1:10]))

merge(df1,df,by.x = 'var',by.y = 'x') %>% 
  mutate(new_y=y1*y) -> df2

#再次绘制图
ggplot(data=df2,aes(x=x,y=new_y))+
  geom_area(aes(fill=var),
            alpha=0.8,
            color="black",
            show.legend = F)+
  coord_polar()+
  theme_bw()+
  theme(axis.text.y = element_blank(),
        axis.ticks = element_blank(),
        panel.border = element_blank(),
        axis.title = element_blank())+
  scale_x_continuous(breaks = seq(9,180,18),
                     labels = df$x)+
  geom_text(data=df,aes(x=seq(9,180,18),
                        y=y+1,
                        label=y))


#####绘图模板
#准备配色
col <- colorRampPalette(brewer.pal(12,"Paired"))(10)
#背景色
color <- colorRampPalette(brewer.pal(11,"PuOr"))(30)
ggplot(data=df2,aes(x=x,y=new_y))+
  geom_area(aes(fill=var),
            alpha=0.8,
            color="black",
            show.legend = T)+
  coord_polar()+
  theme_bw()+
  theme(axis.text= element_blank(),
        axis.ticks = element_blank(),
        panel.border = element_blank(),
        axis.title = element_blank(),
        panel.grid = element_blank(),
        legend.title = element_blank(),
        legend.position = c(0.95,0.9),
        legend.justification = c(1, 1),
        legend.direction = 'vertical')+
  scale_x_continuous(breaks = seq(9,180,18),
                     labels = df$x)+
  geom_text(data=df,aes(x=seq(9,180,18),
                        y=y+1,
                        label=y))+
  scale_fill_manual(values = col)
#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)
