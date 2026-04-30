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

