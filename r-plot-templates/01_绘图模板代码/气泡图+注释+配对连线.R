rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/气泡图+注释+配对连线")

#加载R包
library(ggplot2)

##绘制气泡图
#加载数据（数据随意编写，无实际意义）
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)
df$group1 <- factor(df$group1,levels = df$group1[1:40])
df$group2 <- factor(df$group2,levels = c("AAA","BBB","CCC","DDD","EEE","FFF","GGG"))
#绘图
p1 <- ggplot(df, aes(sample, group1))+
  geom_point(aes(color=group2,size=value),alpha=0.6)+
  scale_color_manual(values = c("#ff0000","#ffed00","#ff0092","#00b2a9",
                                "#00c7f2","#dc5034","#a626aa"))+
  scale_size_continuous(range = c(0.1, 7))+
  theme_bw()+
  theme(panel.grid = element_blank(), 
        axis.text=element_text(color='black',size=12),
        legend.text = element_text(color='black',size=12),
        plot.margin= margin())+
  labs(x = NULL, y = NULL)
p1

##绘制配对连线
#获取气泡图的坐标值
plot_build <- ggplot_build(p1)
coords <- plot_build$data[[1]][, c("x", "y")]
#通过气泡图的坐标值构建配对网络数据的坐标
df_line <- read.table(file="data_line.txt",sep="\t",header=T,check.names=FALSE)
#绘制网络连线图
p2 <- ggplot(df_line)+
  geom_segment(aes(x1,y1,xend=x2,yend=y2,color=group1),size=0.6)+
  geom_point(aes(x=x1,y=y1,fill=group1),size=3.5,color="#c68143",
             stroke=0.5,shape = 21)+
  geom_point(aes(x=x2,y=y2),size=3.5,
             fill="#004eaf",color="#c68143",
             stroke=0.5,shape = 21)+
  scale_y_continuous(limits = c(0.5,40.5),expand = c(0,0))+
  scale_color_manual(values = c("#47cf73","#ff3c41","#76daff","#ffa500"))+
  scale_fill_manual(values = c("#47cf73","#ff3c41","#76daff","#ffa500"))+
  theme_void()+
  theme(legend.position = "none",
        plot.margin= margin())+
  geom_text(aes(x1-0.2,y1,label=group1))
p2
p2+geom_text(aes(x2+0.1,y2,label=group2))#检查y轴是否对应
#拼图
library(patchwork)
p2+p1+plot_layout(widths = c(1, 2))
