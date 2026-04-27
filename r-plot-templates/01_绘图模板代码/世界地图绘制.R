rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/map绘制/世界地图绘制")

#加载R包
library(ggplot2)

#使用ggplot2创建世界地图的数据
df_map <- map_data("world")

##绘制基础世界地图
p <- ggplot(df_map,aes(long, lat, group = group)) + 
  geom_polygon()+
  borders("world",regions = ".",color = "grey20",fill="white")+
  #主题设置
  theme_void()
p

##给不同国家添加颜色并为海水添加蓝色
p+geom_polygon(aes(fill=region),show.legend = F)+
  theme(plot.background = element_rect(fill="#76daff"))

##连续变量——这里直接使用数据中的order列数据
p+geom_polygon(aes(fill=order))

##转变为极地地图
p+coord_map("ortho")

##添加采样点信息
#构造采样点的经纬度
df_sample1 <- data.frame(
  lon=runif(12, min = 0, max = 120),
  lat=runif(12, min = 25, max = 45),
  group=rep(c('1980','2000','2005','2010'),times=c(3,3,3,3)))
df_sample2 <- data.frame(
  lon=runif(12, min = -125, max = -75),
  lat=runif(12, min = 30, max = 65),
  group=rep(c('1980','2000','2005','2010'),times=c(1,5,4,2)))
df_sample3 <- data.frame(
  lon=runif(12, min = -5, max = 20),
  lat=runif(12, min = 10, max = 25),
  group=rep(c('1980','2000','2005','2010'),times=c(2,5,3,2)))
#合并数据
df_sample <- rbind(df_sample1,df_sample2,df_sample3)
#顺便统计出各组的数量
data <- data.frame(group=c('1980','2000','2005','2010'),
                   value=c(6,13,10,7))
##绘制子图
p2 <- ggplot(data,aes(group,value,fill=group))+
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
p2


#添加采样点信息
p+geom_point(df_sample,
             mapping=aes(lon, lat, fill = group),
             size=3,shape=21,color="black",
             show.legend = T)+
  scale_fill_manual(name=NULL,values = c("#00c700", "#da0000","#0054da","#6a3d00"))+
  annotation_custom(grob=ggplotGrob(p2),
                    ymin = -75, ymax = -30, 
                    xmin=-190, xmax=-80)+
  theme(legend.position = c(0.1,0.5))

