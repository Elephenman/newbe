rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/三角形热图+聚类+柱状图注释")

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(ggtree) # an R package for visualization of tree and annotation data
library(ape) # Analyses of Phylogenetics and Evolution
library(vegan) # Community Ecology Package
library(aplot) # Decorate a 'ggplot' with Associated Information
##加载数据（随机编写，无实际意义）
df <- read.table("data1.txt", check.names = F, header = 1)
df2 <- read.table("data2.txt", check.names = F, header = 1)

##数据整理-将宽数据转换为长数据格式
df1 <- melt(df)
# 创建形状列
df1$shape <- ifelse(df1$value > 0, "up", "down")

##绘制三角热图
p1 <- ggplot(df1, aes(Gene, variable, size = value, fill = value, shape = shape))+
  geom_point(color = "black")+
  #自定义形状
  scale_shape_manual(values = c("up" = 24, "down" = 25))+
  #自定义颜色
  scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0)+
  #自定义大小
  scale_size_continuous(range = c(0.5,4))+
  #y轴调整
  scale_y_discrete(position = "right")+
  labs(x = NULL, y = NULL)+
  #图例调整
  guides(size = "none",
         shape=guide_legend(override.aes = list(size=3)))+
  theme_classic()+
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1))
p1

##进化树的构建
#处理数据
df3 <- df
rownames(df3) <- df3$Gene
df3 <- df3[-1]
#计算距离矩阵
df_dist <- vegdist(t(df3),method = 'bray')#使用bray curtis方法计算距离矩阵
####进行层次聚类,可选择方法有single、complete、median、mcquitty、average 、centroid 、ward 
df_hc <- hclust(df_dist,method="average")#使用类平均法进行聚类
#绘图
plot(as.dendrogram(df_hc),type="rectangle",horiz=T)#实现将垂直的聚类树变成水平聚类树，绘图
# 将聚类结果转成系统发育格式
df_tree <- as.phylo(df_hc)
# 对树分组
gro <- list(group1=c("A","E","F","H"),
            group2=c("B","C","D","G"))
# 将分组信息和进化树组合到一起
tree<-groupOTU(df_tree, gro)
# ggtree绘图
p2 <- ggtree(tree,aes(color=group),size=1,show.legend = F)+
  geom_tiplab(size=5,align = F,show.legend = F)
p2
#去除分支名称
p2 <- ggtree(tree,aes(color=group),size=0.8,show.legend = F)
p2
##组合
p1%>%insert_left(p2,width = 0.15)

###绘制顶部的注释柱状图
p3 <- ggplot(df2, aes(Gene, Abundance))+
  geom_col()+
  #y轴调整
  scale_y_continuous(position = "right", breaks = c(0,10),
                     expand = c(0,0),limits = c(0,12))+
  theme_classic()+
  theme(axis.text.x = element_blank(),
        axis.text.y = element_text(vjust = 0),
        axis.title.y=element_text(size=8),
        axis.line.y = element_line(linewidth = 1, color = "black"),
        axis.line.x = element_line(linewidth = 1, color = "grey60"),
        axis.ticks = element_blank())+
  labs(x = NULL)
p3
p4 <- ggplot(df2, aes(Gene, Prevalence))+
  geom_col()+
  #y轴调整
  scale_y_continuous(position = "right", breaks = c(0,1), 
                     expand = c(0,0),limits = c(0,1.2))+
  theme_classic()+
  theme(axis.text.x = element_blank(),
        axis.title.y=element_text(size=8),
        axis.text.y = element_text(vjust = 0),
        axis.line.y = element_line(linewidth = 1, color = "black"),
        axis.line.x = element_line(linewidth = 1, color = "grey60"),
        axis.ticks = element_blank())+
  labs(x = NULL)
p4

##组合图形
p1%>%insert_left(p2,width = 0.1) %>% 
  insert_top(p3,height = 0.3) %>% 
  insert_top(p4,height = 0.3)


