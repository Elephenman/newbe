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

