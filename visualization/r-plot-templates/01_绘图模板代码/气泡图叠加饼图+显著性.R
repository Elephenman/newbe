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