---
jupyter:
  jupytext:
    cell_metadata_filter: -all
    formats: ipynb,md
    main_language: python
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.1
---

# 🎨 R语言绘图代码全集 — Obsidian学习笔记

> 本文档整合了 **106个R语言绘图模板代码**，按图表类型分为 **12大类**，附完整代码，方便复制学习。

>
> **使用方式：** 直接点击代码块右上角「复制」按钮即可复制完整代码到RStudio运行。


---

## 📊 一、柱状图 & 条形图

### 条形图

```r

#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/条形图")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics

#加载数据
df <- read.table("data.txt",header = T, check.names = F)

#绘图
col <- c("#d91481","#e7524e","#f8a250","#f9f05f","#4ea363","#7bc8f6","#5193f4","#ae77e8")
ggplot(df,aes(samples,value,fill=group))+
  geom_bar(stat="summary",fun=mean,position="dodge")+
  theme_classic()+
  theme(axis.text.x=element_blank(),
        axis.text.y=element_text(color='black',size=9),
        axis.ticks.x = element_blank(),
        legend.text = element_text(color='black',size=12),
        legend.title = element_blank(),
        legend.background = element_blank(),
        legend.position = c(0.5,0.9),
        axis.title = element_text(color='black',size=12))+
  scale_y_continuous(expand = c(0, 0), limit = c(0, 100))+
  scale_x_continuous(expand = c(0, 0.5), limit = c(0, 125))+
  scale_fill_manual(values = col)+
  labs(x="Genome assembly",y="Number of duplicated \nprotein-coding genes")+
  guides(fill = guide_legend(nrow = 1))

```


---

### 条形图+黑白色填充+条纹+显著性

```r

#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/条形图+黑白色填充+条纹+显著性")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(ggpubr) # 'ggplot2' Based Publication Ready Plots

#加载数据
df <- read.table("data.txt",header = T, check.names = F)
#转换数据
data=melt(df)
data$G<-rep(c("T","F","H"), each = 24)

#基础绘图
p1 <- ggplot(data,aes(G,value))+
  #绘制条形图
  geom_bar(aes(fill=G),color='grey50', stat="summary",
           fun=mean,position="dodge", linewidth = 0.8)+ 
  #误差棒
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.2, linewidth = 0.8)+
  labs(x=NULL,y=NULL)+
  #颜色
  scale_fill_manual(values = c("#4c4c4c","#6f6f6f","#ffffff"))+
  #显著性
  geom_signif(comparisons = list(c("F","H"),
                                 c("H","T"),
                                 c("F","T")),
              map_signif_level = T, 
              test = "t.test",
              textsize = 6,
              y_position = c(50,55,60),
              tip_length = c(0,0,0),
              size=0.8,color="black")+
  scale_y_continuous(expand = c(0,0), limits = c(0,70), breaks = c(0,10,20,30,40,50,60))+
  # 主题相关设置
  theme_classic()+
  theme(axis.text = element_text(size = 14),
        legend.position = "none",
        axis.line = element_line(linewidth = 0.8))
p1

###添加花纹——需要借助ggpattern包
#安装并加载ggpattern包
# remotes::install_github("coolbutuseless/ggpattern")
library(ggpattern)
p2 <- ggplot(data,aes(G,value))+
  #利用ggpattern包中的geom_bar_pattern函数绘制条形图
  geom_bar_pattern(aes(fill=G,pattern=G),color='grey50', stat="summary",
                   fun=mean,position="dodge", linewidth = 0.8,
                   pattern_color = "black",
                   pattern_size = 0.5,
                   pattern_spacing = 0.03)+ 
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.2, linewidth = 0.8)+
  labs(x=NULL,y=NULL)+
  scale_fill_manual(values = c("#4c4c4c","#6f6f6f","#ffffff"))+
  geom_signif(comparisons = list(c("F","H"),
                                 c("H","T"),
                                 c("F","T")),
              map_signif_level = T, 
              test = "t.test",
              textsize = 6,
              y_position = c(50,55,60),
              tip_length = c(0,0,0),
              size=0.8,color="black")+
  scale_y_continuous(expand = c(0,0), limits = c(0,70), breaks = c(0,10,20,30,40,50,60))+
  theme_classic()+
  theme(axis.text = element_text(size = 14),
        legend.position = "none",
        axis.line = element_line(linewidth = 0.8))
p2

##去除填充色
p3 <- ggplot(data,aes(G,value))+
  geom_bar_pattern(aes(pattern=G),
                   color='grey50', fill = "white",stat="summary",
                   fun=mean,position="dodge", linewidth = 0.8,
                   pattern_color = "white",
                   pattern_fill = "black",
                   pattern_size = 0.5,
                   pattern_spacing = 0.05)+ 
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.2, linewidth = 0.8)+
  labs(x=NULL,y=NULL)+
  geom_signif(comparisons = list(c("F","H"),
                                 c("H","T"),
                                 c("F","T")),
              map_signif_level = T, 
              test = "t.test",
              textsize = 6,
              y_position = c(50,55,60),
              tip_length = c(0,0,0),
              size=0.8,color="black")+
  scale_y_continuous(expand = c(0,0), limits = c(0,70), breaks = c(0,10,20,30,40,50,60))+
  theme_classic()+
  theme(axis.text = element_text(size = 14),
        legend.position = "none",
        axis.line = element_line(linewidth = 0.8))
p3

##根据分组添加条纹
p4 <- ggplot(data,aes(G,value))+
  geom_bar_pattern(aes(pattern_type = G),
                   color='grey50', fill = "white",stat="summary",
                   fun=mean,position="dodge", linewidth = 0.8,
                   pattern = 'polygon_tiling',#'stripe' (default), 'crosshatch', 'point', 'circle', 'none'
                   pattern_key_scale_factor = 1.2,
                   pattern_fill = "white",
                   pattern_color = "black"
                   )+ 
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.2, linewidth = 0.8)+
  labs(x=NULL,y=NULL)+
  geom_signif(comparisons = list(c("F","H"),
                                 c("H","T"),
                                 c("F","T")),
              map_signif_level = T, 
              test = "t.test",
              textsize = 6,
              y_position = c(50,55,60),
              tip_length = c(0,0,0),
              size=0.8,color="black")+
  scale_y_continuous(expand = c(0,0), limits = c(0,70), breaks = c(0,10,20,30,40,50,60))+
  theme_classic()+
  theme(axis.text = element_text(size = 14),
        legend.position = "none",
        axis.line = element_line(linewidth = 0.8))+
  scale_pattern_type_manual(values = c("hexagonal", "rhombille",
                                       "pythagorean"))
p4

####拓展
p5 <- ggplot(data,aes(G,value))+
  geom_bar_pattern(aes(pattern_angle = G),
                   stat="summary",
                   fun=mean,position="dodge", linewidth = 0.8,
                   pattern         = 'placeholder',
                   pattern_type    = 'kitten',
                   fill            = 'white', 
                   colour          = 'black',
                   pattern_spacing = 0.025
  )+ 
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.2, linewidth = 0.8)+
  labs(x=NULL,y=NULL)+
  geom_signif(comparisons = list(c("F","H"),
                                 c("H","T"),
                                 c("F","T")),
              map_signif_level = T, 
              test = "t.test",
              textsize = 6,
              y_position = c(50,55,60),
              tip_length = c(0,0,0),
              size=0.8,color="black")+
  scale_y_continuous(expand = c(0,0), limits = c(0,70), breaks = c(0,10,20,30,40,50,60))+
  theme_classic()+
  theme(axis.text = element_text(size = 14),
        legend.position = "none",
        axis.line = element_line(linewidth = 0.8))
p5

p6 <- ggplot(data,aes(G,value))+
  geom_bar_pattern(aes(pattern_fill = G),
                   stat="summary",color='grey50', fill = "white",
                   fun=mean,position="dodge", linewidth = 0.8,
                   pattern       = 'plasma'
  )+ 
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.2, linewidth = 0.8)+
  labs(x=NULL,y=NULL)+
  geom_signif(comparisons = list(c("F","H"),
                                 c("H","T"),
                                 c("F","T")),
              map_signif_level = T, 
              test = "t.test",
              textsize = 6,
              y_position = c(50,55,60),
              tip_length = c(0,0,0),
              size=0.8,color="black")+
  scale_y_continuous(expand = c(0,0), limits = c(0,70), breaks = c(0,10,20,30,40,50,60))+
  theme_classic()+
  theme(axis.text = element_text(size = 14),
        legend.position = "none",
        axis.line = element_line(linewidth = 0.8))
p6

####拼图
(p1+p2+p3)/(p4+p5+p6)

```


---

### 条形图+双y轴+双x轴

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/条形图+双y轴+双x轴')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(gtable) # Arrange 'Grobs' in Tables
library(grid) # The Grid Graphics Package

##加载数据（随机编写，无实际意义）
df <- read.table("data.txt",sep = "\t",header=1,check.names=FALSE)

###测试使用sec.axis添加双轴
ggplot(df)+
  geom_line(aes(x1, y1), color = "#616f67", linewidth = 1)+
  geom_point(aes(x = x1, y = y1), fill = "#76daff", shape = 21, size = 3)+
  geom_line(aes(x = x2/100, y = y2/4), color = "#616f67", linewidth = 1)+
  geom_point(aes(x = x2/100, y = y2/4), fill = "#dc5034", shape = 21, size = 3)+
  scale_y_continuous(name = "This is y1-axis",#y1特征
                     sec.axis = sec_axis( trans=~.*4, name="This is y2-axis"))+#y2特征
  scale_x_continuous(name = "This is x1-axis",#x1特征
                     sec.axis = sec_axis( trans=~.*100, name="This is x2-axis"))#x2特征
#劣势：对于分类变量不适用，可操作性太差，如果想实现副轴的倒转也没办法实现

####基于gtable包进行绘制
##绘制基础图形，为了更好的区分合并的图形，对图形坐标进行相应颜色的修改
p1<-ggplot(df, aes(x = x1, y = y1))+
  geom_col(fill="#ff4e00", color = "black", linewidth = 0.1, alpha = 0.8)+
  geom_line(color = "#616f67", linewidth = 1)+
  geom_point(fill = "#76daff", shape = 21, size = 3)+
  scale_y_continuous(limits = c(0,32),expand = c(0,0))+
  scale_x_continuous(expand = c(0,0), breaks = c(0,5,10,15,20,25,30))+
  theme_bw()+
  theme(panel.background = element_rect(fill = NA),#去除背景这一步很关键，否则后续合并图像会导致背景覆盖不显示
        panel.grid = element_blank(),
        axis.text = element_text(color = "#ff4e00", size = 12),
        axis.title = element_text(color = "#ff4e00", size = 13),
        axis.ticks = element_line(linewidth = 0.8),
        panel.border = element_rect(fill=NA, color="black", linewidth =1, linetype="solid"))+
  labs(x = "This is X1-axis", y = "This is y1-axis")
p2<-ggplot(df, aes(x = x2, y = y2))+
  geom_col(fill="#01cd74", color = "black", linewidth = 0.1, alpha = 0.8)+
  geom_line(color = "#616f67", linewidth = 1)+
  geom_point(fill = "#dc5034", shape = 21, size = 3)+
  scale_y_reverse(limits = c(130,0),expand = c(0,0))+
  scale_x_continuous(expand = c(0,0), breaks = c(0,500,1000,1500,2000,2500,3000))+
  theme_bw()+
  theme(panel.background = element_rect(fill = NA),#去除背景这一步很关键，否则后续合并图像会导致背景覆盖不显示
        panel.grid = element_blank(),
        axis.text = element_text(color = "#01cd74", size = 12),
        axis.title = element_text(color = "#01cd74", size = 13),
        axis.ticks = element_line(linewidth = 0.8),
        panel.border = element_rect(fill=NA, color="black", linewidth =1, linetype="solid"))+
  labs(x = "This is X2-axis", y = "This is y2-axis")
cowplot::plot_grid(p1,p2,ncol = 2)

##分别获取基于ggplot绘制的两张图象
g1 <- ggplotGrob(p1)
g2 <- ggplotGrob(p2)
pos <- c(subset(g1$layout, name == "panel", select = t:r))

##使用gtable_add_grob函数g2的主体图形添加到g1布局中
g <- gtable_add_grob(g1, g2$grobs[[which(g2$layout$name == "panel")]], 
                     pos$t, pos$l, pos$b, pos$l)
plot(g)

####将g2的坐标轴添加进合并的图像中
###将g2的y轴添加到图形右侧
##添加标签
#获取标签信息
index <- which(g2$layout$name == "ylab-l")
ylab <- g2$grobs[[index]]
#交换y轴标签位置并修改文本的对齐方式
# 交换宽度
widths <- ylab$widths
ylab$widths[1] <- widths[3]
ylab$widths[3] <- widths[1]
ylab$vp[[1]]$layout$widths[1] <- widths[3]
ylab$vp[[1]]$layout$widths[3] <- widths[1]

# 修改对齐
ylab$children[[1]]$hjust <- 1 - ylab$children[[1]]$hjust 
ylab$children[[1]]$vjust <- 1 - ylab$children[[1]]$vjust 
ylab$children[[1]]$x <- unit(1, "npc") - ylab$children[[1]]$x
#展示图形
g <- gtable_add_cols(g, g2$widths[g2$layout[index, ]$l], pos$r)
g <- gtable_add_grob(g, ylab, pos$t, pos$r + 1, pos$b, pos$r + 1, clip = "off", name = "ylab-r")
plot(g)

##添加坐标轴并将其移动到右边
index <- which(g2$layout$name == "axis-l")
yaxis <- g2$grobs[[index]]
ticks <- yaxis$children[[2]]
# 交换刻度线和刻度标签的相对位置
ticks$widths <- rev(ticks$widths)
ticks$grobs <- rev(ticks$grobs)
# 移动刻度线
ticks$grobs[[1]]$x <- ticks$grobs[[1]]$x - unit(1, "npc") + unit(3, "pt")
#将所有的修改覆盖原来的设置
#交换y轴标签位置并修改文本的对齐方式
# 交换宽度
widths <- ylab$widths
ticks$grobs[[2]]$widths[1] <- widths[3]
ticks$grobs[[2]]$widths[3] <- widths[1]
ticks$grobs[[2]]$vp[[1]]$layout$widths[1] <- widths[3]
ticks$grobs[[2]]$vp[[1]]$layout$widths[3] <- widths[1]

# 修改对齐
ticks$grobs[[2]]$children[[1]]$hjust <- 1 - ticks$grobs[[2]]$children[[1]]$hjust 
ticks$grobs[[2]]$children[[1]]$vjust <- 1 - ticks$grobs[[2]]$children[[1]]$vjust 
ticks$grobs[[2]]$children[[1]]$x <- unit(1, "npc") - ticks$grobs[[2]]$children[[1]]$x
yaxis$children[[2]] <- ticks
#展示图形
g <- gtable_add_cols(g, g2$widths[g2$layout[index, ]$l], pos$r)
g <- gtable_add_grob(g, yaxis, pos$t, pos$r + 1, pos$b, pos$r + 1, clip = "off", name = "axis-r")
plot(g)

###将g2的x轴添加到图形顶部
##添加标签
#获取标签信息
index2 <- which(g2$layout$name == "xlab-b")
xlab <- g2$grobs[[index2]]
# 修改对齐
xlab$children[[1]]$hjust <- 1 - xlab$children[[1]]$hjust 
xlab$children[[1]]$vjust <- 1 - xlab$children[[1]]$vjust 

#展示图形
g <- gtable_add_rows(g, g2$heights[g2$layout[index2,]$b], 5)#这里设置需要根据实际布局进行调整，可使用gtable_show_layout()函数查看具体布局
g <- gtable_add_grob(g, xlab, pos$t, pos$r, pos$b, pos$r, clip = "off", name = "xlab-t")
plot(g)

##添加坐标轴并将其移动到顶部
index2 <- which(g2$layout$name == "axis-b")
xaxis <- g2$grobs[[index2]]
ticks <- xaxis$children[[2]]
# 交换刻度线和刻度标签的相对位置
ticks$heights <- rev(ticks$heights)
ticks$grobs <- rev(ticks$grobs)
# 移动刻度线
ticks$grobs[[1]]$heights <- ticks$grobs[[1]]$heights - unit(1, "npc") + unit(3, "pt")
# 水平交换文本标签
heights <- ticks$grobs[[2]]$y
ticks$grobs[[2]]$y[1] <- heights[3]
ticks$grobs[[2]]$y[3] <- heights[1]
# 修改对齐
ticks$grobs[[2]]$children[[1]]$hjust <- 1 
ticks$grobs[[2]]$children[[1]]$vjust <- 1
#将所有的修改覆盖原来的设置
xaxis$children[[2]] <- ticks
#展示图形
g <- gtable_add_rows(g, g2$heights[g2$layout[index2, ]$b], pos$t)
g <- gtable_add_grob(g, xaxis, pos$t+1, pos$l, pos$b, pos$r, clip = "off", name = "axis-t")
plot(g)


##########将所有操作封装成几个函数进行操作
####添加右侧坐标轴及标签
add_y2_axis <- function(g, g2){
  ############添加标签##############
  #获取标签信息
  index <- which(g2$layout$name == "ylab-l")
  ylab <- g2$grobs[[index]]
  #交换y轴标签位置并修改文本的对齐方式
  # 交换宽度
  widths <- ylab$widths
  ylab$widths[1] <- widths[3]
  ylab$widths[3] <- widths[1]
  ylab$vp[[1]]$layout$widths[1] <- widths[3]
  ylab$vp[[1]]$layout$widths[3] <- widths[1]
  
  # 修改对齐
  ylab$children[[1]]$hjust <- 1 - ylab$children[[1]]$hjust 
  ylab$children[[1]]$vjust <- 1 - ylab$children[[1]]$vjust 
  ylab$children[[1]]$x <- unit(1, "npc") - ylab$children[[1]]$x
  #展示图形
  g <- gtable_add_cols(g, g2$widths[g2$layout[index, ]$l], pos$r)
  g <- gtable_add_grob(g, ylab, pos$t, pos$r + 1, pos$b, pos$r + 1, clip = "off", name = "ylab-r")
  
  ######添加坐标轴并将其移动到右边############
  index <- which(g2$layout$name == "axis-l")
  yaxis <- g2$grobs[[index]]
  ticks <- yaxis$children[[2]]
  # 交换刻度线和刻度标签的相对位置
  ticks$widths <- rev(ticks$widths)
  ticks$grobs <- rev(ticks$grobs)
  # 移动刻度线
  ticks$grobs[[1]]$x <- ticks$grobs[[1]]$x - unit(1, "npc") + unit(3, "pt")
  #将所有的修改覆盖原来的设置
  #交换y轴标签位置并修改文本的对齐方式
  # 交换宽度
  widths <- ylab$widths
  ticks$grobs[[2]]$widths[1] <- widths[3]
  ticks$grobs[[2]]$widths[3] <- widths[1]
  ticks$grobs[[2]]$vp[[1]]$layout$widths[1] <- widths[3]
  ticks$grobs[[2]]$vp[[1]]$layout$widths[3] <- widths[1]
  
  # 修改对齐
  ticks$grobs[[2]]$children[[1]]$hjust <- 1 - ticks$grobs[[2]]$children[[1]]$hjust 
  ticks$grobs[[2]]$children[[1]]$vjust <- 1 - ticks$grobs[[2]]$children[[1]]$vjust 
  ticks$grobs[[2]]$children[[1]]$x <- unit(1, "npc") - ticks$grobs[[2]]$children[[1]]$x
  yaxis$children[[2]] <- ticks
  #展示图形
  g <- gtable_add_cols(g, g2$widths[g2$layout[index, ]$l], pos$r)
  g <- gtable_add_grob(g, yaxis, pos$t, pos$r + 1, pos$b, pos$r + 1, clip = "off", name = "axis-r")
  g
}

####添加顶部坐标轴及标签
add_x2_axis <- function(g, g2){
  ##############添加标签#############
  #获取标签信息
  index2 <- which(g2$layout$name == "xlab-b")
  xlab <- g2$grobs[[index2]]
  # 修改对齐
  xlab$children[[1]]$hjust <- 1 - xlab$children[[1]]$hjust 
  xlab$children[[1]]$vjust <- 1 - xlab$children[[1]]$vjust 
  
  #展示图形
  g <- gtable_add_rows(g, g2$heights[g2$layout[index2,]$b], 5)#这里设置需要根据实际布局进行调整，可使用gtable_show_layout()函数查看具体布局
  g <- gtable_add_grob(g, xlab, pos$t, pos$r, pos$b, pos$r, clip = "off", name = "xlab-t")
  
  ############添加坐标轴并将其移动到顶部##########
  index2 <- which(g2$layout$name == "axis-b")
  xaxis <- g2$grobs[[index2]]
  ticks <- xaxis$children[[2]]
  # 交换刻度线和刻度标签的相对位置
  ticks$heights <- rev(ticks$heights)
  ticks$grobs <- rev(ticks$grobs)
  # 移动刻度线
  ticks$grobs[[1]]$heights <- ticks$grobs[[1]]$heights - unit(1, "npc") + unit(3, "pt")
  # 水平交换文本标签
  heights <- ticks$grobs[[2]]$y
  ticks$grobs[[2]]$y[1] <- heights[3]
  ticks$grobs[[2]]$y[3] <- heights[1]
  # 修改对齐
  ticks$grobs[[2]]$children[[1]]$hjust <- 1 
  ticks$grobs[[2]]$children[[1]]$vjust <- 1
  #将所有的修改覆盖原来的设置
  xaxis$children[[2]] <- ticks
  #展示图形
  g <- gtable_add_rows(g, g2$heights[g2$layout[index2, ]$b], pos$t)
  g <- gtable_add_grob(g, xaxis, pos$t+1, pos$l, pos$b, pos$r, clip = "off", name = "axis-t")
  g
}

###主函数
add_axis <- function(p1, p2){
  ##分别获取基于ggplot绘制的两张图象
  g1 <- ggplotGrob(p1)
  g2 <- ggplotGrob(p2)
  pos <<- c(subset(g1$layout, name == "panel", select = t:r))
  ##使用gtable_add_grob函数g2的主体图形添加到g1布局中
  g <- gtable_add_grob(g1, g2$grobs[[which(g2$layout$name == "panel")]], 
                       pos$t, pos$l, pos$b, pos$l)
  ##添加右侧y2坐标轴
  g <- add_y2_axis(g, g2)
  ##添加顶部的x2坐标轴
  g <- add_x2_axis(g, g2)#只添加y2可注释掉这一行
  ##显示图形
  plot(g)
}

#####测试
##同时添加x2,y2
add_axis(p1, p2)

##只添加x2或y2,只需要注释掉add_axis函数中相应的代码并重新运行该函数即可
#只添加x2
add_axis <- function(p1, p2){
  ##分别获取基于ggplot绘制的两张图象
  g1 <- ggplotGrob(p1)
  g2 <- ggplotGrob(p2)
  pos <<- c(subset(g1$layout, name == "panel", select = t:r))
  ##使用gtable_add_grob函数g2的主体图形添加到g1布局中
  g <- gtable_add_grob(g1, g2$grobs[[which(g2$layout$name == "panel")]], 
                       pos$t, pos$l, pos$b, pos$l)
  ##添加右侧y2坐标轴
  # g <- add_y2_axis(g, g2)
  ##添加顶部的x2坐标轴
  g <- add_x2_axis(g, g2)#只添加y2可注释掉这一行
  ##显示图形
  plot(g)
}
add_axis(p1, p2)

#只添加y2
add_axis <- function(p1, p2){
  ##分别获取基于ggplot绘制的两张图象
  g1 <- ggplotGrob(p1)
  g2 <- ggplotGrob(p2)
  pos <<- c(subset(g1$layout, name == "panel", select = t:r))
  ##使用gtable_add_grob函数g2的主体图形添加到g1布局中
  g <- gtable_add_grob(g1, g2$grobs[[which(g2$layout$name == "panel")]], 
                       pos$t, pos$l, pos$b, pos$l)
  ##添加右侧y2坐标轴
  g <- add_y2_axis(g, g2)
  ##添加顶部的x2坐标轴
  # g <- add_x2_axis(g, g2)#只添加y2可注释掉这一行
  ##显示图形
  plot(g)
}
add_axis(p1, p2)

```


---

### 条形图替代方案—气球图

```r

rm(list=ls())#clear Global Environment
setwd('D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\气球图')#设置工作路径

#加载包
# install.packages("ggpubr")
library(ggpubr) # 'ggplot2' Based Publication Ready Plots
#读取数据
df <- read.table(file="Genus.txt",sep="\t",header=T,check.names=FALSE,row.names = 1)

head(df)#查看

#简单绘图
ggballoonplot(df)

####个性化设置########
color=c("blue", "white", "red")
ggballoonplot(df, 
              fill = "value", #气球填充颜色
              ggtheme = theme_bw(),#画板主题
              size = "value",#气球大小
              color = "grey",#气球边框颜色
              shape = 22,#shape可以改变显示形状
              show.label = F)+#是否显示标签
  scale_fill_viridis_c(option = "C")+
  guides(size = FALSE)+#气球图例是否显示
  scale_fill_gradientn(colors = color)#设置颜色
  
###整体使用方法
ggballoonplot(
  data,#数据集
  x = NULL,#x轴向量
  y = NULL,#y轴向量
  size = "value",#气球大小依据
  facet.by = NULL,#气球形状选择
  size.range = c(1, 10),#气球大小选择范围
  shape = 21,#气球形状
  color = "black",#气球边框颜色
  fill = "gray",#气球填充颜色
  show.label = FALSE,#是否显示每个气球代表的具体大小
  font.label = list(size = 12, color = "black"),#示每个气球代表的具体大小的字体设定
  rotate.x.text = TRUE,#是否旋转标注字体
  ggtheme = theme_minimal(),#画板主题
  ...)


##ggplot2包绘制
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization
#转换数据
df$Tax=rownames(df)
df1=melt(df)
colnames(df1)=c("Tax","Samples","value")
#绘图
col <- colorRampPalette(brewer.pal(12,"Paired"))(11)
#绘图
ggplot()+ 
  geom_point(df1,mapping = aes(x = Samples, y = Tax, size = value, fill=Samples),shape=21)+
  scale_fill_manual(values = col)+
  scale_size_continuous(range = c(0, 10))+
  theme(panel.background = element_blank(),
        legend.key = element_blank(),
        axis.text = element_text(color = "black",size = 10),
        panel.grid.major = element_line(color = "gray"),#网格线条颜色
        panel.border = element_rect(color="black",fill=NA))+#边框色
  labs(x=NULL,y=NULL)
#背景色
color <- colorRampPalette(brewer.pal(11,"BrBG"))(30)
#添加背景
grid.raster(alpha(color, 0.1), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

```


---

### 分组分面条形图

```r

#设置工作环境
rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/分组分面条形图")

##加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package

##加载数据（随机编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")

##将数据整理为绘图所需格式
data <- melt(df)
data$group <- factor(data$group, levels = c("A","B","C","D"))
data$sample <- factor(data$sample, levels = rev(df$sample))

##绘图
ggplot(data, aes(value, sample, fill = group))+
  #绘制条形图函数
  geom_col()+
  #指定分面变量
  facet_grid(~variable)+
  #设置轴标题并去除图例的标题
  labs(fill=NULL, y = NULL, x = "This is X-axis!")+
  #主题设置
  theme_bw()+
  theme(axis.text.y = element_text(size = 10, color = "black"),
        axis.text.x = element_text(size = 10, color = "black",
                                   angle = 270, vjust = 0.5, hjust = 0),
        strip.text = element_text(size = 12, color = "black"),
        legend.text = element_text(size = 12, color = "black"),
        axis.title.x = element_text(size = 14, color = "black"))+
  #自定义颜色并设置图例长宽
  scale_fill_manual(values = c("#ff3c41","#fcd000","#47cf73","#0ebeff"),
                    guide=guide_legend(keywidth=1.5, keyheight=7))

```


---

### 蝶形条形图&蝶形柱状堆积图

```r

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

```


---

### 双向柱状图

```r

#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/双向柱状图")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics

#加载数据
df <- read.table("data.txt",header = T,sep='\t')
df$group <- factor(df$group,levels = c("HPRC.EAS","CPC"))
df$sample <- factor(df$sample,levels = c("OR4K2","OR4K1","GRPIN2","OR9G1","SULT1A3","OR4Q3",
                                         "PDPR","CYP2D6","PRAMEF18"))
#数据处理——将其中一组的数据转换为负值
df$value <- ifelse(df$group=="HPRC.EAS",-df$value,df$value)
#颜色
col <- c("#f89f68","#4b84b3")
#绘图
ggplot(df,aes(sample,value,fill=group))+
  #柱状图
  geom_col(width = 0.8)+
  #坐标转换
  coord_flip()+
  #自定义颜色
  scale_fill_manual(values = col)+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.x = element_text(color = "black", size = 13),
        axis.text.y = element_text(color = "black",size = 14,face = "italic"),
        axis.title = element_text(color = "black",size = 16),
        legend.position = "top",
        legend.title = element_blank(),
        legend.text = element_text(color = "black",size = 15))+
  #标题设置
  labs(x=NULL,y="CNV Frequency")+
  #y轴范围设置
  scale_y_continuous(breaks = seq(-1, 1, 0.5), 
                     labels = as.character(abs(seq(-1, 1, 0.5))),
                     limits = c(-1, 1))

```


---

### 双向柱状堆积图+排序

```r

#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/双向柱状堆积图+排序")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(dplyr) # A Grammar of Data Manipulation

#加载数据
df <- read.table("data.txt",header = T,sep='\t')

#将宽数据转变为长数据
df2 <- melt(df, id.vars = c("sample","group"), 
            measure.vars = c('value5','value4','value3',
                             'value2','value1'))
df2$group <- factor(df$group,levels = c("group1","group2"))
df2$sample <- factor(df$sample,levels = c("OR4K2","OR4K1","GRPIN2","OR9G1","SULT1A3","OR4Q3",
                                         "PDPR","CYP2D6","PRAMEF18"))

#数据处理——将其中一组的数据转换为负值
df2$value <- ifelse(df2$group=="group2",-df2$value,df2$value)

#双向柱状堆积图
df2 %>% 
  ggplot()+
  #柱状图
  geom_col(aes(sample, value, fill = variable), width = 0.9)+
  #坐标转换
  coord_flip()+
  #自定义颜色
  scale_fill_manual(values = c(value1="#d20962", 
                               value2="#f47721", 
                               value3="#7ac143", 
                               value4="#00a78e", 
                               value5="#00bce4"))+
  #标注y=0刻度线
  geom_hline(yintercept = 0, 
             color = "black", linetype = 1,linewidth=0.6)+
  #主题设置
  theme_bw()+
  theme(panel.grid.major.y = element_blank(),
        axis.text.x = element_text(color = "black", size = 13),
        axis.text.y = element_text(color = "black",size = 14,face = "italic"),
        axis.title = element_text(color = "black",size = 16),
        legend.position = "top",
        legend.title = element_blank(),
        legend.text = element_text(color = "black",size = 15))+
  #标题设置
  labs(x=NULL,y="Frequency")+
  #y轴范围设置
  scale_y_continuous(breaks = seq(-400, 400, 200), 
                     labels = as.character(abs(seq(-400, 400, 200))),
                     limits = c(-480, 480))->p1
p1

####排序-金字塔型
#根据原始数据计算各样本值和（根据个人需求制定排序方式）
df3 <- df %>%
  melt(id.vars = c("sample","group"), 
       measure.vars = c('value5','value4','value3',
                        'value2','value1')) %>% 
  select(sample,value) %>%
  group_by(sample) %>% 
  summarise_all(sum)
#排序
df3 <- df3[order(abs(df3$value),decreasing=TRUE),]

#将绘图数据按照得到的排序顺序进行排序
df2$sample <- factor(df$sample,levels = df3$sample)

#重新绘图
df2 %>% 
  ggplot()+
  #柱状图
  geom_col(aes(sample, value, fill = variable), width = 0.9)+
  #坐标转换
  coord_flip()+
  #自定义颜色
  scale_fill_manual(values = c(value1="#d20962", 
                               value2="#f47721", 
                               value3="#7ac143", 
                               value4="#00a78e", 
                               value5="#00bce4"))+
  #标注y=0刻度线
  geom_hline(yintercept = 0, 
             color = "black", linetype = 1,linewidth=0.6)+
  #主题设置
  theme_bw()+
  theme(panel.grid.major.y = element_blank(),
        axis.text.x = element_text(color = "black", size = 13),
        axis.text.y = element_text(color = "black",size = 14,face = "italic"),
        axis.title = element_text(color = "black",size = 16),
        legend.position = "top",
        legend.title = element_blank(),
        legend.text = element_text(color = "black",size = 15))+
  #标题设置
  labs(x=NULL,y="Frequency")+
  #y轴范围设置
  scale_y_continuous(breaks = seq(-400, 400, 200), 
                     labels = as.character(abs(seq(-400, 400, 200))),
                     limits = c(-480, 480))->p2
p2

###排序——倒金字塔型
df2$sample <- factor(df$sample,levels = rev(df3$sample))
df2 %>% 
  ggplot()+
  #柱状图
  geom_col(aes(sample, value, fill = variable), width = 0.9)+
  #坐标转换
  coord_flip()+
  #自定义颜色
  scale_fill_manual(values = c(value1="#d20962", 
                               value2="#f47721", 
                               value3="#7ac143", 
                               value4="#00a78e", 
                               value5="#00bce4"))+
  #标注y=0刻度线
  geom_hline(yintercept = 0, 
             color = "black", linetype = 1,linewidth=0.6)+
  #主题设置
  theme_bw()+
  theme(panel.grid.major.y = element_blank(),
        axis.text.x = element_text(color = "black", size = 13),
        axis.text.y = element_text(color = "black",size = 14,face = "italic"),
        axis.title = element_text(color = "black",size = 16),
        legend.position = "top",
        legend.title = element_blank(),
        legend.text = element_text(color = "black",size = 15))+
  #标题设置
  labs(x=NULL,y="Frequency")+
  #y轴范围设置
  scale_y_continuous(breaks = seq(-400, 400, 200), 
                     labels = as.character(abs(seq(-400, 400, 200))),
                     limits = c(-480, 480))->p3
p3


###排序——中间值最大，两端最小
# 在排序数据基础上添加一列数据，这列数据按照最大值在中间，其他值依次向两端延续
# 如 计算的df3中有9行数据，则最大值对于新的排序序号就是5，然后临近两个依次降低的排序为4和6
df3$x <- c(5,4,6,3,7,2,8,1,9)
#按照新的列排序
df4 <- df3[order(df3$x),]
df2$sample <- factor(df$sample,levels = df4$sample)
#重新绘图
df2 %>% 
  ggplot()+
  #柱状图
  geom_col(aes(sample, value, fill = variable), width = 0.9)+
  #坐标转换
  coord_flip()+
  #自定义颜色
  scale_fill_manual(values = c(value1="#d20962", 
                               value2="#f47721", 
                               value3="#7ac143", 
                               value4="#00a78e", 
                               value5="#00bce4"))+
  #标注y=0刻度线
  geom_hline(yintercept = 0, 
             color = "black", linetype = 1,linewidth=0.6)+
  #主题设置
  theme_bw()+
  theme(panel.grid.major.y = element_blank(),
        axis.text.x = element_text(color = "black", size = 13),
        axis.text.y = element_text(color = "black",size = 14,face = "italic"),
        axis.title = element_text(color = "black",size = 16),
        legend.position = "top",
        legend.title = element_blank(),
        legend.text = element_text(color = "black",size = 15))+
  #标题设置
  labs(x=NULL,y="Frequency")+
  #y轴范围设置
  scale_y_continuous(breaks = seq(-400, 400, 200), 
                     labels = as.character(abs(seq(-400, 400, 200))),
                     limits = c(-480, 480))->p4
p4


###排序——两端值最大，中间最小
# 在排序数据基础上添加一列数据，这列数据按照最小值在两端，其他值按照由小到大依次向两端延续
# 如计算的df3中有9行数据，则最小值对于新的排序序号就是5，然后临近两个依次降低的排序为4和6
df3$x2 <- c(1,9,2,8,3,7,4,6,5)
#按照新的列排序
df5 <- df3[order(df3$x2),]
df2$sample <- factor(df$sample,levels = df5$sample)
#重新绘图
df2 %>% 
  ggplot()+
  #柱状图
  geom_col(aes(sample, value, fill = variable), width = 0.9)+
  #坐标转换
  coord_flip()+
  #自定义颜色
  scale_fill_manual(values = c(value1="#d20962", 
                               value2="#f47721", 
                               value3="#7ac143", 
                               value4="#00a78e", 
                               value5="#00bce4"))+
  #标注y=0刻度线
  geom_hline(yintercept = 0, 
             color = "black", linetype = 1,linewidth=0.6)+
  #主题设置
  theme_bw()+
  theme(panel.grid.major.y = element_blank(),
        axis.text.x = element_text(color = "black", size = 13),
        axis.text.y = element_text(color = "black",size = 14,face = "italic"),
        axis.title = element_text(color = "black",size = 16),
        legend.position = "top",
        legend.title = element_blank(),
        legend.text = element_text(color = "black",size = 15))+
  #标题设置
  labs(x=NULL,y="Frequency")+
  #y轴范围设置
  scale_y_continuous(breaks = seq(-400, 400, 200), 
                     labels = as.character(abs(seq(-400, 400, 200))),
                     limits = c(-480, 480))->p5
p5

###拼图
library(patchwork)
patch <- (p2+p3)/(p4+p5)
guide_area()/(p1+patch+plot_layout(widths = c(1.5,2)))+
  plot_layout(heights = c(0.2,2))+
  plot_layout(guides = 'collect')+
  plot_annotation(
    tag_levels = c('A', '1'), 
    tag_prefix = 'Fig. ',
    tag_sep = '.',
  ) & theme(plot.tag.position = c(0, 1.05),
            plot.tag = element_text(size = 15, hjust = 0, vjust = 0,color="red")
  )

```


---

### 柱状图

```r

#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/柱状图+散点图+折线图")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(tidyr) # Tidy Messy Data
library(dplyr) # A Grammar of Data Manipulation
library(ggsignif) # Significance Brackets for 'ggplot2'

#数据——ggplot自带的ToothGrowth数据
df <- ToothGrowth
df$dose <- as.factor(df$dose)
data <- df
#计算均值及标准差
df1 <- data%>% group_by(dose)%>%
  summarise(mean= mean(len), sd= sd(len))
#绘图
ggplot()+ 
  geom_bar(df1,mapping=aes(x=dose,y=mean), fill = "white",
           size = 1.5,color = c("#d20962","#f47721","#7ac143"),position="dodge",
           stat="identity",width = 0.6)+
  geom_errorbar(df1,mapping=aes(x = dose,ymin = mean-sd, ymax = mean+sd),
                width = 0.3,color = c("#d20962","#f47721","#7ac143"), size=1.5)+
  geom_jitter(df, mapping=aes(x=dose,y=len,fill = dose,color = dose,shape = dose),
              size = 2.5,width = 0.2,alpha=0.9)+ 
  geom_line(df1,mapping=aes(x=dose,y=mean,group=1),
            size=1,color="#00aee6")+
  geom_point(df1,mapping=aes(x=dose,y=mean),color="black",size=3,shape=8)+
  scale_color_manual(values = c("#d20962","#f47721","#7ac143"))+ 
  geom_signif(df,mapping=aes(x=dose,y=len), 
              comparisons = list(c("0.5", "1"),
                                 c("1","2"),
                                 c("0.5","2")),
              map_signif_level=T, 
              tip_length=c(0,0,0,0,0,0), 
              y_position = c(35,40,45), 
              size=1, textsize = 7, 
              test = "t.test")+
  scale_y_continuous(expand = c(0, 0), limit = c(0, 50))+
  theme_classic(base_line_size = 1)+
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='black',size=13,face = "bold"),
        axis.title.y = element_text(color='black',size=15,face = "bold"),
        legend.text = element_text(color='black',size=13,face = "bold"),
        legend.title = element_blank(),
        legend.position = "none")+
  labs(x=NULL,y="Value")

```


---

### 柱状堆积图

```r

rm(list=ls())#clear Global Environment
#安装包
# install.packages("ggplot2")
# install.packages("ggprism")
# install.packages("reshape")
# install.packages("ggalluvial")
#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape) # Flexibly Reshape Data
library(ggalluvial) # Alluvial Plots in 'ggplot2'
library(ggprism) # A 'ggplot2' Extension Inspired by 'GraphPad Prism'

# 构造数据
df<-data.frame(samples=c('a','b','c','d','e'),
               A=c(0.3,0.25,0.1,0.2,0.15),
               B=c(0.6,0.1,0.05,0.2,0.05),
               C=c(0.4,0.2,0.1,0.15,0.15),
               D=c(0.1,0.2,0.3,0.3,0.1),
               E=c(0.3,0.25,0.1,0.2,0.15),
               F=c(0.6,0.1,0.05,0.2,0.05),
               G=c(0.4,0.2,0.1,0.15,0.15),
               H=c(0.1,0.2,0.3,0.3,0.1),
               I=c(0.3,0.25,0.1,0.2,0.15),
               J=c(0.6,0.1,0.05,0.2,0.05),
               K=c(0.4,0.2,0.1,0.15,0.15),
               L=c(0.1,0.2,0.3,0.3,0.1))
# 变量格式转换,宽数据转化为长数据,方便后续作图
df1 <- melt(df,id.vars = 'samples')
names(df1)[1:2] <- c("group","X")  #修改列名

#绘图
p1 <- ggplot(df1, aes( x = X,y=100 * value,fill = group,
                 stratum = group, alluvium = group))+
  geom_stratum(width = 0.9, color='white')+
  # geom_flow(alpha = 0.3,width = 0.5)+
  geom_alluvium(alpha = 0.3,#透明度
                width = 0.9,#宽度
                color='white',#间隔颜色
                size = 1,#间隔宽度
                curve_type = "linear")+#曲线形状，有linear、cubic、quintic、sine、arctangent、sigmoid几种类型可供调整
  scale_y_continuous(expand = c(0,0))+# 调整y轴属性，使柱子与X轴坐标接触
  labs(x=NULL,y="Relative Abundance(%)",#设置X轴和Y轴的名称以及添加标题
       fill="group")+
  scale_fill_prism(palette = "summer")+#使用ggprism包修改颜色
  theme_light()+
  theme(legend.position = 'none')+
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='#333c41',size=12),
        legend.text = element_text(color='#333c41',size=12))
p1

p2 <- ggplot(df1, aes( x = X,y=100 * value,fill = group,
                       stratum = group, alluvium = group))+
  geom_alluvium(curve_type = "sine",#曲线形状，有linear、cubic、quintic、sine、arctangent、sigmoid几种类型可供调整
                alpha=1)+
  scale_y_continuous(expand = c(0,0))+# 调整y轴属性，使柱子与X轴坐标接触
  labs(x=NULL,y=NULL,#设置X轴和Y轴的名称以及添加标题
       fill="group")+
  scale_fill_prism(palette = "summer")+#使用ggprism包修改颜色
  theme_minimal()+
  theme(legend.position = 'right')+
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='#333c41',size=12),
        legend.text = element_text(color='#333c41',size=12),
        axis.text.y = element_blank())
p2
#拼图
cowplot::plot_grid(p1,p2,ncol = 2)

```


---

### 柱状堆积图+多因子分面+柱间连线

```r

rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/柱状堆积图+多因子分面+柱间连线")

##加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape) # Flexibly Reshape Data
library(ggalluvial) # Alluvial Plots in 'ggplot2'
library(dplyr) # A Grammar of Data Manipulation
# remotes::install_github("teunbrand/ggh4x")
library(ggh4x) # Hacks for 'ggplot2'

##加载数据
df <- read.table("data.txt", check.names = F, header = 1, sep = "\t",row.names = 1)

##计算相对丰度
df2 <- as.data.frame(t(apply(t(df[5:9]),2,function(x) x/sum(x))))
df2$sample <- rownames(df2)
#合并数据
df3 <- df[1:4]
df3$sample <- rownames(df3)
data <- merge(df3, df2, by = "sample")

##变量格式转换,宽数据转化为长数据
data1 <- melt(data,
            id.vars = c("sample","group1","group2","group3","time"), 
            measure.vars = c('SpeciesA','SpeciesB','SpeciesC',
                             'SpeciesD','SpeciesE'))
names(data1)[6] <- 'Species'  #修改列名
data1$time <- factor(data1$time, levels = df$time[1:6])

#####按照分组time绘制未分面柱状堆积图
##计算分组time的均值
df_time <- data1 %>%
  select(time,Species,value) %>%
  group_by(time,Species) %>% 
  summarise_all(mean)# 求均值
##绘图
ggplot(df_time, aes(time, y = value*100,
                    fill = Species,
                    stratum = Species, alluvium = Species))+
  #柱状堆积图+柱间连线
  geom_stratum(width = 0.6, color='white')+
  geom_alluvium(alpha = 0.4,#透明度
                width = 0.6,#宽度
                color='white',#间隔颜色
                linewidth = 1,#间隔宽度
                curve_type = "linear")+
  ##主题相关设置
  scale_y_continuous(expand = c(0,0))+
  labs(y="Relative Abundance(%)")+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.y = element_text(size=10),
        axis.text.x = element_text(size=10, angle = 45, vjust = 1, hjust = 1),
        axis.title = element_text(size=12))+
  guides(fill=guide_legend(keywidth = 1.2, keyheight = 1.2)) +
  #颜色设置
  scale_fill_manual(values = c("#fc636b","#3be8b0","#1aafd0",
                               "#6a67ce","#ffb900"))

#####绘制按照分组time并按照group1进行分面柱状堆积图
df_time_group1 <- data1 %>%
  select(group1,time,Species,value) %>%
  group_by(group1,time,Species) %>% 
  summarise_all(mean)# 求均值
##绘图
ggplot(df_time_group1, aes(time, y = value*100,
                    fill = Species,
                    stratum = Species, alluvium = Species))+
  geom_stratum(width = 0.6, color='white')+
  geom_alluvium(alpha = 0.4,
                width = 0.6,
                color='white',
                linewidth = 1,
                curve_type = "linear")+
  scale_y_continuous(expand = c(0,0))+
  #分面
  facet_grid(~group1)+
  labs(y="Relative Abundance(%)")+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.y = element_text(size=10),
        axis.text.x = element_text(size=10, angle = 45, vjust = 1, hjust = 1),
        axis.title = element_text(size=12),
        strip.text = element_text(color = "black", size = 12),
        strip.background = element_rect(color = "black", fill="grey90"))+
  guides(fill=guide_legend(keywidth = 1.2, keyheight = 1.2)) +
  scale_fill_manual(values = c("#fc636b","#3be8b0","#1aafd0",
                               "#6a67ce","#ffb900"))

#####绘制按照分组time并按照group1+group2进行分面柱状堆积图
df_time_group12 <- data1 %>%
  select(group1,group2,time,Species,value) %>%
  group_by(group1,group2,time,Species) %>% 
  summarise_all(mean)# 求均值
##绘图
ggplot(df_time_group12, aes(time, y = value*100,
                           fill = Species,
                           stratum = Species, alluvium = Species))+
  geom_stratum(width = 0.6, color='white')+
  geom_alluvium(alpha = 0.4,
                width = 0.6,
                color='white',
                linewidth = 1,
                curve_type = "linear")+
  scale_y_continuous(expand = c(0,0))+
  #分面（facet_nested函数可以解决多因子分面过程中分面标签的不同框问题）
  facet_nested(~group1+group2,scales = "free",space = "free")+
  labs(y="Relative Abundance(%)")+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.y = element_text(size=10),
        axis.text.x = element_text(size=10, angle = 45, vjust = 1, hjust = 1),
        axis.title = element_text(size=12),
        strip.text = element_text(color = "black", size = 12),
        strip.background = element_rect(color = "black", fill="grey90"))+
  guides(fill=guide_legend(keywidth = 1.2, keyheight = 1.2)) +
  scale_fill_manual(values = c("#fc636b","#3be8b0","#1aafd0",
                               "#6a67ce","#ffb900"))


#####绘制按照分组time并按照group1+group2+group3进行分面柱状堆积图
df_time_group123 <- data1 %>%
  select(group1,group2,group3,time,Species,value) %>%
  group_by(group1,group2,group3,time,Species) %>% 
  summarise_all(mean)# 求均值
##绘图
ggplot(df_time_group123, aes(time, y = value*100,
                            fill = Species,
                            stratum = Species, alluvium = Species))+
  geom_stratum(width = 0.6, color='white')+
  geom_alluvium(alpha = 0.4,
                width = 0.6,
                color='white',
                linewidth = 1,
                curve_type = "linear")+
  scale_y_continuous(expand = c(0,0))+
  #分面
  facet_nested(~group1+group2+group3,scales = "free",space = "free")+
  labs(y="Relative Abundance(%)")+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.y = element_text(size=9),
        axis.text.x = element_text(size=9, angle = 45, vjust = 1, hjust = 1),
        axis.title = element_text(size=12),
        strip.text = element_text(color = "black", size = 10),
        strip.background = element_rect(color = "black", fill="grey90"),
        panel.spacing = unit(0.1, "cm"))+
  guides(fill=guide_legend(keywidth = 1.2, keyheight = 1.2)) +
  scale_fill_manual(values = c("#fc636b","#3be8b0","#1aafd0",
                               "#6a67ce","#ffb900"))

```


---

### 柱状图+散点+配对连线+显著性

```r

rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/柱状图+散点+配对连线+显著性")
#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggsignif) # Significance Brackets for 'ggplot2'
library(ggpubr) # 'ggplot2' Based Publication Ready Plots

#加载数据
df <- read.table("data.txt",header = 1,check.names = F,sep = "\t")
df$group1 <- factor(df$group1,levels = c("mCherry","hM3Dq","Cherry","M3Dq"))
df$group2 <- factor(df$group2,levels = c("Saline","CNO"))
#绘图
ggplot(df,aes(group2,value))+
  #误差线
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.15,size=0.8)+
  #柱状图
  geom_bar(aes(fill=group3),color="black",stat="summary",fun=mean,position="dodge",width = 0.7)+
  #配对连线
  geom_line(aes(group=paired),color="grey30",linewidth=0.8)+
  #散点
  geom_point(fill="black",size=3,color="grey",shape=21)+
  #分面
  facet_grid(~group1,scales = 'free_x',space = "free")+
  #显著性
  geom_signif(comparisons = list(c("Saline","CNO")),
              map_signif_level=T, y_position = 170, 
              tip_length = c(c(0.05,0.05),c(0.05,0.05)),
              size=1, textsize = 6, test = "t.test")+
  #y轴范围
  scale_y_continuous(limits = c(0,200),expand = c(0,0))+
  #主题
  theme_classic()+
  theme(legend.position = "none",
        strip.background = element_blank(),
        strip.text = element_text(color = "black",size = 16),
        axis.text.x = element_text(color = "black", angle = 90,vjust = 0.5,hjust = 1,size = 15),
        axis.text.y = element_text(color = "black",size = 15),
        axis.line = element_line(size = 1),
        axis.ticks = element_line(color = "black",size = 1),
        axis.title = element_text(color = "black",size = 18),
        axis.ticks.length.x = unit(0.2, "cm"))+
  #轴标题
  labs(x=NULL,y="Investigation duration (s)")+
  #颜色
  scale_fill_manual(values = c("#84bd00","#efdf00","#fe5000","#e4002b",
                               "#da1884","#a51890","#0077c8","#008eaa"))

```


---

### 柱状图+散点图+折线图

```r

#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/柱状图+散点图+折线图")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(tidyr) # Tidy Messy Data
library(dplyr) # A Grammar of Data Manipulation
library(ggsignif) # Significance Brackets for 'ggplot2'

#数据——ggplot自带的ToothGrowth数据
df <- ToothGrowth
df$dose <- as.factor(df$dose)
data <- df
#计算均值及标准差
df1 <- data%>% group_by(dose)%>%
  summarise(mean= mean(len), sd= sd(len))
#绘图
ggplot()+ 
  #柱状图绘制
  geom_bar(df1,mapping=aes(x=dose,y=mean), fill = "white",
           size = 1.5,color = c("#d20962","#f47721","#7ac143"),position="dodge",
           stat="identity",width = 0.6)+
  #误差线
  geom_errorbar(df1,mapping=aes(x = dose,ymin = mean-sd, ymax = mean+sd),
                width = 0.3,color = c("#d20962","#f47721","#7ac143"), size=1.5)+
  #散点图
  geom_jitter(df, mapping=aes(x=dose,y=len,fill = dose,color = dose,shape = dose),
              size = 2.5,width = 0.2,alpha=0.9)+ 
  #折线图
  geom_line(df1,mapping=aes(x=dose,y=mean,group=1),
            size=1,color="#00aee6")+
  #为折线图添加数据点
  geom_point(df1,mapping=aes(x=dose,y=mean),color="black",size=3,shape=8)+
  #自定义颜色
  scale_color_manual(values = c("#d20962","#f47721","#7ac143"))+ 
  #显著性
  geom_signif(df,mapping=aes(x=dose,y=len), 
              comparisons = list(c("0.5", "1"),
                                 c("1","2"),
                                 c("0.5","2")),
              map_signif_level=T, 
              tip_length=c(0,0,0,0,0,0), 
              y_position = c(35,40,45), 
              size=1, textsize = 7, 
              test = "t.test")+
  #y轴范围
  scale_y_continuous(expand = c(0, 0), limit = c(0, 50))+
  #主题设置
  theme_classic(base_line_size = 1)+
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='black',size=13,face = "bold"),
        axis.title.y = element_text(color='black',size=15,face = "bold"),
        legend.text = element_text(color='black',size=13,face = "bold"),
        legend.title = element_blank(),
        legend.position = "none")+
  #轴标题
  labs(x=NULL,y="Value")

```


---

### 并列柱状堆积图+误差线+显著性

```r

#########微信公众号：科研后花园
######推文题目：跟着Nature Communications学绘图—并列柱状堆积图+误差线+显著性！！！

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/并列柱状堆积图+误差线+显著性')#设置工作路径

##加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(dplyr) # A Grammar of Data Manipulation
library(rstatix) # Pipe-Friendly Framework for Basic Statistical Tests
library(ggpubr) # 'ggplot2' Based Publication Ready Plots

##加载数据
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")

##计算均值及误差，并按照均值确定误差线位置
df %>% 
  group_by(X, Period, Group) %>% 
  summarise(mean=mean(value),sd=sd(value,na.rm = T)) %>% 
  mutate(ep=cumsum(mean))-> df1
#保证误差线可以对应其正确位置
df1$Group <- factor(df1$Group, levels = c("group4","group3","group2","group1"))

##根据分类变量将其转变为数值型变量
#“A”“B”“C”“D”中间各隔开一个数值,根据个人需要确立间隔即可
df1$X2 <- ifelse(df1$X=="A"&df1$Period=="T1", 1,
                 ifelse(df1$X=="A"&df1$Period=="T2", 2,
                        ifelse(df1$X=="B"&df1$Period=="T1", 3.5,
                               ifelse(df1$X=="B"&df1$Period=="T2", 4.5,
                                      ifelse(df1$X=="C"&df1$Period=="T1", 6,7)))))

##计算显著性
df_sig <- df %>% 
  group_by(X) %>%
  wilcox_test(value ~ Period) %>% 
  adjust_pvalue() %>% 
  add_significance("p.adj") %>% 
  add_xy_position(x = "X")

##根据数据调整标签位置
#y轴位置
df_sig$y.position <- ifelse(df_sig$X=="A", max(df1[df1$X=="A",]$ep)+15,#这里的数值需要根据df1数据中的ep列各组最大值进行确定
                            ifelse(df_sig$X=="B", max(df1[df1$X=="B",]$ep)+15, 
                                   max(df1[df1$X=="C",]$ep)+15))
#x轴位置,根据此前添加数值型数据添加
df_sig$xmin <- ifelse(df_sig$X=="A", 1,
                      ifelse(df_sig$X=="B", 3.5, 6))
df_sig$xmax <- ifelse(df_sig$X=="A", 2,
                      ifelse(df_sig$X=="B", 4.5, 7))

##绘图
df1 %>% 
  ggplot()+
  #绘制柱状堆积图
  geom_col(aes(X2, mean, fill = Group), position = 'stack', 
           width = 1, color = "black",alpha = 0.8)+
  #添加误差线
  geom_errorbar(aes(X2, ymin=ep-sd,ymax=ep+sd),
                width=0.1,color = "black",linewidth = 0.6)+
  #自定义X轴标签
  scale_x_continuous(breaks = c(1,2,3.5,4.5,6,7),
                     labels = c("T1","T2","T1","T2","T1","T2"),
                     limits = c(0.5,7.5))+
  #确定y轴范围
  scale_y_continuous(expand = c(0,0), limits = c(0,190))+
  #主题相关设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        legend.position = "right",
        legend.background = element_blank(),
        axis.text = element_text(size=12),
        axis.title = element_text(size=15),
        legend.title = element_text(color = 'red',size=15),
        legend.text = element_text(color = 'black',size=11))+
  #图例设置
  guides(fill=guide_legend(ncol = 1, byrow = F,reverse = T,
                           keywidth=1, keyheight=3))+
  labs(x="Period",y="mean")+
  #自定义颜色
  scale_fill_manual(values = c("#ff3c41","#fcd000","#47cf73","#76daff"))+
  #根据计算的显著性数据添加显著性标签
  stat_pvalue_manual(df_sig[1,],label = "p.adj.signif",
                     label.size = 5.5, linetype = 2,
                     tip.length = c(0.55,0.05))+
  stat_pvalue_manual(df_sig[2,],label = "p.adj.signif",
                     label.size = 6, linetype = 2,
                     tip.length = c(0.05,0.15))+
  stat_pvalue_manual(df_sig[3,],label = "p.adj.signif",
                     label.size = 6, linetype = 2,
                     tip.length = c(0.05,0.6))+
  ##添加大的分组注释
  geom_segment(aes(x=1,xend=2,y=170,yend=170),
               color="black",linewidth=0.8)+
  annotate("text", x = 1.5, y = 180, label = "A", size=6, color = "#c68143")+
  geom_segment(aes(x=3.5,xend=4.5,y=170,yend=170),
               color="black",linewidth=0.8)+
  annotate("text", x = 4, y = 180, label = "B", size=6, color = "#c68143")+
  geom_segment(aes(x=6,xend=7,y=170,yend=170),
               color="black",linewidth=0.8)+
  annotate("text", x = 6.5, y = 180, label = "C", size=6, color = "#c68143")

```


---

### 带误差线的柱状堆积图

```r

rm(list=ls())#clear Global Environment
#加载包
library(ggplot2)
library(reshape2)

# 创建示例数据
df <- data.frame(
  group = c("A", "B", "C","D","F"),
  value1 = c(10, 20, 30, 20, 15),
  value2 = c(15, 25, 35, 15, 20)
)
df1 <- melt(df)
#添加误差数据
df1$sd <- c(1,2,3,2.5,1,1,2,3,2,1.5)
#误差线位置
df1 <- df1 %>% 
  group_by(group) %>% 
  mutate(xx=cumsum(value))
df1$variable <- factor(df1$variable,levels = c("value2","value1"))#保证误差线可以对应其正确位置
# 绘制堆积柱状图
ggplot(df1, aes( x = group,y=value,fill = variable))+
  geom_col(position = 'stack', width = 0.6)+
  geom_errorbar(aes(ymin=xx-sd,ymax=xx+sd),
                width=0.1,linewidth=0.8)+
  scale_y_continuous(expand = c(0,0),limits = c(0,70))+
  labs(x=NULL,y=NULL)+
  theme_bw()+
  theme(panel.grid = element_blank(),
        legend.position = c(0.92,0.88),
        legend.background = element_blank())+
  scale_fill_manual(values = c("#0099cc","#ff9933"))

```


---

### 绝对量柱状堆积图+环形图数量统计+特数量标注

```r

#设置工作环境
rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/绝对量柱状堆积图+环形图数量统计+特数量标注")

##加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(formattable) # Create 'Formattable' Data Structures

##加载数据（随机编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")
df$group <- factor(df$group, levels = df$group[1:10])
##绘图
#绘制绝对量的柱状堆积图
p1 <- ggplot(df, aes(sample, value, fill = group))+
  #绘制柱状堆积图
  geom_col(width = 0.6, color = ifelse(df$`Special marking`==1, 
                                       "black", "transparent"),
           linetype = ifelse(df$`Special marking`==1, 2, 0))+
  #轴标题
  labs(y = "Absolute quantity value", x = NULL, fill = NULL)+
  #y轴范围
  scale_y_continuous(expand = c(0,0), limits = c(0, 320), 
                     breaks = c(50,100,150,200,250,300))+
  #主题相关设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.x = element_text(size = 10, color = "black", 
                                   angle = 45, vjust = 1, hjust = 1),
        axis.text.y = element_text(size = 10, color = "black"),
        axis.title.y = element_text(size = 12, color = "black"))+
  #自定义颜色
  scale_fill_manual(values = c("#ffaaaa", "#ffc2e5","#ebffac","#c1f1fc","#00c7f2",
                               "#c2ff00", "#ff0092","#ffed00","#ff0000","#cd595a"),
                    guide=guide_legend(keywidth=1, keyheight=1))
p1

#使用aggregate函数计算每个组的值和
data <- aggregate(value ~ group, df, sum)
#计算相对丰度
data$Rel <- data$value/sum(data$value)
#转换为百分比
data$per <- percent (data$Rel,1)
data$group <- factor(df$group, levels = df$group[1:10])
#确定位置
data$ymax<-cumsum(data$Rel)
data$ymin<-c(0,head(data$ymax,n=-1))
data$labelposition<-(data$ymax + data$ymin)/2
#绘制环形图
p2 <- ggplot(data,aes(ymax=ymax,ymin=ymin,
              xmax=3,xmin=2))+
  #通过方块先绘制柱状堆积图
  geom_rect(aes(fill=group))+
  #添加标签
  geom_text(x=2.5,aes(y=labelposition,label=per),size=3, color = "black")+
  #通过拉大x轴范围实现环图绘制
  xlim(1,3)+
  #转换为极坐标
  coord_polar(theta="y")+
  theme_void()+
  theme(legend.position = "none")+
  #自定义颜色
  scale_fill_manual(values = c("#ffaaaa", "#ffc2e5","#ebffac","#c1f1fc","#00c7f2",
                               "#c2ff00", "#ff0092","#ffed00","#ff0000","#cd595a"))
p2

##组合图形
p1 + annotation_custom(grob=ggplotGrob(p2),xmin = 3.5, xmax = 6.5, ymin=150, ymax=320)

```


---

### 嵌套柱状图+显著性+字母标记

```r

#########微信公众号：科研后花园
######推文题目：嵌套柱状图+显著性+字母标记！！！

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/嵌套柱状图+显著性+字母标记')#设置工作路径

##加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(agricolae) # Statistical Procedures for Agricultural Research
library(ggpubr) # 'ggplot2' Based Publication Ready Plots
library(dplyr) # A Grammar of Data Manipulation
library(rstatix) # Pipe-Friendly Framework for Basic Statistical Tests

##加载数据(随机编写，无实际意义)
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")

##计算各Group的value1差异-多重比较
#方差分析
variance<-aov(value1 ~ Group, data=df)
# LSD法
MC <- LSD.test(variance,"Group", p.adj="bonferroni")
data_sg1 <- MC$groups
data_sg1$Group <- rownames(data_sg1)

##计算Group内各时期（Period）value2的差异
data_sig2 <- df %>% 
  group_by(Group) %>%
  wilcox_test(value2 ~ Period) %>% #选择wilcox方法
  adjust_pvalue() %>% #校正p值
  add_significance("p.adj") %>% 
  add_xy_position(x = "Group")#确定x与y位置

##绘图模板
ggplot(df, aes(x = Group))+
  ##绘制外围柱状图的误差线及柱子-利用value1
  stat_summary(aes(y = value1), fun.data = 'mean_sd', 
               geom = "errorbar", width = 0.15,size=0.6)+
  geom_bar(aes(y = value1), fill = "#33cc99", color="black",stat="summary",fun=mean,
           position="dodge",size=0.5,width = 0.8)+
  #添加外围柱状图的显著性——字母标记，data_sg1中储存的结果
  geom_text(data = data_sg1, aes(Group, value1+20, label = groups),olor = "black", size=6, fontface="bold")+
  ##绘制嵌套的并列柱状图的误差线及柱子-利用value2
  stat_summary(aes(y = value2, fill = Period), fun.data = 'mean_sd', 
               geom = "errorbar", width = 0.15,size=0.6,
               position = position_dodge(0.8))+
  geom_bar(aes(y = value2, fill = Period), color="black",stat="summary",
           fun=mean, position = position_dodge(0.8),size=0.5, width = 0.8)+
  #添加嵌套的并列柱状图的显著性——*号显示，data_sg2中储存的结果
  stat_pvalue_manual(data_sig2,label = "p.adj.signif",
                     label.size = 6, linetype = 1,tip.length = 0,bracket.nudge.y=-6,bracket.size=0.6)+
  #自定义颜色
  scale_fill_manual(values = c("#e95f5c","#ffc168"))+
  #自定义y轴范围
  scale_y_continuous(expand = c(0,0), limits = c(0,190), breaks = seq(0,190,25))+
  #主题相关设置
  labs(x=NULL,y="This is y-axis")+
  theme_bw()+
  theme(panel.grid = element_blank(),
        legend.position = "right",
        legend.background = element_blank(),
        axis.text = element_text(size=12),
        axis.text.x = element_text(angle = 45, vjust = 1, hjust = 1),
        axis.title = element_text(size=15),
        legend.title = element_text(color = 'red',size=15),
        legend.text = element_text(color = 'black',size=11))

```


---

### 环形水平条形图+柱状堆积图

```r

#########微信公众号：科研后花园
######推文题目：环形水平条形图+柱状堆积图的绘制方法！！！

##清除环境并设置工作目录
rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/水平环形条形图+柱状堆积图")

##加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(dplyr) # A Grammar of Data Manipulation
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(plyr) # Tools for Splitting, Applying and Combining Data

##加载数据（随机编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")

###绘制环形水平条形图
##根据value1进行绘制，先将数据按照由小到大进行排序（可视化效果为数据最大柱子的在最外层）
df2 <- df[order(abs(df$value1),decreasing=F),]
##为了达到随意调节环形图内层圈的大小，需要根据排序的sample列增加一列数值型数据
df2$x <- 1:9
##绘图
df2 %>% 
  ggplot(aes(x, value1))+#这里将增加的数值列作为x轴
  #绘制条形图，并按照group进行着色
  geom_col(aes(fill = group))+
  #转换为极坐标
  coord_polar(theta = 'y')+
  #自定义x轴，通过将范围中的最小值设为负数以实现环形内部空白圈大小的目的
  scale_x_continuous(limits = c(-2,9.5))+
  #自定义y轴，通过将范围中的最大值设为大于数据中的最大值以实现环形中水平条形图是否首位相接及首位间的距离
  scale_y_continuous(limits = c(0,130))+
  #添加sample文本
  geom_text(aes(x = x, y = 0, label = sample, color = group),
            hjust = 1, size = 3.5, show.legend = F)+
  #添加各条形图的数值标注
  geom_text(aes(x = x, y = ifelse(x>4, value1+1, value1+3), 
                label = value1, color = group),
            size = 3.5, show.legend = F)+
  #将主题设置为空白,图例放置在空白处
  theme_void()+
  theme(legend.position = c(0.2,0.78),
        legend.text = element_text(size = 10),
        legend.title = element_text(size = 14, color = "red"))+
  guides(fill=guide_legend(ncol = 1, keywidth=1.5, keyheight=1.2))+
  #自定义分组颜色
  scale_fill_manual(values = c("#ec1c24","#fdbd10","#0066b2","#ed7902"))+
  scale_color_manual(values = c("#ec1c24","#fdbd10","#0066b2","#ed7902"))


###绘制环形水平柱状堆积图
##先将宽数据转换为长数据
df3 <- melt(df, id.vars = c("sample","group"), 
            measure.vars = c('value1','value2','value3',
                             'value4','value5'))
df3$group <- factor(df3$group,levels = c("groupA","groupB","groupC","groupD"))
##排序，此时需要根据原始数据计算各样本值和（根据个人需求制定排序方式），并按照值和进行排序：
df4 <- df3 %>%
  select(sample,value) %>%
  group_by(sample) %>% 
  summarise_all(sum)
df4 <- df4[order(abs(df4$value),decreasing=F),]
##为了达到随意调节环形图内层圈的大小，同样需要根据排序的sample列增加一列数值型数据
df4$x <- 1:9
##将绘图数据按照得到的排序顺序进行排序
df3$sample <- factor(df3$sample,levels = df4$sample)
##将数值型列按照sample匹配进作图数据
df3 <- left_join(df3, df4[c(1,3)], by = "sample")
##绘图
df3 %>% 
  ggplot(aes(x, value))+#这里将增加的数值列作为x轴
  #绘制柱状堆积图，并按照variable进行着色
  geom_col(aes(fill = variable))+
  #转换为极坐标
  coord_polar(theta = 'y')+
  #自定义x轴，通过将范围中的最小值设为负数以实现环形内部空白圈大小的目的
  scale_x_continuous(limits = c(-2,9.5))+
  #自定义y轴，通过将范围中的最大值设为大于数据中的样本和最大值以实现环形中水平条形图是否首位相接及首位间的距离
  scale_y_continuous(limits = c(0,500))+
  #添加sample文本
  geom_text(data = df4, aes(x = x, y = 0, label = sample),
            hjust = 1, size = 3.5, show.legend = F)+
  #将主题设置为空白,图例放置在空白处
  theme_void()+
  theme(legend.position = c(0.2,0.78),
        legend.text = element_text(size = 10),
        legend.title = element_text(size = 14, color = "red"))+
  guides(fill=guide_legend(ncol = 1, keywidth=1.3, keyheight=1))+
  #自定义分组颜色
  scale_fill_manual(values = c("#ec1c24","#fdbd10","#0066b2","#ed7902","#acc236"))

###当然，也可以绘制环形水平百分比柱状堆积图
##计算各样本中的百分比情况
df5 <- ddply(df3, 'sample', transform, percent_con = value/sum(value)*100)
##绘图
df5 %>% 
  ggplot(aes(x, percent_con))+#这里将增加的数值列作为x轴
  #绘制柱状堆积图，并按照variable进行着色
  geom_col(aes(fill = variable))+
  #转换为极坐标
  coord_polar(theta = 'y')+
  #自定义x轴，通过将范围中的最小值设为负数以实现环形内部空白圈大小的目的
  scale_x_continuous(limits = c(-2,9.5))+
  #自定义y轴，百分比柱状堆积图y轴范围为（0，100）（%），这里将范围设为大于100即可实现
  scale_y_continuous(limits = c(0,130))+
  #添加sample文本
  geom_text(data = df4, aes(x = x, y = 0, label = sample),
            hjust = 1, size = 3.5, show.legend = F)+
  #将主题设置为空白,图例放置在空白处
  theme_void()+
  theme(legend.position = c(0.2,0.78),
        legend.text = element_text(size = 10),
        legend.title = element_text(size = 14, color = "red"))+
  guides(fill=guide_legend(ncol = 1, keywidth=1.3, keyheight=1))+
  #自定义分组颜色
  scale_fill_manual(values = c("#ec1c24","#fdbd10","#0066b2","#ed7902","#acc236"))

```


---

### 环状柱状图

```r

#设置工作环境
rm(list=ls())
setwd("D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\环状柱形图")

#加载R包
library(tidyverse)
library(reshape2)
library(ggplot2)
library(ggprism)

#加载数据
df <- read.table("data.txt",header = T, check.names = F)
#转换数据
data=melt(df)
data$G<-rep(c("T","F","H"), each = 24)
data_label <- data
data_label$ID <- as.numeric(rownames(data_label))

#####绘图————无分组情况
#计算标签角度
number_of_bar <- nrow(data_label)
angle <-  90 - 360 * (data_label$ID-0.5) /number_of_bar
data_label$hjust<-ifelse(angle < -90, 1, 0)
data_label$angle<-ifelse(angle < -90, angle+180, angle)

#绘图
p1 <- ggplot(data_label, aes(x=ID, y=value))+
  geom_bar(stat="identity", fill="blue", alpha=0.7) +
  ylim(-75,75) +#y轴范围，控制内圆大小与条形大小
  theme_minimal() +#主题
  theme(axis.text = element_blank(),
        axis.title = element_blank(),
        panel.grid = element_blank(),
        plot.margin = unit(rep(-1,4), "cm")) +#调整边缘以使得标签不会被截断
  coord_polar(start = 0) +#极坐标
  geom_text(data=data_label, aes(x=ID, y=value+10, label=variable, hjust=hjust), 
            color="black", fontface="bold",alpha=0.6, size=2.5, 
            angle= data_label$angle, inherit.aes = F) #标签

p1

#####绘图————添加分组并增加分组间隔
#调整柱子显示顺序
data_label = data_label %>% arrange(G, value)
#设置分组间的空白间隔
data_label$G<-as.factor(data_label$G)
number_empty_bar <- 3
to_add <- data.frame(matrix(NA, number_empty_bar*nlevels(as.factor(data_label$G)), ncol(data_label)) )
colnames(to_add) <- colnames(data_label)
to_add$G <- rep(levels(data_label$G), each=number_empty_bar)
data_label <- rbind(data_label, to_add)
data_label <- data_label %>% arrange(G)
data_label$ID <- seq(1, nrow(data_label))
##标签设置
number_of_bar <- nrow(data_label)
angle <-  90 - 360 * (data_label$ID-0.5) /number_of_bar
data_label$hjust<-ifelse(angle < -90, 1, 0)
data_label$angle<-ifelse(angle < -90, angle+180, angle)
#绘图
p2 <- ggplot(data_label, aes(x=ID, y=value, fill=G)) +
  geom_bar(stat="identity", alpha=0.5) +
  ylim(-75,75) +
  theme_minimal() +
  theme(legend.position = "none",
        axis.text = element_blank(),
        axis.title = element_blank(),
        panel.grid = element_blank(),
        plot.margin = unit(rep(-1,4), "cm")) +
  coord_polar() + #极坐标
  geom_text(data=data_label, aes(x=ID, y=value+10, label=variable, hjust=hjust), 
            color="black", fontface="bold",alpha=0.6, size=2.5, 
            angle= angle, inherit.aes = F)+#标签
  scale_fill_prism(palette = "candy_bright")#使用ggprism包修改颜色

p2
####添加分组标签
#创建标签数据及位置
base_data <- data_label %>% 
  group_by(G) %>% 
  summarize(start=min(ID), end=max(ID) - number_empty_bar) %>% 
  rowwise() %>% 
  mutate(title=mean(c(start, end)))
#绘图
p2+geom_segment(data=base_data, aes(x = start, y = -5, xend = end, yend = -5),
                color = "red", alpha=0.8, size=0.8 , inherit.aes = F)+#添加分组线
  geom_text(data=base_data, aes(x = title, y = -18, label=G), 
            hjust=c(1,1,0), colour = "black", alpha=0.8, size=4, 
            fontface="bold", inherit.aes = F)#分组标签

#参考:https://r-graph-gallery.com/297-circular-barplot-with-groups.html

```


---

### 环形柱状图+误差棒+显著性+分组标签+灰白间隔背景+辅助线

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/环形柱状图+误差棒+显著性+分组标签+灰白间隔背景+辅助线')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(dplyr) # A Grammar of Data Manipulation

##加载数据（随机编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")

##将数据根据是否大于0添加分组
df$group3 <- ifelse(df$mean>0, "T", "F")
df$group3 <- factor(df$group3,levels = c("T","F"))


##计算标签角度
df$group1 <- factor(df$group1,levels = c("A","B","C","D","E","F","G","H","I","J"))
df$ID <- as.numeric(rownames(df))##根据行数添加一列数值型数据（1：40）
number_of_bar <- nrow(df)
angle <-  90 - 360 * (df$ID-0.5) /(number_of_bar+4)##+4的目的在于达到间隔分离
df$hjust<-ifelse(angle < -90, 1, 0)
df$angle<-ifelse(angle < -90, angle+180, angle)
#创建标签数据及位置
df2 <- df %>% 
  group_by(group1) %>% 
  summarize(start=min(ID)+4, end=max(ID) - 4) %>% 
  rowwise() %>% 
  mutate(title=mean(c(start, end)))
df2$group1 <- factor(df2$group1,levels = c("A","B","C","D","E","F","G","H","I","J"))
df2$group2 <- c("G1","G1","G2","G2","G3","G4","G4","G5","G5","G6")
#第二组标签
df3 <- df %>% 
  group_by(group2) %>% 
  summarize(start=min(ID)+4, end=max(ID) - 4) %>% 
  rowwise() %>% 
  mutate(title=mean(c(start, end)))
df3$group2 <- factor(df3$group2,levels = c("G1","G2","G3","G4","G5","G6"))

##寻找数据中的最大值与最小值以便后续添加灰白色间隔的柱子
df_bg <- df %>%
  group_by(group1) %>% 
  summarize(max = max(mean),min = min(mean))
##确定灰白色背景宽度及对应颜色标记
df_bg2 <- df %>%
  group_by(group1) %>% 
  summarize(max = max(ID),min = min(ID))
df_bg2$G <- rep(c("g","w"), times=2, len = 10)

##绘制基础柱状图
ggplot(df)+
  #手动添加辅助线(坐标轴)
  geom_linerange(aes(xmin=0.5,xmax=35, y = -10),lty="solid", color = "grey80")+
  geom_linerange(aes(xmin=0.5,xmax=35, y = -5),lty="solid", color = "grey80")+
  geom_linerange(aes(xmin=0.5,xmax=35, y = 0),lty="solid", color = "black")+
  geom_linerange(aes(xmin=0.5,xmax=35, y = 5),lty="solid", color = "grey80")+
  geom_linerange(aes(xmin=0.5,xmax=35, y = 10),lty="solid", color = "grey80")+
  #手动添加坐标及标题
  geom_text(x=0.1,y=-15,label="-15",color="black",size=3)+
  geom_text(x=0.1,y=-10,label="-10",color="black",size=3)+
  geom_text(x=0.1,y=-5,label="-5",color="black",size=3)+
  geom_text(x=0.1,y=0,label="0",color="black",size=3)+
  geom_text(x=0.1,y=5,label="5",color="black",size=3)+
  geom_text(x=0.1,y=10,label="10",color="black",size=3)+
  geom_text(x=0.1,y=15,label="15",color="black",size=3)+
  #根据目标分组添加灰白色间隔背景
  geom_rect(df_bg2,mapping=aes(xmin=min-0.5,xmax=max+0.5,ymin=-15,ymax=15,fill=G),alpha=0.5)+
  #分组数量少也可手动添加
  # annotate("rect", xmin = 0.5, xmax = 5.5, ymin = -15, ymax = 15, fill="grey90", alpha = 0.5)+
  # annotate("rect", xmin = 7.5, xmax = 10.5, ymin = -15, ymax = 15, fill="grey90", alpha = 0.5)+
  # annotate("rect", xmin = 14.5, xmax = 20.5, ymin = -15, ymax = 15, fill="grey90", alpha = 0.5)+
  #柱状图
  geom_col(aes(ID, mean, fill=group3), alpha = 0.6)+
  #添加误差线
  geom_errorbar(mapping=aes(x=ID,ymin=mean-sd,ymax=mean+sd),
                width=0.15,linewidth=0.2)+
  #极坐标转换
  coord_polar(direction=1)+
  #x,y轴范围确定
  scale_y_continuous(limits = c(-23,38))+
  scale_x_continuous(limits = c(0,44))+
  #修改填充颜色
  scale_fill_manual(values = c("T"="red",
                               "F"="blue",
                               "g"="grey90",
                               "w"="white"))+
  #主题
  theme_void()+
  theme(legend.position = 'none')+
  #手动添加显著性
  geom_text(aes(x=ID, y=17, label=sig,
                         hjust=hjust,color=group2),
            fontface="bold", size=4, 
            angle= df$angle, inherit.aes = F)+
  #手动添加第一层标签
  geom_text(aes(x=ID, y=20, label=sample,
                          hjust=hjust,color=group2), 
            fontface="bold", size=3, 
            angle= df$angle, inherit.aes = F)+
  ##分组第二层标签
  geom_text(data=df2, aes(x = title, y = 30, label=group1,color=group2), 
            hjust=c(1,1,1,1,1,0,0,0,0,0), size=4.5,  
            angle=c(340,310,0,0,0,0,-20,0,0,0),#需要根据分组数量及绘制图形的标签角度自己调整
            fontface="bold", inherit.aes = F)+
  ##分组第二层标签
  geom_text(data=df3, aes(x = title, y = 36, label=group2,color=group2),
            size=5.5,  angle=c(330,0,0,0,0,0),#需要根据分组数量及绘制图形的标签角度自己调整
            fontface="bold", inherit.aes = F)+
  #自定义颜色
  scale_color_manual(values = c("#4fbb98","#f46024","#dd6ab0","#aea400","#00ad45","#00aee6"))

```


---

### 环状柱状堆积图+分组+显著性

```r

#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/环状柱状堆积图+分组+显著性")

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(tidyverse) # Easily Install and Load the 'Tidyverse'
#加载数据（随机编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")
df$group <- factor(df$group,levels = c("M","N","G","F"))
##计算标签角度
df2 <- as.data.frame(df[c(1:10,51:62,103:114,155:166,207:208),]) 
rownames(df2) <- 1:48
df2$group <- factor(df2$group,levels = c("M","N","G","F"))
df2$ID <- as.numeric(rownames(df2))
number_of_bar <- nrow(df2)
angle <-  90 - 360 * (df2$ID-0.5) /number_of_bar
df2$hjust<-ifelse(angle < -90, 1, 0)
df2$angle<-ifelse(angle < -90, angle+180, angle)
#确定显著性标签位置
result <- aggregate(value ~ group3, data = df, sum)
#创建标签数据及位置
df3 <- df2 %>% 
  group_by(group) %>% 
  summarize(start=min(ID), end=max(ID) - 4) %>% 
  rowwise() %>% 
  mutate(title=mean(c(start, end)))
df3$group <- factor(df3$group,levels = c("M","N","G","F"))
#绘图
ggplot()+
  #手动添加辅助线
  geom_hline(yintercept = 0,lty="solid", color = "black",linewidth=0.6)+
  geom_hline(yintercept = 20,lty="solid", color = "grey80")+
  geom_hline(yintercept = 60,lty="solid", color = "grey80")+
  geom_hline(yintercept = 40,lty="solid", color = "grey80")+
  geom_hline(yintercept = 80,lty="solid", color = "grey80")+
  geom_hline(yintercept = 100,lty="solid", color = "grey80")+
  #柱状堆积图绘制
  geom_col(df, mapping=aes(group3, value, fill = group), color = "grey20", linewidth = 0.5, width = 0.8)+
  #y轴范围确定
  scale_y_continuous(limits = c(-25,150))+
  #颜色
  scale_fill_manual(values = c("#4fbb98","#f46024","#dd6ab0","#7c8ebe"))+
  #主题
  theme_void()+
  theme(legend.position = 'none'
        )+
  #手动添加显著性
  geom_text(data=df2, aes(x=ID, y=103, label=c("Contral", "ADOM", "LHy1","LHA", "LFA","SHy1","SHA","SFA","RHy1","RHA","  "," ",
                                               "Contral", "ADOM", "LHy1","LHA", "LFA","SHy1","SHA","SFA","RHy1","RHA","  ","  ",
                                               "Contral", "ADOM", "LHy1","LHA", "LFA","SHy1","SHA","SFA","RHy1","RHA","  ","  ",
                                               "Contral", "ADOM", "LHy1","LHA", "LFA","SHy1","SHA","SFA","RHy1","RHA","  ","  "),
                          hjust=hjust,color=group), 
             fontface="bold", size=3, 
            angle= df2$angle, inherit.aes = F)+
  #手动添加标签
  geom_text(data=df2, aes(x=ID, y=result$value+4, 
                          label=c("", "", "***","", "","","**","","","","","",
                                  "", "", "**","", "","","","***","","","","",
                                  "", "***", "***","***", "**","***","**","***","**","***","","",
                                  "", "***", "","", "","","","**","**","","",""),
                          color=group), 
             fontface="bold", size=4, 
            angle= df2$angle+90, inherit.aes = F)+ #标签
  #手动添加坐标及标题
  geom_text(data=df2,x=11,y=30, label="Biodegradation rate(%)",color="black",size=3.5)+
  geom_text(data=df2, x=-0.2,y=5,label="0",color="black",size=3)+
  geom_text(data=df2, x=-0.2,y=25,label="20",color="black",size=3)+
  geom_text(data=df2, x=-0.2,y=45,label="40",color="black",size=3)+
  geom_text(data=df2, x=-0.2,y=65,label="60",color="black",size=3)+
  geom_text(data=df2, x=-0.2,y=85,label="80",color="black",size=3)+
  geom_text(data=df2, x=-0.2,y=105,label="100",color="black",size=3)+
  #极坐标转换
  coord_polar(direction=1)+
  ##分组标签
  geom_text(data=df3, aes(x = title, y = 140, label=group,color=group), 
            hjust=c(1,1,0,0), angle=c(335,250,135,60), size=5, 
            fontface="bold", inherit.aes = F)+
  #颜色
  scale_color_manual(values = c("#4fbb98","#f46024","#dd6ab0","#7c8ebe"))

```


---

### 南丁格尔玫瑰图

```r

#设置工作环境
rm(list=ls())
setwd("D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\环状柱形图")

#加载相关R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggthemes) # Extra Themes, Scales and Geoms for 'ggplot2'
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization
#加载数据
df <- read.table("data1.txt",header = T, check.names = F)
#配色
col <- colorRampPalette(brewer.pal(9,"Set1"))(7)
#背景色
color <- colorRampPalette(brewer.pal(11,"BrBG"))(30)
#绘图
ggplot(df, aes(x = sample, y = value, fill = sample)) +
  geom_bar(stat = "identity", color = "white",
           lwd = 1, show.legend = FALSE,width = 0.6)+
  geom_text(aes(y=value+5,label=value,color=sample))+
  scale_fill_manual(values = col)+
  scale_color_manual(values = col)+
  theme_pander()+
  coord_polar()+
  theme(axis.text.y = element_blank(),
        axis.ticks.y =element_blank(),
        axis.text.x = element_text(color='black',size=15),
        legend.position = "none",
        panel.grid.major.x = element_blank())+
  labs(y=NULL,x=NULL)
#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

###根据分组不同进行着色
#绘图
ggplot(df, aes(x = sample, y = value, fill = group)) +
  geom_bar(stat = "identity", color = "white",
           lwd = 1, show.legend = T,width = 0.6)+
  geom_text(aes(y=value+5,label=value,color=group),show.legend = F)+
  scale_fill_manual(values = col)+
  scale_color_manual(values = col)+
  theme_pander()+
  coord_polar()+
  theme(axis.text.y = element_blank(),
        axis.ticks.y =element_blank(),
        axis.text.x = element_text(color='black',size=15),
        legend.position = "right",
        panel.grid.major.x = element_blank())+
  labs(y=NULL,x=NULL)
#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

```


---

### 瀑布图绘制

```r

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

```


---

## 🔵 二、散点图 & 回归拟合

### 分组散点图

```r

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

```


---

### 不同组散点+回归曲线+多项式拟合+线性拟合

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/不同组散点+回归曲线+多项式拟合+线性拟合')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggpmisc) # Miscellaneous Extensions to 'ggplot2'

#读取数据——以Chiplot绘图平台数据为例
df <- read.table("data.txt",sep = "\t",header=1,check.names=FALSE)

######绘图#######
#绘制基础散点图
ggplot(df,aes(x,y))+
  geom_point(aes(fill=group),shape=21,size=3,alpha=0.5)

##为了方便展示，在X=6.25处将图形分割成两部分，并对X<6.25和X>6.25的数据分别添加拟合曲线
#在X=6.25处添加辅助线进区分
ggplot(df,aes(x,y))+
  geom_point(aes(fill=group),shape=21,size=3,alpha=0.5)+
  geom_vline(xintercept = 6.25, linetype = 2, color = "#08538c",linewidth=0.8)
#对X<6.25的散点进行线性拟合
ggplot(df,aes(x,y))+
  geom_point(aes(fill=group),shape=21,size=3,alpha=0.5)+
  geom_vline(xintercept = 6.25, linetype = 2, color = "#08538c",linewidth=0.8)+
  geom_smooth(data = df[df$x<6.25,],
              method = "lm", color = "red", 
              formula = y ~ x,
              linetype=1,alpha=0.5,linewidth = 0.8)
#对X>6.25的散点进行二次拟合
ggplot(df,aes(x,y))+
  geom_point(aes(fill=group),shape=21,size=3,alpha=0.5)+
  geom_vline(xintercept = 6.25, linetype = 2, color = "#08538c",linewidth=0.8)+
  geom_smooth(data = df[df$x<6.25,],
              method = "lm", color = "red", 
              formula = y ~ x,
              linetype=1,alpha=0.5,linewidth = 0.8)+
  geom_smooth(data = df[df$x>6.25,],
              method = "lm", color = "red", 
              formula = y ~ poly(x, 2, raw = TRUE),
              linetype=1,alpha=0.5,linewidth = 0.8)
#分别对两次拟合添加回归方程
ggplot(df,aes(x,y))+
  geom_point(aes(fill=group),shape=21,size=3,alpha=0.5)+
  geom_vline(xintercept = 6.25, linetype = 2, color = "#08538c",linewidth=0.8)+
  geom_smooth(data = df[df$x<6.25,],
              method = "lm", color = "red", 
              formula = y ~ x,
              linetype=1,alpha=0.5,linewidth = 0.8)+
  geom_smooth(data = df[df$x>6.25,],
              method = "lm", color = "red", 
              formula = y ~ poly(x, 2, raw = TRUE),
              linetype=1,alpha=0.5,linewidth = 0.8)+
  stat_poly_eq(data = df[df$x<6.25,],
               formula = y ~ x, 
               aes(label = paste(after_stat(eq.label),
                                 after_stat(adj.rr.label),
                                 sep = "~~~")), 
               parse = TRUE,label.x = "left")+
  stat_poly_eq(data = df[df$x<6.25,],
               formula = y ~ poly(x, 2, raw = TRUE), 
               aes(label = paste(after_stat(eq.label),
                                 after_stat(adj.rr.label),
                                 sep = "~~~")), 
               parse = TRUE,label.x = "right")

####个性化绘图模板
#自定义颜色
col<-c("#ec1c24", "#fdbd10", "#0066b2", "#ed7902")
##绘图
ggplot(df,aes(x,y))+
  #绘制基础散点图
  geom_point(aes(fill=group),shape=21,size=5,alpha=0.7)+
  #在X=6.25处添加辅助线进区分
  geom_vline(xintercept = 6.25, linetype = 2, color = "#08538c",linewidth=0.8)+
  # 对X<6.25的散点进行线性拟合
  geom_smooth(data = df[df$x<6.25,],
              method = "lm", color = "#84754e", 
              formula = y ~ x,
              linetype=1,alpha=0.5,linewidth = 0.8)+
  # 对X>6.25的散点进行线性拟合
  geom_smooth(data = df[df$x>6.25,],
              method = "lm", color = "#bc0024", 
              formula = y ~ poly(x, 2, raw = TRUE),
              linetype=1,alpha=0.5,linewidth = 0.8)+
  # 对X<6.25散点的线性拟合曲线添加回归方程
  stat_poly_eq(data = df[df$x<6.25,],
               formula = y ~ x, 
               aes(label = paste(after_stat(eq.label),
                                 after_stat(adj.rr.label),
                                 sep = "~~~")), 
               parse = TRUE,label.x = 0.05, label.y = 0.95,
               color = "#84754e")+
  # 对X>6.25散点的二次拟合曲线添加回归方程
  stat_poly_eq(data = df[df$x<6.25,],
               formula = y ~ poly(x, 2, raw = TRUE), 
               aes(label = paste(after_stat(eq.label),
                                 after_stat(adj.rr.label),
                                 sep = "~~~")), 
               parse = TRUE,label.x = 0.05, label.y = 0.9,
               color = "#bc0024")+
  #自定义颜色
  scale_fill_manual(values = col)+
  #对主题进行一些修改
  theme_bw()+
  theme(axis.text=element_text(color='black',size=14),
        legend.text = element_text(color='black',size=14),
        axis.title = element_text(color='black',size=15),
        panel.grid = element_blank(),
        legend.title = element_blank(),
        legend.position = c(0.9,0.2))+
  labs(x = "XXXXXXX", y = "XXXXXXX\n(XXXXXXXXXXXXX)", fill = NULL)+
  scale_x_continuous(expand = c(0,0))

#保存图片
ggsave(filename = "test.png", #文件名称及其类型，一般通过改变后缀生成相应格式的图片
       width = 7,#宽
       height = 6, #高
       units = "in",#单位
       dpi = 300)#设置分辨率

```


---

### 不一样的点线图

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/不一样的点线图')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics

#加载数据
df <- read.table("data.txt",header = 1,check.names = F,sep="\t")
df$group <- factor(df$group,levels = c("all","WB","PL","IT","IR","AJ","IN","CH","CB","NG"))

#绘图
ggplot(df,aes(sample,value,color=group,group=group))+
  #绘制实线部分的折线
  geom_line(data = df[df$sample==1|df$sample==2|df$sample==3|
                        df$sample==4|df$sample==5,],linewidth=0.5)+
  #绘制虚线部分的折线
  geom_line(data = df[df$sample==5|df$sample==6.5|df$sample==8,],
            linewidth=0.5,linetype=2)+
  #绘制散点
  geom_point(data = df[df$sample==6.5|df$sample==8,],size=1.5)+
  #调整并更改X轴标签
  scale_x_continuous(breaks = c(1,2,3,4,5,6.5,8), labels = c("PCA\n(J=1)","PCA\n(J=5)","PCA\n(J=10)",
                                                 "PCA\n(J=15)","PCA\n(J=20)","GRM\n(PCA SNPs)","GRM\n(PGS SNPs)"))+
  #Y轴范围及标签
  scale_y_continuous(breaks = seq(0, 1, len = 5),limits = c(0,1))+
  #主题
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.x = element_text(color = "black", size = 11),
        axis.text.y = element_text(color = "black",size = 11),
        axis.title = element_text(color = "black",size = 15),
        legend.position = "right",
        legend.title = element_text(color = "black",size = 14),
        legend.text = element_text(color = "black",size = 12))+
  #标题设置
  labs(x="Genetic distance from training data",
       y="UKBB: -cor("*r[i]^2~","~d[i]*")",
       color="ancestry")+
  #颜色
  scale_color_manual(values = c("#000000","#989898","#781a18","#029c6f",
                                "#55b4e4","#d174a8","#e19e09","#dd5b00",
                                "#8562bf","#2d50d9"))

```


---

### 散点+多辅助线+特定区域颜色及标签标记

```r

rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点+多辅助线+特定区域颜色及标签标记")

##加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggrepel) # Automatically Position Non-Overlapping Text Labels with'

##加载数据（随机编写，无实际意义，具体应用场景根据个人数据进行数据分析，这里不做展示）
df <- read.table("data.txt",sep="\t",header = T, check.names = F)

##根据预设辅助线位置及划定区域添加分组信息
df$G <- ifelse(abs(df$x)>=30|abs(df$y)>=30, "Y","N")
#也可以给不同区域划定不同分组
df$G2 <- ifelse(df$x>=30&abs(df$y)<=30, "g1", ifelse(df$x<=-30&abs(df$y)<=30, "g2", ifelse(abs(df$x<=30)&df$y>=30, "g3",ifelse(abs(df$x<=30)&df$y<=-30,"g4", "g5"))))

##根据预设条件为符合的数据添加标签
df$label <- ifelse(abs(df$x)>=40|abs(df$y)>=40, df$sample,"")


##绘图——区域指定统一颜色
p1 <- ggplot(df, aes(x,y))+
  #添加辅助线
  geom_vline(xintercept = 30, lty="dashed", color = "grey50", linewidth = 0.8)+
  geom_vline(xintercept = -30, lty="dashed", color = "grey50", linewidth = 0.8)+
  geom_hline(yintercept = 30, lty="dashed", color = "grey50", linewidth = 0.8)+
  geom_hline(yintercept = -30, lty="dashed", color = "grey50", linewidth = 0.8)+
  #绘制散点图
  geom_point(aes(color = G), shape = 16, size = 4, alpha = 0.8)+
  scale_color_manual(values = c("grey80","#ea4c89"))+
  labs(x = "xxxxxxxxxxx\nxxxxxxx", y = "XXXXXXXXXXXXX\nXXXXXX")+
  #主题相关设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        legend.position = "none")+
  #为特定区域统一添加颜色
  annotate("rect", xmin = -Inf, xmax = -30, ymin = -30, ymax = 30, alpha = 0.2,fill="#ea4c89")+
  annotate("rect", xmin = 30, xmax = Inf, ymin = -30, ymax = 30, alpha = 0.2,fill="#ea4c89")+
  annotate("rect", xmin = -30, xmax = 30, ymin = -Inf, ymax = -30, alpha = 0.2,fill="#ea4c89")+
  annotate("rect", xmin = -30, xmax = 30, ymin = 30, ymax = Inf, alpha = 0.2,fill="#ea4c89")+
  #添加显著性标签
  geom_text_repel(aes(label = label),
                  color="#ea4c89",
                  max.overlaps = 10000,
                  size=4,
                  box.padding=unit(0.8,'lines'),
                  point.padding=unit(0.8, 'lines'),
                  segment.color='black',
                  show.legend=FALSE)
p1

##绘图——区域指定不同颜色
p2 <- ggplot(df, aes(x,y))+
  #添加辅助线
  geom_vline(xintercept = 30, lty="dashed", color = "grey50", linewidth = 0.8)+
  geom_vline(xintercept = -30, lty="dashed", color = "grey50", linewidth = 0.8)+
  geom_hline(yintercept = 30, lty="dashed", color = "grey50", linewidth = 0.8)+
  geom_hline(yintercept = -30, lty="dashed", color = "grey50", linewidth = 0.8)+
  #绘制散点图
  geom_point(aes(color = G2), shape = 16, size = 4, alpha = 0.8)+
  scale_color_manual(values = c("g5"="grey80",
                                "g2"="#4dc9f6",
                                "g1"="#f67019",
                                "g4"="#f53794",
                                "g3"="#acc236"))+
  labs(x = "xxxxxxxxxxx\nxxxxxxx", y = "XXXXXXXXXXXXX\nXXXXXX", color=NULL)+
  #主题相关设置
  theme_bw()+
  theme(panel.grid = element_blank())+
  #为特定区域统一添加颜色
  annotate("rect", xmin = -Inf, xmax = -30, ymin = -30, ymax = 30, alpha = 0.2, fill="#4dc9f6")+
  annotate("rect", xmin = 30, xmax = Inf, ymin = -30, ymax = 30, alpha = 0.2, fill="#f67019")+
  annotate("rect", xmin = -30, xmax = 30, ymin = -Inf, ymax = -30, alpha = 0.2, fill="#f53794")+
  annotate("rect", xmin = -30, xmax = 30, ymin = 30, ymax = Inf, alpha = 0.2, fill="#acc236")+
  #添加显著性标签
  geom_text_repel(aes(label = label,color=G2),
                  max.overlaps = 10000,
                  size=4,
                  box.padding=unit(0.8,'lines'),
                  point.padding=unit(0.8, 'lines'),
                  segment.color='black',
                  show.legend=FALSE)+
  #图例大小设置
  guides(color=guide_legend(override.aes = list(size=5,alpha=1)))
p2  

##拼图
cowplot::plot_grid(p1,p2,rel_widths = c(1,1.2),ncol = 2)

```


---

### 散点+分组+置信圈+质心连线

```r

rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点+分组+置信圈+质心连线")

##加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(dplyr) # A Grammar of Data Manipulation

##加载数据——iris数据集
# data(iris)
df <- read.table("iris.txt", header = 1, check.names = F, sep = "\t")


##绘制基础散点图并根据分组着色
p <- ggplot(iris,aes(Sepal.Length,Sepal.Width))+
  geom_point(aes(color=Species))+
  theme_bw()
p

##添加置信圈
p1 <- p+stat_ellipse(aes(fill=Species,color=Species),
                     geom = "polygon", 
                     level = 0.95,#置信度95%
                     linetype=1,linewidth=0.6,alpha=0.2)
p1

##添加质心连线
#按照分组计算均值(质心点)：
mean <- aggregate(df[,1:2], by=list(df$Species), mean)
colnames(mean)[1] <- "Species"
#合并结果
df1 <- merge(df, mean, by = 'Species') #按分组合并均值列
df1
#绘图
p2 <- p1+geom_segment(data = df1, aes(x = Sepal.Length.y, y = Sepal.Width.y,
                                      xend = Sepal.Length.x, yend = Sepal.Width.x, color = Species),
                      alpha = 0.6, show.legend = FALSE)
p2


###个性化绘图模板
##散点
plot1 <- ggplot(iris,aes(Sepal.Length,Sepal.Width))+
  #散点
  geom_point(aes(fill = Species), 
             size = 3, shape = 21, color = "black")+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(size = 10),
        axis.title = element_text(color = "black", size = 12))+
  scale_fill_manual(values = c("#46bc99","#f68d42","#5ec6f2"))

##散点+质心连线
plot2 <- ggplot(iris,aes(Sepal.Length,Sepal.Width))+
  #质心连线
  geom_segment(data = df1, aes(x = Sepal.Length.y, y = Sepal.Width.y,
                               xend = Sepal.Length.x, yend = Sepal.Width.x, 
                               color = Species),
               alpha = 0.8, linewidth = 1, show.legend = FALSE)+
  #散点
  geom_point(aes(fill = Species), 
             size = 3, shape = 21, color = "black")+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(size = 10),
        axis.title = element_text(color = "black", size = 12))+
  scale_color_manual(values = c("#46bc99","#f68d42","#5ec6f2"))+
  scale_fill_manual(values = c("#46bc99","#f68d42","#5ec6f2"))

##散点+置信圈
plot3 <- ggplot(iris,aes(Sepal.Length,Sepal.Width))+
  #散点
  geom_point(aes(fill = Species), 
             size = 3, shape = 21, color = "black")+
  #置信圈
  stat_ellipse(aes(fill=Species,color=Species),
               geom = "polygon", 
               level = 0.95,#置信度95%
               linetype=1,linewidth=0.6,alpha=0.2)+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(size = 10),
        axis.title = element_text(color = "black", size = 12))+
  scale_color_manual(values = c("#46bc99","#f68d42","#5ec6f2"))+
  scale_fill_manual(values = c("#46bc99","#f68d42","#5ec6f2"))

##散点+质心连线+置信圈
plot4 <- ggplot(iris,aes(Sepal.Length,Sepal.Width))+
  #质心连线
  geom_segment(data = df1, aes(x = Sepal.Length.y, y = Sepal.Width.y,
                               xend = Sepal.Length.x, yend = Sepal.Width.x, 
                               color = Species),
               alpha = 0.8, linewidth = 1, show.legend = FALSE)+
  #散点
  geom_point(aes(fill = Species), 
             size = 3, shape = 21, color = "black")+
  #置信圈
  stat_ellipse(aes(fill=Species,color=Species),
               geom = "polygon", 
               level = 0.95,#置信度95%
               linetype=1,linewidth=0.6,alpha=0.2)+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(size = 10),
        axis.title = element_text(color = "black", size = 12))+
  scale_color_manual(values = c("#46bc99","#f68d42","#5ec6f2"))+
  scale_fill_manual(values = c("#46bc99","#f68d42","#5ec6f2"))

##拼图
library(patchwork)
(plot1+plot2)/(plot3+plot4)

```


---

### 散点+分组+size+显著性

```r

rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点+分组+size+显著性")

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(rstatix) # Pipe-Friendly Framework for Basic Statistical Tests

#加载绘图数据（随机编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F)
df$group1 <- factor(df$group1, levels = c("One", "Two", "Three"))
df$group2 <- factor(df$group2, levels = c("1", "2", "3","4", "5", "6"))
df$group3 <- factor(df$group3, levels = c("A", "B"))

#计算显著性
p <- df[df$group1 == "Two", ] %>% 
  wilcox_test(Score ~ group3) %>%
  adjust_pvalue()
p

# # A tibble: 1 × 8
# .y.   group1 group2    n1    n2 statistic        p    p.adj
# <chr> <chr>  <chr>  <int> <int>     <dbl>    <dbl>    <dbl>
#   1 Score A      B         13     9       113 0.000271 0.000271

#绘图
ggplot(df)+
  #散点图
  geom_point(aes(x = group2, y = Score, 
                 color = group3, size = Count))+
  #设置分面
  facet_grid(~group1,
             switch='x')+#switch='x'可将标签位置由顶部移至底部，当switch='y'时，可将位于右边的分面标签移至左边
  #主题设置
  theme_bw()+
  theme(axis.text.x = element_blank(),
        axis.text.y = element_text(color = "black", size = 12),
        axis.title = element_text(color = "black", size = 14),
        axis.ticks.x = element_blank(),
        strip.background = element_blank(),
        strip.text = element_text(color = "black", size = 12),
        panel.grid = element_blank())+
  #调整size范围
  scale_size_continuous(range = c(2, 7), breaks = c(1,3,6))+
  #颜色
  scale_color_manual(values = c("#ff4e00","#01cd74"))+
  #y轴范围及刻度设置
  scale_y_continuous(breaks = c(0,1,2,3,4,5,6,7))+
  #图例
  guides(color=guide_legend(override.aes = list(size=4,alpha=1)))+
  labs(x = NULL, color = NULL)+
  #手动添加显著性
  geom_segment(df[df$group1 == "Two", ], mapping = aes(x = 2, xend = 5, y = 7.5, yend = 7.5),
               color = "black", linewidth = 0.6)+
  geom_text(df[df$group1 == "Two", ], mapping = aes(x = 3.5, y = 8, label = 'p < 0.001'), size =4.5, color="black")

```


---

### 散点+回归曲线+多项式拟合+分组

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点+回归曲线+多项式拟合+分组')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggpmisc) # Miscellaneous Extensions to 'ggplot2'
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization
#读取数据——以Chiplot绘图平台数据为例
df <- read.table("data.txt",sep = "\t",header=1,check.names=FALSE)
df2 <- read.table("data2.txt",sep = "\t",header=1,check.names=FALSE)
######绘图#######
#自定义颜色
col<-c("#be0027", "#cf8d2e")
#构建背景色
color1 <- colorRampPalette(brewer.pal(11,"PiYG"))(30)
color2 <- colorRampPalette(brewer.pal(11,"PuOr"))(30)

##绘图
#三次回归曲线
p <- ggplot(df,aes(x,y,fill=group))+
  geom_point(shape=21,size=3,alpha=0.5)+
  #添加回归曲线并添加置信区间
  geom_smooth(method = "lm",aes(color=group), 
              formula = y ~ poly(x, 3, raw = TRUE),
              linetype=1,alpha=0.5)+
  #添加回归方程
  stat_poly_eq(formula = y ~ poly(x, 3, raw = TRUE), 
               aes(color=group,label = paste(after_stat(eq.label),
                                             after_stat(adj.rr.label),
                                             sep = "~~~")), 
               parse = TRUE,label.x = "left") +
  scale_fill_manual(values = col)+
  scale_color_manual(values = col)+
  theme_bw()+
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='#333c41',size=12),
        legend.text = element_text(color='#333c41',size=12),
        legend.title = element_blank(),
        legend.position = 'none')+
  labs(x=NULL,y=NULL)
p
#二次回归曲线
p2 <- ggplot(df2,aes(x,y,fill=group))+
  geom_point(shape=21,size=3,alpha=0.5)+
  #添加回归曲线并添加置信区间
  geom_smooth(method = "lm",aes(color=group), 
              formula = y ~ poly(x, 2, raw = TRUE),
              linetype=1,alpha=0.5)+
  #添加回归方程
  stat_poly_eq(formula = y ~ poly(x, 2, raw = TRUE), 
               aes(color=group,label = paste(after_stat(eq.label),
                                             after_stat(adj.rr.label),
                                             ..p.value.label..,sep = "~~~")), 
               parse = TRUE,label.x = "right",label.y = "bottom") +
  scale_fill_manual(values = col)+
  scale_color_manual(values = col)+
  theme_bw()+
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='#333c41',size=12),
        legend.text = element_text(color='#333c41',size=12),
        legend.title = element_blank(),
        legend.position = c(0.9,0.9))+
  labs(x=NULL,y=NULL)
p2

#组合图形
cowplot::plot_grid(p,p2,labels = c('A','B'))
#添加背景
grid.raster(alpha(color1, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

```


---

### 散点+回归线+误差线+显著性

```r

rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点+回归线+误差线+显著性")

#加载R包
library(ggplot2)
library(ggpubr)
library(ggpmisc)

#加载数据（随机编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F)
#分别求取size,X和Y的均值
X <- aggregate(X ~ group, df, function(x) c(mean = mean(x), sd = sd(x)))
Y <- aggregate(Y ~ group, df, function(x) c(mean = mean(x), sd = sd(x)))
size <- aggregate(size ~ group, df, function(x) c(mean = mean(x), sd = sd(x)))
# 保留两位小数
X$X <- round(X$X, 2)
Y$Y <- round(Y$Y , 2)
size$size <- round(size$size , 2)
#整理绘图数据
data <- data.frame(
  group=X$group,
  X=X$X[,1],
  X_error=X$X[,2],
  Y=Y$Y[,1],
  Y_error=Y$Y[,2],
  size=size$size[,1]
)

#绘图
ggplot(data, aes(X, Y))+
  #水平方向误差线
  geom_errorbar(aes(xmin=X-X_error,xmax=X+X_error), linewidth = 0.8, width = 0)+
  #垂直方向误差线
  geom_errorbar(aes(ymin=Y-Y_error,ymax=Y+Y_error), linewidth = 0.8, width = 0)+
  #散点
  geom_point(aes(color = group, size = size))+
  #回归线
  geom_smooth(method = "lm", color="red", fill = "red", se=T, 
              formula = y ~ x,
              linetype=1, alpha=0.2)+
  #回归方程及R2、p值
  # stat_cor(method = "pearson",label.x = 17, label.y = 27, size=4.5)+
  stat_poly_eq(formula = y ~ x, 
               aes(label = paste(eq.label,after_stat(adj.rr.label),..p.value.label..,sep = "~~~~")), parse = TRUE,
               size=4.5, label.x = "left")+
  #点大小范围
  scale_size_continuous(range = c(3, 12))+
  #图例
  guides(color=guide_legend(override.aes = list(size=5,alpha=1)),
         size = "none")+
  #标题
  labs(x = "X_lab", y = "Y_lab", color = NULL)+
  #主题
  theme_bw()+
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='black',size=12),
        axis.title = element_text(color='black',size=14),
        legend.position = c(0.92,0.35))+
  #颜色
  scale_color_manual(values = c("#ff0000","#ffed00","#ff0092","#00b2a9",
                                "#00c7f2","#dc5034","#a626aa","green","blue"))

```


---

### 散点+均值+误差棒+字母标记+双刻度标记

```r

rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点+均值+误差棒+字母标记+双刻度标记")

##加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(dplyr) # A Grammar of Data Manipulation
library(gridExtra) # Miscellaneous Functions for "Grid" Graphics
library(agricolae)#实现多重比较的包

##加载数据（随机编写，无实际意义）
df <- read.table("data.txt",sep="\t",header = T, check.names = F)

##计算均值并指定其在x轴上的位置
df %>% 
  group_by(group) %>% 
  summarise(mean_value=mean(value)) %>% 
  bind_cols(x=c(1:5))-> df1

##多重比较
#数据的方差检验
variance<-aov(value ~ group, data=df)
variance
#进行多重比较，不矫正P值
MC <- LSD.test(variance,"group", p.adj="none")#结果显示：标记字母法out$group
GB<- group_by(df,group)#数据转换
error <- summarise(GB,sd(value,na.rm = T))#计算误差
#整理数据
error2 <- merge(error ,MC$group,by.x="group",by.y = "row.names",all = F)#合并数据

##生成X轴替换的刻度表格
df2 <- data.frame(
  " "=c("HFD","PPP"),
  group1=c("-","0"),
  group2=c("-","0.25"),
  group3=c("+","0.5"),
  group4=c("+","0.75"),
  group5=c("+","1")
)
rownames(df2) <- df2$X.
df2 <- df2[-1]
##绘图
p1 <- ggplot(df, aes(group, value))+
  #散点图绘制
  geom_jitter(aes(fill = group), shape = 21, color = "black",
              width = 0.3, size = 3, alpha = 0.4)+
  #根据计算结果添加均值线
  geom_segment(data=df1,aes(x=x-0.2,xend=x+0.2,y=mean_value,yend=mean_value),
               color="grey20",linewidth=0.8)+
  #添加误差棒
  stat_summary(color="grey10",fun.data = "mean_cl_normal",
               geom = "errorbar",
               width = 0.15,size=0.8) +
  #根据多重比较的结果添加字母标记
  geom_text(data=error2, aes(group, value+13, 
                             label=groups, color = group), size = 6)+
  labs(x=NULL, y = "This is y-axis")+
  #颜色设置
  scale_fill_manual(values = c("#00b2a9","#a626aa","#6639b7","#aea400","#ff6319"))+
  scale_color_manual(values = c("#00b2a9","#a626aa","#6639b7","#aea400","#ff6319"))+
  #主题调整
  theme_classic()+
  theme(legend.position = "none",
        axis.text.x = element_blank(),
        axis.line = element_line(linewidth = 0.8),
        axis.ticks = element_line(linewidth = 0.8),
        axis.ticks.x = element_blank(),
        axis.text.y = element_text(size=10, colour = "black"),
        axis.title = element_text(size=12, colour = "black"))
p1

##绘制表格
table <- tableGrob(df2,theme=ttheme_minimal())

##拼图
grid.arrange(p1,table, heights = c(2, 0.45))

###保存
pdf(file='test.pdf', height=4,width=4)#新建一个PDF文件
grid.arrange(p1,table, heights = c(2, 0.45))
dev.off()#关闭PDF

##最后基于AI软件微调图片即可

```


---

### 散点+热图注释

```r

#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点+热图注释")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape) # Flexibly Reshape Data
library(aplot) # Decorate a 'ggplot' with Associated Information
library(dplyr) # A Grammar of Data Manipulation
#加载数据（随机编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")

##绘图
#散点图
p1 <- ggplot(df, aes(value, sample))+
  geom_point(aes(fill = value), shape = 21, color = "black", size = 4, show.legend = F)+
  labs(y = NULL, x = NULL)+
  scale_fill_gradient(high = "red", low = "blue")+
  theme_classic()+
  theme(axis.text = element_text(size = 14, face = "bold",color = "black"))
p1

#热图
#提取数据并转换为作图格式
df2 <- df[c(1,3:5)]
df2 <- melt(df2)
#设置渐变色
col <- colorRampPalette(c("#0066b2","#fdbd10","#ec1c24"))(50) #设置渐变色
p2 <- ggplot(df2,aes(variable,sample,fill=value))+
  #绘制热图
  geom_tile(color="black",alpha = 0.8)+
  #标题
  labs(x=NULL,y=NULL,fill=NULL)+
  #颜色
  scale_fill_gradientn(colours = col)+
  scale_x_discrete(position = "top")+
  #主题
  theme_void()+
  theme(axis.text.x = element_text(color = "black",size=14, angle = 45,
                                   hjust = 0.5, vjust = 0.5, face = "bold"),
        axis.text.y = element_blank(),
        legend.position = "right")#去除图例
p2

#组合图片
p1%>%insert_right(p2,width = 0.3)

```


---

### 散点+折线+局部放大

```r

rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点+折线+局部放大")
#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2)
#加载数据
data <- read.table("data.txt",header = T)
data2 <- data[1:15,]
#生成绘图数据
df <- melt(data,id.vars = "time")
df2 <- melt(data2,id.vars = "time")
#准备配色
col <- c("black", "#c3c0d4",
              "yellow","blue",
              "red","green","#2072A8")

#绘图
p1 <- ggplot(df,aes(time,value,color=variable))+
  geom_line(linewidth=0.5)+
  geom_point(size=1)+
  theme_bw()+
  theme(legend.position = "none",
        axis.title.x=element_text(size=12),
        axis.title.y=element_text(size=12,angle=90),
        axis.text=element_text(size=12,color = "black"),
        panel.grid=element_blank())+
  scale_color_manual(values = col)+
  labs(x="Time(s)")
p1
#绘制子图形
p2 <- ggplot(df2,aes(time,value,color=variable))+
  geom_line(linewidth=0.5)+
  geom_point(size=1)+
  theme_bw()+
  theme(legend.position = c(0.9,0.65),
        legend.title = element_blank(),
        legend.background = element_blank(),
        legend.key.height = unit(0.5, "cm"),
        axis.title.x=element_text(size=12),
        axis.title.y=element_text(size=12,angle=90),
        axis.text=element_text(size=12,color = "black"),
        panel.grid=element_blank(),
        panel.background = element_blank(),
        plot.background = element_blank())+
  scale_color_manual(values = col)+
  labs(x="Time(s)")+
  scale_x_continuous(breaks = seq(0, 30, len = 6))
p2

#组合图形
p1 + annotation_custom(grob=ggplotGrob(p2),ymin = 15, ymax = 100, xmin=35, xmax=100)

##修饰
p1+geom_rect(xmin = -2, xmax = 22, ymin = 0, ymax = 102,
             fill = "transparent", color = "#00bce4", linetype = "dashed",linewidth=0.8)+
  geom_segment(aes(x = 22, y = 60, xend = 35, yend = 60),
               arrow = arrow(length = unit(0.3, "cm"),type="closed"),
               color = "#00bce4",linewidth=0.8)+
  annotation_custom(grob=ggplotGrob(p2),ymin = 15, ymax = 100, xmin=35, xmax=100)

```


---

### 散点+折线+误差棒+面积填充

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点+折线+误差棒+面积填充')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(aplot) # Decorate a 'ggplot' with Associated Information
#加载数据（随机编写，无实际意义）
df <- read.table("data.txt", header = 1, sep = "\t", check.names = F)
df$group <- factor(df$group, levels = c("group1","group2","group3","group4","group5",
                                            "group6","group7","group8","group9","group10",
                                            "group11","group12","group13","group14","group15"))
head(df)

#计算分组数据的均值及误差
data <- aggregate(value ~ group, df, function(x) c(mean = mean(x), sd = sd(x)))
data$mean <- data$value[,1]
data$sd <- data$value[,2]
data$group <- factor(data$group, levels = c("group1","group2","group3","group4","group5",
                                            "group6","group7","group8","group9","group10",
                                            "group11","group12","group13","group14","group15"))
data$X <- 1:15

#对填充图的数据进行分割以同时显示大于0的和小于0的数据填充不同颜色
data2 <- data[1:5,c(1,3,5)]
data3 <- data[6:15,c(1,3,5)]
##在数据前后各加一行数据
#创建需要添加的行
r1 <- data.frame(
  group="X",
  mean=-51,
  X=0
)
r2 <- data.frame(
  group="X",
  mean=0,
  X=6
)
r3 <- data.frame(
  group="X",
  mean=54,
  X=15.5
)
data2 <- rbind(data2,r1,r2)
data3 <- rbind(data3,r3)

##绘图
#折线+散点+误差棒
p1 <- ggplot(data, aes(X, mean))+
  #折线
  geom_line(color="#6a67ce")+
  #误差棒
  geom_errorbar(aes(ymin=mean-sd,ymax=mean+sd), linewidth = 0.4, width = 0.1)+
  #散点
  geom_point(color = "black", size = 2, shape = 15)+
  #设置X轴范围
  scale_x_continuous(limits = c(0,15.5), breaks = c(1:15), expand = c(0,0),
                     labels = data$group)+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.x = element_text(color = "black", size = 10),
        axis.text.y = element_blank(),
        axis.ticks.y = element_blank())+
  labs(x=NULL,y=NULL)+
  coord_flip()
p1
#散点+误差棒
p2 <- ggplot(data, aes(X, mean))+
  #误差棒
  geom_errorbar(aes(ymin=mean-sd,ymax=mean+sd), linewidth = 0.4, width = 0.1)+
  #散点
  geom_point(color = "black", size = 2, shape = 15)+
  #设置X轴范围
  scale_x_continuous(limits = c(0,15.5), breaks = c(1:15), expand = c(0,0),
                     labels = data$group)+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.x = element_text(color = "black", size = 10),
        axis.text.y = element_blank(),
        axis.ticks.y = element_blank())+
  labs(x=NULL,y=NULL)+
  coord_flip()
p2
#散点+折线+误差棒+面积填充
p3 <- ggplot(data, aes(X, mean))+
  #面积填充
  geom_area(data2, mapping=aes(X, mean), fill="#ff0b00", alpha = 0.5)+
  geom_area(data3, mapping=aes(X, mean), fill="#00c4ff", alpha = 0.5)+
  #误差棒
  geom_errorbar(aes(ymin=mean-sd,ymax=mean+sd), linewidth = 0.4, width = 0.1)+
  #散点
  geom_point(color = "black", size = 2, shape = 15)+
  #设置X轴范围
  scale_x_continuous(limits = c(0,15.5), breaks = c(1:15), expand = c(0,0),
                     labels = data$group)+
  #在y=0处添加辅助线
  geom_hline(yintercept = 0, linetype = 1, color = "red",linewidth=0.4)+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.x = element_text(color = "black", size = 10),
        axis.text.y = element_text(color = "black", size = 10))+
  labs(x=NULL,y=NULL)+
  coord_flip()
p3

##拼图
p1%>%insert_left(p2,width = 1) %>% 
  insert_left(p3,width = 1)

```


---

### 散点密度图

```r

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

```


---

### 散点图+拟合曲线+边际组合图形

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点图+拟合曲线+边际组合图形')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggpmisc) # Miscellaneous Extensions to 'ggplot2'
library(ggpubr) # 'ggplot2' Based Publication Ready Plots
library(gghalves) # Compose Half-Half Plots Using Your Favourite Geoms

#读取数据——以Chiplot绘图平台数据为例
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)

#自定义颜色
col<-c("#0099e5")

###绘图
#散点图
p1 <- ggplot(df,aes(x,y,fill=group))+
  geom_point(shape=21,size=3,alpha=0.5)+
  #添加回归曲线并添加置信区间
  geom_smooth(method = "lm",aes(color=group), se=T, 
              formula = y ~ x,
              linetype=1,alpha=0.5)+
  #计算R值和p值
  stat_cor(color=col,method = "pearson",label.x = 0.2, label.y = 8.5,size=4)+
  #添加回归方程
  stat_poly_eq(formula = y ~ x, 
               aes(color=group,label = paste(after_stat(eq.label),
                                             sep = "~~~")), parse = TRUE) +
  #颜色
  scale_fill_manual(values = col)+
  scale_color_manual(values = col)+
  #主题设置
  theme_bw()+
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='black',size=12),
        axis.title = element_text(color='black',size=14),
        legend.position = "none")+
  #标题设置
  labs(x="The title of x",y="The title of y")
p1

###添加边际组合图形——散点+箱线图+半小提琴
#小提示：这里可以以group作为X轴输入，但是由于X轴范围过大，故更换为固定数值1，大家可以试试
# 右边边际图
p2 <- ggplot(df,aes(1,y))+
  #半小提琴图
  geom_half_violin(fill="#00d1b2",position = position_nudge(x=0.26),side = "r",width=0.5,color=NA)+
  #箱线图
  geom_boxplot(fill="#ff4c4c",width=0.1,size=1.2,outlier.color =NA,position = position_nudge(x=0.2))+
  #散点图
  geom_jitter(fill="#0099e5",shape=21,size=3,width=0.12,alpha=0.5)+
  theme_void()+
  theme(legend.position = "none")
p2
#顶部边际图
p3 <- ggplot(df,aes(1,x))+
  geom_half_violin(fill="#00d1b2",position = position_nudge(x=0.26),side = "r",width=0.5,color=NA)+
  geom_boxplot(fill="#ff4c4c",width=0.1,size=1.2,outlier.color =NA,position = position_nudge(x=0.2))+
  geom_jitter(fill="#0099e5",shape=21,size=3,width=0.12,alpha=0.5)+
  theme_void()+
  theme(legend.position = "none")+
  coord_flip()
p3

#组合图形——基于aplot包进行组合
library(aplot) # Decorate a 'ggplot' with Associated Information
p1%>%insert_top(p3,height = 0.4)%>%
  insert_right(p2,width = 0.4)

```


---

### 散点图+拟合曲线+分面

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点图+拟合曲线+分面')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggpmisc) # Miscellaneous Extensions to 'ggplot2'
library(ggpubr) # 'ggplot2' Based Publication Ready Plots
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization
#读取数
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)

######绘图#######
#自定义颜色
col<-c("#1e90ff", "#cb78a6","#e6cf00","#fe0076","#28e5a1")
#构建背景色
color1 <- colorRampPalette(brewer.pal(11,"PiYG"))(30)
#绘图
p1 <- ggplot()+
  geom_point(df,mapping=aes(x,y,color=group),size=2,alpha=0.7)+
  geom_smooth(df,mapping=aes(x,y),method = "lm",
              formula = y ~ x,se=F,
              linetype=1,alpha=0.5)+
  stat_cor(df,mapping=aes(x,y),method = "pearson",label.x = 0, label.y = 15,color="black",size=4)+
  stat_poly_eq(df,mapping=aes(x,y,label = ..eq.label..),
               formula = y ~ x, parse = T,color="black",
               geom = "text",label.x = 0,label.y = 10, hjust = 0,size=4)+
  scale_color_manual(values = col)+
  theme_classic()+
  theme(axis.text=element_text(color='black',size=12),
        legend.text = element_text(color='black',size=12),
        legend.title = element_blank(),
        legend.position = c(0.95,0.85),
        legend.background = element_blank())+
  labs(x=NULL,y=NULL)
p1
##分面
p2 <- ggplot()+
  geom_point(df,mapping=aes(x,y,color=group),size=2,alpha=0.5)+
  geom_smooth(df,mapping=aes(x,y,color=group),method = "lm",
              formula = y ~ x,se=F,
              linetype=1)+
  stat_cor(df,mapping=aes(x,y),color="black",method = "pearson",label.x = 0, label.y = 15,size=4)+
  stat_poly_eq(df,mapping=aes(x,y,label = ..eq.label..),color="black",
               formula = y ~ x, parse = T,
               geom = "text",label.x = 0,label.y = 10, hjust = 0,size=4)+
  scale_color_manual(values = col)+
  theme_classic()+
  theme(axis.text=element_text(color='black',size=12),
        legend.text = element_text(color='black',size=12),
        legend.title = element_blank())+
  labs(x=NULL,y=NULL)+
  facet_grid(~group, scales = "fixed")+
  theme(legend.position = "none",
        strip.background=element_blank(),
        strip.text = element_blank())
  
p2
#拼图
cowplot::plot_grid(p2,p1,ncol = 1)
#添加背景
grid.raster(alpha(color1, 0.1), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

```


---

### 散点图+误差线+连线

```r

###科研后花园####
####@wzs#####

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/箱线图+散点图')#设置工作目录

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(tidyverse) # Easily Install and Load the 'Tidyverse'
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization
#这里使用我自己随机编写的数据
df <- data.frame(
  A = c(2,5,6,5,4,8,6,3,8,9),
  B = c(15,10,5,18,12,13,16,14,10,9),
  C = c(1,3,6,5,2,3,6,2,4,1),
  D = c(20,15,14,16,10,22,18,10,11,12),
  E = c(2,5,6,5,4,8,6,3,8,9),
  F = c(15,10,5,18,12,13,16,14,10,9),
  G = c(1,3,6,5,2,3,6,2,4,1),
  H = c(20,15,14,16,10,22,18,10,11,12),
  I = c(2,5,6,5,4,8,6,3,8,9)
)
#预览数据
head(df)

#使用tidyverse包对数据进行处理
df <- df %>% 
  gather(key = 'group',value = 'values')#gather()函数可以把多列数据合并成一列数据
head(df)#预览数据

#绘图
col = c("#ffa500","#00858a","#006400","#87ceeb","#e8d9c5","#00ff7f","#e5ad21","#ff7f50","#be92e6")
ggplot(df,aes(group,values)) +
  geom_dotplot(binaxis = "y",fill = "lightgray", dotsize = 0.9,
               stackdir = "center",position = position_dodge(1)) + 
  stat_summary(aes(color=group),fun.data = "mean_cl_normal",
               geom = "errorbar",
               width = 0.1,size=1) +
  stat_summary(fun = "mean", geom = "line",group=1,size=0.8,color="red")+
  stat_summary(aes(color=group),fun = "mean", geom = "point",size=5)+
  theme_bw()+
  theme(axis.text.x = element_text(color = "black", angle = 45,vjust = 1,hjust = 1,size = 12),
        axis.text.y = element_text(color = "black",size = 12),
        axis.title.y = element_text(color = "black",size = 14),
        legend.position = "none",
        panel.grid = element_blank())+
  labs(x=NULL,y="Temperature (℃)")+
  scale_color_manual(values = col)

#构建背景色
color1 <- colorRampPalette(brewer.pal(11,"PiYG"))(30)
#添加背景
grid.raster(alpha(color1, 0.1), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

```


---

### 散点图+柱状堆积图+折线图

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点图+柱状堆积图+折线图')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggpmisc) # Miscellaneous Extensions to 'ggplot2'
library(ggalt) # Extra Coordinate Systems, 'Geoms', Statistical Transformations,Scales and Fonts for 'ggplot2' 
#读取数据
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)
df2 <- read.table(file="data2.txt",sep="\t",header=T,check.names=FALSE)
df3 <- read.table(file="data3.txt",sep="\t",header=T,check.names=FALSE)
######绘图#######
##散点图
#绘图
p <- ggplot(df,aes(x,y))+
  geom_point(shape=21,size=3,alpha=0.5,fill="#be0027")+
  #添加回归曲线并添加置信区间
  geom_smooth(method = "lm", se=T, 
              formula = y ~ x,
              linetype=1,alpha=0.5,color="#00c7f2")+
  #添加回归方程
  stat_poly_eq(formula = y ~ x, 
               aes(label = paste(after_stat(eq.label),
                                             after_stat(rr.label),sep = "~~~")), parse = TRUE,
               color="blue") +
  theme_bw()+
  theme(panel.grid=element_blank())+
  labs(x=NULL,y=NULL)
p

###柱状堆积图+折线图
#构建颜色
col2 <- c("#ffed00","#ff0092","#c2ff00","#00c7f2")
p1<-ggplot()+
  geom_col(df2, mapping=aes(x = sample,y=value,fill = group),
           position = 'stack', width = 0.6)+
  geom_line(df3,mapping=aes(x = sample,y=value,group=1),linewidth=1,color="black",linetype=3)+
  geom_point(df3,mapping=aes(x = sample,y=value),shape=21,color="black",fill= "#db3552",size=3)+
  scale_y_continuous(expand = c(0,0),limits = c(0,210))+
  labs(x="Samples",y="Relative Abundance(%)",
       fill=NULL)+
  guides(fill=guide_legend(keywidth = 1, keyheight = 1))+
  theme_bw()+
  theme(legend.position = c(0.04, .93),
        legend.justification = c(0.05, 0.5),
        legend.direction = 'horizontal',
        axis.title.x=element_text(size=12),
        axis.title.y=element_text(size=12,angle=90),
        axis.text.y=element_text(size=10,color = "black"),
        axis.text.x=element_text(size=10,color = "black"),
        panel.grid=element_blank())+
  scale_fill_manual(values = col2)
p1

####组合图
p1 + annotation_custom(grob=ggplotGrob(p),ymin = 70, ymax = 205, xmin=4.2, xmax=8.5)

```


---

## 🫧 三、气泡图 & 棒棒糖图

### 气泡图

```r

rm(list=ls())#clear Global Environment
setwd('D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\气泡图')#设置工作路径

#安装包
# install.packages("ggplot2")
# install.packages("ggprism")
#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggprism) # A 'ggplot2' Extension Inspired by 'GraphPad Prism'
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization
#读取数据
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)

######绘图#######
#1、基本绘图
p1<-ggplot(df,aes(A,B,fill=C))+
  geom_point(aes(size=D,color=C))
p1

#自定义颜色
col<-c("#000000", "#be0027", "#cf8d2e","#e4e932","#2c9f45")
p2<-p1+scale_color_manual(values=col)
p2

#调整气泡相对大小
p3<-p2+scale_size_continuous(range = c(0.5, 15))
p3

#更换数据显示为不同气泡图
p4<-ggplot(df,aes(C,B,fill=A))+
  geom_point(aes(size=D,color=A))+
  scale_size_continuous(range = c(0.5, 15))
p4

#气泡形状
p5<-ggplot(df,aes(A,B,color=C,size=D,fill=C))+
  geom_point(color="black",shape=22)#设置形状
p5


#结合ggprism包进行个性化设置
ggplot(df,aes(A,B,#数据
              color=C,#根据C列的数据填充颜色
              size=D,#气泡大小根据D列数据
              fill=C))+#根据C列数据填充颜色
  geom_point(color="black",#气泡边框色
             shape=21)+#形状
  scale_size_continuous(range = c(0.5, 15))+#气泡的相对大小
  theme_prism(palette = "flames",
              base_fontface = "plain", # 字体样式，可选 bold, plain, italic
              base_family = "serif", # 字体格式，可选 serif, sans, mono, Arial等
              base_size = 16,  # 图形的字体大小
              base_line_size = 0.8, # 坐标轴的粗细
              axis_text_angle = 45)+ # 可选值有 0，45，90，270
  scale_fill_prism(palette = "candy_bright")+#填充色
  labs(title = "Chart", # 定义主标题
       subtitle = "XXXXXXX", # 定义子标题
       x = "XXXXX", # 定义x轴文本
       y = "XXXXX")# 定义y轴文本



###绘图模板
ggplot(df,aes(A,B,color=C,size=D,fill=C))+#色
  geom_point(color="black",#气泡边框色
             shape=21,alpha=0.9)+#形状
  scale_size_continuous(range = c(1, 15))+#气泡的相对大小
  theme_bw()+
  theme(panel.grid = element_blank(), #背景
        axis.line=element_line(),#坐标轴的线设为显示
        axis.text=element_text(color='black',size=12),
        legend.text = element_text(color='black',size=12),
        axis.title= element_text(size=12),
        axis.text.x=element_text(vjust = 1,hjust = 1),
        legend.key = element_blank())+
  scale_fill_manual(values=c("#34a186","#f9cb45","#b5182b","#4cb1c4","#ab96d2"))+#指定颜色
  labs(x = NULL, # 定义x轴文本
       y = NULL)# 定义y轴文本

#背景色
color <- colorRampPalette(brewer.pal(11,"BrBG"))(30)
#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

```


---

### 气泡图+注释+配对连线

```r

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

```


---

### 气泡图叠加饼图+显著性

```r

#########微信公众号：科研后花园
######推文题目：跟着PANS学绘图—气泡图叠加饼图+显著性（多饼图的绘制）！！！

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/气泡图叠加饼图+显著性')#设置工作路径

##加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(scatterpie) # Scatter Pie Plot
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package

##加载数据
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")

##将物种丰度信息转换为长数据
df1 <- melt(df, id.vars = c("X","Y","X2","Y2","n BGCs"))
df1$X <- factor(df1$X, levels = df$X[1:10])
df1$Y <- factor(df1$Y, levels = c("groupA","groupB"))

##绘图
ggplot() +
  #绘制多个饼图
  geom_scatterpie(data=df1, aes(X2,Y2,#这里的坐标轴必须是数值型的
                                r = `n BGCs`*0.35),#根据图形调整半径大小
                  cols = 'variable', #填充色根据物种进行着色
                  long_format = T, color = "transparent")+
  #添加图例
  geom_scatterpie_legend(df1$`n BGCs`*0.5,#图形半径缩小一倍
                         x = 5, y = 2,
                         labeller = function(x) x * 2)+#数值扩大一倍恢复原来数值
  #保持x轴和y轴比例相等，维持饼图为圆形
  coord_fixed(ratio = 1)+
  #主题相关设置
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust = 1, size = 10),
        axis.text.y = element_text(size=10))+
  #自定义x轴和y轴的标签
  scale_x_continuous(breaks = c(1,2,3,4,5,6,7,8,9,10),
                     labels = df$X[1:10],
                     minor_breaks = seq(1, 10, 1))+
  scale_y_continuous(breaks = c(1,2),
                     labels = c("groupA","groupB"),
                     minor_breaks = seq(1, 2, 1))+
  #自定义填充色
  scale_fill_manual(values = c(SpeciesA="#037ef3",SpeciesB="#f85a40",
                               SpeciesC="#00c16e",SpeciesD="#7552cc",
                               SpeciesE="#0cb9c1",SpeciesF="#f48924"),
                    name="Species")+
  labs(x=NULL,y=NULL)+
  #手动添加显著性，代入个人数据时需要先计算显著性
  annotate("text", x = 4, y = 2.5, label = "***", size=6, color = "black")+
  annotate("text", x = 8, y = 2.5, label = "**", size=6, color = "black")


####最后在AI或者PS中对图片进行美化，包括调整图例位置等!

```


---

### 绘制气泡图+分组+边际数量统计

```r

#设置工作环境
rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/气泡图+分组+边际数量统计")

##加载R包（没有安装相关包的同学可以先安装相应的R包）
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(stringr) # Simple, Consistent Wrappers for Common String Operations
library(aplot) # Decorate a 'ggplot' with Associated Information

##加载数据（随机编写，无实际意义）
data <- read.table("data.txt", header = 1, check.names = F, sep = "\t")
#整理数据
df <- melt(data)
df$sample <- factor(df$sample, levels = data$sample)
#利用正则表达式重新将分组信息添加进去
df$group <- str_sub(df$variable, 1, 1)

##绘制主体气泡图
p1 <- ggplot(df, aes(variable, sample))+
  #利用散点图绘制方式绘制气泡图
  geom_point(aes(fill = group, size = value), shape = 21, color = "black")+
  #调整气泡图大小范围
  scale_size_continuous(range = c(2, 15), guide = "none")+
  #调整图例
  guides(fill=guide_legend(override.aes = list(size=6,alpha=1)))+
  #主题相关设置
  theme_bw()+
  theme(axis.text = element_text(size = 10, color = "black"))+
  labs(fill = NULL, x = NULL, y = NULL)+
  #自定义颜色
  scale_fill_manual(values = c("#e64b50", "#dbc65d"))
p1

##绘制边际条形图
#使用aggregate函数统计X轴与Y轴上的数量
df1 <- aggregate(value ~ variable, df, sum)
#利用正则表达式重新将分组信息添加进去
df1$group <- str_sub(df1$variable, 1, 1)
df2 <- aggregate(value ~ sample, df, sum)
#绘图——X轴上的边际条形图
p2 <- ggplot(df1, aes(variable, value))+
  #绘制条形图
  geom_col(aes(fill = group))+
  #添加文字注释
  geom_text(aes(y = value-20, label = value))+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        legend.position = "none",
        axis.text.x = element_blank(),
        axis.text.y = element_text(size = 10, color = "black", vjust = 0),
        axis.title.y = element_text(size = 12, color = "black"),
        axis.ticks.x = element_blank())+
  labs(x = NULL, y = "number of x")+
  scale_y_continuous(expand = c(0,0))+
  #自定义颜色
  scale_fill_manual(values = c("#e64b50", "#dbc65d"))
p2
#绘图——Y轴上的边际条形图
p3 <- ggplot(df2, aes(sample, value))+
  #绘制条形图
  geom_col(fill = "#56c1ab")+
  #添加文字注释
  geom_text(aes(y = value-30, label = value))+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        legend.position = "none",
        axis.text.y = element_blank(),
        axis.text.x = element_text(size = 10, color = "black", vjust = 0, angle = 270),
        axis.title.x = element_text(size = 12, color = "black"),
        axis.ticks.y = element_blank())+
  labs(x = NULL, y = "number of y")+
  scale_y_continuous(expand = c(0,0))+
  #翻转X轴与Y轴位置
  coord_flip()
p3

##拼图
p1%>%insert_top(p2, height = 0.3) %>% 
  insert_right(p3, width = 0.3)

```


---

### 棒棒糖图&哑铃图

```r

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

```


---

## 📈 四、折线图 & 时间序列

### 折线图

```r

rm(list=ls())
#设置工作环境
setwd("D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\折线图")

#安装包
# install.packages("ggplot2")
# install.packages("reshape2")
# install.packages("ggprism")
# install.packages("ggalt")
#加载包
library(ggplot2)
library(reshape2)
library(ggprism)
library(ggalt)
#生成作图数据
df <- data.frame(
  y1=c(2,5,6,7,8,6,7,10,4),
  y2=c(10,12,14,15,10,12,13,9,10),
  y3=c(7,8,9,6,4,8,9,3,6)
)
#转换数据
data=melt(df)
data$x<-rep(c(1,2,3,4,5,6,7,8,9))
#修改列名
colnames(data)=c("group","y","x")
####绘图
#基础绘图
p1<-ggplot(data, aes(x, y, group=group, color=group, shape=group,linetype=group))+
  geom_point(size=3)+
  geom_line(size=1)
p1
#修改线形
p1+scale_linetype_manual(values = c(y1 = 4, y2 = 1, y3 = 3))
#自定义颜色
p1+scale_color_manual(values = c('#ec1c24','#fdbd10','#0066b2'))
#自定义节点形状
p1+scale_shape_manual(values = c(17,18,19))
#修改主题
p1+theme_bw()
#修改图例
p1+theme(legend.title = element_blank(),#图例标题去除
      legend.text = element_text(family = 'serif'),#字体
      legend.position = c(0.05,0.9),#位置
      legend.direction = "vertical")#水平或垂直
#使得折线图曲线平滑
ggplot(data, aes(x, y, group=group, color=group, shape=group))+
  geom_point(size=3)+
  geom_xspline(spline_shape = -0.3,size=1)

###个性化绘图
ggplot(data, aes(x, y, group=group, color=group, shape=group,linetype=group))+
  geom_point(size=3)+#散点
  geom_xspline(spline_shape = -0.3,size=1)+#曲线平滑
  scale_color_manual(values = c('#ec1c24','#fdbd10','#0066b2'))+#自定义颜色
  theme_prism(palette = "candy_soft",#主题设置
              base_fontface = "plain", 
              base_family = "serif", 
              base_size = 16,  
              base_line_size = 0.8, 
              axis_text_angle = 45)+
  theme(legend.title = element_blank(),#图例标题去除
        legend.text = element_text(family = 'serif'),#字体
        legend.position = c(0.9,0.9),#位置
        legend.direction = "vertical")+#水平或垂直
  labs(title = "XXX", # 定义主标题
       subtitle = "XXXXXXX", # 定义子标题
       x = "XXXXX", # 定义x轴文本
       y = "XXXXX")# 定义y轴文本

```


---

### 平滑曲线折线图

```r

rm(list=ls())
setwd("D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\平滑曲线折线图")
#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggalt) # Extra Coordinate Systems, 'Geoms', Statistical Transformations,
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization
#读取数据
data <- read.delim("data.txt",
                       header=T, 
                       row.names=1, 
                       sep="\t",
                       stringsAsFactors = FALSE,
                       check.names = FALSE)

data
#赋予因子水平
data$Genus<-factor(
  data$Genus,
  levels=c("Bacillus","Cronobacter",
           "Enterobacterales",
           "Klebsiella","Pantoea",
           "Pseudomonas","Rosenbergiella"), 
  labels = c("Bacillus","Cronobacter",
             "Enterobacterales",
             "Klebsiella","Pantoea",
             "Pseudomonas","Rosenbergiella"))

data
#准备配色
col <- c("#85BA8F", "#A3C8DC",
              "#349839","#EA5D2D",
              "black","#F09594","#2072A8")
#背景色
color <- colorRampPalette(brewer.pal(11,"PuOr"))(30)
#普通折线图绘制
p=ggplot(data=data,
         aes(x=Compartment,y=RA,
             group=Genus,color=Genus))+
  geom_point(size=2.5)+
  labs(x="Compartments", y="Relative abundance (%)")+
  geom_line()+
  scale_x_discrete(limits=c("RS","RE","VE","SE","LE","P","BS"))+
  scale_colour_manual(values=col)+
  theme_bw() +
  theme(axis.text.x = element_text(size = 8),axis.text.y = element_text(size = 8))+
  theme(axis.title.y= element_text(size=12))+theme(axis.title.x = element_text(size = 12))+
  theme(legend.title=element_text(size=5),legend.text=element_text(size=5))+theme(legend.position = "bottom")
p
#平滑曲线的绘制
p2<-ggplot(data=data,aes(x=Compartment,y=RA,
                              group=Genus,color=Genus))+
  geom_point(size=2.5)+
  labs(x="Compartments", y="Relative abundance (%)")+
  geom_xspline(spline_shape = -0.5)+
  scale_x_discrete(limits=c("RS","RE","VE","SE","LE","P"))+
  scale_colour_manual(values=col)+
  theme_bw() +
  theme(axis.text.x = element_text(size = 8),axis.text.y = element_text(size = 8))+
  theme(axis.title.y= element_text(size=12))+theme(axis.title.x = element_text(size = 12))+
  theme(legend.title=element_text(size=5),legend.text=element_text(size=5))+theme(legend.position = "bottom")
p2

#拼图
library(patchwork) # The Composer of Plots

p+ p2 +
  plot_layout(guides = "collect")+
  plot_annotation(theme = theme(legend.position = "bottom"))


########拓展
##绘图模板
ggplot(data=data,aes(x=Compartment,y=RA,
                     group=Genus,color=Genus))+
  geom_point(size=3)+
  labs(x="Compartments", y="Relative abundance (%)")+
  geom_xspline(spline_shape = -0.25)+
  scale_x_discrete(limits=c("RS","RE","VE","SE","LE","P"))+
  scale_color_manual(values=col)+
  theme_bw() +
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='#333c41',size=10),
        legend.text = element_text(color='#333c41',size=10),
        legend.title = element_blank(),
        legend.position = "bottom",
        axis.title= element_text(size=12))
#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

```


---

### 时间序列图

```r

rm(list=ls())
#设置工作环境
setwd("D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\时间序列图")

#安装包
# install.packages("ggplot2")
# install.packages("ggprism")
#加载包
library(ggplot2)
library(ggprism)
#加载数据
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)
####绘图
#Jan
p1<-ggplot(df)+
  geom_line(aes(date, Jan),size=0.8,color="red")+
  theme_prism(palette = "candy_soft",#主题设置
              base_fontface = "plain", 
              base_family = "serif", 
              base_size = 16,  
              base_line_size = 0.8, 
              axis_text_angle = 45)+
  scale_x_continuous(breaks=seq(1,31, 3))+#设置X轴标签范围及间隔
  labs(title = "Jan", # 定义主标题
       x = "Date", # 定义x轴文本
       y = "Value")# 定义y轴文本
p1
#Feb
p2<-ggplot(df)+
  geom_line(aes(date, Feb),size=0.8,color="green")+
  theme_prism(palette = "candy_soft",#主题设置
              base_fontface = "plain", 
              base_family = "serif", 
              base_size = 16,  
              base_line_size = 0.8, 
              axis_text_angle = 45)+
  scale_x_continuous(breaks=seq(1,31, 3))+#设置X轴标签范围及间隔
  labs(title = "Feb", # 定义主标题
       x = "Date", # 定义x轴文本
       y = "Value")# 定义y轴文本
p2
#Mar
p3<-ggplot(df)+
  geom_line(aes(date, Mar),size=0.8,color="blue")+
  theme_prism(palette = "candy_soft",#主题设置
              base_fontface = "plain", 
              base_family = "serif", 
              base_size = 16,  
              base_line_size = 0.8, 
              axis_text_angle = 45)+
  scale_x_continuous(breaks=seq(1,31, 3))+#设置X轴标签范围及间隔
  labs(title = "Mar", # 定义主标题
       x = "Date", # 定义x轴文本
       y = "Value")# 定义y轴文本
p3
#Apr
p4<-ggplot(df)+
  geom_line(aes(date, Apr),size=0.8,color="yellow")+
  theme_prism(palette = "candy_soft",#主题设置
              base_fontface = "plain", 
              base_family = "serif", 
              base_size = 16,  
              base_line_size = 0.8, 
              axis_text_angle = 45)+
  scale_x_continuous(breaks=seq(1,31, 3))+#设置X轴标签范围及间隔
  labs(title = "Apr", # 定义主标题
       x = "Date", # 定义x轴文本
       y = "Value")# 定义y轴文本
p4

#拼图
library(cowplot)
plot_grid(p1,p2,p3,p4,ncol=2)

```


---

### 折线+散点+误差棒+显著性

```r

#设置工作环境
rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/折线+散点+误差棒+显著性+分面")

##加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggpubr) # 'ggplot2' Based Publication Ready Plots

##加载数据（随机编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")
df$group <- factor(df$group, levels = c("A", "B", "C"))
df$G <- factor(df$G, levels = c("group1", "group2", "group3"))

#计算分组数据的均值及误差
data <- aggregate(value ~ group+G+facet, df, function(x) c(mean = mean(x), sd = sd(x)))
data$mean <- data$value[,1]
data$sd <- data$value[,2]

##绘图
p1 <- ggplot(data, aes(group, mean))+
  #散点
  geom_point(aes(color = G, shape = G), size = 3)+
  #折线
  geom_line(aes(color = G, group = G), linewidth = 0.8)+
  #误差棒
  geom_errorbar(aes(ymin=mean-sd,ymax=mean+sd, color = G), linewidth = 0.8, width = 0.08)+
  #分面
  facet_wrap(~facet, nrow = 2)+
  #自定义散点形状
  scale_shape_manual(values = c(15, 16, 17))+
  #设置y轴范围
  scale_y_continuous(limits = c(0,190))+
  #主题相关设置
  labs(x= NULL, y= "Absolute quantity value", color = NULL, shape = NULL)+
  theme_bw()+
  theme(panel.grid = element_blank())+
  scale_color_manual(values = c("#fcd000","#ff3c41","#00a78e"))+
  #显著性
  geom_signif(comparisons = list(c("A","B"),
                                 c("B","C"),
                                 c("A","C")),
              map_signif_level = T, #使用*号显示显著性
              test = "t.test",#检验方法
              textsize = 4,#字号大小
              y_position = c(155,165,175),#横线位置
              tip_length = c(0,0,0),#横线下方线条的长度
              size=0.8,color="black")#线条颜色及粗细
p1

##转置横纵坐标
p2 <- p1+coord_flip()+
  theme(legend.position = "none")
p2

##拼图
cowplot::plot_grid(p2,p1,ncol = 2,
                   rel_widths = c(0.72, 1))

```


---

## 📦 五、箱线图 & 小提琴图

### 分组箱线图

```r

rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/分组箱线图")

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics

#加载数据（随机编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")

#绘图
p1 <- ggplot(df, aes(group, value, fill = XG))+
  geom_boxplot(linewidth = 0.6)+#箱线图绘制函数
  #添加分组矩形
  annotate("rect", xmin = 0.4, xmax = 1.5, ymin = -Inf, ymax = Inf, alpha = 0.2,fill="#c1f1fc") +
  annotate("rect", xmin = 1.5, xmax = 2.5, ymin = -Inf, ymax = Inf, alpha = 0.2,fill="#ebffac") +
  annotate("rect", xmin = 2.5, xmax = 3.5, ymin = -Inf, ymax = Inf, alpha = 0.2,fill="#53d769")+
  annotate("rect", xmin = 3.5, xmax = 4.5, ymin = -Inf, ymax = Inf, alpha = 0.2,fill="#ffaaaa") +
  annotate("rect", xmin = 4.5, xmax = 5.6, ymin = -Inf, ymax = Inf, alpha = 0.2,fill="#d7dcdd")+
  #添加散点
  geom_dotplot(dotsize = 0.8,binaxis = "y", stackdir = "center",position = position_dodge(0.8))+
  #添加分组辅助线
  geom_vline(xintercept = 1.5, lty="dashed", color = "grey50", linewidth = 0.8)+
  geom_vline(xintercept = 2.5, lty="dashed", color = "grey50", linewidth = 0.8)+
  geom_vline(xintercept = 3.5, lty="dashed", color = "grey50", linewidth = 0.8)+
  geom_vline(xintercept = 4.5, lty="dashed", color = "grey50", linewidth = 0.8)+
  #主题
  theme_bw()+
  theme(axis.text.y = element_text(size=10, color = "#204056"),
        axis.text.x = element_text(size=10, angle = 45, hjust = 1, vjust = 1, color = "#204056"),
        axis.title = element_blank(),
        panel.grid = element_blank())+
  #自定义颜色
  scale_fill_manual(values = c("#0ebeff", "#47cf73", "#ae63e4", "#fcd000", "#ff3c41"))
p1

##以分面形式进行展示
p2 <- ggplot(df, aes(XG, value, fill = XG))+
  geom_boxplot(linewidth = 0.6)+#箱线图绘制函数
  geom_point(shape = 21,size=2)+
  #分面
  facet_grid(~group)+
  #主题
  theme_bw()+
  theme(axis.text.y = element_text(size=10, color = "#204056"),
        axis.text.x = element_text(size=10, color = "#204056"),
        axis.title = element_blank(),
        panel.grid = element_blank())+
  #自定义颜色
  scale_fill_manual(values = c("#0ebeff", "#47cf73", "#ae63e4", "#fcd000", "#ff3c41"))
p2
#拼图
p1/p2

```


---

### 同变量多组箱线图

```r

#########微信公众号：科研后花园
######推文题目：跟着Nature Communications学绘图—同变量多组箱线图！！！

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/同变量多组箱线图')#设置工作路径

##加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics

##加载数据
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")
df$X <- factor(df$X, levels = c("A", "B", "C", "D", "E"))

##绘制分组箱线图
ggplot(df, aes(X, value, fill = Group))+
  #误差线
  stat_boxplot(width=0.3, 
               geom = "errorbar",linewidth = 0.8,
               position = position_dodge(0.5))+
  #绘制箱线图并按照分组着色
  geom_boxplot(position = position_dodge(0.5))+
  #自定义颜色
  scale_fill_manual(values = c("#bb1e10","#f67828","#237f52"))+
  #主题相关设置
  labs(x = NULL, y = NULL)+
  theme_bw()+
  theme(axis.text = element_text(size=12),
        axis.title = element_text(size=15),
        legend.title = element_text(color = 'red',size=15),
        legend.text = element_text(color = 'black',size=10))->p1
p1


##绘制同变量多组箱线图
ggplot()+
  #按照分组进行单独绘制，分开绘制可将三组放在同一垂直线上
  stat_boxplot(data = df[df$Group == "group1",],
               aes(X, value),
               geom = "errorbar", width=0.2, linewidth = 0.8)+
  geom_boxplot(data = df[df$Group == "group1",],
               aes(X, value, fill = Group), width = 0.5)+
  stat_boxplot(data = df[df$Group == "group2",],
               aes(X, value),
               geom = "errorbar", width=0.2, linewidth = 0.8)+
  geom_boxplot(data = df[df$Group == "group2",],
               aes(X, value, fill = Group), width = 0.5)+
  stat_boxplot(data = df[df$Group == "group3",],
               aes(X, value),
               geom = "errorbar", width=0.2, linewidth = 0.8)+
  geom_boxplot(data = df[df$Group == "group3",],
               aes(X, value, fill = Group), width = 0.5)+
  #自定义颜色
  scale_fill_manual(values = c("#bb1e10","#f67828","#237f52"))+
  #主题相关设置
  labs(x = NULL, y = NULL)+
  theme_bw()+
  theme(axis.text = element_text(size=12),
        axis.title = element_text(size=15),
        legend.title = element_text(color = 'red',size=15),
        legend.text = element_text(color = 'black',size=10))->p2
p2


##拼图
library(patchwork)
p1+p2+
  plot_layout(guides = 'collect')

```


---

### 箱线图+点线图+显著性+分组

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/箱线图+点线图+显著性+分组')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(dplyr) # A Grammar of Data Manipulation
#加载数据
data1 <- read.table("data1.txt",header = 1,check.names = F,sep = "\t")
data2 <- read.table("data2.txt",header = 1,check.names = F,sep = "\t")

#数据清洗及处理
df1 <- melt(data1,id.vars = c("sample","group"))
df1$sample <- factor(df1$sample,levels = rev(data1$sample))
df1$group <- factor(df1$group,levels = c("A","B","C","D","E","F"))
df1$facet <- rep("Community-weighted trait means",times=132)
df2 <- melt(data2,id.vars = "sample")
df2$sample <- factor(df2$sample,levels = rev(data1$sample))
df2$group <- rep(c("Control","Warming"),each=66)#添加一列数据以区分Control和Warming组

###绘制第一张箱线图
#绘制基础箱线图
p <- ggplot(df1,aes(sample,value))+
  stat_boxplot(aes(color=group),geom = "errorbar", width=0.3,size=0.5)+#添加误差线
  geom_boxplot(aes(fill=group,color=group),outlier.shape = 18,size=0.5)#绘制箱线图
p
#计算均值位置并根据基础箱线图确定位置
df1 %>% 
  group_by(sample) %>% 
  summarise(mean_value=mean(value)) %>%
  cbind(ggplot_build(p)$data[[1]]) -> mean
#绘图
p1 <- ggplot(df1,aes(sample,value))+
  #在y轴为0的位置添加辅助线
  geom_hline(yintercept = 0, linetype = 2, color = "grey60",linewidth=0.8)+
  stat_boxplot(aes(color=group),geom = "errorbar", width=0.3,size=0.6)+#添加误差线
  geom_boxplot(aes(fill=group,color=group),outlier.shape = 18,size=0.6)+#绘制箱线图
  geom_segment(mean,
               mapping=aes(x=xmin-0.25,xend=xmax+0.25,y=mean_value,yend=mean_value),
               color="white",size=0.5)+
  #转变x轴与y轴位置
  coord_flip()+
  #自定义颜色
  scale_fill_manual(values = c("#e3ac6d","#9d7bb8","#6caf83","#d9586e","#3c74bb","#f85b2b"))+
  scale_color_manual(values = c("#e3ac6d","#9d7bb8","#6caf83","#d9586e","#3c74bb","#f85b2b"))+
  #y轴范围设置
  scale_y_continuous(limits = c(-100, 100))+
  #主题设置
  theme_bw()+
  theme(legend.position = "none",
        panel.grid = element_blank(),
        axis.text = element_text(color = "black",size=10),
        strip.background = element_rect(fill = "grey", color = "transparent"),
        strip.text = element_text(color="black",size=10))+
  #标题位置
  labs(y="Response to warming (%)",x=NULL)+
  #添加分组矩形
  annotate("rect", xmin = 0, xmax = 6.5, ymin = -Inf, ymax = Inf, alpha = 0.2,fill="#d7ebce") +
  annotate("rect", xmin = 6.5, xmax = 20.5, ymin = -Inf, ymax = Inf, alpha = 0.2,fill="#bcced6") +
  annotate("rect", xmin = 20.5, xmax = 23, ymin = -Inf, ymax = Inf, alpha = 0.2,fill="#ffdc80")+
  #手动添加显著性标记，图中列出部分，具体根据个人数据进行调整
  annotate('text', label = '**', x =21, y =5, angle=-90, size =5,color="black")+
  annotate('text', label = '***', x =2, y =55, angle=-90, size =5,color="black")+
  annotate('text', label = '***', x =19, y =65, angle=-90, size =5,color="black")+
  annotate('text', label = '***', x =16, y =35, angle=-90, size =5,color="black")+
  annotate('text', label = '***', x =9, y =35, angle=-90, size =5,color="black")+
  annotate('text', label = '***', x =5, y =100, angle=-90, size =5,color="black")+
  facet_grid(~ facet)#基于分面函数添加图顶部标题
p1

###绘制第二张点线图
#计算均值
library(Rmisc) # Ryan Miscellaneous
mean2 <- summarySE(df2, measurevar = "value", groupvars = c("sample", "group"))
mean2
mean2$sample <- factor(mean2$sample,levels = rev(data2$sample))
mean2$facet <- rep("Functional diversity",times=44)
#绘图
p2 <- ggplot(mean2, aes(sample,value, color = group)) + 
  geom_errorbar(aes(ymin = value- se, ymax = value + se), 
                width = 0,position = position_dodge(0.8),linewidth=0.5) + 
  geom_point(position = position_dodge(0.8),shape=18,size=3)+
  #转变x轴与y轴位置
  coord_flip()+
  #y轴范围设置
  scale_y_continuous(limits = c(30, 110))+
  #主题设置
  theme_bw()+
  theme(legend.position = c(0.8,0.95),
        legend.background = element_blank(),
        legend.key = element_blank(),
        panel.grid = element_blank(),
        axis.text.x = element_text(color = "black",size=10),
        axis.text.y = element_blank(),
        axis.ticks.y = element_blank(),
        strip.background = element_rect(fill = "grey", color = "transparent"),
        strip.text = element_text(color="black",size=10))+
  #标题位置
  labs(y="Functional dispersion values",x=NULL,color=NULL)+
  scale_color_manual(values = c("#7fc190","#efb684"))+
  #添加分组矩形
  annotate("rect", xmin = 0, xmax = 6.5, ymin = -Inf, ymax = Inf, alpha = 0.2,fill="#d7ebce") +
  annotate("rect", xmin = 6.5, xmax = 20.5, ymin = -Inf, ymax = Inf, alpha = 0.2,fill="#bcced6") +
  annotate("rect", xmin = 20.5, xmax = 23, ymin = -Inf, ymax = Inf, alpha = 0.2,fill="#ffdc80")+
  #手动添加显著性标记，图中列出部分，具体根据个人数据进行调整
  annotate('text', label = '**', x =11, y =80, angle=-90, size =5,color="black")+
  geom_segment(x = 10.5, xend = 11.5, y = 78, yend = 78,color = "black", size = 0.8)+
  facet_grid(~ facet)#基于分面函数添加图顶部标题
p2
#拼图
library(aplot) # Decorate a 'ggplot' with Associated Information
p1%>%insert_right(p2,width = 1)

###最后用AI进行微调即可

```


---

### 箱线图+组内显著性+组内线性回归分析趋势性P值

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/箱线图+组内显著性+组内线性回归分析趋势性P值')#设置工作路径

##加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(ggpmisc) # Miscellaneous Extensions to 'ggplot2'

##加载数据（随机编写，无实际意义）
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE, row.names = 1)
df$Sample <- rownames(df)

##Z-score法标准化数据
#提取数值型数据所在列
df1 <- df[2:5]
#标准化数据，获得Z-score
df_zscore <-as.data.frame(scale(df1))
df_zscore$Sample <- rownames(df_zscore)
#整理标准化后的数据
data <- merge(df[c(1,6)], df_zscore, by = "Sample")

##将长数据转换为长数据
data2 <- melt(data, id.vars = c("Sample", "Period"), 
            measure.vars = c('ACE','Chao','Shannon', 'Simpson'))
data2$Period <- factor(data2$Period, levels = c("period1", "period2", "period3", "period4", "period5"))
data2$variable <- factor(data2$variable, levels = c("ACE", "Chao", "Shannon", "Simpson"))

##根据分组信息构造对应的数值型x轴
#确保此时的长格式数据分组顺序与个人需求一致
#ACE对应的period1-5构造为1-5，Chao对应的period1-5构造为7-11，以此类推，确保没两组之间间隔为1
data2$x <- rep(c(1:5, 7:11, 13:17, 19:23), each = 10)
#ACE、Chao、Shannon以及Simpson对应坐标则为3、9、15、21

####计算组间显著性
###基于Wilcoxon秩和检验方法分别计算'ACE','Chao','Shannon', 'Simpson'四个组内部各period的显著性
###这里根据原始数据计算
##将长数据转换为长数据
df2 <- melt(df, id.vars = c("Sample", "Period"), 
              measure.vars = c('ACE','Chao','Shannon', 'Simpson'))
df2$Period <- factor(df2$Period, levels = c("period1", "period2", "period3", "period4", "period5"))
df2$variable <- factor(df2$variable, levels = c("ACE", "Chao", "Shannon", "Simpson"))
##ACE
# 创建一个矩阵来存储结果
ACE_results_matrix <- matrix(NA, nrow = 5, ncol = 5)
rownames(ACE_results_matrix) <- colnames(ACE_results_matrix) <- paste0("period", 1:5)

# 利用循环进行比较并存储结果
for (i in 1:5) {
  for (j in 1:5) {
    if (i == j) {
      # 对角线上的比较，略过
      next
    } else {
      # 获取数据
      x <- subset(df2, variable == "ACE" & Period == paste0("period", i))$value
      y <- subset(df2, variable == "ACE" & Period == paste0("period", j))$value
      
      # 执行Wilcoxon秩和检验,使用approximate方法进行近似计算,根据个人需求进行更改
      result <- wilcox.test(x, y,exact = FALSE)
      
      # 提取p 值
      p_value <- result$p.value
      
      # 存储结果
      ACE_results_matrix[i, j] <- p_value
    }
  }
}
#显示结果
ACE_results_matrix <- as.data.frame(ACE_results_matrix)
##Chao
# 创建一个矩阵来存储结果
Chao_results_matrix <- matrix(NA, nrow = 5, ncol = 5)
rownames(Chao_results_matrix) <- colnames(Chao_results_matrix) <- paste0("period", 1:5)

# 利用循环进行比较并存储结果
for (i in 1:5) {
  for (j in 1:5) {
    if (i == j) {
      # 对角线上的比较，略过
      next
    } else {
      # 获取数据
      x <- subset(df2, variable == "Chao" & Period == paste0("period", i))$value
      y <- subset(df2, variable == "Chao" & Period == paste0("period", j))$value
      
      # 执行Wilcoxon秩和检验,使用approximate方法进行近似计算,根据个人需求进行更改
      result <- wilcox.test(x, y,exact = FALSE)
      
      # 提取p 值
      p_value <- result$p.value
      
      # 存储结果
      Chao_results_matrix[i, j] <- p_value
    }
  }
}
#显示结果
Chao_results_matrix <- as.data.frame(Chao_results_matrix)
##Shannon
# 创建一个矩阵来存储结果
Shannon_results_matrix <- matrix(NA, nrow = 5, ncol = 5)
rownames(Shannon_results_matrix) <- colnames(Shannon_results_matrix) <- paste0("period", 1:5)

# 利用循环进行比较并存储结果
for (i in 1:5) {
  for (j in 1:5) {
    if (i == j) {
      # 对角线上的比较，略过
      next
    } else {
      # 获取数据
      x <- subset(df2, variable == "Shannon" & Period == paste0("period", i))$value
      y <- subset(df2, variable == "Shannon" & Period == paste0("period", j))$value
      
      # 执行Wilcoxon秩和检验,使用approximate方法进行近似计算,根据个人需求进行更改
      result <- wilcox.test(x, y,exact = FALSE)
      
      # 提取p 值
      p_value <- result$p.value
      
      # 存储结果
      Shannon_results_matrix[i, j] <- p_value
    }
  }
}
#显示结果
Shannon_results_matrix <- as.data.frame(Shannon_results_matrix)
##Simpson
# 创建一个矩阵来存储结果
Simpson_results_matrix <- matrix(NA, nrow = 5, ncol = 5)
rownames(Simpson_results_matrix) <- colnames(Simpson_results_matrix) <- paste0("period", 1:5)

# 利用循环进行比较并存储结果
for (i in 1:5) {
  for (j in 1:5) {
    if (i == j) {
      # 对角线上的比较，略过
      next
    } else {
      # 获取数据
      x <- subset(df2, variable == "Simpson" & Period == paste0("period", i))$value
      y <- subset(df2, variable == "Simpson" & Period == paste0("period", j))$value
      
      # 执行Wilcoxon秩和检验,使用approximate方法进行近似计算,根据个人需求进行更改
      result <- wilcox.test(x, y,exact = FALSE)
      
      # 提取p 值
      p_value <- result$p.value
      
      # 存储结果
      Simpson_results_matrix[i, j] <- p_value
    }
  }
}
#显示结果
Simpson_results_matrix <- as.data.frame(Simpson_results_matrix)


###绘图
ggplot()+
  #根据分组分别绘制各组的箱线图
  geom_boxplot(data=data2[data2$variable=="ACE",],
               aes(x, value, fill = Period), outlier.color = NA)+
  geom_boxplot(data=data2[data2$variable=="Chao",],
               aes(x, value, fill = Period), outlier.color = NA)+
  geom_boxplot(data=data2[data2$variable=="Shannon",],
               aes(x, value, fill = Period), outlier.color = NA)+
  geom_boxplot(data=data2[data2$variable=="Simpson",],
               aes(x, value, fill = Period), outlier.color = NA)+
  ##为各组箱线图添加散点
  geom_jitter(data=data2[data2$variable=="ACE",],
              aes(x, value, fill = Period), 
              color = "grey30", size = 1.5, width = 0.3, shape = 21)+
  geom_jitter(data=data2[data2$variable=="Chao",],
              aes(x, value, fill = Period), 
              color = "grey30", size = 1.5, width = 0.3, shape = 21)+
  geom_jitter(data=data2[data2$variable=="Shannon",],
              aes(x, value, fill = Period), 
              color = "grey30", size = 1.5, width = 0.3, shape = 21)+
  geom_jitter(data=data2[data2$variable=="Simpson",],
              aes(x, value, fill = Period), 
              color = "grey30", size = 1.5, width = 0.3, shape = 21)+
  #给每个分组内部的小分组添加拟合曲线
  geom_smooth(data=data2[data2$variable=="ACE",],
              aes(x, value),method = "lm", se=F,
              formula = y ~ x,linewidth = 0.8,
              linetype=1)+
  geom_smooth(data=data2[data2$variable=="Chao",],
              aes(x, value),method = "lm", se=F,
              formula = y ~ x, linewidth = 0.8,
              linetype=1)+
  geom_smooth(data=data2[data2$variable=="Shannon",],
              aes(x, value),method = "lm", se=F,
              formula = y ~ x,linewidth = 0.8,
              linetype=1)+
  geom_smooth(data=data2[data2$variable=="Simpson",],
              aes(x, value),method = "lm", se=F,
              formula = y ~ x,linewidth = 0.8,
              linetype=1)+
  #组内线性回归分析趋势性P值
  stat_poly_eq(data=data2[data2$variable=="ACE",],
               aes(x, value, label = after_stat(p.value.label)),
               formula = y ~ x,
               parse = TRUE,label.x = 0.1, label.y = 0.1,size=4,
               color = "black")+
  stat_poly_eq(data=data2[data2$variable=="Chao",],
               aes(x, value, label = after_stat(p.value.label)),
               formula = y ~ x,
               parse = TRUE,label.x = 0.35, label.y = 0.1,size=4,
               color = "black")+
  stat_poly_eq(data=data2[data2$variable=="Shannon",],
               aes(x, value, label = after_stat(p.value.label)),
               formula = y ~ x,
               parse = TRUE,label.x = 0.65, label.y = 0.1,size=4,
               color = "black")+
  stat_poly_eq(data=data2[data2$variable=="Simpson",],
               aes(x, value, label = after_stat(p.value.label)),
               formula = y ~ x,
               parse = TRUE,label.x = 0.9, label.y = 0.1,size=4,
               color = "black")+
  ##在P值上面添加短横线区分组
  geom_segment(data=data2,aes(x=1,xend=5,y=-2.2,yend=-2.2),
               color="black",linewidth=0.6)+
  geom_segment(data=data2,aes(x=7,xend=11,y=-2.2,yend=-2.2),
               color="black",linewidth=0.6)+
  geom_segment(data=data2,aes(x=13,xend=17,y=-2.2,yend=-2.2),
               color="black",linewidth=0.6)+
  geom_segment(data=data2,aes(x=19,xend=23,y=-2.2,yend=-2.2),
               color="black",linewidth=0.6)+
  ##根据前面计算得到的各组内各时期间的p值手动添加显著性
  ##"*":p<0.05;"**":p<0.01;"***":p<0.001
  geom_segment(data=data2,aes(x=1,xend=2,y=0.3,yend=0.3),
               color="black",linewidth=0.6)+
  annotate("text", x = 1.5 , y = 0.4,label = "*", size= 5,color = "black")+
  geom_segment(data=data2,aes(x=4,xend=5,y=2.3,yend=2.3),
               color="black",linewidth=0.6)+
  annotate("text", x = 4.5 , y = 2.4,label = "*", size= 5,color = "black")+
  geom_segment(data=data2,aes(x=7, xend=8, y=-0.3,yend=-0.3),
               color="black",linewidth=0.6)+
  annotate("text", x = 7.5 , y = 0,label = "**", size= 5,color = "black")+
  geom_segment(data=data2,aes(x=9,xend=10,y=1.5,yend=1.5),
               color="black",linewidth=0.6)+
  annotate("text", x = 9.5 , y = 1.6,label = "*", size= 5,color = "black")+
  geom_segment(data=data2,aes(x=16,xend=17,y=2,yend=2),
               color="black",linewidth=0.6)+
  annotate("text", x = 16.5 , y = 2.1,label = "**", size= 5,color = "black")+
  geom_segment(data=data2,aes(x=21,xend=22,y=1,yend=1),
               color="black",linewidth=0.6)+
  annotate("text", x = 21.5 , y = 1.1,label = "**", size= 5,color = "black")+
  ##手动修改X轴标签为大分组的标签
  scale_x_continuous(breaks = c(3,9,15,21),
                     labels = c("ACE", "Chao", "Shannon", "Simpson"))+
  scale_y_continuous(limits = c(-2.8, 2.5))+
  labs(x=NULL,y="Alpha diversity index")+
  ##添加组间分割线
  geom_vline(xintercept = 6, linetype = 2, color = "black",linewidth=0.8)+
  geom_vline(xintercept = 12, linetype = 2, color = "black",linewidth=0.8)+
  geom_vline(xintercept = 18, linetype = 2, color = "black",linewidth=0.8)+
  ##主题相关设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.x = element_text(angle = 45, vjust = 1, hjust = 1, size = 12),
        axis.text.y = element_text(size = 12),
        axis.title = element_text(size = 14),
        legend.position = c(0.95,0.8),
        legend.background = element_blank())+
  ##自定义颜色
  scale_fill_manual(values = c("#ff3c41","#fbb034","#fcd000","#47cf73","#0ebeff"))

```


---

### 小提琴图

```r

rm(list=ls())#clear Global Environment
setwd('D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\小提琴图')#设置工作目录

#安装包
# install.packages("ggplot2")
# install.packages("ggpubr")
# install.packages("ggsignif")
# install.packages("tidyverse")
# install.packages("ggprism")
# install.packages("vioplot")
#加载包
library(ggplot2)#绘图包
library(ggpubr)#基于ggplot2的可视化包，主要用于绘制符合出版要求的图形
library(ggsignif)#用于P值计算和显著性标记
library(tidyverse)#数据预处理
library(ggprism)#提供了GraphPad prism风格的主题和颜色，主要用于美化我们的图形
library(vioplot)#小提琴图绘制包
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization
#准备数据
# df <- read.table("data.txt",header = T,  check.names = F)
#自己随机编写的数据
df <- data.frame(
  A_1 = c(2,5,6,5,4,8,6,3,8,9),
  A_2 = c(5,8,6,3,4,7,9,3,6,4),
  B_1 = c(15,10,5,18,12,13,16,14,10,9),
  B_2 = c(25,20,23,15,14,24,20,22,25,26),
  C_1 = c(1,3,6,5,2,3,6,2,4,1),
  C_2 = c(7,8,9,6,7,8,9,6,7,10)
)
#预览数据
head(df)
#使用tidyverse包对数据进行处理
df <- df %>% 
  gather(key = 'samples',value = 'values') #gather()函数可以把多列数据合并成一列数据

#添加分组信息
df$group = rep(c("A","B","C"), each = 20)
head(df)#预览数据

###############绘图###############
###1、使用vioplot包进行绘制
??vioplot#查看具体参数

vioplot(values~samples, data = df, 
        main = "vioplot", # 设置标题
        col=c("#000000", "#be0027", "#cf8d2e","#e4e932","#2c9f45","#371777"),# 设置小提琴颜色
        xlab="Samples", ylab="values") 
#具体大家可以在参数中进行设置

###2、基于ggplot2包进行绘制，也是我们主要讲的
#基本绘图
p1 <- ggplot(df, aes(x=samples, y=values, fill=samples)) + 
  geom_violin()

p1

#添加箱线图及均值点
p2<-p1+geom_boxplot(alpha=1,outlier.size=0, size=0.3, width=0.2,fill="white")+
  stat_summary(fun="mean",geom="point",shape=21, size=2,fill="blue")
p2

#自定义颜色
col=c("#000000", "#be0027", "#cf8d2e","#e4e932","#2c9f45","#371777")
p3<-p2+scale_fill_manual(values = col)
p3

#分面
p4<-p3+facet_grid(~group,scales = 'free')
p4
  
##显著性标记
p5<-p1+geom_signif(comparisons = list(c("A_1","A_2"),
                                      c("B_1","B_2"),
                                      c("C_1","C_2")),# 设置需要比较的组
                   map_signif_level = T, #是否使用星号显示
                   test = t.test, ##计算方法
                   size=0.8,color="black")
p5

#结合ggprism包进行个性化设置
p <- ggplot(df, aes(x=samples, y=values, fill=group))+#指定数据
  geom_violin(trim = T,position = position_dodge(width = 0.1), scale = 'width')+#绘制小提琴图函数
  geom_boxplot(alpha=1,outlier.size=0, size=0.3, width=0.2,fill="white")+#添加箱线图
  stat_summary(fun="mean",geom="point",shape=21, size=2,fill="blue")+#均值点
  labs(x="Samples",y=NULL)+#标题
  # geom_jitter(width = 0.2,size=2,pch=20,color="black")+#添加抖动点
  theme_prism(palette = "flames",
              base_fontface = "plain", # 字体样式，可选 bold, plain, italic
              base_family = "serif", # 字体格式，可选 serif, sans, mono, Arial等
              base_size = 16,  # 图形的字体大小
              base_line_size = 0.8, # 坐标轴的粗细
              axis_text_angle = 45)+ # 可选值有 0，45，90，270
  scale_fill_prism(palette = "flames")+
  geom_signif(comparisons = list(c("A_1","A_2"),#显著性
                                 c("B_1","B_2"),
                                 c("C_1","C_2")),# 设置需要比较的组
              map_signif_level = T, #是否使用星号显示
              test = "t.test", ##计算方法
              tip_length = c(c(0.01,0.01),
                             c(0.01,0.01),
                             c(0.01,0.01)),#横线下方的竖线设置
              size=0.8,color="black")
p


#背景色
color <- colorRampPalette(brewer.pal(11,"BrBG"))(30)
#配色
col <- colorRampPalette(brewer.pal(9,"Set1"))(6)
####绘图模板
ggplot(df, aes(x=samples, y=values, fill=samples))+#指定数据
  geom_violin(trim = T,position = position_dodge(width = 0.1), scale = 'width')+#绘制小提琴图函数
  geom_boxplot(alpha=1,outlier.size=0, size=0.3, width=0.2,fill="white")+#添加箱线图
  stat_summary(fun="mean",geom="point",shape=21, size=2,fill="blue")+#均值点
  labs(x=NULL,y=NULL)+#标题
  theme_bw()+
  theme(panel.grid = element_blank(), #背景
        axis.line=element_line(),#坐标轴的线设为显示
        legend.position="none",#图例位置
        axis.text=element_text(color='#003b64',size=12),
        legend.text = element_text(color='#003b64',size=12),
        axis.title= element_text(size=12),
        axis.text.x=element_text(angle = 45,vjust = 1,hjust = 1))+
  scale_fill_manual(values = col)+
  geom_signif(comparisons = list(c("A_1","A_2"),#显著性
                                 c("B_1","B_2"),
                                 c("C_1","C_2")),# 设置需要比较的组
              map_signif_level = T, #是否使用星号显示
              test = "t.test", ##计算方法
              tip_length = c(c(0.01,0.01),
                             c(0.01,0.01),
                             c(0.01,0.01)),#横线下方的竖线设置
              size=0.8,color="black")

#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

```


---

### 小提琴图-添加数据点-半小提琴图-雨云图

```r

rm(list=ls())#clear Global Environment
setwd('D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\小提琴图-添加数据点-半小提琴图-雨云图')#设置工作目录

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(palmerpenguins) # Palmer Archipelago (Antarctica) Penguin Data
library(tidyverse) # Easily Install and Load the 'Tidyverse'
library(ggforce) # Accelerating 'ggplot2'
library(gghalves) # Compose Half-Half Plots Using Your Favourite Geoms
library(ggdist) # Visualizations of Distributions and Uncertainty

#使用palmerpenguin包中的数据
df <- penguins
# df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")
#使用tidyverse包对数据进行处理
df <- df %>% 
  drop_na()

##绘制小提琴图-无数据点模板
p1 <- ggplot(df, aes(x=species, y=flipper_length_mm, fill=species))+#指定数据
  geom_violin()+
  scale_fill_manual(values = c("#5cc3e8","#ffdb00","#79ceb8"))+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(color = 'black',size=12),
        axis.title = element_text(color = 'black',size=15),
        legend.position = "none")
p1

##绘制小提琴图-添加数据点模板
p2 <- ggplot(df, aes(x=species, y=flipper_length_mm, fill=species))+#指定数据
  geom_violin()+
  geom_sina(alpha=0.5,size=2,color="black")+
  scale_fill_manual(values = c("#5cc3e8","#ffdb00","#79ceb8"))+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(color = 'black',size=12),
        axis.title = element_text(color = 'black',size=15),
        legend.position = "none")
p2

##分组小提琴模板
p3 <- ggplot(df, aes(x=species, y=flipper_length_mm, fill=sex))+#指定数据
  geom_violin()+
  geom_sina(alpha=0.5,size=2,color="black")+
  scale_fill_manual(values = c("#5cc3e8","#ffdb00"))+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(color = 'black',size=12),
        axis.title = element_text(color = 'black',size=15),
        legend.title = element_text(color = 'red',size=15),
        legend.text = element_text(color = 'black',size=10))
p3

##半小提琴图绘制模板
p4 <- ggplot(df, aes(x=species, y=flipper_length_mm, fill=species))+#指定数据
  geom_half_violin()+
  scale_fill_manual(values = c("#5cc3e8","#ffdb00","#79ceb8"))+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(color = 'black',size=12),
        axis.title = element_text(color = 'black',size=15),
        legend.position = "none")
p4

##半小提琴图联合散点图、箱线图复杂图形绘制模板
p5 <- ggplot(df,aes(species,flipper_length_mm,fill=species))+
  geom_half_violin(position = position_nudge(x=0.25),side = "r",width=0.8,color=NA)+
  geom_boxplot(width=0.4,size=1.2,outlier.color =NA)+
  geom_jitter(aes(fill=species),shape=21,size=2.5,width=0.2)+
  scale_fill_manual(values = c("#5cc3e8","#ffdb00","#79ceb8"))+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(color = 'black',size=12),
        axis.title = element_text(color = 'black',size=15),
        legend.position = "none")
p5

##云雨图绘制模板1
p6 <- ggplot(df,aes(species,flipper_length_mm,fill=species))+
  geom_half_violin(position = position_nudge(x=0.25),side = "r",width=0.8)+
  geom_jitter(aes(fill=species),shape=21,size=2,width=0.15,color='black')+
  coord_flip()+
  scale_fill_manual(values = c("#5cc3e8","#ffdb00","#79ceb8"))+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(color = 'black',size=12),
        axis.title = element_text(color = 'black',size=15),
        legend.position = "none")
p6

##云雨图绘制模板2
p7 <- ggplot(df,aes(species,flipper_length_mm,fill=species))+
  stat_slab(aes(thickness = after_stat(pdf * n)),scale = 0.7)+#绘制半小提琴图
  stat_dotsinterval(side = "bottom", 
                    scale = 0.7, 
                    slab_size = NA)+#通过添加“stat_dotsinterval”功能，可以制作雨云图
  coord_flip()+
  scale_fill_manual(values = c("#5cc3e8","#ffdb00","#79ceb8"))+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(color = 'black',size=12),
        axis.title = element_text(color = 'black',size=15),
        legend.position = "none")
p7

##拼图
cowplot::plot_grid(p1,p2,p3,p4,p5,p7, ncol = 3)

```


---

### 云雨图

```r

###科研后花园####
####@wzs#####

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/云雨图')#设置工作目录

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(tidyverse) # Easily Install and Load the 'Tidyverse'
library(ggsignif) # Significance Brackets for 'ggplot2'
library(gghalves) # Compose Half-Half Plots Using Your Favourite Geoms

#这里使用我自己随机编写的数据
df <- data.frame(
  A = c(2,5,6,5,4,8,6,3,8,9),
  B = c(15,10,5,18,12,13,16,14,10,9),
  C = c(1,3,6,5,2,3,6,2,4,1),
  D = c(20,15,14,16,10,22,18,10,11,12)
)
#预览数据
head(df)

#使用tidyverse包对数据进行处理
df <- df %>% 
  gather(key = 'group',value = 'values')#gather()函数可以把多列数据合并成一列数据
head(df)#预览数据

#绘图
df$group <- factor(df$group,levels = c("A","B","C","D"))
p<-ggplot(df,aes(group,values,color=group))+#指定数据及坐标数据
  geom_half_violin(position = position_nudge(x = 0),side=1.5,size=1.2)+
  stat_boxplot(geom = "errorbar", width=0.1, size=1.2)+#添加误差线,注意位置，放到最后则这条先不会被箱体覆盖
  geom_boxplot(position="dodge",width=0.8,size=1.2)+#绘制箱线图函数
  geom_signif(comparisons = list(c("A","B"),
                                 c("A","D")),# 设置需要比较的组
              map_signif_level = T, #是否使用星号显示
              test = t.test, ##计算方法
              y_position = c(24,26),#图中横线位置设置
              tip_length = c(c(0.7,0.3),
                             c(0.7,0.2)),#横线下方的竖线设置
              size=1,color="#007fbd")+
  geom_jitter(alpha=0.3,width = 0.3,size=3)+#添加抖动点
  theme_bw()+
  theme(legend.position = 'none',#去除图例
        panel.grid = element_blank(),
        axis.text.x = element_text(angle = 45,vjust = 1,hjust = 1,size = 12),
        axis.text.y = element_text(size = 12))+
  scale_y_continuous(limits = c(0,28))+
  scale_color_manual(values=c("#3be8b0","#1aafd0","#6a67ce","#fc636b"))
p

```


---

## 🔥 六、热图

### 单列热图+文字注释+显著性注释+箭头注释

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/单列热图+文字注释+显著性注释+箭头注释')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics

#加载数据
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")

##绘图
#自定义颜色
col <- colorRampPalette(c("#00d1b2","white","#f99104"))(50)
#绘图
ggplot(df, aes(X, Y))+
  #绘制主体的热图
  geom_tile(aes(fill = value), width = 0.3, color = "white", linewidth = 0.1)+
  #在热图旁边添加相应文字注释
  geom_text(data=df[df$group=="A",], aes(1.8, Y, label = label), vjust = 0.5, hjust = 1)+
  geom_text(data=df[df$group=="B",], aes(3.3, Y, label = label), vjust = 0.5, hjust = 1)+
  #添加两条竖线
  geom_segment(aes(x=1.4,xend=1.4,y=0.5,yend=13.5), linetype = 1, color = "black",linewidth=0.6)+
  geom_segment(aes(x=2.7,xend=2.7,y=0.5,yend=13.5), linetype = 1, color = "black",linewidth=0.6)+
  #在竖直的线旁边添加相应文字信息
  geom_text(aes(1.3, 2, label = "Climatic"), angle = 90)+
  geom_text(aes(1.3, 9, label = "Substrate properties"), angle = 90)+
  geom_text(aes(2.6, 3, label = "Microbial properties"), angle = 90)+
  geom_text(aes(2.6, 9, label = "Water chemistry"), angle = 90)+
  ##添加显著性信息
  geom_text(data=df[df$group=="A",], aes(2, Y, label = sig), vjust = 0.5, hjust = 0.5, size = 6)+
  geom_text(data=df[df$group=="B",], aes(3.5, Y, label = sig), vjust = 0.5, hjust = 0.5, size = 6)+
  #反转坐标轴并调整范围
  scale_x_continuous(limits = c(1.3,3.8))+
  scale_y_reverse()+
  #这里通过分面形式给图形添加标题，普通标题添加方式暂时没找到怎么设置背景色
  facet_grid(~ facet, scales = "free")+
  #主题设置及图例设置
  theme_void()+
  theme(legend.position = "bottom",
        strip.background = element_rect(fill = "grey", color = "transparent"),
        strip.text = element_text(color="black",size=15))+
  scale_fill_gradientn(colors = col, limits = c(-0.3,0.3), name = "Standardized regression coefficients", 
                       breaks = c(-0.3, 0, 0.3))+
  guides(fill = guide_colorbar(barwidth = 10, title.position = "bottom",title.vjust = 1))

##通过调整RStudio图形窗口显示至合适大小，导出PDF，最后在AI软件中进行细节调整，包括标题及一些特殊字体格式

```


---

### 热图+显著性+间隔+注释+柱状图

```r

rm(list=ls())#clear Global Environment
#设置工作目录
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/热图+显著性+间隔+注释+柱状图")

##加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
#加载绘图数据
data1 <- read.table("data1.txt",sep="\t",header = T,check.names = F)
data2 <- read.table("data2.txt",sep="\t",header = T,check.names = F)

##数据清洗与转换
#为方便后续添加方框，需要将x和y轴转变成数值型，这里我们添加一列数据
data1$Y <- c(1,2,3,4)
data2$Y <- c(1,2,3,4)
#将数据转变成长格式
df1 <- melt(data1,id.vars = c("group","Y"))
#为方便后续添加方框，需要将x和y轴转变成数值型，这里我们添加一列数据
df1$X <- rep(1:9, each = 4)
#添加一个分组，方便后续进行间隔添加
df1$gap <- rep(c(1,2,3),times = c(4,4,28))

##绘制基本热图
p1 <- ggplot(df1, aes(X, Y)) +
  #添加圆周围的方框
  geom_rect(aes(xmin = X-0.5, xmax = X+0.5, ymin = Y-0.5, ymax = Y+0.5), color = "grey40",fill="white") +
  #绘制散点图，这里先将其中符合要求的点进行绘制
  geom_point(aes(size= ifelse(value > 0, value, 0),color=ifelse(value > 0, value, 0)))+
  #颜色
  scale_color_continuous(low = "white", high = "#23589e") +
  #将不符合要求的点使用固定大小和颜色的点显示
  geom_point(data = df1[df1$value == 0, ], shape = 21, size = 1, color = "black",fill="grey50")+
  #为图中不显著的数据添加NS标记
  geom_text(data = subset(df1, value > 0 & value < 0.5),
            aes(label = "NS"), size=4,color="#92461f",vjust=-0.1)+
  #自定义X轴和Y轴的标签
  scale_x_continuous(position = "top",breaks = c(1:9), labels = c("Overall transm.", "CosteaPl_2017_DEU", "BritolL_2016",
                                                 "Guinea-Bissau", "PasolliE_2018_MDG","PehrssonE_2016_PER",
                                                 "PehrssonE_2016_SLV","Ghana","Tanzania")) +
  scale_y_continuous(breaks = c(1:4), labels = data1$group)+
  #主题设置
  theme_void()+
  theme(axis.text.x = element_text(angle = 45,hjust = 0,vjust = 0,size=10,color="black"),
        axis.text.y = element_text(color="black",size=10,vjust = 0,hjust = 1))+
  #标题
  labs(x=NULL,y=NULL,color="SGB transmissibility")+
  guides(size = "none")+#去除size的图例
  #设置散点的显示范围
  scale_size_continuous(range = c(1,8))+
  #通过分面形式为图形添加间隔
  facet_grid(~gap,scales = 'free',space = "free")+
  theme(strip.text = element_blank())+
  #添加最下方的矩形注释
  geom_rect(data = df1[df1$gap == 2, ], aes(xmin = 1.5, xmax = 2.5, ymin = -Inf, ymax = 0.3),
            fill = "#6c3417")+
  geom_rect(data = df1[df1$gap == 3, ], aes(xmin = 2.5, xmax = 9.5, ymin = -Inf, ymax = 0.3),
            fill = "#68a030")
p1

#绘制柱状图
p2 <- ggplot(data2,aes(Y,value))+
  geom_col(fill="#b2b2b2",width = 0.8)+
  theme_classic()+
  theme(axis.text.x = element_text(color = "black",size=12),
        axis.ticks.x = element_line(color = "black",linewidth=0.8),
        axis.line.x = element_line(color = "black",linewidth=0.8),
        axis.text.y=element_blank(),
        axis.ticks.y=element_blank(),
        axis.line.y = element_blank(),
        plot.title = element_text(color="black",hjust = 0.5,size=15),
        plot.background = element_blank())+
  coord_flip()+#旋转图形
  labs(x=NULL,y=NULL,title = "Prevalence(%)")+
  scale_y_continuous(expand = c(0,0))
p2

###拼接图形
p1%>%aplot::insert_right(p2,width = 0.2)

###最后使用AI或者PS调整图形细节即可

```


---

### 热图+重要值计算及标记+解释度条形图

```r

rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/热图+重要值计算及标记+解释度条形图")

##加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(Hmisc) # Harrell Miscellaneous
library(randomForest) # Breiman and Cutler's Random Forests for Classification and Regression
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(caret) # Classification and Regression Training
library(aplot) # Decorate a 'ggplot' with Associated Information

##加载数据（随机编写，无实际意义）
otu <- read.table("otu.txt",sep="\t", row.names = 1, header = T, check.names = F)
env <- read.table("env.txt",sep="\t",row.names = 1, header = T, check.names = F)

#########取OTU数据前20行与env数据进行相关性分析（随机选取，无实际意义，可根据实际需要选取）
######rcorr函数计算
#合并数据
OTU <- as.data.frame(t(otu[1:20,]))
OTU$sample <- rownames(OTU)
env$sample <- rownames(env)
df <- merge(OTU,env,by="sample")
#相关性计算
data <- rcorr(as.matrix(df[2:31]),type="spear")#计算相关矩阵,或者pearson
#提取r和p值
df_r<-data$r
df_p<-data$P
df_r<-as.data.frame(df_r[1:20,21:30])
df_p<-as.data.frame(df_p[1:20,21:30])
##将数据转换为绘图所需数据
df_r$OTUID <- rownames(df_r)
df_R <- melt(df_r, id = 'OTUID')
df_R$OTUID <- factor(df_R$OTUID, levels = df_r$OTUID)
####计算Explained variation(%)及Importance(%)——随机森林
set.seed(2023)
#数据集划分
trains <- createDataPartition(y = df$pH,p=0.70,list = F)
traindata <- df[trains,]
testdata <- df[-trains,]
# 构建自变量与因变量之间的公式
form_reg <- as.formula(paste0("pH ~",
                              paste(colnames(traindata)[2:21],collapse = "+")))
form_reg
pH <- randomForest(form_reg, data=traindata, importance = TRUE, ntree = 500)
pH#结果解释：Var explained：47.16意味着使用随机森林方法计算OTU1被理化性质解释了47.16%，该值为图形上方的条形图
pH$importance#Importance(%)结果
#初步展示结果
varImpPlot(pH,main = "Variable Importance plot")

###同理，计算每一个env的随机森林并基于结果手动统计结果
##N_P
trains <- createDataPartition(y = df$N_P,p=0.70,list = F)
traindata <- df[trains,]
testdata <- df[-trains,]
form_reg <- as.formula(paste0("N_P ~",
                              paste(colnames(traindata)[2:21],collapse = "+")))
N_P <- randomForest(form_reg, data=traindata, importance = TRUE, ntree = 500)
N_P
##C_N
trains <- createDataPartition(y = df$C_N,p=0.70,list = F)
traindata <- df[trains,]
testdata <- df[-trains,]
form_reg <- as.formula(paste0("C_N ~",
                              paste(colnames(traindata)[2:21],collapse = "+")))
C_N<- randomForest(form_reg, data=traindata, importance = TRUE, ntree = 500)
C_N
##AK
trains <- createDataPartition(y = df$AK,p=0.70,list = F)
traindata <- df[trains,]
testdata <- df[-trains,]
form_reg <- as.formula(paste0("AK ~",
                              paste(colnames(traindata)[2:21],collapse = "+")))
AK <- randomForest(form_reg, data=traindata, importance = TRUE, ntree = 500)
AK
##AP
trains <- createDataPartition(y = df$AP,p=0.70,list = F)
traindata <- df[trains,]
testdata <- df[-trains,]
form_reg <- as.formula(paste0("AP ~",
                              paste(colnames(traindata)[2:21],collapse = "+")))
AP <- randomForest(form_reg, data=traindata, importance = TRUE, ntree = 500)
AP
##AN
trains <- createDataPartition(y = df$AN,p=0.70,list = F)
traindata <- df[trains,]
testdata <- df[-trains,]
form_reg <- as.formula(paste0("AN ~",
                              paste(colnames(traindata)[2:21],collapse = "+")))
AN <- randomForest(form_reg, data=traindata, importance = TRUE, ntree = 500)
AN
##TK
trains <- createDataPartition(y = df$TK,p=0.70,list = F)
traindata <- df[trains,]
testdata <- df[-trains,]
form_reg <- as.formula(paste0("TK ~",
                              paste(colnames(traindata)[2:21],collapse = "+")))
TK <- randomForest(form_reg, data=traindata, importance = TRUE, ntree = 500)
TK
##TP
trains <- createDataPartition(y = df$TP,p=0.70,list = F)
traindata <- df[trains,]
testdata <- df[-trains,]
form_reg <- as.formula(paste0("TP ~",
                              paste(colnames(traindata)[2:21],collapse = "+")))
TP <- randomForest(form_reg, data=traindata, importance = TRUE, ntree = 500)
TP
##TN
trains <- createDataPartition(y = df$TN,p=0.70,list = F)
traindata <- df[trains,]
testdata <- df[-trains,]
form_reg <- as.formula(paste0("TN ~",
                              paste(colnames(traindata)[2:21],collapse = "+")))
TN <- randomForest(form_reg, data=traindata, importance = TRUE, ntree = 500)
TN
##SOM
trains <- createDataPartition(y = df$SOM,p=0.70,list = F)
traindata <- df[trains,]
testdata <- df[-trains,]
form_reg <- as.formula(paste0("SOM ~",
                              paste(colnames(traindata)[2:21],collapse = "+")))
SOM <- randomForest(form_reg, data=traindata, importance = TRUE, ntree = 500)
SOM

##读取Explained variation(%)统计结果
df_EV <- read.table("Explained variation(%).txt",sep="\t", header = T, check.names = F)
df_EV$env <- factor(df_EV$env, levels = df_EV$env)
##统计Importance(%)结果
df_Importance <-as.data.frame(pH$importance)
df_Importance <- df_Importance[-2]
colnames(df_Importance) <- "pH"
df_Importance$N_P <- N_P$importance[1:20]
df_Importance$C_N <- C_N$importance[1:20]
df_Importance$AK <- AK$importance[1:20]
df_Importance$AP <- AP$importance[1:20]
df_Importance$AN <- AN$importance[1:20]
df_Importance$TK <- TK$importance[1:20]
df_Importance$TP <- TP$importance[1:20]
df_Importance$TN <- TN$importance[1:20]
df_Importance$SOM <- SOM$importance[1:20]
#数据过滤——小于0的及空值全部过滤
df_Importance[df_Importance<0] <- 0
df_Importance[is.na(df_Importance<0)] <- 0
df_Importance$OTUID <- rownames(df_Importance)#将行名作为新列加入
write.csv(df_Importance,file = "Importance(%).CSV")#写出重要性数据到默认路径
##将数据转换为绘图所需数据
df_Importance2 <- melt(df_Importance, id = 'OTUID')

####绘图
#绘制带有圆圈的热图
p1 <- ggplot(df_R, aes(variable, OTUID))+
  #热图
  geom_tile(aes(fill=value), color = "grey90")+
  #基于Importance(%)结果绘制圆圈
  geom_point(data=df_Importance2[df_Importance2$value>0,], aes(variable, OTUID, size = value), shape = 1)+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.y = element_text(size=10, color = "black"),
        axis.text.x = element_text(size=10, color = "black", angle = 45, hjust = 1, vjust = 1))+
  labs(x = NULL, y = NULL, fill = "Correlation", size = "Importance(%)")+
  scale_fill_gradientn(limit = c(-1, 1), colors = c('#2D6DB1', 'white', '#DC1623'))+
  scale_size_continuous(range = c(2,7))
p1
#基于Explained variation(%)统计结果绘制条形图
p2 <- ggplot(df_EV, aes(env, `Explained variation(%)`))+
  geom_col(fill = "#ff9c2a")+
  theme_classic()+
  theme(axis.text.y = element_text(size=9, color = "black"),
        axis.text.x = element_blank(),
        axis.ticks.x = element_blank(),
        axis.title.y = element_text(size=10, color = "black"))+
  labs(x = NULL, y = "Explained variation(%)")+
  scale_y_continuous(expand = c(0,0))
p2  

##拼图
p1%>%insert_top(p2, height = 0.3)


#参考：
# 1）https://blog.csdn.net/amyniez/article/details/129215149；
# 2）https://mp.weixin.qq.com/s/nnsH3OqOjLY5KKYh93_FGA

```


---

### 热图+柱状堆积图

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/热图+柱状堆积图')#设置工作路径

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(aplot) # Decorate a 'ggplot' with Associated Information

#加载数据
df <- read.table("data.txt",header = 1,check.names = F)
df$group <- factor(df$group,levels = c("F","CK"))
df$species <- factor(df$species,levels = c("Pedobacter","Aridibacter","Devosia","Rhizobium",
                                           "Phenylobacterium","Arthrobacter","Bradvrhizobium",
                                           "Pseudomonas","Gemmatimonas","Sphingomonas"))

##绘制热图
#设置渐变色
col <- colorRampPalette(c("#0066b2","#fdbd10","#ec1c24"))(50) #设置渐变色
p1 <- ggplot(df,aes(group,species,fill=value))+
  #绘制热图
  geom_tile(color="black")+
  #添加数值
  geom_text(aes(label = value), color = 'white', size = 5)+
  #标题
  labs(x=NULL,y=NULL,fill=NULL)+
  #颜色
  scale_fill_gradientn(colours = col)+
  #主题
  theme_void()+
  theme(axis.text.x = element_text(color = "black",size=12),
        axis.text.y = element_text(color = "black",size=12,hjust = 1),
        legend.position = "right")#去除图例
p1

##绘制柱状堆积图
p2 <- ggplot(df,aes(species,value,fill=group))+
  #柱状堆积图
  geom_col()+
  coord_flip()+
  #标题
  labs(x=NULL,y=NULL,fill=NULL)+
  #颜色
  scale_fill_manual(values = c("#f0b240","#62d7f6"))+
  #主题
  theme_classic()+
  theme(axis.text.x = element_text(color = "black",size=12),
        axis.text.y = element_blank(),
        axis.line.x = element_line(color = "black",linewidth = 0.8),
        axis.line.y = element_blank(),
        axis.ticks.y = element_blank(),
        axis.ticks.length.x = unit(-0.15, "cm"),
        axis.ticks.x = element_line(color = "black",linewidth = 0.8),
        legend.position = "right")+#图例设置
  scale_y_continuous(expand = c(0,0),breaks = c(0,5,10,15,20,25))#设置刻度从0开始
p2

##拼图
p1%>%insert_right(p2,width = 2)

```


---

### 三角形热图+聚类+柱状图注释

```r

rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/三角形热图+聚类+柱状图注释")

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(ggtree) # an R package for visualization of tree and annotation data
library(ape) # Analyses of Phylogenetics and Evolution
library(vegan) # Community Ecology Package
library(aplot) # Decorate a 'ggplot' with Associated Information
##加载数据（随机编写，无实际意义）
df <- read.table("data1.txt", check.names = F, header = 1)
df2 <- read.table("data2.txt", check.names = F, header = 1)

##数据整理-将宽数据转换为长数据格式
df1 <- melt(df)
# 创建形状列
df1$shape <- ifelse(df1$value > 0, "up", "down")

##绘制三角热图
p1 <- ggplot(df1, aes(Gene, variable, size = value, fill = value, shape = shape))+
  geom_point(color = "black")+
  #自定义形状
  scale_shape_manual(values = c("up" = 24, "down" = 25))+
  #自定义颜色
  scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0)+
  #自定义大小
  scale_size_continuous(range = c(0.5,4))+
  #y轴调整
  scale_y_discrete(position = "right")+
  labs(x = NULL, y = NULL)+
  #图例调整
  guides(size = "none",
         shape=guide_legend(override.aes = list(size=3)))+
  theme_classic()+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1))
p1

##进化树的构建
#处理数据
df3 <- df
rownames(df3) <- df3$Gene
df3 <- df3[-1]
#计算距离矩阵
df_dist <- vegdist(t(df3),method = 'bray')#使用bray curtis方法计算距离矩阵
####进行层次聚类,可选择方法有single、complete、median、mcquitty、average 、centroid 、ward 
df_hc <- hclust(df_dist,method="average")#使用类平均法进行聚类
#绘图
plot(as.dendrogram(df_hc),type="rectangle",horiz=T)#实现将垂直的聚类树变成水平聚类树，绘图
# 将聚类结果转成系统发育格式
df_tree <- as.phylo(df_hc)
# 对树分组
gro <- list(group1=c("A","E","F","H"),
            group2=c("B","C","D","G"))
# 将分组信息和进化树组合到一起
tree<-groupOTU(df_tree, gro)
# ggtree绘图
p2 <- ggtree(tree,aes(color=group),size=1,show.legend = F)+
  geom_tiplab(size=5,align = F,show.legend = F)
p2
#去除分支名称
p2 <- ggtree(tree,aes(color=group),size=0.8,show.legend = F)
p2
##组合
p1%>%insert_left(p2,width = 0.15)

###绘制顶部的注释柱状图
p3 <- ggplot(df2, aes(Gene, Abundance))+
  geom_col()+
  #y轴调整
  scale_y_continuous(position = "right", breaks = c(0,10),
                     expand = c(0,0),limits = c(0,12))+
  theme_classic()+
  theme(axis.text.x = element_blank(),
        axis.text.y = element_text(vjust = 0),
        axis.title.y=element_text(size=8),
        axis.line.y = element_line(linewidth = 1, color = "black"),
        axis.line.x = element_line(linewidth = 1, color = "grey60"),
        axis.ticks = element_blank())+
  labs(x = NULL)
p3
p4 <- ggplot(df2, aes(Gene, Prevalence))+
  geom_col()+
  #y轴调整
  scale_y_continuous(position = "right", breaks = c(0,1), 
                     expand = c(0,0),limits = c(0,1.2))+
  theme_classic()+
  theme(axis.text.x = element_blank(),
        axis.title.y=element_text(size=8),
        axis.text.y = element_text(vjust = 0),
        axis.line.y = element_line(linewidth = 1, color = "black"),
        axis.line.x = element_line(linewidth = 1, color = "grey60"),
        axis.ticks = element_blank())+
  labs(x = NULL)
p4

##组合图形
p1%>%insert_left(p2,width = 0.1) %>% 
  insert_top(p3,height = 0.3) %>% 
  insert_top(p4,height = 0.3)

```


---

### 环形热图

```r

rm(list=ls())#clear Global Environment
setwd('D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\ggtree画环形热图')#设置工作路径

#安装包
if(!requireNamespace("BiocManager", quietly = T))
  install.packages("BiocManager") 
BiocManager::install("ComplexHeatmap")
install.packages("circlize")

#加载包
library(circlize)
library(ComplexHeatmap)


#读取数据
df <- read.table(file="example.txt",sep="\t",header=T,check.names=FALSE,row.names = 1)
#常规热图
Heatmap(df)
###绘制环形热图
#颜色
color <- colorRamp2(c(-5, 0, 5), c("blue", "white", "green"))
circos.par(gap.after = c(20))#空出一段用于添加组名
circos.heatmap(df, #数据
               col = color,#颜色
               dend.side = "inside",#确定聚类结果放在圈内还是圈外
               rownames.side = "outside",#组名
               track.height = 0.4
               # clustering.method = "complete",#归一化处理
               # distance.method = "euclidean"#聚类方法，默认为欧氏距离
               )
#添加组名
circos.track(track.index = get.current.track.index(), panel.fun = function(x, y) {
  if(CELL_META$sector.numeric.index == 1) {
    A = length(colnames(df))
    circos.text(rep(CELL_META$cell.xlim[2], A) + convert_x(0.2, "mm"), #x坐标
                28+(1:A)*10,#y坐标
                colnames(df), #标签
                cex = 0.5, adj = c(0, 1), facing = "inside")
  }
}, bg.border = NA)
##组名的标签位置需要耐心调整参数以到合适的位置，当然也可以导出PDF在AI中进行添加及位置调整
#添加图例
grid.draw(Legend(title = "Title", col_fun = color))

circos.clear()#清除参数，如果前面需要调整参数，必须先执行此命令，否则绘制的新图会和之前的图重叠在一起

#可以再加一个热图
color2=colorRamp2(c(-5, 0, 5), c("green", "white", "red"))
circos.heatmap(df,  col = color, dend.side = "outside")
circos.heatmap(df, col = color2,rownames.side = "inside")

circos.clear()#清除参数，如果前面需要调整参数，必须先执行此命令，否则绘制的新图会和之前的图重叠在一起


#参考资料：https://jokergoo.github.io/circlize_book/book/
??circos.heatmap
circos.heatmap(mat, split = NULL, col, na.col = "grey",
               cell.border = NA, cell.lty = 1, cell.lwd = 1,
               bg.border = NA, bg.lty = par("lty"), bg.lwd = par("lwd"),
               ignore.white = is.na(cell.border),
               cluster = TRUE, clustering.method = "complete", distance.method = "euclidean",
               dend.callback = function(dend, m, si) reorder(dend, rowMeans(m)),
               dend.side = c("none", "outside", "inside"), dend.track.height = 0.1,
               rownames.side = c("none", "outside", "inside"), rownames.cex = 0.5,
               rownames.font = par("font"), rownames.col = "black",
               show.sector.labels = FALSE, cell_width = rep(1, nrow(mat)), ...)

```


---

### 双层环形热图+不同方式显著性标注

```r

#设置工作环境
rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/双层环形热图+不同方式显著性标注")

##加载R包（没有安装相关包的同学可以先安装相应的R包）
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(psych) # Procedures for Psychological, Psychometric, and Personality Research
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(dplyr) # A Grammar of Data Manipulation
library(agricolae) # Statistical Procedures for Agricultural Research

#####内层热图——颜色与样本归一化值呈正相关
#加载数据
df3 <- as.data.frame(t(read.table("data_内层.txt", sep="\t", header=T, check.names=F,row.names = 1)))
df3$sample <- rownames(df3)
group <- read.table("group.txt", sep="\t", header=T, check.names=F)
#合并分组与数据
df3 <- merge(df3,group,by="sample")
rownames(df3) <- df3$sample
df3 <- df3[-1]
#将宽数据转换为长数据
df4 <- melt(df3, id.vars = c("group"))
##利用循环并采用多重比较法比较各组显著性
#初始化
variance<-aov(Ni ~ group, data=df3)
MC <- LSD.test(variance,"group", p.adj="none")
GB<- group_by(df3,group)
sg<- MC$groups
sg$group <- rownames(sg)
#修改列名
colnames(sg)[2] <- "Ni_label"
for (i in colnames(df3[2:12])) {
  variance<-aov(df3[,i] ~ group, data=df3)
  MC <- LSD.test(variance,"group", p.adj="none")
  data <- MC$groups
  data$group <- rownames(data)
  colnames(data)[1:2]<-c(i,paste0(i,"_label"))
  sg<-merge(sg,data,by="group")
}
#将数据和字母分开储存
df_label <- sg[c(1,3,5,7,9,11,13,15,17,19,21,23,25)]
df_data <- sg[c(1,2,4,6,8,10,12,14,16,18,20,22,24)]
rownames(df_data) <- df_data$group
#数据标准化（0-1）——根据个人数据选择方法处理
df_data2 <- as.data.frame(lapply(df_data[2:13], function(x) (x - min(x)) / (max(x) - min(x))))
df_data2$group <- df_data$group
#转换为长数据
df_label2 <- melt(df_label, id.vars = c("group"))
df_data3 <- melt(df_data2, id.vars = c("group"))
##增加空白间隔-通过转换为数值型x轴实现
#这里在As和Cu之间增加空白间隔并在首位增加间隔
#添加x列数据
df_data3$x <- rep(c(1:5,7:13),each=5)
df_label2$x <- rep(c(1:5,7:13),each=5)
#添加y列数据
df_data3$y <- rep(c(1:5),times=12)
df_label2$y <- rep(c(1:5),times=12)
##计算标签角度
number_of_bar <- 15
angle <-  90 - 360 * (df_label2$x-0.5) /(number_of_bar)
df_label2$angle<-ifelse(angle < -90, angle+180, angle)

##基于ggplot2绘图
ggplot()+
  #绘制热图
  geom_tile(data=df_data3,aes(x,y,fill=value),#x轴和y轴都需要用添加的数值型数据绘制
            color="grey",linewidth=0.6)+
  #自定义颜色
  scale_fill_gradientn(limit = c(0, 1), colors = c('white', '#fd5c63'))+
  #添加显著性标签
  geom_text(data=df_label2,aes(x,y,label = value,angle=angle))+#x轴和y轴都需要用添加的数值型数据绘制
  #转换为极坐标
  coord_polar()+
  #主题相关设置
  theme_void()+
  theme(panel.grid = element_blank(),
        axis.text.x=element_text(size = 11, color = "black"),
        legend.position = "top")+
  #去除轴标题并指定图例标题
  labs(x=NULL,y=NULL,fill="Normalize")+
  #自定义x轴标签，注意需要按照此前添加顺序指定
  scale_x_continuous(limits = c(0,15),
                     breaks = c(1,2,3,4,5,7,8,9,10,11,12,13),
                     labels = c("Ni","Pb","Cr","Cd","As","Cu","Zn",
                                "Mo","Mn","Fe","B","S"))+
  #设置y轴范围
  #注意：这里的范围内层与外层图要一致且同时包含内外层，以便后续在AI中拼图
  scale_y_continuous(limits = c(-1.5,8.5))+
  #添加内层分组
  annotate("rect", xmin = 0.5, xmax = 5.5, ymin = 0.1, ymax = 0.4, fill="#00c4ff")+
  annotate("rect", xmin = 6.5, xmax = 13.5, ymin = 0.1, ymax = 0.4, fill="#11862f")+
  #手动添加y轴标签
  annotate("text", x = 14 , y = 1, label = "AK", size=3.5, color = "black",angle=30)+
  annotate("text", x = 13.9 , y = 2, label = "BK", size=3.5, color = "black",angle=30)+
  annotate("text", x = 13.8 , y = 3, label = "CK", size=3.5, color = "black",angle=30)+
  annotate("text", x = 13.8 , y = 4, label = "DK", size=3.5, color = "black",angle=30)+
  annotate("text", x = 13.8 , y = 5, label = "EK", size=3.5, color = "black",angle=30)->p1
p1


#####外层热图——pearson相关性
#加载数据（随机编写，无实际意义）
df1 <- read.table("data1_外层.txt", sep="\t", header=T, check.names=F)
df2 <- read.table("data2_外层.txt", sep="\t", header=T, check.names=F)
#合并数据
data <- merge(df1,df2,by="sample")
#将行名设置为样本名并删除多余列
rownames(data) <- data$sample
data <- data[-1]
#计算相关性并提取R值与P值
cor<- corr.test(data, method="pearson",adjust="BH")
r.cor<-data.frame(cor$r)[1:12,13:14]
p.cor<-data.frame(cor$p)[1:12,13:14]
#将宽数据转换为长数据
r.cor$G <- rownames(r.cor)
df_r <- melt(r.cor, id.vars = c("G"), 
             measure.vars = c("groupA","groupB"))
#指定顺序
df_r$G <- factor(df_r$G,levels = c("Ni","Pb","Cr","Cd","As","Cu","Zn",
                                   "Mo","Mn","Fe","B","S"))
p.cor$G <- rownames(p.cor)
df_p <- melt(p.cor, id.vars = c("G"), 
             measure.vars = c("groupA","groupB"))
#通过不同p值转换为*
df_p$sg <- ifelse(df_p$value>=0.05, "", ifelse(df_p$value<0.05&df_p$value>0.01,"*", 
                                               ifelse(df_p$value<=0.01&df_p$value>0.001,"**","***")))
##增加空白间隔-通过转换为数值型x轴实现
#这里在As和Cu之间增加空白间隔并在首位增加间隔
#添加x列数据
df_r$x <- c(1:5,7:13)
df_p$x <- c(1:5,7:13)
##将外层图片y轴设置为紧邻内层数据并间隔1
df_r$y <- rep(c(7:8),each=12)
df_p$y <- rep(c(7:8),each=12)
##计算标签角度
number_of_bar <- 15
angle <-  180 - 360 * (df_p$x-0.5) /(number_of_bar)
df_p$angle<-ifelse(angle < -90, angle+180, angle)

#基于ggplot2绘图
ggplot()+
  #热图
  geom_tile(data=df_r,aes(x,y,fill=value),#x轴和y轴都需要用添加的数值型数据绘制
            color="grey",linewidth=0.6)+
  #自定义颜色
  scale_fill_gradientn(limit = c(-1, 1), colors = c('#0099cc', 'white', '#ff9933'))+
  #显著性标签
  geom_text(data=df_p,aes(x,y,label = sg,angle=angle))+#x轴和y轴都需要用添加的数值型数据绘制
  #极坐标
  coord_polar()+
  #主题设置
  theme_void()+
  theme(panel.grid = element_blank(),
        axis.text.x=element_text(size = 11, color = "black"),
        legend.position = "top")+
  #去除轴标题并指定图例标题
  labs(x=NULL,y=NULL,fill="Pearson r")+
  #自定义x轴标签，注意需要按照此前添加顺序指定
  scale_x_continuous(limits = c(0,15),
                     breaks = c(1,2,3,4,5,7,8,9,10,11,12,13),
                     labels = c("Ni","Pb","Cr","Cd","As","Cu","Zn",
                                "Mo","Mn","Fe","B","S"))+
  #设置y轴范围
  #注意：这里的范围内层与外层图要一致且同时包含内外层，以便后续在AI中拼图
  scale_y_continuous(limits = c(-1.5,8.5))+
  #自定义y轴标签
  annotate("text", x = 13.8 , y = 7, label = "groupA", size=3, color = "black",angle=30)+
  annotate("text", x = 13.8 , y = 8, label = "groupB", size=3, color = "black",angle=30)->p2
p2

###由于ggplot2包中极坐标形式图形的拼图限制，这里需要将图形保存后在AI软件中拼接
##拼接方法：将图1选中平移到图2中心即可
library(patchwork)
p1+p2+
  plot_layout(guides = 'collect')
##最后在AI软件中拼图并对细节进行调整


######拓展——常规绘制并进行拼接
#内层图形
ggplot()+
  geom_tile(data=df_data3,aes(x,group,fill=value),
            color="grey",linewidth=0.6)+
  scale_fill_gradientn(limit = c(0, 1), colors = c('white', '#fd5c63'))+
  geom_text(data=df_label2,aes(x,group,label = value))+
  theme_void()+
  theme(panel.grid = element_blank(),
        axis.text.x=element_text(size = 11, color = "black"),
        legend.position = "top")+
  labs(x=NULL,y=NULL,fill="Normalize")+
  scale_x_continuous(limits = c(0,15),
                     breaks = c(1,2,3,4,5,7,8,9,10,11,12,13),
                     labels = c("Ni","Pb","Cr","Cd","As","Cu","Zn",
                                "Mo","Mn","Fe","B","S"))+
  #添加内层分组
  annotate("rect", xmin = 0.5, xmax = 5.5, ymin = 0.1, ymax = 0.4, fill="#00c4ff")+
  annotate("rect", xmin = 6.5, xmax = 13.5, ymin = 0.1, ymax = 0.4, fill="#11862f")+
  #手动添加y轴标签
  annotate("text", x = 13.8 , y = 1, label = "AK", size=3.5, color = "black")+
  annotate("text", x = 13.8 , y = 2, label = "BK", size=3.5, color = "black")+
  annotate("text", x = 13.8 , y = 3, label = "CK", size=3.5, color = "black")+
  annotate("text", x = 13.8 , y = 4, label = "DK", size=3.5, color = "black")+
  annotate("text", x = 13.8 , y = 5, label = "EK", size=3.5, color = "black")->p3
p3
#外层图形
ggplot()+
  geom_tile(data=df_r,aes(x,variable,fill=value),
            color="grey",linewidth=0.6)+
  scale_fill_gradientn(limit = c(-1, 1), colors = c('#0099cc', 'white', '#ff9933'))+
  geom_text(data=df_p,aes(x,variable,label = sg))+
  theme_void()+
  theme(panel.grid = element_blank(),
        legend.position = "top")+
  labs(x=NULL,y=NULL,fill="Pearson r")+
  scale_x_continuous(limits = c(0,15),
                     breaks = c(1,2,3,4,5,7,8,9,10,11,12,13),
                     labels = c("Ni","Pb","Cr","Cd","As","Cu","Zn",
                                "Mo","Mn","Fe","B","S"))+
  annotate("text", x = 14 , y = 1, label = "groupA", size=3.5, color = "black")+
  annotate("text", x = 14 , y = 2, label = "groupB", size=3.5, color = "black")->p4
p4

##拼图
library(aplot)
p3 %>% insert_top(p4, height = 0.4)

```


---

### heatmap

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/热图')#设置工作路径

#加载R包
library (pheatmap)
#读取数据
df <- read.table(file="data.txt",sep="\t",row.names = 1, header=T,check.names=FALSE)
#查看前3行
head(df)[1:5,]
####Z-score转换以保留数据的真实差异
df1 <-df[apply(df,1,var)!=0,]  ##去掉方差为0的行，也就是值全都一致的行
df_zscore <-as.data.frame(t(apply(df1,1,scale)))#标准化数据，获得Z-score
colnames(df_zscore)<- colnames(df)
###初步绘图
pheatmap(df_zscore,
         angle_col = "45", 
         cellwidth=25, cellheight=8, 
         treeheight_col = 15)
#设置颜色
pheatmap(df_zscore,
         angle_col = "45", 
         cellwidth=25, cellheight=8, 
         treeheight_col = 15,
         color=colorRampPalette(c("#3952a2","black","#f5ea14"))(100))
#添加行注释信息
annotation_col<- data.frame( "Treatment" = c("Saline","Saline","Saline","Cocaine","Saline",
                                           "LSD","LSD","LSD","LSD","Saline",
                                           "Saline","Saline","MDMA","MDMA","MDMA",
                                           "Ketamine","Ketamine","Ketamine","Ketamine","Ketamine"),
                            "Batch" = c("1","1","1","1","2",
                                       "1","2","3","2","1",
                                       "2","2","2","1","2",
                                       "1","3","3","3","3"),
                             "Post_treatment" = c("48 h","2 wk","2 wk","48 h","48 h",
                                                "48 h","2 wk","48 h","48 h","2 wk",
                                                "48 h","2 wk","2 wk","2 wk","2 wk",
                                                "2 wk","48 h","48 h","48 h","48 h"),
                            "Critical_period" = c("Closed","Closed","Closed","Closed","Closed",
                                                   "Closed","Closed","Closed","Closed","Open",
                                                   "Open","Open","Open","Open","Open",
                                                   "Open","Open","Open","Open","Open"))#行注释矩阵
rownames(annotation_col) = colnames(df_zscore)
colors  <-  list("Treatment" = c(Saline = "#000000", Cocaine = "#575757",LSD = "#e79600",MDMA="#a42422",Ketamine="#c53a8e"), 
                 "Batch" = c( "1"= "#3953a3", "2" = "#ef4a4a", "3" = "#009848"),
                 "Post_treatment" = c("48 h"="#64838c","2 wk"="#2c3a3e"),
                 "Critical_period" = c(Closed="#94c83d",Open="#4e2469"))
pheatmap(df_zscore,
         angle_col = "45", 
         cellwidth=25, cellheight=8, 
         treeheight_col = 15,
         color=colorRampPalette(c("#3952a2","black","#f5ea14"))(100),
         annotation_col = annotation_col,
         annotation_colors = colors,
         show_colnames = F)
###美化
pheatmap(df_zscore,
         angle_col = "45", 
         cellwidth=25, cellheight=8, 
         treeheight_col = 15,
         color=colorRampPalette(c("#3952a2","black","#f5ea14"))(100),
         annotation_col = annotation_col,
         annotation_colors = colors,
         show_colnames = F,
         fontsize_row=9, fontsize=12,
         labels_row = as.expression(lapply(rownames(df_zscore),function(x) bquote(italic(.(x))))),#行名斜体
         filename = "heatmap.pdf")

```


---

## 🍩 七、饼图 & 圆环图 & 旭日图

### 饼图

```r

rm(list=ls())

#数据——随机生成
df<-data.frame(
  group=c('A', 'B', 'C', 'D', 'E'),
  value=c(55,75,20,60,100))

###使用pie()函数绘制
col<-rainbow(5)
pie(df$value, #扇形数值大小
    labels = df$group, #各扇形面积标签
    radius = 0.9,#饼图半径
    main = 'Pie',#标题
    clockwise = FALSE, #饼图各个切片是否按顺时针做出分割
    col = col)#自定义颜色
legend("topright", df$group, cex = 0.8,fill = col)#图例

pie(df$value, #扇形数值大小
    labels = df$group, #各扇形面积标签
    radius = 0.9,#饼图半径
    main = 'Pie',#标题
    clockwise = FALSE, #饼图各个切片是否按顺时针做出分割
    density = 20, # 设置阴影线密度
    angle = 45,#设置阴影线角度
    col = rainbow(5))#自定义颜色

###ggplot2包绘制
library(ggplot2)
ggplot(df, aes(x="", y = value, fill = group))+#数据
  geom_bar(width = 1, stat = "identity",color="white")+#绘制柱状图
  coord_polar('y')+#变为极坐标
  theme_void()+#主题
  scale_fill_manual(values=rainbow(5))+#自定义颜色
  geom_text(aes(y = sum(value)-cumsum(value)+value/2,
                    label = scales::percent(value/sum(value))), size=4.5)#标签
  

###ggstatsplot包绘制饼图
#以数据集mtcars为例
df1<-mtcars
library(ggstatsplot)
ggpiestats(df1, 'vs', #数据
           direction = 1, #方向，通过1和-1调整
           title = "Pie",#标题
           factor.levels = df1$vs,#标签
           slice.label = 'percentage',#标签类型，percentage/counts/both
           perc.k = 2,#百分数小数位数
           results.subtitle = F) #标题是否显示统计结果


###pie3D()函数绘制3D饼图
library(plotrix)
col<-rainbow(5)
pie3D(df$value, #数据
      labels = df$group, #标签
      theta = pi/5, 
      labelcex=1.2, #标签大小
      main = "3D pie",#标题
      explode = 0.1, #各扇形间隔
      height = 0.08,#各扇形高度
      radius = 1,#半径，0~1
      col = rainbow(5))#颜色
legend("topright", df$group, cex = 0.8,fill = col)#图例

###ggpubr包绘制
library(ggpubr)
ggpie(df, "value", #数据
      label = "group",#标签
      lab.pos = 'in',#标签位置
      lab.font = c(5, 'white'),#标签大小及颜色
      fill = "group", #填充
      color = "grey",#间隔颜色
      palette = rainbow(5))#填充颜色

###fan.plot()函数绘制扇形
library(plotrix)
col<-rainbow(5)
fan.plot(df$value,#绘图数据
         radius=1,#半径
         col=col,#填充颜色
         labels=df$group,#标签
         label.radius=1.1,#标签距扇形的距离
         align="left",#扇形对齐的位置
         main="Fan plot")#标题
legend("right", df$group, cex = 0.9,fill = col)#图例
# 参考：各函数帮助文档

```


---

### 圆环图&旭日图_ggplot2

```r

rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/圆环图&旭日图_ggplot2")

##绘图思路：
   #通过ggplot2绘制单组或多组条形图，然后变换坐标系即可获圆环图及多环图
   #绘制旭日图时需要调整x轴位置确定各个环的所在位置


###加载所需R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(formattable) # Create 'Formattable' Data Structures

##加载数据（随即编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")
head(df) 

###根据不同分组计算其值和及标签位置
##group1
#使用aggregate函数计算每个组的值和
data1 <- aggregate(value ~ group1, df, sum)
#计算相对丰度
data1$Rel <- data1$value/sum(data1$value)
#转换为百分比
data1$per <- percent (data1$Rel,1)
data1$group1 <- factor(data1$group1, levels = c("g1","g2","g3","g4","g5"))
#确定标签位置
data1$ymax<-cumsum(data1$Rel)
data1$ymin<-c(0,head(data1$ymax,n=-1))
data1$labelposition<-(data1$ymax + data1$ymin)/2

##group2
data2 <- aggregate(value ~ group2, df, sum)
data2$Rel <- data2$value/sum(data2$value)
data2$per <- percent (data2$Rel,1)
data2$group2 <- factor(data2$group2, levels = c("A","B","C"))
data2$ymax<-cumsum(data2$Rel)
data2$ymin<-c(0,head(data2$ymax,n=-1))
data2$labelposition<-(data2$ymax + data2$ymin)/2

##group3
data3 <- aggregate(value ~ group3, df, sum)
data3$Rel <- data3$value/sum(data3$value)
data3$per <- percent (data3$Rel,1)
data3$group3 <- factor(data3$group3, levels = c("G1","G2"))
data3$ymax<-cumsum(data3$Rel)
data3$ymin<-c(0,head(data3$ymax,n=-1))
data3$labelposition<-(data3$ymax + data3$ymin)/2

#########绘制圆环图#############
p1 <- ggplot(data1,aes(ymax=ymax,ymin=ymin,
                xmax=3,xmin=2))+
  #通过方块先绘制柱状堆积图
  geom_rect(aes(fill=group1))+
  #添加标签
  geom_text(x=2.5,aes(y=labelposition,label=paste0(group1,"\n(",per,")")),size=4, color = "black")+
  #通过拉大x轴范围实现环图绘制
  xlim(1,3)+
  #转换为极坐标
  coord_polar(theta="y")+
  theme_void()+
  theme(legend.position = "none")+
  #自定义颜色
  scale_fill_manual(values = c("#ffaaaa", "#ffc2e5","#ebffac","#c1f1fc","#00c7f2"))
p1
##在环图中间增加空白间隔
p2 <- p1+ylim(0,1.1)
p2


###########绘制双环图################
p3 <- ggplot()+
  #通过方块先绘制第一层饼图
  geom_rect(data=data2,aes(ymax=ymax,ymin=ymin,
                      xmax=2,xmin=0,#x轴0-2绘制第一层
                      fill=group2),
            color="white",linewidth=1)+
  #绘制第二层圆环图
  geom_rect(data=data1,aes(ymax=ymax,ymin=ymin,
                      xmax=3.5,xmin=2,#x轴2-3.5绘制第二层
                      fill=group1),
            color="white",linewidth=1,alpha=0.4)+
  #添加第一层标签
  geom_text(data=data2,aes(x=1,#标签在x=1的位置上，确保在0-2中间
                           y=labelposition,
                           label=paste0(group2,"\n(",per,")")),
            size=4, color = "black")+
  # #添加第二层标签
  geom_text(data=data1,aes(x=2.75,#标签在x=2.75的位置上，确保在2-3.5中间
                           y=labelposition,
                           label=paste0(group1,"\n(",per,")")),
            size=3, color = "black")+
  #通过拉大x轴范围实现环图绘制
  xlim(0,3.5)+
  #转换为极坐标
  coord_polar(theta="y")+
  theme_void()+
  theme(legend.position = "none")+
  #自定义颜色,建议将内外环对应的组颜色设置为一致
  scale_fill_manual(values = c("A"="#ffc168","B"="#2dde98","C"="#1cc7d0",
                               "g1"="#ffc168","g2"="#ffc168","g3"="#2dde98",
                               "g4"="#1cc7d0","g5"="#1cc7d0"))
p3

##在环图中间增加空白间隔
p4 <- p3+ylim(0,1.1)
p4


###########绘制三环旭日图################
p5 <- ggplot()+
  #通过方块先绘制第一层饼图
  geom_rect(data=data3,aes(ymax=ymax,ymin=ymin,
                           xmax=2,xmin=0,#x轴0-2绘制第一层
                           fill=group3),
            color="white",linewidth=1)+
  #绘制第二层圆环图
  geom_rect(data=data2,aes(ymax=ymax,ymin=ymin,
                           xmax=3.5,xmin=2,#x轴2-3.5绘制第二层
                           fill=group2),
            color="white",linewidth=1,alpha=0.6)+
  #绘制第三层圆环图
  geom_rect(data=data1,aes(ymax=ymax,ymin=ymin,
                           xmax=5,xmin=3.5,#x轴3.5-5绘制第三层
                           fill=group1),
            color="white",linewidth=1,alpha=0.3)+
  #添加第一层标签
  geom_text(data=data3,aes(x=1,#标签在x=1的位置上，确保在0-2中间
                           y=labelposition,
                           label=paste0(group3,"\n(",per,")")),
            size=3.5, color = "black")+
  ##添加第二层标签
  geom_text(data=data2,aes(x=2.75,#标签在x=2.75的位置上，确保在2-3.5中间
                           y=labelposition,
                           label=paste0(group2,"\n(",per,")")),
            size=3, color = "black")+
  ##添加第三层标签
  geom_text(data=data1,aes(x=4.25,#标签在x=4.25的位置上，确保在3.5-5中间
                           y=labelposition,
                           label=paste0(group1,"\n(",per,")")),
            size=3, color = "black")+
  #通过拉大x轴范围实现环图绘制
  xlim(0,5)+
  #转换为极坐标
  coord_polar(theta="y")+
  theme_void()+
  theme(legend.position = "none")+
  #自定义颜色,建议将内外环对应的组颜色设置为一致
  scale_fill_manual(values = c("G1"="#ff4e00","G2"="#01cd74",
                               "A"="#ff4e00","B"="#ff4e00","C"="#01cd74",
                               "g1"="#ff4e00","g2"="#ff4e00","g3"="#ff4e00",
                               "g4"="#01cd74","g5"="#01cd74"))
p5
##在环图中间增加空白间隔
p6 <- p5+ylim(0,1.1)
p6

###拼图
library(patchwork)
(p1+p3+p5)/(p2+p4+p6)

```


---

### 圆环图&旭日图_PieDonut

```r

rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/圆环图&旭日图")

### 基于webr包中的PieDonut函数进行绘制
## 安装R包
# install.packages("webr")
## 加载R包
library(webr) # Data and Functions for Web-Based Analysis
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics

##加载数据（随即编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")
head(df)
##绘制一张简单的环状图
PieDonut(df,aes(group1,count=value),
         r0 = getOption("PieDonut.r0", 0.8),
         r1 = getOption("PieDonut.r1", 1.3),#设置中间镂空的比例
         labelpositionThreshold=0.1)#设置比例小于10%的数据标签显示在外侧

##绘制旭日图
PieDonut(df,aes(pies = group2, donuts = group1),
         r0 = 0.4,
         r1 = 1,
         r2 = 1.6,
         color = "white",#分割各区域的线条颜色
         pieAlpha = 0.8,#内层填充色的透明度
         donutAlpha = 0.8,#外层填充色的透明度
         start = pi/2,#起始位置
         addPieLabel = T,#是否显示内心圆的标签
         addDonutLabel = T,#是否显示外层的标签
         showRatioDonut = T,#外层标签的比例
         showRatioPie = T,#内层圆标签的比例
         ratioByGroup = F,#是否按分组计算外层比例
         showRatioThreshold = 0.02,#将标签显示为占总数比率的阈值，默认值为0.02。
         labelposition = 2,#设置外层标签位置的数字
         labelpositionThreshold = 0.1,#设置外层比例小于10%的数据标签显示在图形外
         explode = 1,#pies to explode,默认为NULL
         selected = 1,#donuts to explode,默认为NULL
         explodePie = T,#Whether or not explode pies
         explodeDonut = T,#Whether or not explode donuts
         explodePos = 0.1,#分裂的位置设置
         showPieName = T,#是否显示内层饼图名称
         showDonutName = F,#是否显示外层名称
         title = "This is a title",#标题,默认为NULL
         pieLabelSize = 4,#内层标签大小
         donutLabelSize = 3,#外层标签大小
         titlesize = 7,#标题字体大小
         family = getOption("PieDonut.family", "")#字体设置
         )

###PieDonut中没有直接修改颜色的参数，所以直接在原始函数定义中修改，以RColorBrewer中的调色板为例
##在其中新增一个修改调色板名称的参数man_color
library(moonBook) # Functions and Datasets for the Book by Keon-Woong Moon
library(grid) # The Grid Graphics Package
library(ggforce) # Accelerating 'ggplot2'
PieDonut2 <- function (data, mapping, start = getOption("PieDonut.start", 
                                                        0), addPieLabel = TRUE, addDonutLabel = TRUE, showRatioDonut = TRUE, 
                       showRatioPie = TRUE, ratioByGroup = TRUE, showRatioThreshold = getOption("PieDonut.showRatioThreshold", 
                                                                                                0.02), labelposition = getOption("PieDonut.labelposition", 
                                                                                                                                 2), labelpositionThreshold = 0.1, r0 = getOption("PieDonut.r0", 
                                                                                                                                                                                  0.3), r1 = getOption("PieDonut.r1", 1), r2 = getOption("PieDonut.r2", 
                                                                                                                                                                                                                                         1.2), explode = NULL, selected = NULL, explodePos = 0.1, 
                       color = "white", pieAlpha = 0.8, donutAlpha = 1, maxx = NULL, 
                       showPieName = TRUE, showDonutName = FALSE, title = NULL, 
                       pieLabelSize = 4, donutLabelSize = 3, titlesize = 5, explodePie = TRUE, 
                       explodeDonut = FALSE, use.label = TRUE, use.labels = TRUE, 
                       family = getOption("PieDonut.family", ""),
                       man_color="Set1")#输入调色板名称，具体可通过RColorBrewer::display.brewer.all()查看
{
  (cols = colnames(data))
  if (use.labels) 
    data = addLabelDf(data, mapping)
  count <- NULL
  if ("count" %in% names(mapping)) 
    count <- getMapping(mapping, "count")
  count
  pies <- donuts <- NULL
  (pies = getMapping(mapping, "pies"))
  if (is.null(pies)) 
    (pies = getMapping(mapping, "pie"))
  if (is.null(pies)) 
    (pies = getMapping(mapping, "x"))
  (donuts = getMapping(mapping, "donuts"))
  if (is.null(donuts)) 
    (donuts = getMapping(mapping, "donut"))
  if (is.null(donuts)) 
    (donuts = getMapping(mapping, "y"))
  if (!is.null(count)) {
    df <- data %>% group_by(.data[[pies]]) %>% dplyr::summarize(Freq = sum(.data[[count]]))
    df
  }
  else {
    df = data.frame(table(data[[pies]]))
  }
  colnames(df)[1] = pies
  df$end = cumsum(df$Freq)
  df$start = dplyr::lag(df$end)
  df$start[1] = 0
  total = sum(df$Freq)
  df$start1 = df$start * 2 * pi/total
  df$end1 = df$end * 2 * pi/total
  df$start1 = df$start1 + start
  df$end1 = df$end1 + start
  df$focus = 0
  if (explodePie) 
    df$focus[explode] = explodePos
  df$mid = (df$start1 + df$end1)/2
  df$x = ifelse(df$focus == 0, 0, df$focus * sin(df$mid))
  df$y = ifelse(df$focus == 0, 0, df$focus * cos(df$mid))
  df$label = df[[pies]]
  df$ratio = df$Freq/sum(df$Freq)
  if (showRatioPie) {
    df$label = ifelse(df$ratio >= showRatioThreshold, paste0(df$label, 
                                                             "\n(", scales::percent(df$ratio), ")"), as.character(df$label))
  }
  df$labelx = (r0 + r1)/2 * sin(df$mid) + df$x
  df$labely = (r0 + r1)/2 * cos(df$mid) + df$y
  if (!is.factor(df[[pies]])) 
    df[[pies]] <- factor(df[[pies]])
  df
  mainCol = RColorBrewer::brewer.pal(nrow(df), name=man_color)
  df$radius = r1
  df$radius[df$focus != 0] = df$radius[df$focus != 0] + df$focus[df$focus != 
                                                                   0]
  df$hjust = ifelse((df$mid%%(2 * pi)) > pi, 1, 0)
  df$vjust = ifelse(((df$mid%%(2 * pi)) < (pi/2)) | (df$mid%%(2 * 
                                                                pi) > (pi * 3/2)), 0, 1)
  df$segx = df$radius * sin(df$mid)
  df$segy = df$radius * cos(df$mid)
  df$segxend = (df$radius + 0.05) * sin(df$mid)
  df$segyend = (df$radius + 0.05) * cos(df$mid)
  df
  if (!is.null(donuts)) {
    subColor = makeSubColor(mainCol, no = length(unique(data[[donuts]])))
    subColor
    data
    if (!is.null(count)) {
      df3 <- as.data.frame(data[c(donuts, pies, count)])
      colnames(df3) = c("donut", "pie", "Freq")
      df3
      df3 <- eval(parse(text = "complete(df3,donut,pie)"))
      df3$Freq[is.na(df3$Freq)] = 0
      if (!is.factor(df3[[1]])) 
        df3[[1]] = factor(df3[[1]])
      if (!is.factor(df3[[2]])) 
        df3[[2]] = factor(df3[[2]])
      df3 <- df3 %>% arrange(.data$pie, .data$donut)
      a <- df3 %>% spread(.data$pie, value = .data$Freq)
      a = as.data.frame(a)
      a
      rownames(a) = a[[1]]
      a = a[-1]
      a
      colnames(df3)[1:2] = c(donuts, pies)
    }
    else {
      df3 = data.frame(table(data[[donuts]], data[[pies]]), 
                       stringsAsFactors = FALSE)
      colnames(df3)[1:2] = c(donuts, pies)
      a = table(data[[donuts]], data[[pies]])
      a
    }
    a
    df3
    df3$group = rep(colSums(a), each = nrow(a))
    df3$pie = rep(1:ncol(a), each = nrow(a))
    total = sum(df3$Freq)
    total
    df3$ratio1 = df3$Freq/total
    df3
    if (ratioByGroup) {
      df3$ratio = scales::percent(df3$Freq/df3$group)
    }
    else {
      df3$ratio <- scales::percent(df3$ratio1)
    }
    df3$end = cumsum(df3$Freq)
    df3
    df3$start = dplyr::lag(df3$end)
    df3$start[1] = 0
    df3$start1 = df3$start * 2 * pi/total
    df3$end1 = df3$end * 2 * pi/total
    df3$start1 = df3$start1 + start
    df3$end1 = df3$end1 + start
    df3$mid = (df3$start1 + df3$end1)/2
    df3$focus = 0
    if (!is.null(selected)) {
      df3$focus[selected] = explodePos
    }
    else if (!is.null(explode)) {
      selected = c()
      for (i in 1:length(explode)) {
        start = 1 + nrow(a) * (explode[i] - 1)
        selected = c(selected, start:(start + nrow(a) - 
                                        1))
      }
      selected
      df3$focus[selected] = explodePos
    }
    df3
    df3$x = 0
    df3$y = 0
    df
    if (!is.null(explode)) {
      explode
      for (i in 1:length(explode)) {
        xpos = df$focus[explode[i]] * sin(df$mid[explode[i]])
        ypos = df$focus[explode[i]] * cos(df$mid[explode[i]])
        df3$x[df3$pie == explode[i]] = xpos
        df3$y[df3$pie == explode[i]] = ypos
      }
    }
    df3$no = 1:nrow(df3)
    df3$label = df3[[donuts]]
    if (showRatioDonut) {
      if (max(nchar(levels(df3$label))) <= 2) 
        df3$label = paste0(df3$label, "(", df3$ratio, 
                           ")")
      else df3$label = paste0(df3$label, "\n(", df3$ratio, 
                              ")")
    }
    df3$label[df3$ratio1 == 0] = ""
    df3$label[df3$ratio1 < showRatioThreshold] = ""
    df3$hjust = ifelse((df3$mid%%(2 * pi)) > pi, 1, 0)
    df3$vjust = ifelse(((df3$mid%%(2 * pi)) < (pi/2)) | 
                         (df3$mid%%(2 * pi) > (pi * 3/2)), 0, 1)
    df3$no = factor(df3$no)
    df3
    labelposition
    if (labelposition > 0) {
      df3$radius = r2
      if (explodeDonut) 
        df3$radius[df3$focus != 0] = df3$radius[df3$focus != 
                                                  0] + df3$focus[df3$focus != 0]
      df3$segx = df3$radius * sin(df3$mid) + df3$x
      df3$segy = df3$radius * cos(df3$mid) + df3$y
      df3$segxend = (df3$radius + 0.05) * sin(df3$mid) + 
        df3$x
      df3$segyend = (df3$radius + 0.05) * cos(df3$mid) + 
        df3$y
      if (labelposition == 2) 
        df3$radius = (r1 + r2)/2
      df3$labelx = (df3$radius) * sin(df3$mid) + df3$x
      df3$labely = (df3$radius) * cos(df3$mid) + df3$y
    }
    else {
      df3$radius = (r1 + r2)/2
      if (explodeDonut) 
        df3$radius[df3$focus != 0] = df3$radius[df3$focus != 
                                                  0] + df3$focus[df3$focus != 0]
      df3$labelx = df3$radius * sin(df3$mid) + df3$x
      df3$labely = df3$radius * cos(df3$mid) + df3$y
    }
    df3$segx[df3$ratio1 == 0] = 0
    df3$segxend[df3$ratio1 == 0] = 0
    df3$segy[df3$ratio1 == 0] = 0
    df3$segyend[df3$ratio1 == 0] = 0
    if (labelposition == 0) {
      df3$segx[df3$ratio1 < showRatioThreshold] = 0
      df3$segxend[df3$ratio1 < showRatioThreshold] = 0
      df3$segy[df3$ratio1 < showRatioThreshold] = 0
      df3$segyend[df3$ratio1 < showRatioThreshold] = 0
    }
    df3
    del = which(df3$Freq == 0)
    del
    if (length(del) > 0) 
      subColor <- subColor[-del]
    subColor
  }
  p <- ggplot() + theme_no_axes() + coord_fixed()
  if (is.null(maxx)) {
    r3 = r2 + 0.3
  }
  else {
    r3 = maxx
  }
  p1 <- p + geom_arc_bar(aes_string(x0 = "x", y0 = "y", r0 = as.character(r0), 
                                    r = as.character(r1), start = "start1", end = "end1", 
                                    fill = pies), alpha = pieAlpha, color = color, data = df) + 
    transparent() + scale_fill_manual(values = mainCol) + 
    xlim(r3 * c(-1, 1)) + ylim(r3 * c(-1, 1)) + guides(fill = FALSE)
  if ((labelposition == 1) & (is.null(donuts))) {
    p1 <- p1 + geom_segment(aes_string(x = "segx", y = "segy", 
                                       xend = "segxend", yend = "segyend"), data = df) + 
      geom_text(aes_string(x = "segxend", y = "segyend", 
                           label = "label", hjust = "hjust", vjust = "vjust"), 
                size = pieLabelSize, data = df, family = family)
  }
  else if ((labelposition == 2) & (is.null(donuts))) {
    p1 <- p1 + geom_segment(aes_string(x = "segx", y = "segy", 
                                       xend = "segxend", yend = "segyend"), data = df[df$ratio < 
                                                                                        labelpositionThreshold, ]) + geom_text(aes_string(x = "segxend", 
                                                                                                                                          y = "segyend", label = "label", hjust = "hjust", 
                                                                                                                                          vjust = "vjust"), size = pieLabelSize, data = df[df$ratio < 
                                                                                                                                                                                             labelpositionThreshold, ], family = family) + geom_text(aes_string(x = "labelx", 
                                                                                                                                                                                                                                                                y = "labely", label = "label"), size = pieLabelSize, 
                                                                                                                                                                                                                                                     data = df[df$ratio >= labelpositionThreshold, ], 
                                                                                                                                                                                                                                                     family = family)
  }
  else {
    p1 <- p1 + geom_text(aes_string(x = "labelx", y = "labely", 
                                    label = "label"), size = pieLabelSize, data = df, 
                         family = family)
  }
  if (showPieName) 
    p1 <- p1 + annotate("text", x = 0, y = 0, label = pies, 
                        size = titlesize, family = family)
  p1 <- p1 + theme(text = element_text(family = family))
  if (!is.null(donuts)) {
    if (explodeDonut) {
      p3 <- p + geom_arc_bar(aes_string(x0 = "x", y0 = "y", 
                                        r0 = as.character(r1), r = as.character(r2), 
                                        start = "start1", end = "end1", fill = "no", 
                                        explode = "focus"), alpha = donutAlpha, color = color, 
                             data = df3)
    }
    else {
      p3 <- p + geom_arc_bar(aes_string(x0 = "x", y0 = "y", 
                                        r0 = as.character(r1), r = as.character(r2), 
                                        start = "start1", end = "end1", fill = "no"), 
                             alpha = donutAlpha, color = color, data = df3)
    }
    p3 <- p3 + transparent() + scale_fill_manual(values = subColor) + 
      xlim(r3 * c(-1, 1)) + ylim(r3 * c(-1, 1)) + guides(fill = FALSE)
    p3
    if (labelposition == 1) {
      p3 <- p3 + geom_segment(aes_string(x = "segx", y = "segy", 
                                         xend = "segxend", yend = "segyend"), data = df3) + 
        geom_text(aes_string(x = "segxend", y = "segyend", 
                             label = "label", hjust = "hjust", vjust = "vjust"), 
                  size = donutLabelSize, data = df3, family = family)
    }
    else if (labelposition == 0) {
      p3 <- p3 + geom_text(aes_string(x = "labelx", y = "labely", 
                                      label = "label"), size = donutLabelSize, data = df3, 
                           family = family)
    }
    else {
      p3 <- p3 + geom_segment(aes_string(x = "segx", y = "segy", 
                                         xend = "segxend", yend = "segyend"), data = df3[df3$ratio1 < 
                                                                                           labelpositionThreshold, ]) + geom_text(aes_string(x = "segxend", 
                                                                                                                                             y = "segyend", label = "label", hjust = "hjust", 
                                                                                                                                             vjust = "vjust"), size = donutLabelSize, data = df3[df3$ratio1 < 
                                                                                                                                                                                                   labelpositionThreshold, ], family = family) + 
        geom_text(aes_string(x = "labelx", y = "labely", 
                             label = "label"), size = donutLabelSize, data = df3[df3$ratio1 >= 
                                                                                   labelpositionThreshold, ], family = family)
    }
    if (!is.null(title)) 
      p3 <- p3 + annotate("text", x = 0, y = r3, label = title, 
                          size = titlesize, family = family)
    else if (showDonutName) 
      p3 <- p3 + annotate("text", x = (-1) * r3, y = r3, 
                          label = donuts, hjust = 0, size = titlesize, 
                          family = family)
    p3 <- p3 + theme(text = element_text(family = family))
    grid.newpage()
    print(p1, vp = viewport(height = 1, width = 1))
    print(p3, vp = viewport(height = 1, width = 1))
  }
  else {
    p1
  }
}
##输入数据并复制已经设置好的参数进行绘图
PieDonut2(df,aes(pies = group2, donuts = group1),
               r0 = 0.4,
               r1 = 1,
               r2 = 1.6,
               color = "white",#分割各区域的线条颜色
               pieAlpha = 0.8,#内层填充色的透明度
               donutAlpha = 0.8,#外层填充色的透明度
               start = pi/2,#起始位置
               addPieLabel = T,#是否显示内心圆的标签
               addDonutLabel = T,#是否显示外层的标签
               showRatioDonut = T,#外层标签的比例
               showRatioPie = T,#内层圆标签的比例
               ratioByGroup = F,#是否按分组计算外层比例
               showRatioThreshold = 0.02,#将标签显示为占总数比率的阈值，默认值为0.02。
               labelposition = 2,#设置外层标签位置的数字
               labelpositionThreshold = 0.1,#设置外层比例小于10%的数据标签显示在图形外
               explode = 1,#pies to explode,默认为NULL
               selected = 1,#donuts to explode,默认为NULL
               explodePie = T,#Whether or not explode pies
               explodeDonut = T,#Whether or not explode donuts
               explodePos = 0.1,#分裂的位置设置
               showPieName = T,#是否显示内层饼图名称
               showDonutName = F,#是否显示外层名称
               title = "This is a title",#标题,默认为NULL
               pieLabelSize = 4,#内层标签大小
               donutLabelSize = 3,#外层标签大小
               titlesize = 7,#标题字体大小
               family = getOption("PieDonut.family", ""),#字体设置
          man_color="Set1"##修改颜色
               )

##外边框基于AI去除即可

####修改颜色测试
RColorBrewer::display.brewer.all()
PieDonut2(df,aes(pies = group2, donuts = group1),
          r0 = 0.4,
          r1 = 1,
          r2 = 1.6,
          pieAlpha = 0.8,
          donutAlpha = 0.8,
          man_color="Paired")##修改颜色

```


---

### Circle Packing

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/Circle Packing')#设置工作路径
#加载R包
library(packcircles) # Circle Packing
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics

#加载数据
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)

#根据数据集生成圆心和半径
df1 <- circleProgressiveLayout(df$size, sizetype='area')
#合并数据集
data = cbind(df, df1)
df1$group <- df$group
#验证圆的面积和数值大小是否成正比
plot(data$radius^2, data$size)
# 生成50条直线用于绘制圆
data1 <- circleLayoutVertices(df1, #数据
                               npoints=50,#为每个圆生成的顶点数。
                               idcol=4,#圆标识符的可选索引或列名。
                               sizetype = "radius")#The type of size values: either "radius" (default) or "area". May be abbreviated.
data1$G <- rep(1:150,each=51)#由于设置的id列存在重复，绘图时会出现排列错乱现象，所以需要添加一列数据用于直线排列位置标识
ggplot() +
  geom_point(data=data,aes(x,y,size=size),color = "black")+
  scale_size(range = c(1,10))+
  geom_polygon(data = data1, 
               aes(x, y, group = G,
                   fill=as.factor(id)),
               color = "white") +#通过绘制大量的直线来填充这个圆
  scale_fill_manual(values = c("#d20962","#f47721","#7ac143","#00a78e","#00bce4","#7d3f98")) +
  theme_void() + 
  theme(legend.position="right") +
  labs(fill="Group")+#图例标题
  coord_equal()#保证x，y尺度大小相同

#参考：https://www.cnblogs.com/tecdat/p/15839746.html

```


---

## 🌳 八、进化树 & 树状图

### 半圆进化树+分支颜色+注释+标签颜色

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/半圆进化树+分支颜色+注释+标签颜色')#设置工作路径

#加载包
library(ggtree) # an R package for visualization of tree and annotation data
library(ggtreeExtra) # An R Package To Add Geometric Layers On Circular Or Other Layout Tree Of "ggtree"
library(ggnewscale) # Multiple Fill and Colour Scales in 'ggplot2'
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics 

##数据——随机编写
df_tree <- read.tree(text='((((A_1:1,A_2:1,A_3:3,A_4:2,A_5:1,A_6:6,A_7:4,A_8:5):3,(C_1:3,C_2:2,C_3:3,C_4:1,C_5:3,C_6:4,C_7:6,C_8:5):1):2,(B_1:4,B_2:1,B_3:3,B_4:2,B_5:1,B_6:1,B_7:2,B_8:5):2):4,(D_1:2,D_2:1,D_3:5,D_4:3,D_5:4,D_6:1,D_7:5,D_8:7):5):3;')

# 对树分组
sample <- list(A=c("A_1","A_2","A_3","A_4","A_5","A_6","A_7","A_8"),
               B=c("B_1","B_2","B_3","B_4","B_5","B_6","B_7","B_8"),
               C=c("C_1","C_2","C_3","C_4","C_5","C_6","C_7","C_8"),
               D=c("D_1","D_2","D_3","D_4","D_5","D_6","D_7","D_8"))
# 将分组信息和进化树组合到一起
tree<-groupOTU(df_tree,sample)

#突出显示的标签
df_label <- c("A_6",
             "D_8",
             "C_7",
             "B_8")

#注释信息（随机生成）
df_group <- data.frame(
  sample=c("A_1","A_2","A_3","A_4","A_5","A_6","A_7","A_8",
           "B_1","B_2","B_3","B_4","B_5","B_6","B_7","B_8",
           "C_1","C_2","C_3","C_4","C_5","C_6","C_7","C_8",
           "D_1","D_2","D_3","D_4","D_5","D_6","D_7","D_8"),
  group=rep(c("A","B","C","D"),each=8),
  G=rep(c('group1','group2','group3','group4'),each=3,len=32),
  group2=sample(-50:50, 32, replace = FALSE)
)
df_group$G2 <-ifelse(df_group$group2>0,"Yes","No")

##绘图
ggtree(tree,#文件
       aes(color=group),#支长颜色按照分组进行着色
       layout="fan",#进化树类型
       open.angle=180,#开口角度
       linewidth=0.6,#分支线条粗细
       show.legend = F)+
  geom_tiplab(aes(color = label %in% df_label),#设定标签颜色根据筛选条件突出显示特定标签
              size=3.5,#字体大小
              align = T,#使用虚线连接标签与分支
              linetype = 3,linewidth = 0.4,offset = 12.5,show.legend = F)+
  scale_color_manual(values=c("black","#1aafd0","#6a67ce","#ffb900","#fc636b","#aeb6b8","#e53238"))+
  #添加注释信息-G
  new_scale_fill() +
  geom_fruit(
    data=df_group,
    geom=geom_tile,
    mapping=aes(y=sample, fill=G),
    color="grey10",
    width=1.2,
    offset=0.1)+
  scale_fill_manual(
    values=c("#4285f4", "#34a853", "#fbbc05","#ea4335"),
    guide=guide_legend(keywidth=1, keyheight=1, order=2),
    name="Note01")+
  #添加注释信息-group2
  new_scale_fill() +
  geom_fruit(
    data=df_group,#数据
    geom = geom_col,#绘图类型
    mapping = aes(x = group2,y=sample,fill=G2),
    offset = 0.4,
    pwidth = 0.4,
    width=0.8)+#条形图宽度
  scale_fill_manual(
    values=c("Yes"="#4b1702",
             "No"="#8f9696"),
    guide=guide_legend(keywidth=1, keyheight=1, order=1),
    name="Note02")+
  theme(legend.position = "top")#主题设置

```


---

### tree+分支颜色调整+分组注释+热图注释+柱状堆积图注释

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/tree+分支颜色调整+分组注释+热图注释+柱状堆积图注释')#设置工作路径

#加载包
library(ggtree) # an R package for visualization of tree and annotation data
library(ape) # Analyses of Phylogenetics and Evolution
library(vegan) # Community Ecology Package
library(ggtreeExtra) # An R Package To Add Geometric Layers On Circular Or Other Layout Tree Of "ggtree"
library(ggnewscale) # Multiple Fill and Colour Scales in 'ggplot2'
library(ggstar) # Multiple Geometric Shape Point Layer for 'ggplot2'
#读取数据
OTU <- read.table("OTU.txt",check.names = F, row.names = 1, header = 1, sep = "\t")

#计算距离矩阵
df_dist <- vegdist(t(OTU),method = 'bray')#使用bray curtis方法计算距离矩阵
####进行层次聚类,可选择方法有single、complete、median、mcquitty、average 、centroid 、ward 
df_hc <- hclust(df_dist,method="average")#使用类平均法进行聚类
#绘图
plot(as.dendrogram(df_hc),type="rectangle",horiz=T)#实现将垂直的聚类树变成水平聚类树，绘图
# 将聚类结果转成系统发育格式
df_tree <- as.phylo(df_hc)
# 对树分组
sample <- list(A=c("A_1","A_2","A_3","A_4","A_5","A_6","A_7","A_8"),
            B=c("B_1","B_2","B_3","B_4","B_5","B_6","B_7","B_8"),
            C=c("C_1","C_2","C_3","C_4","C_5","C_6","C_7","C_8"),
            D=c("D_1","D_2","D_3","D_4","D_5","D_6","D_7","D_8"),
            E=c("E_1","E_2","E_3","E_4","E_5","E_6","E_7","E_8"),
            F=c("F_1","F_2","F_3","F_4","F_5","F_6","F_7","F_8"),
            G=c("G_1","G_2","G_3","G_4","G_5","G_6","G_7","G_8"))
# 将分组信息和进化树组合到一起
tree<-groupOTU(df_tree,sample)

# ggtree初步展示
ggtree(tree,size=0.8, layout="circular", 
             ladderize=FALSE, branch.length="none", aes(col=group),show.legend = F)+
  geom_tiplab(aes(color=group),size=4,align = F,
              offset = 0.001,show.legend = F)

##读取分组注释信息
group <- read.table("sample.txt",check.names = F, row.names = 1, header = 1, sep = "\t")
group$sample <- rownames(group)

##计算各样本的物种丰度信息
#读取分类信息
tax <- read.table("tax.txt",check.names = F, header = 1, sep = "\t")
#根据OTUID合并OTU数据和分类信息
OTU2 <- OTU
OTU2$OTU_id <- rownames(OTU2)
df <- merge(tax,OTU2,by="OTU_id")
#提取属水平的信息
data_Genus <- df[,c(7,9:64)]
##利用循环处理具有重复的数据
#初始化
data<-aggregate(A_1 ~ Genus,data=data_Genus,sum)
#重命名
colnames(data)[2]<-"example"
for (i in colnames(data_Genus)[2:length(colnames(data_Genus))]){
  #计算每列的和
  data1<-aggregate(data_Genus[,i]~Genus,data=data_Genus,sum)
  colnames(data1)[2]<-i  
  #合并列
  data<-merge(data,data1,by="Genus")
}
df2<-data[,-2]
rownames(df2)=df2$Genus#修改行名
df3=df2[,-1]#删除多的列

#计算物种总丰度并降序排列
df3$rowsum <- apply(df3,1,sum)
df4 <- df3[order (df3$rowsum,decreasing=TRUE),]
df5 = df4[,-57]#删除求和列
#求物种相对丰度
df6 <- apply(df5,2,function(x) x/sum(x))
#由于之间已经按照每行的和进行过升序排列，所以可以直接取前10行
df7 <-  df6[1:10,]
df8 <- 1-apply(df7, 2, sum) #计算剩下物种的总丰度
#合并数据
df9 <- rbind(df7,df8)
row.names(df9)[11]="Others"
df9 <- as.data.frame(df9)
df10 <- as.data.frame(t(df9))
df10$sample <- rownames(df10)

##根据样本名称合并分组与丰度信息
group <- merge(group,df10,by="sample")

##第二层注释的数据
data2 <- group[,c(1,4:11)]
data2 <- melt(data2)
data2$`Diet (detailed)` <- as.character(data2$variable)
data2$value <- as.character(data2$value)

##第六层注释的数据
data6 <- group[,c(1,15:25)]
data6 <- melt(data6)

###为进化树添加注释信息
ggtree(tree,size=0.8, layout="circular", 
       ladderize=FALSE, branch.length="none", aes(col=group),show.legend = F)+#图形主体
  geom_tiplab(aes(color=group),size=3,align = F,
              offset = 0.001,show.legend = F)+#分支标签
  scale_color_manual(
    values=c("black", "#0ebeff", "#47cf73","#ae63e4",
             "#fcd000","#ff3c41","#b62b6e","#00b7c9"))+#自定义分支颜色
  #第一层注释_Diet
  new_scale_fill() + 
  geom_fruit(
    data=group,
    geom=geom_tile,
    mapping=aes(y=sample, fill=Diet),
    width = 0.4,#注释的宽度
    offset=0.3 #位置
  )+
  scale_fill_manual(
    values=c("#00ff01", "#fecc32", "#ff0100"),
    guide=guide_legend(keywidth=1, keyheight=1, order=1))+
  #第二层注释_Diet (detailed)
  new_scale_fill() +
  geom_fruit(
    data=data2,
    geom=geom_tile,
    mapping=aes(y=sample, x=`Diet (detailed)`, fill=value),
    color="grey80",
    pwidth=0.8,
    offset=0.05, #位置
    axis.params=list(
      axis="x", # 添加图层的轴文本
      text.angle=0, #x 轴的文本角度
      hjust=0.5,  # 调整文字轴的水平位置
      text.size = 4,#文字大小
      line.alpha = 0
    )
  )+
  scale_fill_manual(
    values=c("#000000", "#a95401", "#ff8000","#ffff00"),
    guide=guide_legend(keywidth=1, keyheight=1, order=2),
    name="Diet (detailed)")+
  #添加第三层注释——Habitat
  new_scale_fill() +
  geom_fruit(data=group,
             geom = geom_star,
             mapping = aes(y=sample,fill = Habitat), 
             starshape = 13, color = NA,
             size = 5, starstroke = 0, pwidth = 2, offset = 0.2,
             grid.params=list(
               linetype=3,
               size=0.4
             ))+
  scale_fill_manual(
    values=c("#ff9901", "#01ccff", "#999601", "#663300"),
    guide=guide_legend(keywidth=1, keyheight=1, order=3)
  )+
  #添加第四层注释——Captive-wild
  new_scale_fill() +
  geom_fruit(data=group,
             geom = geom_star,
             mapping = aes(y=sample,fill = `Captive-wild`), 
             starshape = 13, color = NA,
             size = 5, starstroke = 0, pwidth = 2, offset = 0.2,
             grid.params=list(
               linetype=3,
               size=0.4
             ))+
  scale_fill_manual(
    values=c("#ff9901", "#0000ff", "#009900"),
    guide=guide_legend(keywidth=1, keyheight=1, order=4)
  )+
  #添加第五层注释——Captive-wild
  new_scale_fill() +
  geom_fruit(data=group,
             geom = geom_star,
             mapping = aes(y=sample,fill = `Sample type`), 
             starshape = 13, color = NA,
             size = 5, starstroke = 0, pwidth = 2, offset = 0.2,
             grid.params=list(
               linetype=3,
               size=0.4,
             ))+
  scale_fill_manual(
    values=c("#663300", "#cc9a00"),
    guide=guide_legend(keywidth=1, keyheight=1, order=5)
  )+
  new_scale_fill() +
  geom_fruit(
    data=data6,
    geom=geom_bar,
    mapping=aes(y=sample, x=value, fill=variable),
    pwidth=1,
    width = 0.6,
    offset = 0.1,
    stat="identity",
    orientation="y",
    axis.params = list(axis = "x",
                       text.size = 2,
                       vjust = 0.5,
                       hjust = 0,
                       text.angle = -90,
                       limits = c(0,1)),
    grid.params = list(linetype = 3)
  )+
  scale_fill_manual(
    values=c("#4078c0", "#6cc644", "#bd2c00","#c9510c", "#6e5494",
             "#fbbc05","#ec6400", "#d5df00", "#e30061","#009ee3",
             "#aca6a2"),
    guide=guide_legend(keywidth=1, keyheight=1, order=6),
    name = "Genus"
  )

#####输出PDF
pdf(file='test.pdf', height=10,width=12)#新建一个PDF文件，设置名称、宽高及字体等
ggtree(tree,size=0.8, layout="circular", 
       ladderize=FALSE, branch.length="none", aes(col=group),show.legend = F)+
  geom_tiplab(aes(color=group),size=3,align = F,
              offset = 0.001,show.legend = F)+
  scale_color_manual(
    values=c("black", "#0ebeff", "#47cf73","#ae63e4",
             "#fcd000","#ff3c41","#b62b6e","#00b7c9"))+
  #第一层注释_Diet
  new_scale_fill() + 
  geom_fruit(
    data=group,
    geom=geom_tile,
    mapping=aes(y=sample, fill=Diet),
    width = 0.4,#注释的宽度
    offset=0.3 #位置
  )+
  scale_fill_manual(
    values=c("#00ff01", "#fecc32", "#ff0100"),
    guide=guide_legend(keywidth=1, keyheight=1, order=1))+
  #第二层注释_Diet (detailed)
  new_scale_fill() +
  geom_fruit(
    data=data2,
    geom=geom_tile,
    mapping=aes(y=sample, x=`Diet (detailed)`, fill=value),
    color="grey80",
    pwidth=0.8,
    offset=0.05, #位置
    axis.params=list(
      axis="x", # 添加图层的轴文本
      text.angle=0, #x 轴的文本角度
      hjust=0.5,  # 调整文字轴的水平位置
      text.size = 4,#文字大小
      line.alpha = 0
    )
  )+
  scale_fill_manual(
    values=c("#000000", "#a95401", "#ff8000","#ffff00"),
    guide=guide_legend(keywidth=1, keyheight=1, order=2),
    name="Diet (detailed)")+
  #添加第三层注释——Habitat
  new_scale_fill() +
  geom_fruit(data=group,
             geom = geom_star,
             mapping = aes(y=sample,fill = Habitat), 
             starshape = 13, color = NA,
             size = 5, starstroke = 0, pwidth = 2, offset = 0.2,
             grid.params=list(
               linetype=3,
               size=0.4
             ))+
  scale_fill_manual(
    values=c("#ff9901", "#01ccff", "#999601", "#663300"),
    guide=guide_legend(keywidth=1, keyheight=1, order=3)
  )+
  #添加第四层注释——Captive-wild
  new_scale_fill() +
  geom_fruit(data=group,
             geom = geom_star,
             mapping = aes(y=sample,fill = `Captive-wild`), 
             starshape = 13, color = NA,
             size = 5, starstroke = 0, pwidth = 2, offset = 0.2,
             grid.params=list(
               linetype=3,
               size=0.4
             ))+
  scale_fill_manual(
    values=c("#ff9901", "#0000ff", "#009900"),
    guide=guide_legend(keywidth=1, keyheight=1, order=4)
  )+
  #添加第五层注释——Captive-wild
  new_scale_fill() +
  geom_fruit(data=group,
             geom = geom_star,
             mapping = aes(y=sample,fill = `Sample type`), 
             starshape = 13, color = NA,
             size = 5, starstroke = 0, pwidth = 2, offset = 0.2,
             grid.params=list(
               linetype=3,
               size=0.4,
             ))+
  scale_fill_manual(
    values=c("#663300", "#cc9a00"),
    guide=guide_legend(keywidth=1, keyheight=1, order=5)
  )+
  new_scale_fill() +
  geom_fruit(
    data=data6,
    geom=geom_bar,
    mapping=aes(y=sample, x=value, fill=variable),
    pwidth=1,
    width = 0.6,
    offset = 0.1,
    stat="identity",
    orientation="y",
    axis.params = list(axis = "x",
                       text.size = 2,
                       vjust = 0.5,
                       hjust = 0,
                       text.angle = -90,
                       limits = c(0,1)),
    grid.params = list(linetype = 3)
  )+
  scale_fill_manual(
    values=c("#4078c0", "#6cc644", "#bd2c00","#c9510c", "#6e5494",
             "#fbbc05","#ec6400", "#d5df00", "#e30061","#009ee3",
             "#aca6a2"),
    guide=guide_legend(keywidth=1, keyheight=1, order=6),
    name = "Genus"
  )
dev.off()#关闭PDF

```


---

### tree+柱状堆积图--物种组成可视化

```r

rm(list=ls())#clear Global Environment
setwd('D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\数据分析及可视化\\群落组成分析\\物种丰度计算及可视化')#设置工作路径

#加载R包
library (reshape2)
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(plyr) # Tools for Splitting, Applying and Combining Data
library(ggtree) # an R package for visualization of tree and annotation data
library(vegan) # Community Ecology Package
library(ape) # Analyses of Phylogenetics and Evolution
library( RColorBrewer) # not installed on this machine
library(aplot) # Decorate a 'ggplot' with Associated Information

#读取数据
df1 <- read.table(file="Genus.txt",sep="\t",header=T,check.names=FALSE)
#查看前6行
head(df1)
##利用循环处理具有重复的数据
#初始化
data<-aggregate(E ~ Tax,data=df1,sum)
#重命名
colnames(data)[2]<-"example"
for (i in colnames(df1)[2:length(colnames(df1))]){
  #计算每列的和
  data1<-aggregate(df1[,i]~Tax,data=df1,sum)
  colnames(data1)[2]<-i  
  #合并列
  data<-merge(data,data1,by="Tax")
  }
df2<-data[,-2]
rownames(df2)=df2$Tax#修改行名
df3=df2[,-1]#删除多的列

#计算物种总丰度并降序排列
df3$rowsum <- apply(df3,1,sum)
df4 <- df3[order (df3$rowsum,decreasing=TRUE),]
df5 = df4[,-6]#删除求和列
#求物种相对丰度
df6 <- apply(df5,2,function(x) x/sum(x))
#由于之间已经按照每行的和进行过升序排列，所以可以直接取前10行
df7 <-  df6[1:10,]
df8 <- 1-apply(df7, 2, sum) #计算剩下物种的总丰度
#合并数据
df9 <- rbind(df7,df8)
row.names(df9)[11]="Others"
#导出数据
write.table (df9, file ="genus_x.csv",sep =",", quote =FALSE)
#变量格式转换,宽数据转化为长数据,方便后续作图
df_genus <- melt(df9)
names(df_genus)[1:2] <- c("Taxonomy","sample")  #修改列名
#颜色
col <-colorRampPalette(brewer.pal(12,"Paired"))(11)
##柱状堆积图绘制绘图
p1<-ggplot(df_genus, aes( x = sample,y=100 * value,fill = Taxonomy))+#geom_col和geom_bar这两条命令都可以绘制堆叠柱形图
  geom_col(position = 'stack',width = 0.8)+
  #geom_bar(position = "stack", stat = "identity", width = 0.6) 
  scale_y_continuous(expand = c(0,0))+# 调整y轴属性，使柱子与X轴坐标接触
  labs(x=NULL,y="Relative Abundance(%)",#设置X轴和Y轴的名称以及添加标题
       fill="Taxonomy")+
  guides(fill=guide_legend(keywidth = 1, keyheight = 1)) +
  coord_flip()+
  theme(panel.grid = element_blank(),
        panel.background = element_blank())+
  scale_fill_manual(values = col)
p1     

####聚类树
data2 <- df3[-6]
#计算距离矩阵
df_dist <- vegdist(t(data2),method = 'bray')#使用bray curtis方法计算距离矩阵
####进行层次聚类,可选择方法有single、complete、median、mcquitty、average 、centroid 、ward 
df_hc <- hclust(df_dist,method="average")#使用类平均法进行聚类
#绘图
plot(as.dendrogram(df_hc),type="rectangle",horiz=T)#实现将垂直的聚类树变成水平聚类树，绘图
# 将聚类结果转成系统发育格式
df_tree <- as.phylo(df_hc)
# 对树分组
gro <- list(group1=c("A","E"),
            group2=c("C","D"),
            group3=c("B"))
# 将分组信息和进化树组合到一起
tree<-groupOTU(df_tree,gro)
# ggtree绘图
p2 <- ggtree(tree,size=1.2)+
  geom_tiplab(aes(color=group),size=5,align = F,
              offset = 0.008,show.legend = F)+
  geom_tippoint(aes(shape=group,color=group),
              show.legend = T,
              size=4)
p2


#####将柱状堆积图与树图进行组合
p1 <- p1+theme(axis.text.y = element_text(color = "black",size=12))
col2 <-colorRampPalette(brewer.pal(9,"Set1"))(3)
p3 <- ggtree(tree,size=1)+
  geom_tippoint(aes(shape=group,color=group),
                show.legend = T,
                size=4)+
  scale_color_manual(values = col2)
p <- p1%>%insert_left(p3,width = 0.3)
p

```


---

## 📊 九、分布图 & 密度图

### 密度图+分组标记+均值线

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/密度图+分组标记+均值线')#Set working path

##加载R包
#remotes::install_github("AllanCameron/geomtextpath")
library(geomtextpath) # Curved Text in 'ggplot2'
library(tidyverse) # Easily Install and Load the 'Tidyverse'
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(palmerpenguins) # Palmer Archipelago (Antarctica) Penguin Data
library(ggridges) # Ridgeline Plots in 'ggplot2'

##加载数据（以palmerpenguins包中的penguins数据集为例）
df <- read.table("data.txt", sep="\t", header=T, check.names=F)
# data(penguins)

##去除数据中的NA值
df <- df %>%
  drop_na()

###绘图
#绘制常规密度图-无填充
p1 <- df %>% 
  ggplot(aes(x = body_mass_g, color = species)) +
  #绘制密度图
  geom_density(linewidth=1.5)+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(size = 10),
        axis.title = element_text(size = 14))+
  #颜色设置
  scale_color_manual(values = c("#0099e5","#ff4c4c","#34bf49"))
p1

#绘制密度图+均值线-无填充
p2 <- df %>% 
  ggplot(aes(x = body_mass_g, color = species)) +
  geom_density(linewidth=1.5)+
  #添加均值线
  geom_vline(xintercept = mean(df[df$species=="Adelie",]$body_mass_g), 
             color = "#0099e5", linetype = "dashed",linewidth=0.6) +
  geom_vline(xintercept = mean(df[df$species=="Chinstrap",]$body_mass_g), 
             color = "#ff4c4c", linetype = "dashed",linewidth=0.6)+
  geom_vline(xintercept = mean(df[df$species=="Gentoo",]$body_mass_g), 
             color = "#34bf49", linetype = "dashed",linewidth=0.6)+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(size = 10),
        axis.title = element_text(size = 14))+
  scale_color_manual(values = c("#0099e5","#ff4c4c","#34bf49"))
p2

#绘制密度图+均值线+分组标记（直接在线上标记）-无填充
p3 <- df %>% 
  ggplot(aes(x = body_mass_g, color = species)) +
  #利用geom_textdensity函数绘制带标签的密度图
  geom_textdensity(aes(label = species),#标签
                   fontface = 3, #字体
                   linewidth=1.5,
                   hjust = 0.5, vjust = 0.5)+#位置
  geom_vline(xintercept = mean(df[df$species=="Adelie",]$body_mass_g), 
             color = "#0099e5", linetype = "dashed",linewidth=0.6) +
  geom_vline(xintercept = mean(df[df$species=="Chinstrap",]$body_mass_g), 
             color = "#ff4c4c", linetype = "dashed",linewidth=0.6)+
  geom_vline(xintercept = mean(df[df$species=="Gentoo",]$body_mass_g), 
             color = "#34bf49", linetype = "dashed",linewidth=0.6)+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(size = 10),
        axis.title = element_text(size = 14),
        legend.position = "none")+
  scale_color_manual(values = c("#0099e5","#ff4c4c","#34bf49"))
p3

#绘制密度图+均值线+分组标记（直接在线上标记）-有填充
p4 <- df %>% 
  ggplot(aes(x = body_mass_g, fill = species, color = species)) +
  #绘制带填充的密度图，设置线为0以去除线条
  geom_density(linewidth=0,alpha = 0.6)+
  #只需要标签，故设置线条粗细为0
  geom_textdensity(aes(label = species),
                   fontface = 3, linewidth=0,
                   hjust = 0.5, vjust = -0.5)+
  scale_y_continuous(expand = c(0,0))+
  geom_vline(xintercept = mean(df[df$species=="Adelie",]$body_mass_g), 
             color = "#0099e5", linetype = "dashed",linewidth=0.6) +
  geom_vline(xintercept = mean(df[df$species=="Chinstrap",]$body_mass_g), 
             color = "#ff4c4c", linetype = "dashed",linewidth=0.6)+
  geom_vline(xintercept = mean(df[df$species=="Gentoo",]$body_mass_g), 
             color = "#34bf49", linetype = "dashed",linewidth=0.6)+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(size = 10),
        axis.title = element_text(size = 14),
        legend.position = "none")+
  scale_fill_manual(values = c("#0099e5","#ff4c4c","#34bf49"))+
  scale_color_manual(values = c("#0099e5","#ff4c4c","#34bf49"))
p4

###拼图
library(patchwork)
(p1+p3)/(p2+p4)

```


---

### 分组直方图

```r

#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/分组直方图")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggpubr)
#加载数据
df <- read.table("data.txt",header = T,sep='\t')
df$group <- factor(df$group,levels = c("Sal","Coca","Ket","LSD","MDMA"))
df$sample <- factor(df$sample,levels = c("48 h","2 wk"))

#绘图
col <- c("#000000","#575757","#c53a8e","#e79600","#a42422")
col2 <- c("#767475","#000000","#872860","#f0b75b","#c97c7b")
ggplot(df,aes(sample,value))+
  geom_bar(aes(fill=group),color="black",stat="summary",fun=mean,position="dodge",size=1)+
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0,linewidth=1)+
  geom_point(aes(color=group),shape=21,size=4,stroke=1.5)+
  geom_hline(yintercept = 0, linetype = 1, color = "black", size = 1)+
  facet_grid(~group,scales = 'free_x',space = "free")+
  scale_color_manual(values = col2)+
  scale_fill_manual(values = col)+
  theme_classic()+
  theme(axis.line = element_line(size = 1),
        axis.text.x = element_text(color = "black", angle = 90,vjust = 0.5,hjust = 1,size = 15),
        axis.text.y = element_text(color = "black",size = 15),
        axis.ticks = element_line(color = "black",size = 1),
        legend.position = "none",
        strip.background = element_blank(),
        strip.text = element_text(color = "black",size = 18))+
  labs(x=NULL,y=NULL)

```


---

### 山脊图

```r

m(list = ls())
setwd("D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\山脊图")

#安装R包
# install.packages("ggplot2")
# install.packages("ggridges")
# install.packages("reshape")
# install.packages("ggprism")
#加载R包
library(ggplot2)
library(ggridges)
library(reshape)
library(ggprism)

# 加载数据
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)
#变量格式转换,宽数据转化为长数据,方便后续作图
df1 <- melt(df)

####绘图
#展示形式1
p1 <- ggplot(df1, aes(x = value, y = variable, fill = variable)) +#数据
  geom_density_ridges(stat = "density_ridges") +#绘制山脊图
  theme_prism(palette = "candy_bright",#主题样式
              base_fontface = "plain", # 字体样式
              base_family = "serif", # 字体格式
              base_size = 16,  #字体大小
              base_line_size = 0.8)+ #坐标轴粗细
  scale_fill_prism(palette = "candy_bright")+#颜色
  theme(legend.position = "none",#图例去除
        axis.line.y = element_blank(),#去除Y轴轴线
        axis.ticks.y = element_blank())+#去除Y轴刻度
  scale_y_discrete(expand = c(0.05, 0))#调整起始图形距离X轴距离
p1

#展示形式2
p2 <- ggplot(df1, aes(x = value, y = variable, fill = variable)) +
  geom_density_ridges(stat="binline", bins=40) +
  theme_prism(palette = "candy_bright",
              base_fontface = "plain", # 字体样式
              base_family = "serif", # 字体格式
              base_size = 16,  #字体大小
              base_line_size = 0.8)+ #坐标轴粗细
  scale_fill_prism(palette = "candy_bright")+
  theme(legend.position = "none",
        axis.line.y = element_blank(),
        axis.ticks.y = element_blank())+
  scale_y_discrete(expand = c(0.05, 0))
p2

#拼接图片
cowplot::plot_grid(p1, p2, ncol = 2)

```


---

### ECDF图

```r

# ECDF图,即经验累积密度函数，通过图可以看出低于特定数值个体百分比
rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/ECDF图")

##加载所需R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(tidyverse) # Easily Install and Load the 'Tidyverse'

##加载数据（随即编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")
head(df)

##简单绘制其中一组的ECDF图
df %>% filter(group=="group1") %>%
  ggplot(aes(x=value)) +
  stat_ecdf(linewidth=1)

##按照分组进行绘制
df %>% 
  ggplot(aes(x=value,col=group)) +
  ##绘制ecdf图的主要函数stat_ecdf()
  stat_ecdf(linewidth=0.6)+
  scale_color_manual(values = c("#00b2a9","#a626aa","#6639b7","#aea400","#ff6319"))+
  labs(title = "ECDF plot")+
  theme_bw()+
  theme(panel.grid = element_blank(),
        legend.position = c(0.9,0.3),
        plot.title = element_text(hjust = 0.5),
        axis.text = element_text(size = 10),
        axis.title = element_text(size=14, color = "black"))

```


---

## 🕸️ 十、相关性 & 网络图

### 两组矩阵的相关性分析

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/R绘图模板合集/两组矩阵的相关性分析')#设置工作路径


#加载包
library(psych)
library(circlize)
#加载数据
#OTU表格
df1 <- read.table("otu.txt",sep="\t",header = T,row.names = 1,check.names = F)
df1 <- as.data.frame(t(df1)) 
#环境因子
df2 <- read.table("data.txt",sep="\t",header = T,row.names = 1,check.names = F)

#相关性计算
data <- corr.test(df1,df2,use = "pairwise",
                  method="spearman",#指定方法
                  adjust="BH",#矫正P值,"holm", "hochberg", "hommel", "bonferroni", "BH", "BY", "fdr", "none"
                  alpha=0.05,#指定显著性阈值
                  minlength=3)#指定缩写最小长度
#查看p、r值并提取p、r值
# df_p <- data$p#未矫正
df_p <- data$p.adj
df_r <- data$r
#确定存在相互作用关系的阈值，将相关性R矩阵内不符合的数据转换为0
df_r[abs(df_r)<0.3] = 0
df_r <- t(df_r)#转置矩阵为作图要求格式
###可视化
#pheatmap包
library(pheatmap)
pheatmap(df_r,
         angle_col = "45",
         cellwidth=12, cellheight=17,
         cluster_rows=F, treeheight_col = 30,
         fontsize=5,
         color = colorRampPalette(c("navy", "white", "firebrick3"))(50))

###ComplexHeatmap包
library(ComplexHeatmap)
#颜色
col_fun <- colorRamp2(
  c(-1, 0, 1),
  c("navy", "white", "firebrick3"))
col <- col_fun(seq(-1, 1))
#绘图
Heatmap(df_r,
        col = col,#颜色设置
        # show_row_dend = T,#取消行聚类
        rect_gp = gpar(col = "white", lwd = 1),#网格颜色、宽度
        row_names_side = "right",#行名显示在左或右
        # cluster_rows = FALSE,#取消行聚类，保证行名顺序不变
        clustering_distance_columns = "euclidean",#聚类方法
        #图例设置
        heatmap_legend_param = list(
          # at = c(-1, 0, 1),
          # labels = c("low", "zero", "high"),``
          title = NULL,
          legend_height = unit(4, "cm"),
          title_position = "lefttop-rot"),
        # 居中对齐
        row_names_centered = F,
        column_names_centered = F,
        # 设置选择角度
        row_names_rot = 0,
        column_names_rot = 45,
        # 设置标签字体大小
        row_names_gp = gpar(
          col = "black",
          fontsize = 8
        ),
        column_names_gp = gpar(
          col = "black",
          fontsize = 8
        ),
        #热图整体长宽
        width = unit(25, "cm"),
        height = unit(17, "cm"),
        #设置显示r绝对值大于等于0.5的数据
        cell_fun = function(j, i, x, y, width, height, fill) {
          if(df_r[i, j] >= 0.5 |df_r[i, j] <= -0.5)
            grid.text(sprintf("*", df_r[i, j]), x, y, gp = gpar(fontsize = 15))
        }
)

```


---

### 线性相关性

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/R绘图模板合集/线性相关性分析')#设置工作路径

####数据这里我们自己编写一段数据
##水稻株高
A<-c(55,58,62,75,69,59,55,66,88,69,47,58,75,68,64)
##水稻根毛数量
B<-c(100,102,105,115,109,105,101,110,125,104,95,102,120,116,109)
data <- data.frame(A,B)
#计算相关性
cor.test(A,B,data=data)
df_cor<-lm(B~A,data=data)
summary(df_cor)
###根据结果可以知道株高与根毛数量之间的相关性系数为0.936734，且呈正相关，P值为2.72e-07<0.05
###回归方程为B=0.76*A+58.96
###拟合优度R^2=0.88,即拟合度很好
###回归系数的置信区间为[0.82，0.98]

###绘图
#最简单展示——plot函数
 plot(A, B, 
     xlab = "株高", ylab = "根毛数量",
     pch = 16, frame = T)
# 添加回归线
abline(lm(B ~ A), col = "red")

####使用ggplot2包进行绘制
library(ggplot2)
library(ggprism)

p1<-ggplot(data,aes(x=A,y=B,color="orange"))+#指定数据、X轴、Y轴，颜色
  theme_bw()+#主题设置
  geom_point(size=3,shape=16)+#绘制点图并设定大小
  theme(panel.grid = element_blank())+
  labs(x="株高",y="根毛数量")+#x、y轴标题
  geom_smooth(method='lm', se=FALSE, color='turquoise4')+#添加回归线
  geom_text(aes(x=55,y=124,label="R^2=0.88\ny=0.75x+58.96"),
            color="red",family = "serif",fontface = "plain",size = 5)+
  theme_prism(palette = "candy_bright",
              base_fontface = "plain", # 字体样式，可选 bold, plain, italic
              base_family = "serif", # 字体格式，可选 serif, sans, mono, Arial等
              base_size = 16,  # 图形的字体大小
              base_line_size = 0.8, # 坐标轴的粗细
              axis_text_angle = 45)+ # 可选值有 0，45，90，270
  scale_fill_prism(palette = "candy_bright")+
  theme(legend.position = 'none')#去除图例
p1

######当然我们也可以做回归诊断，之后剔除离群点重新进行线性相关性分析
#回归诊断
par(mfrow=c(2,2))
plot(df_cor)  #绘制回归诊断图
# 图1是残差拟合，越没有趋势越好，有趋势说明可能需要二次项；
# 图2是残差正态性检验，越落在虚线上越好（理想的残差服从0附件的正态分布，否则说明模型不够充分还有趋势没有提取出来）；
# 图3检验残差是否等方差；
# 图4检验离群点，第6个样本点偏离较远，应该剔除掉重新做回归。
##根据图可以看出第10、13，14个点偏离较远，需要剔除重新进行分析
data2<-data[c(-10,-13,-14),] 
cor.test(A,B,data=data2)
df_cor2<-lm(B~A,data=data2)
summary(df_cor2)
##P值为6.284e-10<0.5,R^2=0.98，线性回归方程为y=0.73x+60.47
###重新绘图
p2<-ggplot(data2,aes(x=A,y=B,color="orange"))+#指定数据、X轴、Y轴，颜色
  theme_bw()+#主题设置
  geom_point(size=3,shape=16)+#绘制点图并设定大小
  theme(panel.grid = element_blank())+
  labs(x="株高",y="根毛数量")+#x、y轴标题
  geom_smooth(method='lm', se=FALSE, color='turquoise4')+#添加回归线
  geom_text(aes(x=55,y=124,label="R^2=0.98\ny=0.73x+60.47"),
            color="red",family = "serif",fontface = "plain",size = 5)+
  theme_prism(palette = "candy_bright",
              base_fontface = "plain", # 字体样式，可选 bold, plain, italic
              base_family = "serif", # 字体格式，可选 serif, sans, mono, Arial等
              base_size = 16,  # 图形的字体大小
              base_line_size = 0.8, # 坐标轴的粗细
              axis_text_angle = 45)+ # 可选值有 0，45，90，270
  scale_fill_prism(palette = "candy_bright")+
  theme(legend.position = 'none')#去除图例

p2
#显示剔除点
p2+geom_point(aes(x=69,y=104),shape=8,color="red",size=3)+
  geom_point(aes(x=75,y=120),shape=8,color="red",size=3)+
  geom_point(aes(x=68,y=116),shape=8,color="red",size=3)

```


---

### mantel test分析

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/mantel test')#设置工作路径

#加载包
library(vegan)
library(dplyr)
library(ggcor)
library(ggplot2)

#加载数据
#OTU表格，并根据绘图需求对其进行编辑和转换
df <- read.table("otu.txt",header = 1,row.names = 1,check.names = F,sep = "\t")
df <-data.frame(t(df))
df <- df[c(1,3,4,2,8,10,6,9,7,11,5,12),]
#环境因子数据
env <- read.table("env.txt",sep="\t",header = T,row.names = 1,check.names = F)

#绘制环境因子间相关性热图，pearson方法
p <- quickcor(env,#数据
              type = "upper",#绘制上半部分
              method = "pearson",#方法
              show.diag = T) +#是否显示对角线
  geom_square()+#类型
  scale_fill_gradient2( high = '#fe6263', mid = 'white',low = '#7caaff')  #颜色设置
p
#计算OTU与环境因子之间的mantel test的r值和p值并定义OTU数据分组
df_mantel <- mantel_test(df, env, #数据
                         mantel.fun = 'mantel',#方法
                         spec.dist.method = 'bray', 
                         env.dist.method = 'euclidean',
                         spec.select = list("Yield components" = 1:4,
                                            "Wheat growth indicators" = 5:8,
                                            "Yield" = 9:12))#将群落数据按组进行分开
#定义标签,即对mantel分析后的数据按照个人需求进行分割
df_mantel <- df_mantel %>%
  mutate(df_r = cut(r, breaks = c(-Inf, 0.25, 0.5, Inf),
                labels = c("< 0.25", "0.25 - 0.5", ">= 0.5")),#定义Mantel的R值范围标签
         df_p = cut(p.value, breaks = c(-Inf, 0.01, 0.05, Inf),
                    labels = c("< 0.01", "0.01 - 0.05", ">= 0.05")))#定义Mantel的P值范围标签
#自定义连线类型
df_mantel$linetype <- ifelse(df_mantel$p.value>=0.05,2,1)
df_mantel$linetype <- factor(df_mantel$linetype,levels = c("1","2"))
###在热图基础上添加mantel test数据
quickcor(env, type = "upper",method = "pearson",show.diag = T,cor.test = T) +
  geom_square()+
  scale_fill_gradient2( high = '#fe6263', mid = 'white',low = '#7caaff')+
  geom_square() +
  geom_mark(r = NA,sig.thres = 0.05, size = 6, color = "black")+#显著性标签
  anno_link(df_mantel, aes(color = df_p,
                           size = df_r,
                           linetype = linetype),
            label.size = 4,
            label.fontface = 1,
            curvature = 0.2,#连接线变为曲线
            nudge_x =0.2)+#标签位置
  scale_size_manual(values = c(0.8, 1.4, 2))+#连线粗细设置
  scale_color_manual(values = c("#ffa83a","#dc4fff","#cacdd2"))+#线条颜色设置
  scale_linetype_manual(values = c(1,2))+
  guides(fill = guide_colorbar(title = "Pearson's r", order = 1),#图例相关设置
         size = guide_legend(title = "Mantel's r",order = 2),
         color = guide_legend(title = "p-value", order = 3),
         linetype = "none") # 设置线条粗细

```


---

### 网络图+微生物丰度与基因间的相关性+正负相关

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/网络图+微生物丰度与基因间的相关性+正负相关')#Set working path

#加载R包
library(igraph) # Network Analysis and Visualization
library(Hmisc) # Harrell Miscellaneous
library(psych) # Procedures for Psychological, Psychometric, and Personality Research
library(dplyr) # A Grammar of Data Manipulation
library(tidyr) # Tidy Messy Data

##加载OTU数据及基因数据
mic <- read.table("Genus.txt", sep="\t", header=T, check.names=F,row.names = 1)
gene <- read.table("gene.txt", sep="\t", header=T, check.names=F,row.names = 1)
group <- read.table("group.txt", sep="\t", header=T, check.names=F)
##根据样本名合并数据
mic <- as.data.frame(t(mic))
mic$sample <- rownames(mic)
gene$sample <- rownames(gene)
df <- merge(mic, gene, by = "sample")
rownames(df) <- df$sample
df <- df[-1]
head(df)

##转换数据格式
data<-as.matrix(df)

#基于psych包计算相关性并基于Benjamini-Hochberg("FDR-BH")法校正p值
cor<- corr.test(data, method="spearman",adjust="BH")

##提取微生物与基因相关性部分的R值和P值
r.cor<-data.frame(cor$r)[1:11,12:23]
p.cor<-data.frame(cor$p)[1:11,12:23]

##保存数据
write.csv(r.cor,file='cor_r.csv')
write.csv(p.cor,file='cor_p.csv')

###以p>0.05作为筛选阈值,R值不做筛选
r.cor[p.cor>0.05] <- 0

###将数据转换为long format进行合并并添加连接属性
r.cor$from = rownames(r.cor)
p.cor$from = rownames(p.cor)
#将p值转换为long format
p_value <-  p.cor %>% 
  gather(key = "to", value = "p", -from) %>%
  data.frame()
#合并数据并设置阈值、连接线属性等
cor.data<- r.cor %>% 
  gather(key = "to", value = "r", -from) %>%
  data.frame() %>%
  left_join(p_value, by=c("from","to")) %>%
  mutate(
    linecolor = ifelse(r > 0,"positive","negative"), # 设置连接线的属性，可用于设置线型和颜色。
    linesize = abs(r) #设置连接线宽度
  ) # 此输出仍有重复连接，后面需进一步去除。
head(cor.data)

###设置节点属性
vertices <- c(as.character(cor.data$from),as.character(cor.data$to)) %>%
  as_tibble() %>%
  group_by(value) %>% 
  summarise()
colnames(vertices) <- "name"

##添加变量分类属性
vertices <- vertices %>%
  left_join(group,by="name")#将分类属性添加进去

###对节点属性表进行排序
vertices$group <- factor(vertices$group, levels = c("Mic","Gene" ))
vertices <- vertices %>%
  arrange(group) 

###构建graph数据结构
graph <- graph_from_data_frame(cor.data, vertices = vertices, directed = FALSE )
graph

##设置连接线的宽度为r值，并将标签设置为name
E(graph)$weight <- abs(E(graph)$r)
V(graph)$label <- V(graph)$name
###保存数据并基于Gephi进行可视化
write_graph(graph, "net.graphml", format="graphml")

##参考：
# 1）https://blog.csdn.net/qq_39859424/article/details/124462727

```


---

### 弦图_chord

```r

rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/弦图_chord")
#安装、加载包
# install.packages("circlize")
# install.packages("statnet")

library(circlize) # Circular Visualization
library(statnet) # Software Tools for the Statistical Analysis of Network Data

#准备数据
data <- read.table("data.txt",sep="\t",header = T,row.names = 1,check.names = F)
data <- as.matrix(data)
#生成作图数据
df <- data.frame(from = rep(rownames(data), ncol(data)),
                 to = rep(colnames(data), each = nrow(data)),
                 value = as.vector(data))

##颜色设定
color <- NULL
#为“to”列进行颜色赋值
color[c("A","B","C","D","E")] <- c("blue","red","yellow","green","pink")
#为“from”列进行颜色赋值
color[rownames(data)] <- c("#40A4D8","#33BEB7","#B2C224","#FECC2F","#FBA127",
                           "#F66320","#DB3937","#A463D7","#0C5BCE","grey","black")
#绘图
# circos.par(start.degree = 90)#调整放置方向
chordDiagram(df, 
             grid.col =color,#颜色设置
             grid.border=NULL,#边框颜色设置，设置为NULL则默认与填充色一致
             transparency = 0.2,#连接颜色透明度
             link.lwd = 0.01,#线条宽度
             link.lty = 1,    # 线路类型
             link.border = 0,#边框颜色
             directional = -1,#表示线条的方向，0代表没有方向，1代表正向，-1代表反向，2代表双向
             diffHeight = mm_h(2),#外圈和中间连线的间隔
             direction.type = c("diffHeight","arrows"), #线条是否带有箭头
             link.arr.type = "big.arrow")#箭头类型

circos.clear()#重新设置图形参数和内部变量

# 图例制作
legend("right",pch=20,legend=rownames(data),
       col=color[rownames(data)],bty="n",
       cex=1,pt.cex=3,border="black") # 设定图例

# 设置图片文件名、长宽和字体大小
pdf(file="plot.pdf", width=9, height=5, pointsize=8)
# circos.par(start.degree = 90)#调整放置方向
chordDiagram(df, 
             grid.col =color,#颜色设置
             grid.border=NULL,#边框颜色设置，设置为NULL则默认与填充色一致
             transparency = 0.2,#连接颜色透明度
             link.lwd = 0.01,#线条宽度
             link.lty = 1,    # 线路类型
             link.border = 0,#边框颜色
             directional = -1,#表示线条的方向，0代表没有方向，1代表正向，-1代表反向，2代表双向
             diffHeight = mm_h(2),#外圈和中间连线的间隔
             direction.type = c("diffHeight","arrows"), #线条是否带有箭头
             link.arr.type = "big.arrow")#箭头类型
legend("right",pch=20,legend=rownames(data),
       col=color[rownames(data)],bty="n",
       cex=1,pt.cex=3,border="black") # 设定图例
dev.off()

###由于修改文字注释代码的麻烦，所以这里需要后期使用AI软件或PS软件对一些重叠的文字进行调整

```


---

### 桑基图

```r

rm(list=ls())
#设置工作环境
setwd("D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\桑基图")

#下载包
# install.packages("ggplot2")
# install.packages("ggalluvial")
#载入包
library(ggplot2)
library(ggalluvial)

#加载数据
data <- read.table("data.txt",header = T, check.names = F)

#格式转换
df <- to_lodes_form(data[,1:ncol(data)],
                           axes = 1:ncol(data),
                           id = "value")
print(df)#预览数据

##绘制桑基图（Sankey diagram）
col<- rep(c('#2e1f54', '#52057f', '#bf033b', '#f00a36',
            '#ed3b21', '#ff6908', '#ffc719','#598c14', 
            '#335238', '#4a8594', '#051736', '#dbe0e3'), 3)#自定义颜色

pdf("test.pdf",width = 8, height = 6)#新建一个PDF文件
ggplot(df, aes(x = x, fill=stratum, label=stratum,
               stratum = stratum, alluvium  = value))+#数据
  geom_flow(width = 0.3,#连线宽度
            curve_type = "sigmoid",#曲线形状
            alpha = 0.5,#透明度
            color = 'white',#间隔颜色
            size = 0.1)+#间隔宽度
  geom_stratum(width = 0.28)+#图中方块的宽度
  geom_text(stat = 'stratum', size = 2, color = 'black')+
  scale_fill_manual(values = col)+#自定义颜色
  theme_void()+#主题（无轴及网格线）
  theme(axis.line=element_line(linetype=1,color="grey",size=1.5),#坐标轴粗细、类型及颜色设置
        plot.title = element_text(size=15,hjust = 0.5), #标题大小和位置
        legend.position = 'none')#去除图例
dev.off()#关闭PDF

```


---

## 🔬 十一、生信专用图

### 火山图

```r

rm(list=ls())#clear Global Environment
setwd('D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\火山图')#设置工作路径

#安装所需R包
# install.packages("ggplot2")
# install.packages('ggrepel')
#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggrepel) # Automatically Position Non-Overlapping Text Labels with'
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization

# 读取数据
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)

#数据分类
df$group<-as.factor(ifelse(df$pvalue < 0.05 & abs(df$log2FoldChange) >= 2, 
                           ifelse(df$log2FoldChange>= 2 ,'up','down'),'NS'))
#标签
df$label<-ifelse(df$pvalue<0.05&abs(df$log2FoldChange)>=4,"Y","N")
df$label<-ifelse(df$label == 'Y', as.character(df$gene), '')
####绘制火山图
p <- ggplot(df, aes(log2FoldChange, -log10(pvalue),fill = group)) +
  geom_point(color="black",alpha=0.6, size=3,shape=21)+
  theme_bw()+
  theme(panel.grid=element_blank(),
        axis.text=element_text(color='#333c41',size=10),
        legend.text = element_text(color='#333c41',size=10),
        legend.title = element_blank(),
        axis.title= element_text(size=12))+
  geom_vline(xintercept = c(-2, 2), lty=3,color = 'black', lwd=0.8) + #辅助线
  geom_vline(xintercept = c(-4, 4), lty=3,color = 'red', lwd=0.8)+
  geom_hline(yintercept = -log10(0.05), lty=3,color = 'black', lwd=0.8) +
  scale_fill_manual(values = c('blue','grey','red'))+
  labs(title="volcanoplot",
       x = 'log2 fold change',
       y = '-log10 pvalue')+
  geom_text_repel(aes(x = log2FoldChange,#标签
                      y = -log10(pvalue),          
                      label=label),                       
                  max.overlaps = 10000,
                  size=3,
                  box.padding=unit(0.8,'lines'),
                  point.padding=unit(0.8, 'lines'),
                  segment.color='black',
                  show.legend=FALSE)
p

#背景色
color <- colorRampPalette(brewer.pal(11,"BrBG"))(30)
#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

```


---

### 多组火山图

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/多组火山图')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(dplyr) # A Grammar of Data Manipulation
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization

#加载数据（随机编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")
df$group <- factor(df$group, levels = c("group1-group2", "group1-group3", "group2-group3"))
##与之前绘制单组火山图一致，先根据设定阈值确定所有OTU的显著性
df$group2<-as.factor(ifelse(df$p_value < 0.05 & abs(df$log2FC) >= 2, 
                           ifelse(df$log2FC>= 2 ,'up','down'),'NS'))
df$group2 <- factor(df$group2, levels = c("up", "down", "NS"))
##确定添加标签的数据
df$label<-ifelse(df$p_value<0.05&abs(df$log2FC)>=4,"Y","N")
df$label<-ifelse(df$label == 'Y', as.character(df$OTU), '')

##为了构建图形中所有数据点背景框，需要先确定每个组的最大值与最小值
df_bg <- df %>%
  group_by(group) %>%
  summarize(max_log2FC = max(log2FC),min_log2FC = min(log2FC))

##绘制图中各组数据点中的灰色背景柱子
p <- ggplot()+
  ##y轴正半轴的灰色背景
  geom_col(data = df_bg, 
           mapping = aes(group,max_log2FC),
           fill = "grey85", width = 0.8, alpha = 0.5) +
  ##y轴负半轴的灰色背景
  geom_col(data = df_bg, 
           mapping = aes(group, min_log2FC),
           fill = "grey85", width = 0.8, alpha = 0.5)
p

##添加各组的数据点
p1 <- p+geom_jitter(data = df,
                   mapping = aes(x = group, y = log2FC, color = group2),
                   size= 3,width =0.4, alpha = 0.7)
p1

##将分组信息通过在X=0的位置添加方块进行展示
#有两种方式可以实现，1）和灰色背景柱子添加方式一致，采用geom_col函数添加
p2 <- p1+geom_col(data = df_bg,
                  mapping = aes(x= group, y = 0.3, fill = group))+
  geom_col(data = df_bg,
           mapping = aes(x= group, y = -0.3, fill = group))
p2
#2）通过geom_rect函数手动添加,分组太多不推荐使用
p2 <- p1+geom_rect(data = df_bg,
                   aes(xmin = 1-0.4, xmax = 1+0.4, ymin = -0.3, ymax = 0.3),
                   alpha = 0.5,
                   color = NA,
                   fill = "red",
                   show.legend = F)+
  geom_rect(data = df_bg,
            aes(xmin = 2-0.4, xmax = 2+0.4, ymin = -0.3, ymax = 0.3),
            alpha = 0.5,
            color = NA,
            fill = "green",
            show.legend = F)+
  geom_rect(data = df_bg,
            aes(xmin = 3-0.4, xmax = 3+0.4, ymin = -0.3, ymax = 0.3),
            alpha = 0.5,
            color = NA,
            fill = "yellow",
            show.legend = F)
  
p2

##在方块中添加分组的文字信息
p3 <- p2+geom_text(data=df_bg,
                   mapping = aes(x=group, y=0, label=group),
                   size = 4, color ="#dbebfa")
p3


####个性化绘图模板
ggplot()+
  ##y轴正半轴的灰色背景
  geom_col(data = df_bg, 
           mapping = aes(group,max_log2FC),
           fill = "grey85", width = 0.8, alpha = 0.5) +
  ##y轴负半轴的灰色背景
  geom_col(data = df_bg, 
           mapping = aes(group, min_log2FC),
           fill = "grey85", width = 0.8, alpha = 0.5)+
  #添加各组的数据点
  geom_jitter(data = df,
              mapping = aes(x = group, y = log2FC, color = group2),
              size= 3,width = 0.4, alpha = 0.7)+
  # 通过在X=0的位置添加方块进行展示分组信息，采用geom_col方法添加
  geom_col(data = df_bg,
           mapping = aes(x= group, y = 0.4, fill = group),
           width = 0.8)+
  geom_col(data = df_bg,
           mapping = aes(x= group, y = -0.4, fill = group),
           width = 0.8)+
  # 在方块中添加分组的文字信息
  geom_text(data=df_bg,
            mapping = aes(x=group, y=0, label=group),
            size = 4, color ="#dbebfa",fontface = "bold")+
  #根据需要决定是添加辅助线
  # geom_hline(yintercept = 4, lty=2, color = '#ae63e4', lwd=0.8)+
  # geom_hline(yintercept = -4, lty=2, color = '#ae63e4', lwd=0.8)+
  #颜色设置
  scale_color_manual(values = c("#e42313", "#0061d5", "#8b8c8d"))+
  scale_fill_manual(values = c("#ed7902", "#ef5734", "#b5c327"))+
  #添加显著性标签
  geom_text_repel(data = df,
                  mapping = aes(x = group, y = log2FC, label = label),
                  max.overlaps = 10000,
                  size=3,
                  box.padding=unit(0.8,'lines'),
                  point.padding=unit(0.8, 'lines'),
                  segment.color='black',
                  show.legend=FALSE)+
  # 主题设置
  theme_classic()+
  theme(axis.line.x = element_blank(),
        axis.text.x = element_blank(),
        axis.ticks.x = element_blank(),
        axis.line.y = element_line(linewidth = 0.8),
        axis.text.y = element_text(size = 12, color = "black"),
        axis.title = element_text(size = 14, color = "black"),
        axis.ticks.y = element_line(linewidth = 0.8))+
  labs(x = "group", y = "Log2FoldChange", fill= NULL, color = NULL)+
  #调整图例
  guides(color=guide_legend(override.aes = list(size=6,alpha=1)))

#背景色
color <- colorRampPalette(brewer.pal(11,"BrBG"))(30)
#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

```


---

### 曼哈顿图

```r

#设置工作环境
rm(list=ls())
setwd("D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\曼哈顿图")

#安装包
# install.packages("qqman")
# install.packages("CMplot")
# install.packages("ggplot2")
# install.packages("tidyverse")
# install.packages("ggforce")
# install.packages("ggprism")
#加载包
library(qqman)
library(CMplot)
library(ggplot2)
library(tidyverse)
library(ggforce)
library(ggprism)
##############1、使用qqman包进行绘制##################
#加载数据——以qqman包自带示例数据gwasresult数据为例
df1 <- gwasResults#数据中SNP为SNP名称，CHR为染色体编号，BP为碱基位置，P为p值
head(df1)#预览数据

manhattan(df1,#数据
          col = c('#30A9DE','#EFDC05','#E53A40','#090707'),#交替使用颜色展示
          suggestiveline = -log10(1e-05),#－log10(1e－5)处添加"suggestive"横线
          genomewideline = -log10(5e-08),#－log10(5e－10)处添加"genome-wide sigificant"横线
          highlight = snpsOfInterest,#内置高亮的snp数据， 也可以对snpOfInterest进行设置
          annotatePval = 0.05,#标记p值小于0.05的点
          annotateTop = T,#如果为T，则仅批注低于注解阈值的每个染色体上的顶部点，为F则标记所有小于注解阈值的点。
          main = "XXXXXXXX"#标题
          )
##可以使用??manhattan查看具体参数

#############2、使用CMplot包进行绘制##################
#加载数据——以CMplot包自带示例数据pig60k数据为例
data(pig60K)#预览数据

CMplot(pig60K,#示例数据
       chr.den.col=c("black","green","red"),#SNP密度展示
       file="jpg",#绘制图片类型
       memo="",#输出文件名中添加一个字符
       dpi = 600)#绘制图片的分辨率

#可以使用??CMplot查看具体参数,根据需要进行设置
CMplot(Pmap,
       col=c("#4197d8", "#f8c120", "#413496", "#495226",
             "#d60b6f", "#e66519", "#d581b7", "#83d3ad", "#7c162c", "#26755d"),
       bin.size=1e6, bin.range=NULL, bin.legend.num=10, pch=19, type="p",
       band=1, H=1.5, ylim=NULL, cex.axis=1, lwd.axis=1.5, cex.lab=1.5,
       plot.type="b", multracks=FALSE, points.alpha=100L, cex=c(0.5,1,1),
       r=0.3, outward=FALSE, ylab=expression(-log[10](italic(p))), 
       ylab.pos=3, xticks.pos=1, mar = c(3,6,3,3), threshold = NULL, 
       threshold.col="red", threshold.lwd=1, threshold.lty=2, 
       amplify= TRUE, signal.cex = 1.5, signal.pch = 19, 
       signal.col=NULL, signal.line=2, highlight=NULL, highlight.cex=1, 
       highlight.pch=19, highlight.type="p", highlight.col="red", 
       highlight.text=NULL, highlight.text.col="black", highlight.text.cex=1, 
       highlight.text.xadj=NULL, highlight.text.yadj=NULL, 
       highlight.text.font=3, chr.labels=NULL, chr.border=FALSE,
       chr.labels.angle=0, chr.den.col="black", chr.pos.max=FALSE, cir.band=1, 
       cir.chr=TRUE, cir.chr.h=1.5, cir.legend=TRUE, cir.legend.cex=0.6, 
       cir.legend.col="black", LOG10=TRUE, box=FALSE, conf.int=TRUE, 
       conf.int.col=NULL, file.output=TRUE, file=c("jpg","pdf","tiff"), 
       dpi=300, height=NULL, width=NULL, memo="", main="", main.cex=1.5, 
       main.font=2, trait.legend.ncol=NULL, verbose=TRUE)

###################3、使用ggplot2包进行绘制################
#数据，同样以qqman包自带数据gwasresult为例
df <- gwasResults
###数据处理
df %>% 
  group_by(CHR) %>% 
  summarise(df_chr_len=max(BP)) %>% #计算染色体长度
  mutate(total = cumsum(df_chr_len) - df_chr_len) %>%
  select(-df_chr_len) %>% #计算染色体初始位置
  left_join(df, ., by="CHR") %>%
  arrange(CHR, BP) %>%
  mutate( BPcum = BP + total)->df_SNP_position#计算累计SNP的位置

head(df_SNP_position)#预览数据

###绘图
#X轴标签位置
X_axis <-  df_SNP_position %>% group_by(CHR) %>% summarize(center=( max(BPcum) +min(BPcum) ) / 2 )
#添加高亮和注释信息：snpsOfInterest中的rs编号和P值大于10的点
data <- df_SNP_position %>%
  mutate( is_highlight=ifelse(SNP %in% snpsOfInterest, "yes", "no")) %>%
  mutate( is_annotate=ifelse(-log10(P)>10, "yes", "no"))
#绘图
ggplot(data, aes(x=BPcum, y=-log10(P))) +
  geom_point(aes(color=as.factor(CHR)),alpha=0.8, size=1.5)+
  scale_color_manual(values = rep(c('#30A9DE','#EFDC05','#E53A40','#090707'), 22 ))+#颜色设置
  scale_x_continuous(label = X_axis$CHR, breaks= X_axis$center)+#设定X轴
  scale_y_continuous(expand = c(0, 0) ) +#去除绘图区和X轴之间的gap
  geom_hline(yintercept = c(6, -log10(0.05/nrow(df_SNP_position))), #添加阈值线
             color = c('green', 'red'),size = 1.2, 
             linetype = c("dotted", "twodash")) + 
  geom_point(data=subset(data, is_highlight=="yes"), color="green", 
             size=2)+facet_zoom(x = BPcum >= 3000 & BPcum <=3500)+#展示某一区域的p值情况
  theme_prism(palette = "flames",#使用ggprism包自带主题
              base_fontface = "plain", 
              base_family = "serif", 
              base_size = 16,  
              base_line_size = 0.8, 
              axis_text_angle = 45)+ 
  theme(legend.position = "none",#去除图例
        panel.grid = element_blank(),
        panel.border = element_blank(),
        axis.line.x = element_line(),
        axis.line.y = element_line())
#参考：https://blog.csdn.net/ddxygq/article/details/103555955

```


---

### 基于ggmsa多序列比对及可视化

```r

##清空环境变量并设置工作目录
rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/数据分析及可视化/多序列比对及可视化")

####基于ggmsa包进行多序列比对及可视化
##安装包
# if (!require("BiocManager"))
#   install.packages("BiocManager")
# BiocManager::install("ggmsa")
##加载包
library(ggmsa)
library(ggplot2)
##数据-包括蛋白和核酸两种类型数据
protein_sequences <- system.file("extdata", "sample.fasta", 
                                 package = "ggmsa")
miRNA_sequences <- system.file("extdata", "seedSample.fa", 
                               package = "ggmsa")
nt_sequences <- system.file("extdata", "LeaderRepeat_All.fa", 
                            package = "ggmsa")

##可视化
ggmsa(protein_sequences, 320, 350, color = "Clustal", 
      font = "DroidSansMono", char_width = 0.5, seq_name = TRUE )
ggmsa(miRNA_sequences, color = "Chemistry_AA", 
      font = "DroidSansMono", char_width = 0.5, seq_name = TRUE )
ggmsa(nt_sequences, color = "Chemistry_AA", 
      font = "DroidSansMono", char_width = 0.5, seq_name = TRUE )

###基础参数
##颜色
available_colors()
#> 1.color schemes for nucleotide sequences currently available:
#> Chemistry_NT Shapely_NT Taylor_NT Zappo_NT
#> 2.color schemes for AA sequences currently available:
#> ClustalChemistry_AA Shapely_AA Zappo_AA Taylor_AA LETTER CN6 Hydrophobicity
#Clustal
ggmsa(protein_sequences, start = 320, end = 360, color = "Clustal", show.legend = TRUE)
#Color by Chemistry(Default)
ggmsa(protein_sequences, start = 330, end = 360, color = "Chemistry_AA", show.legend = TRUE)
#Color by Shapely
ggmsa(protein_sequences, start = 330, end = 360, color = "Shapely_AA", show.legend = TRUE)
#Color by Taylor
ggmsa(protein_sequences, start = 330, end = 360, color = "Taylor_AA", show.legend = TRUE)
#Color by Zappo
ggmsa(protein_sequences, start = 330, end = 360, color = "Zappo_AA", show.legend = TRUE)
#Color by LETTER
ggmsa(protein_sequences, start = 330, end = 360, color = "LETTER", show.legend = TRUE)

#Color Customzation
library(RColorBrewer)
library(pals)
my_pal <- colorRampPalette(rev(brewer.pal(n = 9, name = "Reds")))
my_cutstom <- data.frame(names = c(LETTERS[1:26],"-"), 
                         color = my_pal(27), 
                         stringsAsFactors = FALSE)
head(my_cutstom)
#>   names   color
#> 1     A #67000D
#> 2     B #7A040F
#> 3     C #8D0911
#> 4     D #A00D14
#> 5     E #AD1116
#> 6     F #B91319
pals::pal.bands(my_cutstom$color)
ggmsa(protein_sequences, 300, 345, 
      custom_color = my_cutstom, 
      char_width = 0.5, 
      border = "white",
      show.legend = TRUE)


##字体
available_fonts()
#> font families currently available:
#> helvetical mono TimesNewRoman DroidSansMono
ggmsa(protein_sequences, start = 340, end = 360, font = "helvetical")
ggmsa(protein_sequences, start = 340, end = 360, font = "TimesNewRoman")
ggmsa(protein_sequences, start = 340, end = 360, font = "DroidSansMono")
ggmsa(protein_sequences, start = 340, end = 360, font = NULL)


####与ggplot2类似，该包支持MSA注释
##geom_seqlogo
ggmsa(protein_sequences, 320, 350, char_width = 0.5, seq_name = TRUE) + 
  geom_seqlogo(color = "Chemistry_AA")

##geom_GC—使用气泡图显示GC含量
ggmsa(nt_sequences, font = NULL,color = "Chemistry_NT") + 
  geom_seqlogo(color = "Chemistry_NT") + geom_GC() + 
  theme(legend.position = "none")

##geom_seed-突出 miRNA 序列上的 seed 区
#有背景
ggmsa(miRNA_sequences, char_width = 0.5, color = "Chemistry_NT") + 
  geom_seed(seed = "GAGGUAG", star = TRUE)
#去除背景
ggmsa(miRNA_sequences, char_width = 0.5, seq_name = TRUE, none_bg = TRUE) + 
  geom_seed(seed = "GAGGUAG")

##geom_msaBar-用条形图显示序列保守性
ggmsa(protein_sequences, 320, 350, char_width = 0.5, seq_name = TRUE) + 
  geom_msaBar()

##geom_helix-用圆弧图表示RNA二级结构
RF03120 <- system.file("extdata/Rfam/RF03120_SS.txt", package="ggmsa")
RF03120_fas <- system.file("extdata/Rfam/RF03120.fasta", package="ggmsa")
SS <- readSSfile(RF03120, type = "Vienna")
ggmsa(RF03120_fas, font = NULL,border = NA, color = "Chemistry_NT", seq_name = FALSE) +
  geom_helix(SS)


###主题修改
##char_width: 字符宽度，默认 0.9
ggmsa(protein_sequences, start = 320, end = 360, char_width = 0.5)

##none_bg = TRUE: 仅显示字符，去除有色背景
ggmsa(protein_sequences, start = 320, end = 360, none_bg = TRUE) + 
  theme_void()

##seq_name = TRUE: 显示序列名称
ggmsa(protein_sequences, 164, 213, seq_name = TRUE)

##show.legend = TRUE: 显示多序列比对图的图例
ggmsa(protein_sequences, 190, 213, font = NULL, show.legend = TRUE)

##border = NA: 去除描边；border = "white": 白色描边
ggmsa(protein_sequences, 164, 213, font = NULL, border = NA)
ggmsa(protein_sequences, 164, 213, font = NULL, border = "white")

##position_highlight: 特定位置高亮
ggmsa(protein_sequences, 164, 213, position_highlight = c(190, 195), char_width = 0.5)

####其他模块
##Sequence logo
seqlogo(protein_sequences, start = 330, end = 350, color = "Chemistry_AA", font = "DroidSansMono")
seqlogo(nt_sequences, start = 1, end = 20, color = "Chemistry_NT", font = "DroidSansMono")

##Sequence Bundles
negative <-  system.file("extdata", "Gram-negative_AKL.fasta", package = "ggmsa")
positive <-  system.file("extdata", "Gram-positive_AKL.fasta", package = "ggmsa")
ggSeqBundle(negative, bundle_color = "red")
ggSeqBundle(msa = c(negative,positive))

##RNA二级结构
transat_file <- system.file("extdata", "helix.txt", package = "R4RNA")
known_file <- system.file("extdata", "vienna.txt", package = "R4RNA")
connect_file <- system.file("extdata", "connect.txt", package = "R4RNA")
known <- readSSfile(known_file, type = "Vienna")
transat <- readSSfile(transat_file, type = "Helix")
connect <- readSSfile(connect_file , type = "Connect")
gghelix(known)
gghelix(list(known = known, predicted = transat), overlap = FALSE)
gghelix(list(known = known, predicted = transat), color_by = "value", overlap = TRUE)
gghelix(list(known = known, predicted = connect), overlap = TRUE)


###查看模式
##四个参数：
# use_dot: 在图中将匹配的字符显示为点
# disagreement: 是否高亮显示不匹配的字符,默认为TRUE
# ignore_gaps: 选择TRUE 时，列中的间隙将被视为该行不存在。
# ref: 指定参考序列（输入参考序列名称即可，必须在输入数据内）

ggmsa(protein_sequences, 330, 350, char_width = 0.5, 
      seq_name = T, consensus_views = T, 
      disagreement = T, use_dot = T)
ggmsa(protein_sequences, 330, 350, char_width = 0.5, 
      seq_name = T, consensus_views = T, 
      disagreement = F, use_dot = F)
ggmsa(protein_sequences, 330, 350, char_width = 0.5, 
      seq_name = T, consensus_views = T, 
      disagreement = F, use_dot = F,
      ignore_gaps = T)
ggmsa(protein_sequences, 330, 350, char_width = 0.5, 
      seq_name = T, consensus_views = T ,
      use_dot = T, ref = "PH4H_Rhizobium_loti")

##根据序列保守性进行着色
ggmsa(protein_sequences, 320, 350, color = "Chemistry_AA", 
      # font = NULL, 
      seq_name = T ,border = "white", by_conservation = TRUE)

######实例操作
##将ggmsa的示例数据下载到本地进行读取
# install.packages ("Biostrings")
library(Biostrings)
fa <- readAAStringSet('sample.fasta')
#个性化绘图模板
ggmsa(fa, #数据文件
      start = 330, end = 360, #显示的位置
      font = "TimesNewRoman",#字体
      color = "Chemistry_AA",#颜色
      char_width = 0.6, #字符宽度
      border = "white",#描边颜色
      show.legend = F
      )+
  #sequenc logo注释
  geom_seqlogo(color = "Chemistry_AA",#配色
               font = "TimesNewRoman",
               adaptive = F)+
  #条形图
  geom_msaBar()


###参考：
# 1）https://yulab-smu.top/ggmsa/articles/ggmsa.html

```


---

### 序列分析图

```r

rm(list=ls())

#安装包
# install.packages("ggseqlogo")
#加载包
library(ggseqlogo)

#数据——支持序列与矩阵两种格式的文件
#以ggseqlogo包自带示例数据ggseqlogo_sample为例
data(ggseqlogo_sample)
#DNA数据
df1<-pfms_dna
#氨基酸数据
df2<-seqs_aa
#序列格式
df3<-seqs_dna$MA0011.1
#矩阵格式——代表碱基位置及相应碱基在该位置的出现次数
df4<-pfms_dna$MA0031.1

###使用函数ggseqlogo()进行展示
??ggseqlogo#查看参数
ggseqlogo(data, facet = "wrap", scales = "free_x", ncol = NULL,
          nrow = NULL, ...)
#基本绘图
ggseqlogo(df1)
ggseqlogo(df3)

#方法的选择——bits(默认)和probability
p1<-ggseqlogo(df3,method="bits")
p2<-ggseqlogo(df3,method="probability")
cowplot::plot_grid(p1,p2,ncol=1)

#绘制多个图时通过facet与ncol控制
ggseqlogo(df1, facet = "wrap",ncol = 1)
ggseqlogo(df1, facet = "wrap",ncol = 2)

#序列类型的指定——通过seq_type参数指定序列类型，默认为“auto”自动识别
ggseqlogo(df1, facet = "wrap",ncol = 2, seq_type="dna")#"aa"、"dna"、"rna"
ggseqlogo(df2, facet = "wrap",ncol = 2, seq_type="aa")

#配色方案——col_scheme参数设置，具体配色方案通过?list_col_schemes查看
list_col_schemes(v = T)#展示配色方案
ggseqlogo(df1,col_scheme='clustalx')
ggseqlogo(df1,col_scheme='taylor')
###自定义配色——make_col_scheme参数实现
#离散型配色
col1<-make_col_scheme(chars = c("A","G", "T", "C"), 
                        groups = c("g1","g2", "g3","g4"),
                        cols = c("red","green","blue","yellow"))
ggseqlogo(df1,col_scheme=col1)
#连续型配色
col2<-make_col_scheme(chars=c("A","G", "T", "C"),
                      values=1:4,
                      name='group')
ggseqlogo(df1,col_scheme=col2)

##设置字体——通过font参数实现，?list_fonts查看内置字体
list_fonts(v = T)#查看内置字体
a<-ggseqlogo(df3,font="xkcd_regular")
b<-ggseqlogo(df3,font="roboto_slab_regular")
c<-ggseqlogo(df3,font="helvetica_regular")
d<-ggseqlogo(df3,font="helvetica_light")
cowplot::plot_grid(a,b,c,d,ncol=2)

##字母宽度——stack_width参数设置
a<-ggseqlogo(df3,stack_width=1)
b<-ggseqlogo(df3,stack_width=0.5)
cowplot::plot_grid(a,b,ncol=1)

##注释——与ggplot2注释类似
p1<-ggplot2::ggplot()+geom_logo(df3)+theme_logo()#可视化
p1
#添加文字注释
p1+ggplot2::annotate("text", x=6, y=1, label="This is a text\n annotation!")
#添加线条
p1+ggplot2::annotate("segment", x=1, xend = 3, y=1.5, yend = 1.5, size=3)
#添加图形注释
p1+ggplot2::annotate("rect", xmin = 6.5, xmax = 7.5, ymin = -0.05, ymax = 0.8, 
                     alpha=0.2, col="grey", fill="green")


###模板代码
library(ggplot2)
col1<-make_col_scheme(chars = c("A","G", "T", "C"), 
                      groups = c("g1","g2", "g3","g4"),
                      cols = c("red","green","blue","yellow"))#自定义配色
ggplot()+geom_logo(df1$MA0018.2,#数据
                            method="bits",#方法
                            seq_type="dna",#序列类型
                            col_scheme=col1,#配色方案
                            font="xkcd_regular",#字体
                            stack_width=0.8#字母宽度
                            )+
  annotate("text", x=5.5, y=2, color='red',label="This is a text\n annotation!")+
  annotate("segment", x=4.5, xend = 6.5, y=1.6, yend = 1.6, size=3)+
  annotate("rect", xmin = 2.5, xmax = 3.5, ymin = -0.05, ymax = 2.05, 
           alpha=0.2, col="grey", fill="green")+
  theme_logo()
#参考:https://omarwagih.github.io/ggseqlogo/

```


---

### Venn

```r

rm(list=ls())#clear Global Environment
setwd('D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\Venn')#设置工作路径

#安装包
#install.packages("venn")
# install.packages("VennDiagram")
#加载R包
library(VennDiagram) # Generate High-Resolution Venn and Euler Plots 
library (venn)
library( RColorBrewer) # not installed on this machine
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggprism) # A 'ggplot2' Extension Inspired by 'GraphPad Prism'
#读取数据,为OTU水平的丰度表
data <- read.table(file="otu.txt",sep="\t",header=T,check.names=FALSE,row.names = 1)
#查看前6行
head(data)
#组内合并
df <- data.frame(A=rowSums(data[,c(1:3)]),
                 B=rowSums(data[,c(4:6)]),
                 C=rowSums(data[,c(7:9)]),
                 D=rowSums(data[,c(10:12)]))
head(df)
#创建空列表
df1 <- list()
#获取每个样本（组）所有的OTU
for (i in 1:length(colnames(df))){
  group<- colnames(df)[i]
  df1[[group]] <- rownames(df)[which(df[,i]!= 0)]
}
###绘图
#Venn包绘制
venn(df1, #数据
     zcolor=c('red','yellow','blue','green'),#颜色设置，可选择自带的“style”或者无色‘bw’
     opacity = 0.6,#颜色透明度
     box=F,#边框去除
     sncs=1.5,#组名字体大小
     ilcs=0.8)#图片中数字大小
####计算各组总OTU个数并绘制柱状图进行展示
df2<-df
df2[df2>0]=1
df3<-rbind(df2,Total=colSums(df2))
#提取作图数据
df4<-as.data.frame(t(df3[3010,])) 
df4$group<-rownames(df4)
#绘图
ggplot(df4,aes(x =group, y = Total)) +
  geom_col(aes(fill=group),width = 0.8,alpha=0.6)+
  geom_text(aes(label=Total, y=Total+20), position=position_dodge(0.9), vjust=0)+
  labs(x = NULL, y = NULL)+
  theme_prism(palette = "candy_bright",
              base_fontface = "plain", 
              base_family = "serif", 
              base_size = 16, 
              base_line_size = 0.8, 
              axis_text_angle = 45)+
  scale_y_continuous(expand = c(0,0),limits = c(0,1500))+
  theme(legend.position = "none")+
  scale_fill_manual(values = c('red','yellow','blue','green'))

# 使用VennDiagram包中的get.venn.partitions函数查看并导出交集结果
df_inter <- get.venn.partitions(df1)
for (i in 1:nrow(df_inter)) df_inter[i,'values'] <- paste(df_inter[[i,'..values..']],
                                                          collapse = ', ')
df_inter<-df_inter[-c(5, 6)]
write.table(df_inter, 'df_Venn.txt', row.names = FALSE, sep = '\t', quote = FALSE)

```


---

### Venn(大于5组)

```r

#加载包
library(UpSetR)
library(RColorBrewer)

#生成作图数据或者导入数据
data <- data.frame(set1 = paste(rep("word_" , 200) , sample(c(1:1000) , 200 , replace=F) , sep=""),
                   set2 = paste(rep("word_" , 200) , sample(c(1:1000) , 200 , replace=F) , sep=""),
                   set3 = paste(rep("word_" , 200) , sample(c(1:1000) , 200 , replace=F) , sep=""),
                   set4 = paste(rep("word_" , 200) , sample(c(1:1000) , 200 , replace=F) , sep=""),
                   set5 = paste(rep("word_" , 200) , sample(c(1:1000) , 200 , replace=F) , sep=""),
                   set6 = paste(rep("word_" , 200) , sample(c(1:1000) , 200 , replace=F) , sep=""))
View(data)
# data <- read.table(file="otu.txt",sep="\t",header=T,check.names=FALSE,row.names = 1)
# data[data>0]=1
#绘图
upset(fromList(data))
#参数调整
upset(fromList(data),
      #显示数据集的所有数据
      nsets = length(data),
      #显示前多少个
      nintersects=30,
      #点点图和条形图的比例
      mb.ratio = c(0.5, 0.5),
      #对集合进行排序
      sets=c("set1","set2","set3","set4","set5","set6"),
      #图中点的大小
      point.size = 3,
      #图中线的粗细
      line.size = 1,  
      #y轴的名称
      mainbar.y.label = "This is y-axis",
      #x轴的名称
      sets.x.label="This is x-axis",      
      #6个参数intersection size title, intersection size tick labels, set size title, set size tick labels, set names, numbers above bars的设置
      text.scale = c(1.5, 1.5, 1.5, 1.5,1.5, 1.5),  
      #图中阴影部分的颜色
      shade.color = "green",
      #柱状图的颜色
      sets.bar.color=brewer.pal(6, "Set1"),
      queries=list(list(query=intersects,params=list("set1","set2"),color="red",active=T),
             list(query=intersects,params=list("set2","set3"),color="blue",active=T),
             list(query=intersects,params=list("set3","set4"),color="green",active=T),
             list(query=intersects,params=list("set4","set5"),color="yellow",active=T)))

```


---

### 成比例Venn图

```r

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/成比例Venn图')#设置工作路径

#安装包
# devtools::install_github("jolars/eulerr")
#加载R包
library(ggvenn) # Draw Venn Diagram by 'ggplot2' 
library(eulerr) # Area-Proportional Euler and Venn Diagrams with Ellipses


###读取数据,以OTU水平的丰度表为例
data <- read.table(file="otu.txt",sep="\t",header=T,check.names=FALSE,row.names = 1)
#查看前6行
head(data)
#组内合并
df <- data.frame(A=rowSums(data[,c(1:3)]),
                 B=rowSums(data[,c(4:6)]),
                 C=rowSums(data[,c(7:9)]))
head(df)
#创建空列表
df1 <- list()
#获取每个样本（组）所有的OTU
for (i in 1:length(colnames(df))){
  group<- colnames(df)[i]
  df1[[group]] <- rownames(df)[which(df[,i]!= 0)]
}

###如果个人数据并非OTU类型数据，可按照过程中产生的df或者df1准备数据


###基于ggvenn包绘制常规Venn图
ggvenn(df1,#数据列表
       fill_color = c("#0099e5", "#ff4c4c", "#34bf49"), # 填充色
       fill_alpha = 0.5,# 填充透明度
       show_percentage = T,#是否显示百分比
       digits = 1,#百分比的小数点位数
       set_name_color = "black", #标签颜色
       set_name_size = 5,# 标签字体大小
       text_color = "black",# 交集个数颜色
       text_size = 4, # 交集个数文字大小
       stroke_color = "white",#边缘线条颜色
       stroke_alpha = 0.5,# 边缘线条透明度
       stroke_size = 0.5,#边缘线条粗细
       stroke_linetype = "solid", #边缘线条,实线：solid;虚线：twodash longdash;点：dotdash dotted dashed;无：blank
       # columns = NULL,# 指定列名绘图，最多选择4个，NULL为默认全选
       # show_elements = F,# 当为TRUE时，显示具体的交集情况，而不是交集个数
       # label_sep = "\n"# 当show_elements = T时生效
       )->p1
p1

####基于eulerr包绘制成比例Venn图
plot(
  euler(
    df1,#数据
    shape = "circle"#图案的形状，ellipse、circle
  ),
  fills = list(fill = c( "#ff4c4c", "#0099e5", "#34bf49"),alpha=0.6), # 填充的颜色和透明度
  labels=list(col="black",#组名标签的颜色
              font=2, fontfamily = "serif",#组名标签的字体设置
              cex=1.5),#组名标签的大小
  edges = list(col = "white", lwd=2, lty=1), #图形边缘线条颜色及粗细设置
  quantities = list(type = c("counts","percent"),#标签显示类型，百分比和数字
                    cex=1),#数字大小
)->p2
p2

###拼图
library(patchwork)
p1+p2+
  plot_annotation(
    tag_levels = c('A', '1'), 
    tag_prefix = 'Fig. ',
    tag_sep = '.',
  ) & theme(plot.tag.position = c(0, 0.98),
            plot.tag = element_text(size = 15,
                                    hjust = 0, 
                                    vjust = 0,
                                    color="black")
  )



##参考：https://cran.r-project.org/web/packages/eulerr/vignettes/gallery.html

```


---

### 分类水平的聚类分析+注释

```r

#########微信公众号：科研后花园
######推文题目：分类水平的聚类分析+注释！！！

rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/分类水平的聚类分析+注释")

#加载R包
library(MicrobiotaProcess) # A comprehensive R package for managing and analyzing microbiome and other ecological data within the tidy framework
library(dplyr) # A Grammar of Data Manipulation
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(phyloseq) # Handling and analysis of high-throughput microbiome census data
library(ggtree) # an R package for visualization of tree and annotation data

#加载数据
sample <- read.table("sample.txt",check.names = F, row.names = 1, header = 1, sep = "\t")
OTU<- read.table("otu.txt",check.names = F, row.names = 1, header = 1, sep = "\t")
Tax <- read.table("tax.txt",check.names = F, row.names = 1, header = 1, sep = "\t")

##利用phyloseq包重新构造可转换为分析的数据格式
ps <- phyloseq(sample_data(sample),
               otu_table(as.matrix(OTU), taxa_are_rows=TRUE), 
               tax_table(as.matrix(Tax)))
ps

#转换数据格式
df <- ps %>% as.MPSE()
df

# 结果提取
taxa.tree <- df %>% 
  mp_extract_tree(type="taxatree")
taxa.tree

###通过ggtree可视化
ggtree(
  taxa.tree,
  linewidth=0.6,
  color = "black",
  size = 0.3) +
  #添加标签
  geom_tiplab(size=2, offset=0.1)+
  #节点散点
  geom_point(data = td_filter(!isTip),
             fill="white",
             size=2,
             shape=21)+
  # 对不同门进行颜色填充
  geom_hilight( 
    data = td_filter(nodeClass == "Phylum"),
    mapping = aes(node = node, fill = label))+
  #自定义颜色
  scale_fill_manual(
    values=c("#3be8b0", "#1aafd0", "#6a67ce","#ffb900","#fc636b"),
    guide=guide_legend(keywidth=1, keyheight=1),
    name="Phylum")

##门水平
ggtree(
  taxa.tree,
  layout="radial",#更改进化树类型
  linewidth=0.6,
  color = "black",
  size = 0.3) +
  #添加标签
  geom_tiplab(size=3, offset=0.1)+
  #节点散点
  geom_point(data = td_filter(!isTip),
             fill="white",
             size=2,
             shape=21)+
  # 对不同门进行颜色填充
  geom_hilight( 
    data = td_filter(nodeClass == "Phylum"),
    mapping = aes(node = node, fill = label))+
  #自定义颜色
  scale_fill_manual(
    values=c("#3be8b0", "#1aafd0", "#6a67ce","#ffb900","#fc636b"),
    guide=guide_legend(keywidth=1, keyheight=1),
    name="Phylum")

##纲水平
ggtree(
  taxa.tree,
  layout="radial",#更改进化树类型
  linewidth=0.6,
  color = "black",
  size = 0.3) +
  #添加标签
  geom_tiplab(size=3, offset=0.1)+
  #节点散点
  geom_point(data = td_filter(!isTip),
             fill="white",
             size=2,
             shape=21)+
  # 对不同门进行颜色填充
  geom_hilight( 
    data = td_filter(nodeClass == "Class"),
    mapping = aes(node = node, fill = label))+
  labs(fill="Class")

##"radial"
ggtree(
  taxa.tree,
  layout="radial",#更改进化树类型
  linewidth=0.6,
  color = "black",
  size = 0.3) +
  #添加标签
  geom_tiplab(size=3, offset=0.1)+
  #节点散点
  geom_point(data = td_filter(!isTip),
             fill="white",
             size=2,
             shape=21)+
  # 对不同纲进行颜色填充
  geom_hilight( 
    data = td_filter(nodeClass == "Phylum"),
    mapping = aes(node = node, fill = label))+
  #自定义颜色
  scale_fill_manual(
    values=c("#3be8b0", "#1aafd0", "#6a67ce","#ffb900","#fc636b"),
    guide=guide_legend(keywidth=1, keyheight=1),
    name="Phylum")

##"circular"
ggtree(
  taxa.tree,
  layout="circular",#更改进化树类型
  linewidth=0.6,
  color = "black",
  size = 0.3) +
  #添加标签
  geom_tiplab(size=3, offset=0.1)+
  #节点散点
  geom_point(data = td_filter(!isTip),
             fill="white",
             size=2,
             shape=21)+
  # 对不同门进行颜色填充
  geom_hilight( 
    data = td_filter(nodeClass == "Phylum"),
    mapping = aes(node = node, fill = label))+
  #自定义颜色
  scale_fill_manual(
    values=c("#3be8b0", "#1aafd0", "#6a67ce","#ffb900","#fc636b"),
    guide=guide_legend(keywidth=1, keyheight=1),
    name="Phylum")

#####导出图片后，可以将图片导入AI或者PS中，将背景色块置于底层

```


---

## ✨ 十二、特殊图表 & 其他

### 3D曲线图+多分组

```r

#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/3D曲线图+多分组")

##加载包
library(scatterplot3d) # 3D Scatter Plot
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package

##加载数——以origin绘图软件模板快中的数据为例
df <- read.table("data.txt",header = T, check.names = F)

##数据格式转换
df1 <- melt(df, id.vars = c("Wavelength"), 
            measure.vars = c('Amplitude_1','Amplitude_2','Amplitude_3',
                             'Amplitude_4','Amplitude_5','Amplitude_6','Amplitude_7'))
#添加轨道列
df1$y <- rep(c(0.5,1.5,2.5,3.5,4.5,5.5,6.5),each = 512)


##绘图
#在第y=0.5上绘制Amplitude_1数据
p <- scatterplot3d(x=df1$Wavelength[1:512], y=df1$y[1:512], z=df1$value[1:512],
                   type = 'l',#图形类型
                   lwd=2,#线条粗细
                   scale.y=0.9,#y轴相对于x轴和z轴的刻度
                   color = "#0099e5",#颜色
                   y.ticklabs=c("",'Amplitude_1','Amplitude_2','Amplitude_3',
                                'Amplitude_4','Amplitude_5','Amplitude_6',
                                'Amplitude_7'),#更改y轴刻度标签
                   xlim = c(min(df1$Wavelength),max(df1$Wavelength)),
                   ylim = c(0, 7),zlim=c(0,2500),#设置各轴范围
                   y.axis.offset=0.5,#y轴刻度标签相对于轴的偏移位置
                   box = F,#是否显示框
                   grid = T,#是否显示网格
                   angle = 40,#调整角度,x轴和y轴之间的角度
                   xlab = paste0(colnames(df1)[1]," (nm)"),
                   ylab = '', zlab = 'Amplitude (mV)'#轴标题设置
                   )

#在第y=1.5上绘制Amplitude_2数据
p$points3d(df1$Wavelength[513:1024], df1$y[513:1024], df1$value[513:1024],
           type = 'l',col="#0099e5",lwd=2)#线条粗细
##同理，添加其他数据
p$points3d(df1$Wavelength[1025:1536], df1$y[1025:1536], df1$value[1025:1536],
           type = 'l',col="#ff4c4c",lwd=2)#线条粗细
p$points3d(df1$Wavelength[1537:2048], df1$y[1537:2048], df1$value[1537:2048],
           type = 'l',col="#ff4c4c",lwd=2)#线条粗细
p$points3d(df1$Wavelength[2049:2560], df1$y[2049:2560], df1$value[2049:2560],
           type = 'l',col="#34bf49",lwd=2)#线条粗细
p$points3d(df1$Wavelength[2561:3072], df1$y[2561:3072], df1$value[2561:3072],
           type = 'l',col="#34bf49",lwd=2)#线条粗细
p$points3d(df1$Wavelength[3073:3584], df1$y[3073:3584], df1$value[3073:3584],
           type = 'l',col="#7d3f98",lwd=2)#线条粗细

##添加图例
legend('topright',c('groupA','groupB','groupC','groupD'),
       col=c("#0099e5","#ff4c4c","#34bf49","#7d3f98"),
       lty=1,bty = 'n',lwd=2)


###后续细节需要借助AI或者PS进行调整
#如：y轴标签及其位置、刻度样式、文字大小等


######通过散点图方式一次性绘制
#根据分组添加颜色
colors <- c("#0099e5","#0099e5", "#ff4c4c", "#ff4c4c","#34bf49","#34bf49","#7d3f98")
colors <- colors[df1$variable]
p1 <- scatterplot3d(x=df1$Wavelength, y=df1$y, z=df1$value,
                    pch = 16,#散点类型
                    color = colors,#颜色
                    cex.symbols = 0.5,#散点大小
                    scale.y=0.9,#y轴相对于x轴和z轴的刻度
                    y.ticklabs=c("",'Amplitude_1','Amplitude_2','Amplitude_3',
                                 'Amplitude_4','Amplitude_5','Amplitude_6',
                                 'Amplitude_7'),#更改y轴刻度标签
                    xlim = c(min(df1$Wavelength),max(df1$Wavelength)),
                    ylim = c(0, 7),zlim=c(0,2500),#设置各轴范围
                    y.axis.offset=0.5,#y轴刻度标签相对于轴的偏移位置
                    box = F,#是否显示框
                    grid = F,#是否显示网格
                    angle = 40,#调整角度,x轴和y轴之间的角度
                    xlab = paste0(colnames(df1)[1]," (nm)"),
                    ylab = '', zlab = 'Amplitude (mV)'#轴标题设置
)
##添加图例
legend('topright',c('groupA','groupB','groupC','groupD'),
       col=c("#0099e5","#ff4c4c","#34bf49","#7d3f98"),
       lty=1,bty = 'n',lwd=2)

```


---

### 凹凸图Bump chart

```r

rm(list = ls())

#安装R包
# install.packages("ggbump")
# install.packages("ggplot2")
# install.packages("ggprism")
#加载R包
library(ggbump)
library(ggplot2)
library(ggprism)
library(dplyr)
#数据——随机生成
#注：要保证X轴和Y轴为数值型数据，否则无法绘制
df<-data.frame(
  x=rep(1:6,4),
  y=c(10,12,14,12,14,16, 12,14,12,10,12,12, 14,16,10,14,16,10, 16,10,16,16,10,14),
  z=c(rep('g1',6),rep('g2',6),rep('g3',6),rep('g4',6)))
head(df)

#绘图
ggplot(df, aes(x = x, y = y, color = z)) +#数据
  geom_bump(size = 1.2)+#基本凹凸图绘制
  geom_point(size = 10)+#添加节点
  scale_color_prism(palette = 'candy_bright')+#自定义颜色
  theme_void() +#主题
  geom_text(data = df,
            aes(x = x, label = z),
            size = 4, color='white')+#添加标签
  theme(legend.position = "none")#去除图例


#参考：https://r-charts.com/ranking/ggbump/

```


---

### 词云图

```r

rm(list = ls())
#安装R包
# install.packages("wordcloud2")
#加载R包
library(wordcloud2)

#数据——以示例数据为例
df1<-demoFreq
df2<-demoFreqC
#基础绘图
wordcloud2(df2, #数据
           size=1.5,#字体大小
           fontFamily = 'Segoe UI',#字体
           fontWeight = 'bold',#字体粗细
           color='random-light',#字体颜色设置
           backgroundColor="black"#背景颜色设置
           )
#改变词云方向
wordcloud2(df1, size = 2, minRotation = -pi/6, maxRotation = -pi/6,#文本旋转角度范围
           rotateRatio = 0.5)#文本选择概率

#####更改形状
##常规形状——'star'、'circle'、'cardioid'、'diamond'、'triangle-forward'、'triangle'、'pentagon'
wordcloud2(df1,size=1.5,color='random-light',backgroundColor="black",
           shape = 'star')#改变形状
wordcloud2(df1,size=1.5,color='random-light',backgroundColor="black",
           shape = 'circle')#改变形状
wordcloud2(df1,size=1.5,color='random-light',backgroundColor="black",
           shape = 'cardioid')#改变形状
wordcloud2(df1,size=1.5,color='random-light',backgroundColor="black",
           shape = 'diamond')#改变形状
wordcloud2(df1,size=1.5,color='random-light',backgroundColor="black",
           shape = 'triangle-forward')#改变形状
wordcloud2(df1,size=1.5,color='random-light',backgroundColor="black",
           shape = 'triangle')#改变形状
wordcloud2(df1,size=1.5,color='random-light',backgroundColor="black",
           shape = 'pentagon')#改变形状
###新版本wordcloud2包已经不支持自定义形状，大家如果需要可根据这个博主的推文进行操作：https://blog.csdn.net/tandelin/article/details/103977242


#参考：https://r-graph-gallery.com/196-the-wordcloud2-library.html

```


---

### 雷达图

```r

rm(list = ls())

#数据——生成绘图数据
set.seed(12)
df <- data.frame(
  group=LETTERS[1:5],
  V1=sample(1:50, 5, replace = FALSE),
  V2=sample(20:50, 5, replace = FALSE),
  V3=sample(1:50, 5, replace = FALSE),
  V4=sample(30:50, 5, replace = FALSE),
  V5=sample(10:50, 5, replace = FALSE))
rownames(df)<-df$group#修改行名
df<-df[-1]#删除多余行
df <- rbind(rep(50,5) , rep(0,5) , df)#加入限定雷达图极限值范围

#安装包
# install.packages("fmsb")
#加载包
library(fmsb) # Functions for Medical Statistics Book with some Demographic Data
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualization 
####绘图
#背景色
color <- colorRampPalette(brewer.pal(11,"PuOr"))(30)
#填充色建议大家使用一些浅色系的颜色，不然容易覆盖底部的图
radarchart(df,#数据
           pcol=rainbow(5),#多边形特征：线的颜色
           # pfcol=rainbow(5),#多边形特征：填充色
           plwd=2,#多边形特征：线宽
           plty=2,#多边形特征：线形
           cglcol='grey',#网格特征:网格颜色
           cglty=1,#网格特征:网格线形
           axistype=1,#坐标轴类型
           axislabcol='red',#网格特征:轴颜色
           caxislabels=seq(0,50,5),#网格特征:轴范围
           cglwd=0.8,#网格特征:网格线宽
           vlcex=0.8)#组标签大小
#添加图例
legend(x=1.2, y=1.2, legend = rownames(df[-c(1,2),]), 
       bty = "n", pch=20 , col=rainbow(5) , 
       text.col = "black", cex=1.2, pt.cex=3)
#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

#加入填充色
col<- rainbow(5)
colors_in <- alpha(col,0.1)
#绘图
radarchart(df,#数据
           pcol=rainbow(5),#多边形特征：线的颜色
           pfcol=colors_in,#多边形特征：填充色
           plwd=1.5,#多边形特征：线宽
           plty=2,#多边形特征：线形
           cglcol='grey70',#网格特征:网格颜色
           cglty=1,#网格特征:网格线形
           axistype=1,#坐标轴类型
           axislabcol='red',#网格特征:轴颜色
           caxislabels=seq(0,50,5),#网格特征:轴范围
           cglwd=0.8,#网格特征:网格线宽
           vlcex=0.8)#组标签大小
#添加图例
legend(x=1.2, y=1.2, legend = rownames(df[-c(1,2),]), 
       bty = "n", pch=20 , col=rainbow(5) , 
       text.col = "black", cex=1.2, pt.cex=3)

#添加背景
grid.raster(alpha(color, 0.2), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)
#参考：https://r-graph-gallery.com/143-spider-chart-with-saveral-individuals.html

```


---

### 平行坐标图

```r

rm(list = ls())

#加载R包
library(GGally)
library(ggthemes)
library(ggprism)
library(scagnostics)
#加载数据，使用R自带数据集iris
df<- iris

####绘图
#可选参数
??ggparcoord#查看该函数下的参数

ggparcoord(data,
           columns = 1:ncol(data),
           groupColumn = NULL,
           scale = "std",
           scaleSummary = "mean",
           centerObsID = 1,
           missing = "exclude",
           order = columns,
           showPoints = FALSE,
           splineFactor = FALSE,
           alphaLines = 1,
           boxplot = FALSE,
           shadeBox = NULL,
           mapping = NULL,
           title = "")
#展示
p1<-ggparcoord(df,
           columns = 1:4, #数据行数
           scale="globalminmax",#No scaling
           groupColumn = "Species",#按照分组显示不同颜色
           order = "anyClass",#水平坐标轴排序，可选参数有'skewness', 'allClass', 'anyClass', 'Outlying', 'Skewed', 'Clumpy', 'Sparse', 'Striated', 'Convex', 'Skinny', 'Stringy', 'Monotonic'
           showPoints = T,#是否显示点 
           title = "Parallel Coordinates chart",#标题
           alphaLines = 0.5) + #线的粗细
  theme_pander()+#模板主题设置
  theme(plot.title = element_text(size=10))+#标题大小设置
  scale_color_prism(palette = "candy_bright")#使用ggrism包的主题颜色
p1

p2<-ggparcoord(df,
               columns = 1:4, #数据行数
               groupColumn = "Species",#按照分组显示不同颜色
               order = "Outlying",#水平坐标轴排序
               showPoints = T,#是否显示点 
               title = "Parallel Coordinates chart",#标题
               scale="uniminmax",#Standardize to Min = 0 and Max = 1
               alphaLines = 0.5) + #线的粗细
  theme_pander()+#模板主题设置
  theme(plot.title = element_text(size=10))+#标题大小设置
  scale_color_prism(palette = "neon")#使用ggrism包的主题颜色
p2

p3<-ggparcoord(df,
               columns = 1:4, #数据行数
               groupColumn = "Species",#按照分组显示不同颜色
               order = "Clumpy",#水平坐标轴排序
               showPoints = T,#是否显示点 
               title = "Parallel Coordinates chart",#标题
               scale="std",#Normalize univariately (substract mean & divide by sd)
               alphaLines = 0.5) + #线的粗细
  theme_pander()+#模板主题设置
  theme(plot.title = element_text(size=10))+#标题大小设置
  scale_color_prism(palette = "autumn_leaves")#使用ggrism包的主题颜色
p3

p4<-ggparcoord(df,
               columns = 1:4, #数据行数
               groupColumn = "Species",#按照分组显示不同颜色
               order = "Sparse",#水平坐标轴排序
               showPoints = T,#是否显示点 
               title = "Parallel Coordinates chart",#标题
               scale="center",#Standardize and center variables
               alphaLines = 0.5) + #线的粗细
  theme_pander()+#模板主题设置
  theme(plot.title = element_text(size=10))+#标题大小设置
  scale_color_prism(palette = "sunny_garden")#使用ggrism包的主题颜色
p4

#拼图
cowplot::plot_grid(p1,p2,p3,p4,ncol=2)

#显示箱线图
ggparcoord(df,
           columns = 1:4, 
           scale="globalminmax",
           groupColumn = "Species",
           showPoints = T,
           title = "Parallel Coordinates chart",
           alphaLines = 0.5,
           boxplot = T) + 
  theme_map()+
  theme(plot.title = element_text(size=10))+
  scale_color_prism(palette = "candy_bright")

#分面显示
p1+facet_wrap(~Species)
p2+facet_wrap(~Species)
p3+facet_wrap(~Species)
p4+facet_wrap(~Species)

```


---

### 三元相图

```r

rm(list = ls())
setwd("D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\三元相图")

#安装R包
# install.packages("ggtern")
#加载R包
library(ggtern) # An Extension to 'ggplot2', for the Creation of Ternary Diagrams
library(RColorBrewer) # ColorBrewer Palettes
library(grid) # The Grid Graphics Package
library(scales) # Scale Functions for Visualizatio
# 加载数据
df <- read.table(file="data.txt",sep="\t",header=T,check.names=FALSE)
# 创建分组信息数据集
df$group <-  rep(c("T", "D", "L", "K"),each = 20)
#计算3个样本的平均值定义点的大小
df$size <- (apply(df[2:4], 1, mean))

#配色
col <- colorRampPalette(brewer.pal(11,"Set1"))(4)
#背景色
color <- colorRampPalette(brewer.pal(11,"PuOr"))(30)
#绘图
ggtern(data=df,aes(x=A,y=B,z=C))+ #X,Y,Z轴分别代表的变量
  geom_mask()+# 显示超出边界的点
  geom_point(aes(size=size,#以散点图形式呈现，大小是size
                 color=group),#颜色映射的为group变量
             alpha=0.8)+#透明度
  scale_colour_manual(values = col)+#自定义颜色
  guides(color = guide_legend(override.aes = list(size = 4)))+#改变颜色映射图例符号大小
  theme_classic()+#主题
  labs(title = "Ternary plot")+#标题
  theme(axis.line=element_line(linetype=1,color="grey",size=1),#坐标轴粗细、类型及颜色设置
    plot.title = element_text(size=15,hjust = 0.5)) #标题大小和位置
#添加背景
grid.raster(alpha(color, 0.1), 
            width = unit(1, "npc"), 
            height = unit(1,"npc"),
            interpolate = T)

```


---

### 花瓣图

```r

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

```


---

### 议会图

```r

###########parliament diagrams###################
rm(list = ls())

#安装包
# install.packages("ggparliament")
# install.packages("tidyverse")
#加载包
library(ggparliament)
library(tidyverse)

#数据
df<-election_data %>% 
  filter(country == "Russia" & year == 2016)
#将数据转换成绘图所需格式,可以在type中修改类型
df1 <- parliament_data(election_data = df,
                                 type = "semicircle", # 议会类型
                                 parl_rows = 10,      # 议会的行数
                                 party_seats = df$seats) # 席位
df2 <- parliament_data(election_data = df,
                       type = "circle", # 议会类型
                       parl_rows = 10,      # 议会的行数
                       party_seats = df$seats) # 席位
df3 <- parliament_data(election_data = df,
                       type = "classroom", # 议会类型
                       parl_rows = 11,      # 议会的行数
                       party_seats = df$seats) # 席位
df4 <- parliament_data(election_data = df,
                       type = "horseshoe", # 议会类型
                       parl_rows = 10,      # 议会的行数
                       party_seats = df$seats) # 席位
#绘图
ggplot(df1, aes(x = x, y = y, colour = party_short)) +
  geom_parliament_seats() + 
  geom_highlight_government(government == 1) +
  geom_parliament_bar(colour = colour, party = party_long, label = TRUE) +#使用条形图显示比例
  draw_majoritythreshold(n = 225, label = TRUE, type = "semicircle") +#添加阈值线
  theme_ggparliament() +
  labs(title = "R") +#标题
  scale_colour_manual(values = df1$colour, 
                      limits = df1$party_short) +#颜色
  draw_partylabels(type = "semicircle",   ##标签
                   party_names = party_long,
                   party_seats = seats,
                   party_colours = colour)+
  draw_totalseats(n = 450, type = "semicircle")#标签

#其他类型
ggplot(df2, aes(x = x, y = y, color = party_short)) +
  geom_parliament_seats() + 
  theme_ggparliament() +
  labs(title = "Russia, 2016") +
  scale_colour_manual(values = df1$colour, 
                      limits = df1$party_short)
ggplot(df3, aes(x = x, y = y, color = party_short)) +
  geom_parliament_seats() + 
  theme_ggparliament() +
  labs(title = "Russia, 2016") +
  scale_colour_manual(values = df1$colour, 
                      limits = df1$party_short)
ggplot(df4, aes(x = x, y = y, color = party_short)) +
  geom_parliament_seats() + 
  theme_ggparliament() +
  labs(title = "Russia, 2016") +
  scale_colour_manual(values = df1$colour, 
                      limits = df1$party_short)

#参考：https://r-charts.com/part-whole/ggparliament/

```


---

### 世界地图+采样点标记+饼图+柱状图

```r

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

```


---

### 世界地图绘制

```r

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

```


---

### 中国地图+散点+柱状图

```r

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

```


---

### 点+误差棒

```r

#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/点+误差棒")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
#构造数据
df <- read.table("data2.txt",header = T, check.names = F)
data=melt(df)
#误差棒这里我们随机编写，无实际意义
data$er=data$value/10
#绘图
ggplot(data,aes(variable,value))+
  geom_point(aes(color=variable),size=3)+
  facet_wrap(~ group, ncol =3)+
  geom_errorbar(aes(ymin = value-er, ymax = value+er,color=variable),
                width = 0.2,position = position_dodge(width = 0.8),cex=1.2)+ #添加误差棒
  labs(x="",y=NULL)+#去除轴标题
  theme_bw()+#主题
  theme(panel.grid=element_blank(),
        axis.text.y=element_text(color='black',size=10),
        axis.text.x=element_blank(),
        axis.ticks.x = element_blank(),
        legend.text = element_text(color='black',size=12),
        legend.title = element_text(color='red',size=13),
        strip.background.x = element_rect(fill = "#0081b4", color = "black"))+
  scale_y_continuous(expand = c(0, 0), limit = c(5, 23))+#去除网格线
  scale_color_manual(values=c("#004a77","#00adee","#ff8100","red"))

```


---

### 豆荚图+显著性+误差棒

```r

#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/豆荚图+显著性+误差棒")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(dplyr) # A Grammar of Data Manipulation
library(gghalves) # Compose Half-Half Plots Using Your Favourite Geoms

##构造数据
df <- read.table("data.txt",header = T, check.names = F)

# 分组计算显著性
df %>%
  group_by(Group, Period) %>%
  summarise(p_value = t.test(value[G == "CG"], value[G == "EG"])$p.value)->df1

###绘图
##groupA组
ggplot(df)+
  #绘制CG组的图
  geom_half_violin(data=df[df$Group=="groupA"&df$G=="CG",],
                   aes(Period, value,fill=G),
                   side = "l",#绘制左边小提琴
                   width=0.8,#控制宽度
                   alpha=0.7,
                   color=NA)+#边缘颜色设置
  #添加CG组的均值点
  stat_summary(data=df[df$Group=="groupA"&df$G=="CG",],
               aes(Period, value),
               position = position_nudge(x=-0.1),#控制均值点的位置
               fun = "mean", geom = "point",size=2)+
  #添加CG组的误差棒
  stat_summary(data=df[df$Group=="groupA"&df$G=="CG",],
               aes(Period, value),
               position = position_nudge(x=-0.1),#控制误差棒的位置
               color="grey10",fun.data = "mean_cl_normal",
               geom = "errorbar",
               width = 0.05,size=0.8) +
  #绘制EG组的图
  geom_half_violin(data=df[df$Group=="groupA"&df$G=="EG",],
                   aes(Period, value,fill=G),
                   side = "r",#绘制右边小提琴
                   width=0.8,alpha=0.7,
                   color=NA)+
  #添加EG组的均值点
  stat_summary(data=df[df$Group=="groupA"&df$G=="EG",],
               aes(Period, value),position = position_nudge(x=0.1),
               fun = "mean", geom = "point",size=2)+
  #添加EG组的误差棒
  stat_summary(data=df[df$Group=="groupA"&df$G=="EG",],
               aes(Period, value),position = position_nudge(x=0.1),
               color="grey10",fun.data = "mean_cl_normal",
               geom = "errorbar",
               width = 0.05,size=0.8)+
  ##手动添加误差
  annotate("text", x = 1 , y = 128,label = "ns", size= 5,color = "black")+
  annotate("text", x = 2 , y = 150,label = "***", size= 5,color = "black")+
  #主题相关设置
  labs(y="This is y-axis",x=NULL,fill=NULL,title = "groupA")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 25, vjust = 1, hjust = 1,size = 11),
        axis.text.y = element_text(size = 11),
        axis.title = element_text(size = 13),
        legend.position = c(0.9,0.2),
        legend.background = element_blank())+
  #颜色设置
  scale_fill_manual(values = c("#ff4e00","#01cd74"))->p1
p1


##groupB组
ggplot(df)+
  #绘制CG组的图
  geom_half_violin(data=df[df$Group=="groupB"&df$G=="CG",],
                   aes(Period, value,fill=G),
                   side = "l",#绘制左边小提琴
                   width=0.8,#控制宽度
                   alpha=0.7,
                   color=NA)+#边缘颜色设置
  #添加CG组的均值点
  stat_summary(data=df[df$Group=="groupB"&df$G=="CG",],
               aes(Period, value),
               position = position_nudge(x=-0.1),#控制均值点的位置
               fun = "mean", geom = "point",size=2)+
  #添加CG组的误差棒
  stat_summary(data=df[df$Group=="groupB"&df$G=="CG",],
               aes(Period, value),
               position = position_nudge(x=-0.1),#控制误差棒的位置
               color="grey10",fun.data = "mean_cl_normal",
               geom = "errorbar",
               width = 0.05,size=0.8) +
  #绘制EG组的图
  geom_half_violin(data=df[df$Group=="groupB"&df$G=="EG",],
                   aes(Period, value,fill=G),
                   side = "r",#绘制右边小提琴
                   width=0.8,alpha=0.7,
                   color=NA)+
  #添加EG组的均值点
  stat_summary(data=df[df$Group=="groupB"&df$G=="EG",],
               aes(Period, value),position = position_nudge(x=0.1),
               fun = "mean", geom = "point",size=2)+
  #添加EG组的误差棒
  stat_summary(data=df[df$Group=="groupB"&df$G=="EG",],
               aes(Period, value),position = position_nudge(x=0.1),
               color="grey10",fun.data = "mean_cl_normal",
               geom = "errorbar",
               width = 0.05,size=0.8)+
  ##手动添加误差
  annotate("text", x = 1 , y = 115,label = "ns", size= 5,color = "black")+
  annotate("text", x = 2 , y = 130,label = "***", size= 5,color = "black")+
  #主题相关设置
  labs(y="This is y-axis",x=NULL,fill=NULL,title = "groupB")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 25, vjust = 1, hjust = 1,size = 11),
        axis.text.y = element_text(size = 11),
        axis.title = element_text(size = 13),
        legend.position = c(0.9,0.2),
        legend.background = element_blank())+
  #颜色设置
  scale_fill_manual(values = c("#ff4e00","#01cd74"))->p2
p2

##拼图
library(patchwork)
p1+p2

```


---

### 分组散点&箱线图&小提琴图&条形图+拟合曲线

```r

rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/分组散点&箱线图&小提琴图&条形图+拟合曲线")

##加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(dplyr) # A Grammar of Data Manipulation
library(stringr) # Simple, Consistent Wrappers for Common String Operations
library(ggpmisc) # Miscellaneous Extensions to 'ggplot2'

##加载数据（随机编写，无实际意义）
df <- read.table("data.txt",sep="\t",header = T, check.names = F)

##为方便添加拟合曲线和后续绘图，需要根据分组信息添加一列数值型数据
#这里提取分组最后一个数字
df$G <- str_sub(df$group, 6, 6)
df$G <- as.numeric(df$G)


#####分组散点+拟合曲线
#计算均值并指定其在x轴上的位置
df %>% 
  group_by(group) %>% 
  summarise(mean_value=mean(value)) %>% 
  bind_cols(x=c(1:5))-> df1
#绘图
p1 <- ggplot(df, aes(group, value))+
  #散点图绘制
  geom_jitter(aes(fill = group), shape = 21, color = "black",
              width = 0.3, size = 3, alpha = 0.4)+
  #根据计算结果添加均值线
  geom_segment(data=df1,aes(x=x-0.2,xend=x+0.2,y=mean_value,yend=mean_value),
               color="grey20",linewidth=0.8)+
  #添加误差棒
  stat_summary(color="grey10",fun.data = "mean_cl_normal",
               geom = "errorbar",
               width = 0.15,linewidth=0.8) +
  #添加拟合曲线
  geom_smooth(aes(x = G, y = value),
              method = "lm", color = "#ee4f4f", 
              level = 0.95,
              formula = y ~ poly(x, 2, raw = TRUE),
              linetype=1,alpha=0.2,linewidth = 1)+
  #添加回归方程及R2值
  stat_poly_eq(formula = y ~ poly(x, 2, raw = TRUE), 
               aes(x = G, y = value, label = paste(after_stat(eq.label),
                                 after_stat(adj.rr.label),
                                 sep = "~~~")), 
               parse = TRUE,label.x = 0.05, label.y = 0.95,size=3.5,
               color = "black")+
  #轴标题设置
  labs(x="This is x-axis", y = "This is y-axis")+
  #颜色设置
  scale_fill_manual(values = c("#00b2a9","#a626aa","#6639b7","#aea400","#ff6319"))+
  #主题调整
  theme_bw()+
  theme(legend.position = "none",
        panel.grid = element_blank(),
        axis.text.x = element_text(size = 10, angle = 45, vjust = 1, hjust = 1),
        axis.text.y = element_text(size = 10),
        axis.title = element_text(size=12, color = "black"))
p1

#####分组箱线图+拟合曲线
p2 <- ggplot(df, aes(group, value))+
  #箱线图
  geom_boxplot(aes(color = group))+
  #散点图绘制
  geom_jitter(aes(color = group), width = 0.3, size = 1.5)+
  #添加拟合曲线
  geom_smooth(aes(x = G, y = value),
              method = "lm", color = "#ee4f4f", 
              level = 0.95,
              formula = y ~ poly(x, 2, raw = TRUE),
              linetype=1,alpha=0.2,linewidth = 1)+
  #添加回归方程及R2值
  stat_poly_eq(formula = y ~ poly(x, 2, raw = TRUE), 
               aes(x = G, y = value, label = paste(after_stat(eq.label),
                                                   after_stat(adj.rr.label),
                                                   sep = "~~~")), 
               parse = TRUE,label.x = 0.05, label.y = 0.95,size=3.5,
               color = "black")+
  #轴标题设置
  labs(x="This is x-axis", y = "This is y-axis")+
  #颜色设置
  scale_color_manual(values = c("#00b2a9","#a626aa","#6639b7","#aea400","#ff6319"))+
  #主题调整
  theme_bw()+
  theme(legend.position = "none",
        panel.grid = element_blank(),
        axis.text.x = element_text(size = 10, angle = 45, vjust = 1, hjust = 1),
        axis.text.y = element_text(size = 10),
        axis.title = element_text(size=12, color = "black"))
p2

#####分组小提琴图+拟合曲线
p3 <- ggplot(df, aes(group, value))+
  #小提琴图
  geom_violin(aes(fill = group),trim = FALSE)+
  #散点图绘制
  geom_jitter(color = "black", fill = "white", shape = 21, width = 0.3, size = 2.5)+
  #添加拟合曲线
  geom_smooth(aes(x = G, y = value),
              method = "lm", color = "#ee4f4f", 
              level = 0.95,
              formula = y ~ poly(x, 2, raw = TRUE),
              linetype=1,alpha=0.2,linewidth = 1)+
  #添加回归方程及R2值
  stat_poly_eq(formula = y ~ poly(x, 2, raw = TRUE), 
               aes(x = G, y = value, label = paste(after_stat(eq.label),
                                                   after_stat(adj.rr.label),
                                                   sep = "~~~")), 
               parse = TRUE,label.x = 0.05, label.y = 0.95,size=3.5,
               color = "black")+
  #轴标题设置
  labs(x="This is x-axis", y = "This is y-axis")+
  #颜色设置
  scale_fill_manual(values = c("#00b2a9","#a626aa","#6639b7","#aea400","#ff6319"))+
  #主题调整
  theme_bw()+
  theme(legend.position = "none",
        panel.grid = element_blank(),
        axis.text.x = element_text(size = 10, angle = 45, vjust = 1, hjust = 1),
        axis.text.y = element_text(size = 10),
        axis.title = element_text(size=12, color = "black"))
p3

#####分组条形图+拟合曲线
p4 <- ggplot(df, aes(group, value))+
  #误差棒
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.15,size=0.8)+
  #条形图
  geom_bar(aes(fill = group),stat="summary",fun=mean,position="dodge",size=0.5)+
  #散点图绘制
  geom_jitter(fill = "white", color = "black", shape = 21, width = 0.3, size = 2.5)+
  #添加拟合曲线
  geom_smooth(aes(x = G, y = value),
              method = "lm", color = "#ee4f4f", 
              level = 0.95,
              formula = y ~ poly(x, 2, raw = TRUE),
              linetype=1,alpha=0.2,linewidth = 1)+
  #添加回归方程及R2值
  stat_poly_eq(formula = y ~ poly(x, 2, raw = TRUE), 
               aes(x = G, y = value, label = paste(after_stat(eq.label),
                                                   after_stat(adj.rr.label),
                                                   sep = "~~~")), 
               parse = TRUE,label.x = 0.05, label.y = 0.95,size=3.5,
               color = "black")+
  #轴标题设置
  labs(x="This is x-axis", y = "This is y-axis")+
  #颜色设置
  scale_fill_manual(values = c("#00b2a9","#a626aa","#6639b7","#aea400","#ff6319"))+
  #主题调整
  scale_y_continuous(expand = c(0,0))+
  theme_bw()+
  theme(legend.position = "none",
        panel.grid = element_blank(),
        axis.text.x = element_text(size = 10, angle = 45, vjust = 1, hjust = 1),
        axis.text.y = element_text(size = 10),
        axis.title = element_text(size=12, color = "black"))
p4

###拼图
library(patchwork)
(p1+p2)/(p3+p4)

```


---

### 散点+箱线图+小提琴图+辅助线+显著性

```r

rm(list=ls())#clear Global Environment
#设置工作目录
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点+箱线图+小提琴图+辅助线+显著性")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggsignif) # Significance Brackets for 'ggplot2'
library(gghalves) # Compose Half-Half Plots Using Your Favourite Geoms
#加载数据
df <- read.table("data.txt",header = 1)
#将分组信息转变为factor类型数据
df$group <- factor(df$group,levels = c("A","B","C","D"))

##绘图
ggplot(df,aes(group,value,fill=group))+
  #半小提琴
  geom_half_violin(position = position_nudge(x=0.25),side = "r",width=0.8,color=NA)+
  #箱线图
  geom_boxplot(width=0.4,size=1.2,outlier.color =NA)+
  #散点图
  geom_jitter(aes(fill=group),shape=21,size=2.5,width=0.2)+
  #水平辅助线
  geom_hline(yintercept = 0, linetype = 2, color = "red",linewidth=1)+
  geom_hline(yintercept = 80, linetype = 2, color = "red",linewidth=1)+
  #显著性
  geom_signif(comparisons = list(c("A","B"),
                                 c("A","C"),
                                 c("C","D")),
              map_signif_level = T, 
              test = t.test, 
              y_position = c(100,120,130),
              tip_length = c(0,0,0,0,0,0),
              size=1,color="black",textsize = 7)+
  #y轴范围
  scale_y_continuous(limits = c(-20,140),breaks = c(0,40,80,120))+
  #主题
  theme_bw()+
  theme(panel.grid = element_blank(),
        panel.border = element_rect(size = 1),
        axis.text.x = element_text(color = "black", size = 13),
        axis.text.y = element_text(color = "black",size = 13),
        legend.position = "none",
        axis.ticks = element_line(color="black",linewidth = 1))+
  #标题设置
  labs(x=NULL,y=NULL)+
  #颜色
  scale_fill_manual(values = c("#5cc3e8","#ffdb00","#79ceb8","#e95f5c"))

```


---

### code

```r

rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/柱状图+散点图+误差线+显著性+截断")
#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggsignif) # Significance Brackets for 'ggplot2'
library(ggpubr) # 'ggplot2' Based Publication Ready Plots
library(ggbreak) # Set Axis Break for 'ggplot2'
# 加载示例数据
data <- read.table("data.txt",check.names = T,header = 1)
data$group <- factor(data$group,levels = c("OT-II","OT-I"))
##绘图
ggplot(data,aes(sample,value))+
  #误差线
  stat_summary(fun.data = 'mean_sd', geom = "errorbar", width = 0.15,size=1)+
  #柱状图
  geom_bar(aes(fill=group),color="black",stat="summary",fun=mean,position="dodge",size=0.5)+
  #散点图
  geom_jitter(color="black",size = 2.5,width = 0.2,alpha=0.9)+
  #显著性
  geom_signif(comparisons = list(c("IM","TC")),
              map_signif_level=T, 
              tip_length=0, 
              y_position = 1200, 
              size=1, 
              test = "t.test")+
  #分面
  facet_wrap(~group)+
  #颜色
  scale_fill_manual(values = c("#009700","#fa3f3f"))+
  #主题设置
  theme_classic()+
  theme(axis.line = element_line(size = 1),
        axis.text.x = element_text(color = "black", angle = 90,vjust = 0.5,hjust = 1,size = 15),
        axis.text.y = element_text(color = "black",size = 15),
        axis.ticks = element_line(color = "black",size = 1),
        legend.position = "none",
        strip.background = element_blank(),
        strip.text = element_text(color = "black",size = 16),
        axis.title = element_text(color = "black",size = 18))+
  #轴标题
  labs(x=NULL,y="cells per"~mm^2)+
  #y轴截断
  scale_y_break(c(10,45),
                scales=1.2, 
                ticklabels=c(50,100),
                space=0.2)+
  scale_y_break(c(100,600),
                scales=2.5, 
                ticklabels=c(600,800,1200),
                space=0.2)

```


---
