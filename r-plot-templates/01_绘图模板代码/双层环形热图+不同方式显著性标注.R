#设置工作环境
rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/双层环形热图+不同方式显著性标注")

##加载R包（没有安装相关包的同学可以先安装相应的R包）
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(psych) # Procedures for Psychological, Psychometric, and Personality Research
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(dplyr) # A Grammar of Data Manipulation
library(agricolae) # Statistical Procedures for Agricultural Research

#####内层热图——颜色与样本归一化值呈正相关
#加载数据
df3 <- as.data.frame(t(read.table("data_内层.txt", sep="\t", header=T, check.names=F,row.names = 1)))
df3$sample <- rownames(df3)
group <- read.table("group.txt", sep="\t", header=T, check.names=F)
#合并分组与数据
df3 <- merge(df3,group,by="sample")
rownames(df3) <- df3$sample
df3 <- df3[-1]
#将宽数据转换为长数据
df4 <- melt(df3, id.vars = c("group"))
##利用循环并采用多重比较法比较各组显著性
#初始化
variance<-aov(Ni ~ group, data=df3)
MC <- LSD.test(variance,"group", p.adj="none")
GB<- group_by(df3,group)
sg<- MC$groups
sg$group <- rownames(sg)
#修改列名
colnames(sg)[2] <- "Ni_label"
for (i in colnames(df3[2:12])) {
  variance<-aov(df3[,i] ~ group, data=df3)
  MC <- LSD.test(variance,"group", p.adj="none")
  data <- MC$groups
  data$group <- rownames(data)
  colnames(data)[1:2]<-c(i,paste0(i,"_label"))
  sg<-merge(sg,data,by="group")
}
#将数据和字母分开储存
df_label <- sg[c(1,3,5,7,9,11,13,15,17,19,21,23,25)]
df_data <- sg[c(1,2,4,6,8,10,12,14,16,18,20,22,24)]
rownames(df_data) <- df_data$group
#数据标准化（0-1）——根据个人数据选择方法处理
df_data2 <- as.data.frame(lapply(df_data[2:13], function(x) (x - min(x)) / (max(x) - min(x))))
df_data2$group <- df_data$group
#转换为长数据
df_label2 <- melt(df_label, id.vars = c("group"))
df_data3 <- melt(df_data2, id.vars = c("group"))
##增加空白间隔-通过转换为数值型x轴实现
#这里在As和Cu之间增加空白间隔并在首位增加间隔
#添加x列数据
df_data3$x <- rep(c(1:5,7:13),each=5)
df_label2$x <- rep(c(1:5,7:13),each=5)
#添加y列数据
df_data3$y <- rep(c(1:5),times=12)
df_label2$y <- rep(c(1:5),times=12)
##计算标签角度
number_of_bar <- 15
angle <-  90 - 360 * (df_label2$x-0.5) /(number_of_bar)
df_label2$angle<-ifelse(angle < -90, angle+180, angle)

