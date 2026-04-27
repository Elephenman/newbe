#########微信公众号：科研后花园
######推文题目：嵌套柱状图+显著性+字母标记！！！

rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/嵌套柱状图+显著性+字母标记')#设置工作路径

##加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(agricolae) # Statistical Procedures for Agricultural Research
library(ggpubr) # 'ggplot2' Based Publication Ready Plots
library(dplyr) # A Grammar of Data Manipulation
library(rstatix) # Pipe-Friendly Framework for Basic Statistical Tests

##加载数据(随机编写，无实际意义)
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")

##计算各Group的value1差异-多重比较
#方差分析
variance<-aov(value1 ~ Group, data=df)
# LSD法
MC <- LSD.test(variance,"Group", p.adj="bonferroni")
data_sg1 <- MC$groups
data_sg1$Group <- rownames(data_sg1)

##计算Group内各时期（Period）value2的差异
data_sig2 <- df %>% 
  group_by(Group) %>%
  wilcox_test(value2 ~ Period) %>% #选择wilcox方法
  adjust_pvalue() %>% #校正p值
  add_significance("p.adj") %>% 
  add_xy_position(x = "Group")#确定x与y位置

##绘图模板
ggplot(df, aes(x = Group))+
  ##绘制外围柱状图的误差线及柱子-利用value1
  stat_summary(aes(y = value1), fun.data = 'mean_sd', 
               geom = "errorbar", width = 0.15,size=0.6)+
  geom_bar(aes(y = value1), fill = "#33cc99", color="black",stat="summary",fun=mean,
           position="dodge",size=0.5,width = 0.8)+
  #添加外围柱状图的显著性——字母标记，data_sg1中储存的结果
  geom_text(data = data_sg1, aes(Group, value1+20, label = groups),olor = "black", size=6, fontface="bold")+
  ##绘制嵌套的并列柱状图的误差线及柱子-利用value2
  stat_summary(aes(y = value2, fill = Period), fun.data = 'mean_sd', 
               geom = "errorbar", width = 0.15,size=0.6,
               position = position_dodge(0.8))+
  geom_bar(aes(y = value2, fill = Period), color="black",stat="summary",
           fun=mean, position = position_dodge(0.8),size=0.5, width = 0.8)+
  #添加嵌套的并列柱状图的显著性——*号显示，data_sg2中储存的结果
  stat_pvalue_manual(data_sig2,label = "p.adj.signif",
                     label.size = 6, linetype = 1,tip.length = 0,bracket.nudge.y=-6,bracket.size=0.6)+
  #自定义颜色
  scale_fill_manual(values = c("#e95f5c","#ffc168"))+
  #自定义y轴范围
  scale_y_continuous(expand = c(0,0), limits = c(0,190), breaks = seq(0,190,25))+
  #主题相关设置
  labs(x=NULL,y="This is y-axis")+
  theme_bw()+
  theme(panel.grid = element_blank(),
        legend.position = "right",
        legend.background = element_blank(),
        axis.text = element_text(size=12),
        axis.text.x = element_text(angle = 45, vjust = 1, hjust = 1),
        axis.title = element_text(size=15),
        legend.title = element_text(color = 'red',size=15),
        legend.text = element_text(color = 'black',size=11))
