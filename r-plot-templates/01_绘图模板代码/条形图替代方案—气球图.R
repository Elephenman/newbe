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