##基于ggplot2绘图
ggplot()+
  #绘制热图
  geom_tile(data=df_data3,aes(x,y,fill=value),#x轴和y轴都需要用添加的数值型数据绘制
            color="grey",linewidth=0.6)+
  #自定义颜色
  scale_fill_gradientn(limit = c(0, 1), colors = c('white', '#fd5c63'))+
  #添加显著性标签
  geom_text(data=df_label2,aes(x,y,label = value,angle=angle))+#x轴和y轴都需要用添加的数值型数据绘制
  #转换为极坐标
  coord_polar()+
  #主题相关设置
  theme_void()+
  theme(panel.grid = element_blank(),
        axis.text.x=element_text(size = 11, color = "black"),
        legend.position = "top")+
  #去除轴标题并指定图例标题
  labs(x=NULL,y=NULL,fill="Normalize")+
  #自定义x轴标签，注意需要按照此前添加顺序指定
  scale_x_continuous(limits = c(0,15),
                     breaks = c(1,2,3,4,5,7,8,9,10,11,12,13),
                     labels = c("Ni","Pb","Cr","Cd","As","Cu","Zn",
                                "Mo","Mn","Fe","B","S"))+
  #设置y轴范围
  #注意：这里的范围内层与外层图要一致且同时包含内外层，以便后续在AI中拼图
  scale_y_continuous(limits = c(-1.5,8.5))+
  #添加内层分组
  annotate("rect", xmin = 0.5, xmax = 5.5, ymin = 0.1, ymax = 0.4, fill="#00c4ff")+
  annotate("rect", xmin = 6.5, xmax = 13.5, ymin = 0.1, ymax = 0.4, fill="#11862f")+
  #手动添加y轴标签
  annotate("text", x = 14 , y = 1, label = "AK", size=3.5, color = "black",angle=30)+
  annotate("text", x = 13.9 , y = 2, label = "BK", size=3.5, color = "black",angle=30)+
  annotate("text", x = 13.8 , y = 3, label = "CK", size=3.5, color = "black",angle=30)+
  annotate("text", x = 13.8 , y = 4, label = "DK", size=3.5, color = "black",angle=30)+
  annotate("text", x = 13.8 , y = 5, label = "EK", size=3.5, color = "black",angle=30)->p1
p1


#####外层热图——pearson相关性
#加载数据（随机编写，无实际意义）
df1 <- read.table("data1_外层.txt", sep="\t", header=T, check.names=F)
df2 <- read.table("data2_外层.txt", sep="\t", header=T, check.names=F)
#合并数据
data <- merge(df1,df2,by="sample")
#将行名设置为样本名并删除多余列
rownames(data) <- data$sample
data <- data[-1]
#计算相关性并提取R值与P值
cor<- corr.test(data, method="pearson",adjust="BH")
r.cor<-data.frame(cor$r)[1:12,13:14]
p.cor<-data.frame(cor$p)[1:12,13:14]
#将宽数据转换为长数据
r.cor$G <- rownames(r.cor)
df_r <- melt(r.cor, id.vars = c("G"), 
             measure.vars = c("groupA","groupB"))
#指定顺序
df_r$G <- factor(df_r$G,levels = c("Ni","Pb","Cr","Cd","As","Cu","Zn",
                                   "Mo","Mn","Fe","B","S"))
p.cor$G <- rownames(p.cor)
df_p <- melt(p.cor, id.vars = c("G"), 
             measure.vars = c("groupA","groupB"))
#通过不同p值转换为*
df_p$sg <- ifelse(df_p$value>=0.05, "", ifelse(df_p$value<0.05&df_p$value>0.01,"*", 
                                               ifelse(df_p$value<=0.01&df_p$value>0.001,"**","***")))
##增加空白间隔-通过转换为数值型x轴实现
#这里在As和Cu之间增加空白间隔并在首位增加间隔
#添加x列数据
df_r$x <- c(1:5,7:13)
df_p$x <- c(1:5,7:13)
##将外层图片y轴设置为紧邻内层数据并间隔1
df_r$y <- rep(c(7:8),each=12)
df_p$y <- rep(c(7:8),each=12)
##计算标签角度
number_of_bar <- 15
angle <-  180 - 360 * (df_p$x-0.5) /(number_of_bar)
df_p$angle<-ifelse(angle < -90, angle+180, angle)

