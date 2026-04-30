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
