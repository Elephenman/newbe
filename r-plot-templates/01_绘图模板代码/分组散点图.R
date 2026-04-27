rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/分组散点图')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggpmisc) # Miscellaneous Extensions to 'ggplot2'
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization
#读取数据——以Chiplot绘图平台数据为例
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)

######绘图#######
#自定义颜色
col<-c("#be0027", "#cf8d2e")
#构建背景色
color1 <- colorRampPalette(brewer.pal(11,"PiYG"))(30)
color2 <- colorRampPalette(brewer.pal(11,"PuOr"))(30)
#绘图
p <- ggplot(df,aes(x,y,fill=group))+
  geom_point(shape=21,size=3,alpha=0.5)+
  #添加回归曲线并添加置信区间
  geom_smooth(method = "lm",aes(color=group), se=T, 
              formula = y ~ x,
              linetype=1,alpha=0.5)+
  #添加回归方程
  stat_poly_eq(formula = y ~ x, 
               aes(color=group,label = paste(after_stat(eq.label),
                                 ..rr.label..,sep = "~~~")), parse = TRUE) +
  scale_fill_manual(values = col)+
  scale_color_manual(values = col)+
  theme_bw()+
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='#333c41',size=12),
        legend.text = element_text(color='#333c41',size=12),
        legend.title = element_blank())+
  labs(x=NULL,y=NULL)
p
#添加背景
grid.raster(alpha(color1, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)
#分面
p+facet_grid(~group, scales = "free")+
  theme(legend.position = "none")
#添加背景
grid.raster(alpha(color2, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

