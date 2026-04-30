rm(list = ls())

#安装R包
# install.packages("waterfalls")
#加载R包
library(waterfalls) # Create Waterfall Charts using 'ggplot2' Simply
library(ggthemes) # Extra Themes, Scales and Geoms for 'ggplot2'
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization

# 数据
df<-data.frame(
  A=LETTERS[1:10],
  B=c(5,2,-3,-2,5,8,-4,3,6,-15))

#绘图
#背景色
color <- colorRampPalette(brewer.pal(11,"PuOr"))(30)
col = ifelse(df$B>0, "#eb2226", "#00aaff")#自定义颜色
# col=c('red','red','green','green','red','red','green','red','red','green')
waterfall(values = df$B, #数值
          labels = df$A,#标签
          rect_width = 0.7,#柱子宽度
          draw_lines = T,#是否显示矩形间的连线
          linetype = 2,#矩形间连线类型
          rect_border = "#333c41",#矩形边框颜色
          fill_by_sign = F,#正值及负值是否具有相同颜色
          fill_colours = col,#自定义颜色
          calc_total = T,#是否显示终值
          total_rect_color = "#2db928",#终值填充色
          total_rect_text_color = "white",#终值标签颜色
          total_axis_text = 'Total')+#终值标签设置
  theme_tufte()+#主题
  theme(axis.text=element_text(color='#333c41',size=12),
        legend.position = "none")+
  labs(x=NULL,y=NULL)#去除轴标题
#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)



