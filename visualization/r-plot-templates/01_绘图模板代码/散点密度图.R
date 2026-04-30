rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点密度图")

##加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggpointdensity) # A Cross Between a 2D Density Plot and a Scatter Plot
library(viridis) # Colorblind-Friendly Color Maps for R
library(ggpmisc) # Miscellaneous Extensions to 'ggplot2'
library(ggpubr) # 'ggplot2' Based Publication Ready Plots

##加载数据（随机编写，无实际意义）
df1 <- read.table(file="data1.txt",sep="\t",header=T,check.names=FALSE)
df2 <- read.table(file="data2.txt",sep="\t",header=T,check.names=FALSE)

###绘制普通散点图
ggplot(df1, aes(x, y))+
  geom_point()
ggplot(df2, aes(x, y))+
  geom_point()

###基于df1数据并基于ggpointdensity包绘制密度散点图
ggplot(df1, aes(x, y)) +
  #绘制密度散点图
  geom_pointdensity() +
  #主题相关设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        legend.position = c(0.15,0.75),
        axis.text = element_text(size = 10))+
  labs(x=NULL, y=NULL)+
  ##基于viridis配置渐变色
  scale_color_viridis(option = "turbo")->p1
p1

###基于df2数据绘制密度散点图并添加拟合曲线及回归方程
ggplot(df2, aes(x, y)) +
  #绘制密度散点图
  geom_pointdensity() +
  #添加拟合曲线
  geom_smooth(method = "lm", 
              formula = y ~ x,
              linewidth = 1,
              linetype=1, color = "#ffcb00")+
  ##添加回归方程及R值
  stat_cor(method = "pearson",label.x = 60, label.y = 20,size=4)+
  stat_poly_eq(formula = y ~ x, aes(label = paste(after_stat(eq.label),
                                             sep = "~~~")), parse = TRUE,
               label.x = 0.88, label.y = 0.22,size=4)+
  #手动添加样品数量
  annotate("text", x = 68 , y = 32,label = "N = 2900", size= 4)+
  #主题相关设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        legend.position = c(0.12,0.78),
        axis.text = element_text(size = 10))+
  labs(x=NULL, y=NULL)+
  ##基于viridis配置渐变色
  scale_color_viridis(option = "turbo")+
  scale_y_continuous(expand = c(0,0))+
  scale_x_continuous(expand = c(0,0))->p2
p2


####拼图
library(patchwork)
p1+p2+
  plot_annotation(
    tag_levels = c('A', '1'), tag_prefix = 'Fig. ', tag_sep = '.',) +
  theme(plot.tag.position = c(0, 0.98),
        plot.tag = element_text(size = 15, hjust = 0, vjust = 0, color="black"))
