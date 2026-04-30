rm(list = ls())
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/map绘制/中国地图+散点+柱状图')
#加载包
library(tidyverse) # Easily Install and Load the 'Tidyverse'
library(sf) # Simple Features for R
library(ggspatial) # Spatial Data Framework for ggplot2
library(cowplot) # Streamlined Plot Theme and Plot Annotations for 'ggplot2'
#读取地图数据，直接去阿里云DataV可视化下载地图数据
map <- read_sf("中华人民共和国.json")

##绘制地图
#绘制中国地图主体部分
ggplot(map)+
  geom_sf(color='black',#线条颜色
          fill=NA,#填充色
          size=0.8)+#地图线条粗细
  annotation_scale(location = "bl", width_hint = 0.3) +#添加比例尺并调整位置及长度
  annotation_north_arrow(location = "tl", which_north = F, 
                         pad_x = unit(0.05, "in"), pad_y = unit(0.05, "in"),
                         style = north_arrow_nautical)+#添加指北针
  coord_sf(crs = "+proj=laea +lat_0=40 +lon_0=104")+#坐标参考系统(CRS)
  #主题设置
  theme_bw()+
  theme(text = element_text(size = 14,face = "bold"),
        panel.grid = element_blank(),
        axis.line = element_blank())+
  labs(x='', y='')

####添加散点图
#随机生成一些作图数据
#设置随机数种子，确保结果可以重现
set.seed(999)
df1 <- data.frame(
  lon=runif(100, min = 85, max = 120),
  lat=runif(100, min = 30, max = 41),
  group=rep(c('1980','2000','2005','2010'),times=c(10,25,25,40)))
df2 <- data.frame(
  lon=runif(40, min = 100, max = 120),
  lat=runif(40, min = 22, max = 30),
  group=rep(c('1980','2000','2005','2010'),times=c(10,20,5,5)))
df3 <- data.frame(
  lon=runif(40, min = 120, max = 130),
  lat=runif(40, min = 41, max = 50),
  group=rep(c('1980','2000','2005','2010'),times=c(5,15,10,10)))
df4 <- data.frame(
  lon=runif(60, min = 80, max = 90),
  lat=runif(60, min = 30, max = 45),
  group=rep(c('1980','2000','2005','2010'),times=c(10,15,25,10)))
df <- rbind(df1,df2,df3,df4)
#顺便统计出各组的数量
data <- data.frame(group=c('1980','2000','2005','2010'),
                   value=c(35,75,65,65))
##绘图
#绘制子图
p <- ggplot(data,aes(group,value,fill=group))+
  geom_col()+
  scale_fill_manual(values = c("#00c700", "#da0000","#0054da","#6a3d00"))+
  theme_classic()+
  theme(legend.position = "none",
        axis.text.x = element_blank(),
        axis.text.y = element_text(color = "black",size=12),
        axis.line.x = element_blank(),
        axis.ticks.x = element_blank(),
        panel.background = element_blank(),
        plot.background = element_blank())+
  labs(x='', y='')+
  scale_y_continuous(expand = c(0,0))
p
#地图中添加散点图并将柱状图作为子图加入
#使用st_as_sf()对数据进行转换
df_st_as_sf <- st_as_sf(df,coords = c("lon", "lat"),crs = 4326)
#绘图
ggplot(map)+
  geom_sf(color='black',#线条颜色
          fill=NA,#填充色
          size=0.8)+#地图线条粗细
  geom_sf(df_st_as_sf,mapping=aes(color=group),shape=16,size=2.5)+
  annotation_scale(location = "bl", width_hint = 0.3) +#添加比例尺并调整位置及长度
  annotation_north_arrow(location = "tl", which_north = F, 
                         pad_x = unit(0.05, "in"), pad_y = unit(0.05, "in"),
                         style = north_arrow_nautical)+#添加指北针
  coord_sf(crs = "+proj=laea +lat_0=40 +lon_0=104")+
  theme_bw()+
  theme(text = element_text(size = 14,face = "bold"),
        panel.grid = element_blank(),
        axis.line = element_blank(),
        legend.position = c(0.15,0.3),
        legend.background = element_blank())+
  labs(x='', y='',color=NULL)+
  scale_color_manual(values = c("#00c700", "#da0000","#0054da","#6a3d00"))+
  #柱状图插入，注意，这里需要自己调整坐标以适应地图
  annotation_custom(grob=ggplotGrob(p),
                    ymin = 200000, ymax = 1600000, 
                    xmin=-1200000, xmax=800000)

####通过cowplot包南海小地图单独插入
Chinamap <- ggplot(map)+
  geom_sf(color='black',#线条颜色
          fill=NA,#填充色
          size=0.8)+#地图线条粗细
  geom_sf(df_st_as_sf,mapping=aes(color=group),shape=16,size=2.5)+
  annotation_scale(location = "bl", width_hint = 0.3) +#添加比例尺并调整位置及长度
  annotation_north_arrow(location = "tl", which_north = F, 
                         pad_x = unit(0.05, "in"), pad_y = unit(0.05, "in"),
                         style = north_arrow_nautical)+#添加指北针
  coord_sf(ylim = c(-2387082,1654989),crs = "+proj=laea +lat_0=40 +lon_0=104")+
  theme_bw()+
  theme(axis.text = element_text(size = 14,face = "bold",color = "black"),
        panel.grid = element_blank(),
        axis.line = element_blank(),
        legend.position = c(0.1,0.2),
        legend.background = element_blank())+
  labs(x='', y='',color=NULL)+
  scale_color_manual(values = c("#00c700", "#da0000","#0054da","#6a3d00"))+
  annotation_custom(grob=ggplotGrob(p),
                    ymin = 500000, ymax = 1800000, 
                    xmin=-1100000, xmax=800000)
Chinamap

nhmap <- ggplot(map)+
  geom_sf(color='black',#线条颜色
          fill=NA,#填充色
          size=0.8)+#地图线条粗细
  coord_sf(ylim = c(-4028017,-1877844),xlim = c(117131.4,2115095),
           crs = "+proj=laea +lat_0=40 +lon_0=104")+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.line = element_blank(),
        legend.position = c(0.1,0.3),
        legend.background = element_blank(),
        axis.text = element_blank(),
        axis.ticks = element_blank(),
        plot.background = element_blank(),
        panel.border = element_rect(linewidth = 1))+
  labs(x='', y='')
nhmap

##组合图形
ggdraw() +
  draw_plot(Chinamap) +
  draw_plot(nhmap, x = 0.73, y = 0, width = 0.1, height = 0.3)


