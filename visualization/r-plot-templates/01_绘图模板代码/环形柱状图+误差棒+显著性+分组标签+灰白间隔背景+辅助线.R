rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/环形柱状图+误差棒+显著性+分组标签+灰白间隔背景+辅助线')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(dplyr) # A Grammar of Data Manipulation

##加载数据（随机编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")

##将数据根据是否大于0添加分组
df$group3 <- ifelse(df$mean>0, "T", "F")
df$group3 <- factor(df$group3,levels = c("T","F"))


##计算标签角度
df$group1 <- factor(df$group1,levels = c("A","B","C","D","E","F","G","H","I","J"))
df$ID <- as.numeric(rownames(df))##根据行数添加一列数值型数据（1：40）
number_of_bar <- nrow(df)
angle <-  90 - 360 * (df$ID-0.5) /(number_of_bar+4)##+4的目的在于达到间隔分离
df$hjust<-ifelse(angle < -90, 1, 0)
df$angle<-ifelse(angle < -90, angle+180, angle)
#创建标签数据及位置
df2 <- df %>% 
  group_by(group1) %>% 
  summarize(start=min(ID)+4, end=max(ID) - 4) %>% 
  rowwise() %>% 
  mutate(title=mean(c(start, end)))
df2$group1 <- factor(df2$group1,levels = c("A","B","C","D","E","F","G","H","I","J"))
df2$group2 <- c("G1","G1","G2","G2","G3","G4","G4","G5","G5","G6")
#第二组标签
df3 <- df %>% 
  group_by(group2) %>% 
  summarize(start=min(ID)+4, end=max(ID) - 4) %>% 
  rowwise() %>% 
  mutate(title=mean(c(start, end)))
df3$group2 <- factor(df3$group2,levels = c("G1","G2","G3","G4","G5","G6"))

##寻找数据中的最大值与最小值以便后续添加灰白色间隔的柱子
df_bg <- df %>%
  group_by(group1) %>% 
  summarize(max = max(mean),min = min(mean))
##确定灰白色背景宽度及对应颜色标记
df_bg2 <- df %>%
  group_by(group1) %>% 
  summarize(max = max(ID),min = min(ID))
df_bg2$G <- rep(c("g","w"), times=2, len = 10)

##绘制基础柱状图
ggplot(df)+
  #手动添加辅助线(坐标轴)
  geom_linerange(aes(xmin=0.5,xmax=35, y = -10),lty="solid", color = "grey80")+
  geom_linerange(aes(xmin=0.5,xmax=35, y = -5),lty="solid", color = "grey80")+
  geom_linerange(aes(xmin=0.5,xmax=35, y = 0),lty="solid", color = "black")+
  geom_linerange(aes(xmin=0.5,xmax=35, y = 5),lty="solid", color = "grey80")+
  geom_linerange(aes(xmin=0.5,xmax=35, y = 10),lty="solid", color = "grey80")+
  #手动添加坐标及标题
  geom_text(x=0.1,y=-15,label="-15",color="black",size=3)+
  geom_text(x=0.1,y=-10,label="-10",color="black",size=3)+
  geom_text(x=0.1,y=-5,label="-5",color="black",size=3)+
  geom_text(x=0.1,y=0,label="0",color="black",size=3)+
  geom_text(x=0.1,y=5,label="5",color="black",size=3)+
  geom_text(x=0.1,y=10,label="10",color="black",size=3)+
  geom_text(x=0.1,y=15,label="15",color="black",size=3)+
  #根据目标分组添加灰白色间隔背景
  geom_rect(df_bg2,mapping=aes(xmin=min-0.5,xmax=max+0.5,ymin=-15,ymax=15,fill=G),alpha=0.5)+
  #分组数量少也可手动添加
  # annotate("rect", xmin = 0.5, xmax = 5.5, ymin = -15, ymax = 15, fill="grey90", alpha = 0.5)+
  # annotate("rect", xmin = 7.5, xmax = 10.5, ymin = -15, ymax = 15, fill="grey90", alpha = 0.5)+
  # annotate("rect", xmin = 14.5, xmax = 20.5, ymin = -15, ymax = 15, fill="grey90", alpha = 0.5)+
  #柱状图
  geom_col(aes(ID, mean, fill=group3), alpha = 0.6)+
  #添加误差线
  geom_errorbar(mapping=aes(x=ID,ymin=mean-sd,ymax=mean+sd),
                width=0.15,linewidth=0.2)+
  #极坐标转换
  coord_polar(direction=1)+
  #x,y轴范围确定
  scale_y_continuous(limits = c(-23,38))+
  scale_x_continuous(limits = c(0,44))+
  #修改填充颜色
  scale_fill_manual(values = c("T"="red",
                               "F"="blue",
                               "g"="grey90",
                               "w"="white"))+
  #主题
  theme_void()+
  theme(legend.position = 'none')+
  #手动添加显著性
  geom_text(aes(x=ID, y=17, label=sig,
                         hjust=hjust,color=group2),
            fontface="bold", size=4, 
            angle= df$angle, inherit.aes = F)+
  #手动添加第一层标签
  geom_text(aes(x=ID, y=20, label=sample,
                          hjust=hjust,color=group2), 
            fontface="bold", size=3, 
            angle= df$angle, inherit.aes = F)+
  ##分组第二层标签
  geom_text(data=df2, aes(x = title, y = 30, label=group1,color=group2), 
            hjust=c(1,1,1,1,1,0,0,0,0,0), size=4.5,  
            angle=c(340,310,0,0,0,0,-20,0,0,0),#需要根据分组数量及绘制图形的标签角度自己调整
            fontface="bold", inherit.aes = F)+
  ##分组第二层标签
  geom_text(data=df3, aes(x = title, y = 36, label=group2,color=group2),
            size=5.5,  angle=c(330,0,0,0,0,0),#需要根据分组数量及绘制图形的标签角度自己调整
            fontface="bold", inherit.aes = F)+
  #自定义颜色
  scale_color_manual(values = c("#4fbb98","#f46024","#dd6ab0","#aea400","#00ad45","#00aee6"))
