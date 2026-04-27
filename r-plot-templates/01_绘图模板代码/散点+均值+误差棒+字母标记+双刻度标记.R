rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点+均值+误差棒+字母标记+双刻度标记")

##加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(dplyr) # A Grammar of Data Manipulation
library(gridExtra) # Miscellaneous Functions for "Grid" Graphics
library(agricolae)#实现多重比较的包

##加载数据（随机编写，无实际意义）
df <- read.table("data.txt",sep="\t",header = T, check.names = F)

##计算均值并指定其在x轴上的位置
df %>% 
  group_by(group) %>% 
  summarise(mean_value=mean(value)) %>% 
  bind_cols(x=c(1:5))-> df1

##多重比较
#数据的方差检验
variance<-aov(value ~ group, data=df)
variance
#进行多重比较，不矫正P值
MC <- LSD.test(variance,"group", p.adj="none")#结果显示：标记字母法out$group
GB<- group_by(df,group)#数据转换
error <- summarise(GB,sd(value,na.rm = T))#计算误差
#整理数据
error2 <- merge(error ,MC$group,by.x="group",by.y = "row.names",all = F)#合并数据

##生成X轴替换的刻度表格
df2 <- data.frame(
  " "=c("HFD","PPP"),
  group1=c("-","0"),
  group2=c("-","0.25"),
  group3=c("+","0.5"),
  group4=c("+","0.75"),
  group5=c("+","1")
)
rownames(df2) <- df2$X.
df2 <- df2[-1]
##绘图
p1 <- ggplot(df, aes(group, value))+
  #散点图绘制
  geom_jitter(aes(fill = group), shape = 21, color = "black",
              width = 0.3, size = 3, alpha = 0.4)+
  #根据计算结果添加均值线
  geom_segment(data=df1,aes(x=x-0.2,xend=x+0.2,y=mean_value,yend=mean_value),
               color="grey20",linewidth=0.8)+
  #添加误差棒
  stat_summary(color="grey10",fun.data = "mean_cl_normal",
               geom = "errorbar",
               width = 0.15,size=0.8) +
  #根据多重比较的结果添加字母标记
  geom_text(data=error2, aes(group, value+13, 
                             label=groups, color = group), size = 6)+
  labs(x=NULL, y = "This is y-axis")+
  #颜色设置
  scale_fill_manual(values = c("#00b2a9","#a626aa","#6639b7","#aea400","#ff6319"))+
  scale_color_manual(values = c("#00b2a9","#a626aa","#6639b7","#aea400","#ff6319"))+
  #主题调整
  theme_classic()+
  theme(legend.position = "none",
        axis.text.x = element_blank(),
        axis.line = element_line(linewidth = 0.8),
        axis.ticks = element_line(linewidth = 0.8),
        axis.ticks.x = element_blank(),
        axis.text.y = element_text(size=10, colour = "black"),
        axis.title = element_text(size=12, colour = "black"))
p1

##绘制表格
table <- tableGrob(df2,theme=ttheme_minimal())

##拼图
grid.arrange(p1,table, heights = c(2, 0.45))

###保存
pdf(file='test.pdf', height=4,width=4)#新建一个PDF文件
grid.arrange(p1,table, heights = c(2, 0.45))
dev.off()#关闭PDF

##最后基于AI软件微调图片即可
