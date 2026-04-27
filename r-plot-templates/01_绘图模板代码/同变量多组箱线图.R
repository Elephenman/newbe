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
