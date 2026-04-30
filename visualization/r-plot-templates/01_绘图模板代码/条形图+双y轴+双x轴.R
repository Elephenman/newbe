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
