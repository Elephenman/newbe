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

