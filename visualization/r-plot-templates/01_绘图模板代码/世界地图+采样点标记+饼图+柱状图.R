##@更多精彩欢迎关注「科研后花园」

##清除环境变量并设置工作目录
rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/map绘制/世界地图+采样点标记+饼图+柱状图")

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(scatterpie) # Scatter Pie Plot
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package

#使用ggplot2创建世界地图的数据
df_map <- map_data("world")
#读取采样点信息及物种信息
site <- read.table("site.txt", header = 1, check.names = F, sep = "\t")
Species <- read.table("Species.txt", header = 1, check.names = F, sep = "\t")
#将物种丰度信息转换为长数据
df_species <- melt(Species, id.vars = c("lon","lat","site","Number of samples"))

##绘制世界地图+采样点+饼图显示物种信息
ggplot() +
  #绘制世界地图
  geom_polygon(data=df_map,aes(long, lat, group = group),fill="grey90")+
  #添加采样点信息
  geom_point(site,
             mapping=aes(lon, lat, fill = group), color = "grey40",
             size=3, shape = 21, show.legend = F)+
  #添加物种信息饼图
  geom_scatterpie(data=df_species, aes(lon,lat, group = site,
                                         r = `Number of samples`),
                  cols = 'variable', #将颜色设置为长数据中的variable
                  long_format = T, color = "transparent")+
  #添加饼图图例
  geom_scatterpie_legend(df_species$`Number of samples`, x = -30, y = -70)+
  #主题设置
  theme_bw()+
  theme(plot.background = element_blank(),
        panel.grid = element_blank())+
  scale_y_continuous(expand = c(0,0))+
  scale_x_continuous(expand = c(0,0))+
  #自定义颜色
  scale_fill_manual(values = c(SpeciesA="#ccc900",SpeciesB="#f784b6",SpeciesC="#005238",
                               SpeciesD="#862633",SpeciesE="#0eb24e",
                               siteA="#037ef3",siteB="#f85a40",siteC="#00c16e",
                               siteD="#7552cc",siteE="#0cb9c1",siteF="#f48924"))+
  labs(x=NULL,y=NULL,fill="Species")+
  #添加分组文字标记
  annotate("text", x = -75, y = 65, label = "siteA", size=5, color = "#037ef3")+
  annotate("text", x = -120, y = -20, label = "siteB", size=5, color = "#f85a40")+
  annotate("text", x = 125, y = 35, label = "siteC", size=5, color = "#00c16e")+
  annotate("text", x = 105, y = -10, label = "siteD", size=5, color = "#7552cc")+
  annotate("text", x = -5, y = 5, label = "siteE", size=5, color = "#0cb9c1")+
  annotate("text", x = 170, y = 35, label = "siteF", size=5, color = "#f48924")

####后期导出PDF再AI中将采样点的多余图例删除


#####绘制世界地图+采样点+柱状图显示物种信息
ggplot() +
  #绘制世界地图
  geom_polygon(data=df_map,aes(long, lat, group = group),fill="grey90")+
  #添加采样点信息
  geom_point(site,
             mapping=aes(lon, lat, fill = group), color = "grey40",
             size=3, shape = 21, show.legend = F)+
  ##采用geom_errorbar函数添加柱状图
  geom_errorbar(data=df_species[df_species$variable=="SpeciesA",],
                aes(x=lon-8,ymin=lat,ymax=lat+value*50,color=variable),size=3.8,width=0)+
  geom_errorbar(data=df_species[df_species$variable=="SpeciesB",],
                aes(x=lon-4,ymin=lat,ymax=lat+value*50,color=variable),size=3.8,width=0)+
  geom_errorbar(data=df_species[df_species$variable=="SpeciesC",],
                aes(x=lon,ymin=lat,ymax=lat+value*50,color=variable),size=3.8,width=0)+
  geom_errorbar(data=df_species[df_species$variable=="SpeciesD",],
                aes(x=lon+4,ymin=lat,ymax=lat+value*50,color=variable),size=3.8,width=0)+
  geom_errorbar(data=df_species[df_species$variable=="SpeciesE",],
                aes(x=lon+8,ymin=lat,ymax=lat+value*50,color=variable),size=3.8,width=0)+
  scale_y_continuous(expand = c(0,0))+
  scale_x_continuous(expand = c(0,0))+
  #自定义颜色
  scale_fill_manual(values = c(siteA="#037ef3",siteB="#f85a40",siteC="#00c16e",
                               siteD="#7552cc",siteE="#0cb9c1",siteF="#f48924"))+
  labs(x=NULL,y=NULL)+
  #添加分组文字标记
  annotate("text", x = -100, y = 60, label = "siteA", size=5, color = "#037ef3")+
  annotate("text", x = -140, y = -25, label = "siteB", size=5, color = "#f85a40")+
  annotate("text", x = 100, y = 30, label = "siteC", size=5, color = "#00c16e")+
  annotate("text", x = 75, y = -15, label = "siteD", size=5, color = "#7552cc")+
  annotate("text", x = -25, y = 0, label = "siteE", size=5, color = "#0cb9c1")+
  annotate("text", x = 180, y = 30, label = "siteF", size=5, color = "#f48924")+
  scale_color_manual(name="Species",values=c(SpeciesA="#ccc900",SpeciesB="#f784b6",
                                             SpeciesC="#005238",SpeciesD="#862633",
                                             SpeciesE="#0eb24e"))+
  #主题设置
  theme_bw()+
  theme(plot.background = element_blank(),
        panel.grid = element_blank(),
        legend.position = c(0.95,0.2),
        legend.background = element_blank())
