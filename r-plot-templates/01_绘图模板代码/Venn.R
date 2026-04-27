rm(list=ls())#clear Global Environment
setwd('D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\Venn')#设置工作路径

#安装包
#install.packages("venn")
# install.packages("VennDiagram")
#加载R包
library(VennDiagram) # Generate High-Resolution Venn and Euler Plots 
library (venn)
library( RColorBrewer) # not installed on this machine
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggprism) # A 'ggplot2' Extension Inspired by 'GraphPad Prism'
#读取数据,为OTU水平的丰度表
data <- read.table(file="otu.txt",sep="\t",header=T,check.names=FALSE,row.names = 1)
#查看前6行
head(data)
#组内合并
df <- data.frame(A=rowSums(data[,c(1:3)]),
                 B=rowSums(data[,c(4:6)]),
                 C=rowSums(data[,c(7:9)]),
                 D=rowSums(data[,c(10:12)]))
head(df)
#创建空列表
df1 <- list()
#获取每个样本（组）所有的OTU
for (i in 1:length(colnames(df))){
  group<- colnames(df)[i]
  df1[[group]] <- rownames(df)[which(df[,i]!= 0)]
}
###绘图
#Venn包绘制
venn(df1, #数据
     zcolor=c('red','yellow','blue','green'),#颜色设置，可选择自带的“style”或者无色‘bw’
     opacity = 0.6,#颜色透明度
     box=F,#边框去除
     sncs=1.5,#组名字体大小
     ilcs=0.8)#图片中数字大小
####计算各组总OTU个数并绘制柱状图进行展示
df2<-df
df2[df2>0]=1
df3<-rbind(df2,Total=colSums(df2))
#提取作图数据
df4<-as.data.frame(t(df3[3010,])) 
df4$group<-rownames(df4)
#绘图
ggplot(df4,aes(x =group, y = Total)) +
  geom_col(aes(fill=group),width = 0.8,alpha=0.6)+
  geom_text(aes(label=Total, y=Total+20), position=position_dodge(0.9), vjust=0)+
  labs(x = NULL, y = NULL)+
  theme_prism(palette = "candy_bright",
              base_fontface = "plain", 
              base_family = "serif", 
              base_size = 16, 
              base_line_size = 0.8, 
              axis_text_angle = 45)+
  scale_y_continuous(expand = c(0,0),limits = c(0,1500))+
  theme(legend.position = "none")+
  scale_fill_manual(values = c('red','yellow','blue','green'))

# 使用VennDiagram包中的get.venn.partitions函数查看并导出交集结果
df_inter <- get.venn.partitions(df1)
for (i in 1:nrow(df_inter)) df_inter[i,'values'] <- paste(df_inter[[i,'..values..']],
                                                          collapse = ', ')
df_inter<-df_inter[-c(5, 6)]
write.table(df_inter, 'df_Venn.txt', row.names = FALSE, sep = '\t', quote = FALSE)


