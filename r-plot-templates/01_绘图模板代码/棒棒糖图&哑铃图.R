rm(list = ls())
setwd("D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\棒棒糖图&哑铃图")

# 加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization
library(ggprism) # A 'ggplot2' Extension Inspired by 'GraphPad Prism'

# 加载数据
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)

# 哑铃图
p1 <- ggplot(df) +
  geom_segment(aes(x=group, xend=group, y=value1, 
                   yend=value2), color="grey",size=1) +#数据点之间的连线
  geom_point( aes(x=group, y=value1), color='#ff9900', size=4 ) +#数据点1
  geom_point( aes(x=group, y=value2), color='#146eb4', size=4 ) +#数据点2
  theme_prism(palette = "pearl",  #利用ggprism包调整主题
              base_fontface = "plain",
              base_family = "serif", 
              base_size = 14, 
              base_line_size = 0.8,
              axis_text_angle = 45) +
  theme(legend.position = "none") + #去除图例
  xlab("XXXX") +#X轴标题
  ylab("XXXX") +#Y轴标题
  ggtitle("Dumbbell Chart")#标题

p1

p2<-p1+  coord_flip() #改变图形显示为横向排布
p2

# 棒棒糖图
p3 <- ggplot(df) +
  geom_segment(aes(x=group, xend=group, y=85, yend=value1), color="grey",size=1) +
  geom_point( aes(x=group, y=value1), size=4,color='red' ) +
  geom_hline(yintercept = 85, lty=2,color = 'grey', lwd=0.8) + #辅助线
  theme_prism(palette = "pearl",
              base_fontface = "plain", 
              base_family = "serif", 
              base_size = 14, 
              base_line_size = 0.8, 
              axis_text_angle = 45) +
  theme(legend.position = "none") +
  xlab("XXXX") +
  ylab("XXXX") +
  ggtitle("Lollipop Chart")

p3

p4 <- ggplot(df) +
  geom_segment(aes(x=group, xend=group, y=120, yend=value2), color="grey",size=1) +
  geom_point( aes(x=group, y=value2,color=group), size=4 ) +
  geom_hline(yintercept = 120, lty=2,color = 'grey', lwd=0.8) + #辅助线
  theme_prism(palette = "pearl",
              base_fontface = "plain", 
              base_family = "serif",
              base_size = 14,
              base_line_size = 0.8, 
              axis_text_angle = 45) +
  theme(legend.position = "none") +
  xlab("XXXX") +
  ylab("XXXX") +
  ggtitle("Lollipop Chart")

p4

#拼图
cowplot::plot_grid(p1, p2, p3, p4, ncol = 2)


###绘图模板
#准备配色
col <- colorRampPalette(brewer.pal(11,"Spectral"))(21)
#背景色
color <- colorRampPalette(brewer.pal(11,"BrBG"))(30)
#绘图
p1 <- ggplot(df) +
  geom_hline(yintercept = 120, lty=4,color = '#00a4e4', lwd=1) + #辅助线
  geom_segment(aes(x=group, xend=group, y=120, yend=value2), color="#cf8d2e",size=1.5,lty=1) +
  geom_point( aes(x=group, y=value2,fill=group), size=4,shape=21,color="black" ) +
  scale_fill_manual(values = col)+
  theme_bw() +
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='#333c41',size=10),
        legend.text = element_text(color='#333c41',size=10),
        legend.title = element_blank(),
        legend.position = "none",
        axis.title= element_text(size=12),
        axis.text.x=element_text(angle = 45,vjust = 1,hjust = 1))+
  labs(x=NULL,y=NULL)
p2 <- ggplot(df) +
  geom_segment(aes(x=group, xend=group, y=value1, 
                   yend=value2), color="#d4c99e",size=1.5) +#数据点之间的连线
  geom_point( aes(x=group, y=value1), color='#ff9900', size=4 ) +#数据点1
  geom_point( aes(x=group, y=value2), color='#146eb4', size=4 ) +#数据点2
  theme_bw() +
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='#333c41',size=10),
        legend.text = element_text(color='#333c41',size=10),
        legend.title = element_blank(),
        legend.position = "none",
        axis.title= element_text(size=12),
        axis.text.x=element_text(angle = 45,vjust = 1,hjust = 1))+
  labs(x=NULL,y=NULL)
#拼图
cowplot::plot_grid(p2,p1,ncol = 2)
#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)