#基于ggplot2绘图
ggplot()+
  #热图
  geom_tile(data=df_r,aes(x,y,fill=value),#x轴和y轴都需要用添加的数值型数据绘制
            color="grey",linewidth=0.6)+
  #自定义颜色
  scale_fill_gradientn(limit = c(-1, 1), colors = c('#0099cc', 'white', '#ff9933'))+
  #显著性标签
  geom_text(data=df_p,aes(x,y,label = sg,angle=angle))+#x轴和y轴都需要用添加的数值型数据绘制
  #极坐标
  coord_polar()+
  #主题设置
  theme_void()+
  theme(panel.grid = element_blank(),
        axis.text.x=element_text(size = 11, color = "black"),
        legend.position = "top")+
  #去除轴标题并指定图例标题
  labs(x=NULL,y=NULL,fill="Pearson r")+
  #自定义x轴标签，注意需要按照此前添加顺序指定
  scale_x_continuous(limits = c(0,15),
                     breaks = c(1,2,3,4,5,7,8,9,10,11,12,13),
                     labels = c("Ni","Pb","Cr","Cd","As","Cu","Zn",
                                "Mo","Mn","Fe","B","S"))+
  #设置y轴范围
  #注意：这里的范围内层与外层图要一致且同时包含内外层，以便后续在AI中拼图
  scale_y_continuous(limits = c(-1.5,8.5))+
  #自定义y轴标签
  annotate("text", x = 13.8 , y = 7, label = "groupA", size=3, color = "black",angle=30)+
  annotate("text", x = 13.8 , y = 8, label = "groupB", size=3, color = "black",angle=30)->p2
p2

###由于ggplot2包中极坐标形式图形的拼图限制，这里需要将图形保存后在AI软件中拼接
##拼接方法：将图1选中平移到图2中心即可
library(patchwork)
p1+p2+
  plot_layout(guides = 'collect')
##最后在AI软件中拼图并对细节进行调整


######拓展——常规绘制并进行拼接
#内层图形
ggplot()+
  geom_tile(data=df_data3,aes(x,group,fill=value),
            color="grey",linewidth=0.6)+
  scale_fill_gradientn(limit = c(0, 1), colors = c('white', '#fd5c63'))+
  geom_text(data=df_label2,aes(x,group,label = value))+
  theme_void()+
  theme(panel.grid = element_blank(),
        axis.text.x=element_text(size = 11, color = "black"),
        legend.position = "top")+
  labs(x=NULL,y=NULL,fill="Normalize")+
  scale_x_continuous(limits = c(0,15),
                     breaks = c(1,2,3,4,5,7,8,9,10,11,12,13),
                     labels = c("Ni","Pb","Cr","Cd","As","Cu","Zn",
                                "Mo","Mn","Fe","B","S"))+
  #添加内层分组
  annotate("rect", xmin = 0.5, xmax = 5.5, ymin = 0.1, ymax = 0.4, fill="#00c4ff")+
  annotate("rect", xmin = 6.5, xmax = 13.5, ymin = 0.1, ymax = 0.4, fill="#11862f")+
  #手动添加y轴标签
  annotate("text", x = 13.8 , y = 1, label = "AK", size=3.5, color = "black")+
  annotate("text", x = 13.8 , y = 2, label = "BK", size=3.5, color = "black")+
  annotate("text", x = 13.8 , y = 3, label = "CK", size=3.5, color = "black")+
  annotate("text", x = 13.8 , y = 4, label = "DK", size=3.5, color = "black")+
  annotate("text", x = 13.8 , y = 5, label = "EK", size=3.5, color = "black")->p3
p3
#外层图形
ggplot()+
  geom_tile(data=df_r,aes(x,variable,fill=value),
            color="grey",linewidth=0.6)+
  scale_fill_gradientn(limit = c(-1, 1), colors = c('#0099cc', 'white', '#ff9933'))+
  geom_text(data=df_p,aes(x,variable,label = sg))+
  theme_void()+
  theme(panel.grid = element_blank(),
        legend.position = "top")+
  labs(x=NULL,y=NULL,fill="Pearson r")+
  scale_x_continuous(limits = c(0,15),
                     breaks = c(1,2,3,4,5,7,8,9,10,11,12,13),
                     labels = c("Ni","Pb","Cr","Cd","As","Cu","Zn",
                                "Mo","Mn","Fe","B","S"))+
  annotate("text", x = 14 , y = 1, label = "groupA", size=3.5, color = "black")+
  annotate("text", x = 14 , y = 2, label = "groupB", size=3.5, color = "black")->p4
p4

##拼图
library(aplot)
p3 %>% insert_top(p4, height = 0.4)
