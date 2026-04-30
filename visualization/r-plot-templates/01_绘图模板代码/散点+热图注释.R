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

