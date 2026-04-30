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


