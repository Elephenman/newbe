rm(list=ls())#clear Global Environment
setwd('D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\数据分析及可视化\\群落组成分析\\物种丰度计算及可视化')#设置工作路径

#加载R包
library (reshape2)
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(plyr) # Tools for Splitting, Applying and Combining Data
library(ggtree) # an R package for visualization of tree and annotation data
library(vegan) # Community Ecology Package
library(ape) # Analyses of Phylogenetics and Evolution
library( RColorBrewer) # not installed on this machine
library(aplot) # Decorate a 'ggplot' with Associated Information

#读取数据
df1 <- read.table(file="Genus.txt",sep="\t",header=T,check.names=FALSE)
#查看前6行
head(df1)
##利用循环处理具有重复的数据
#初始化
data<-aggregate(E ~ Tax,data=df1,sum)
#重命名
colnames(data)[2]<-"example"
for (i in colnames(df1)[2:length(colnames(df1))]){
  #计算每列的和
  data1<-aggregate(df1[,i]~Tax,data=df1,sum)
  colnames(data1)[2]<-i  
  #合并列
  data<-merge(data,data1,by="Tax")
  }
df2<-data[,-2]
rownames(df2)=df2$Tax#修改行名
df3=df2[,-1]#删除多的列

#计算物种总丰度并降序排列
df3$rowsum <- apply(df3,1,sum)
df4 <- df3[order (df3$rowsum,decreasing=TRUE),]
df5 = df4[,-6]#删除求和列
#求物种相对丰度
df6 <- apply(df5,2,function(x) x/sum(x))
#由于之间已经按照每行的和进行过升序排列，所以可以直接取前10行
df7 <-  df6[1:10,]
df8 <- 1-apply(df7, 2, sum) #计算剩下物种的总丰度
#合并数据
df9 <- rbind(df7,df8)
row.names(df9)[11]="Others"
#导出数据
write.table (df9, file ="genus_x.csv",sep =",", quote =FALSE)
#变量格式转换,宽数据转化为长数据,方便后续作图
df_genus <- melt(df9)
names(df_genus)[1:2] <- c("Taxonomy","sample")  #修改列名
#颜色
col <-colorRampPalette(brewer.pal(12,"Paired"))(11)
##柱状堆积图绘制绘图
p1<-ggplot(df_genus, aes( x = sample,y=100 * value,fill = Taxonomy))+#geom_col和geom_bar这两条命令都可以绘制堆叠柱形图
  geom_col(position = 'stack',width = 0.8)+
  #geom_bar(position = "stack", stat = "identity", width = 0.6) 
  scale_y_continuous(expand = c(0,0))+# 调整y轴属性，使柱子与X轴坐标接触
  labs(x=NULL,y="Relative Abundance(%)",#设置X轴和Y轴的名称以及添加标题
       fill="Taxonomy")+
  guides(fill=guide_legend(keywidth = 1, keyheight = 1)) +
  coord_flip()+
  theme(panel.grid = element_blank(),
        panel.background = element_blank())+
  scale_fill_manual(values = col)
p1     

####聚类树
data2 <- df3[-6]
#计算距离矩阵
df_dist <- vegdist(t(data2),method = 'bray')#使用bray curtis方法计算距离矩阵
####进行层次聚类,可选择方法有single、complete、median、mcquitty、average 、centroid 、ward 
df_hc <- hclust(df_dist,method="average")#使用类平均法进行聚类
#绘图
plot(as.dendrogram(df_hc),type="rectangle",horiz=T)#实现将垂直的聚类树变成水平聚类树，绘图
# 将聚类结果转成系统发育格式
df_tree <- as.phylo(df_hc)
# 对树分组
gro <- list(group1=c("A","E"),
            group2=c("C","D"),
            group3=c("B"))
# 将分组信息和进化树组合到一起
tree<-groupOTU(df_tree,gro)
# ggtree绘图
p2 <- ggtree(tree,size=1.2)+
  geom_tiplab(aes(color=group),size=5,align = F,
              offset = 0.008,show.legend = F)+
  geom_tippoint(aes(shape=group,color=group),
              show.legend = T,
              size=4)
p2


#####将柱状堆积图与树图进行组合
p1 <- p1+theme(axis.text.y = element_text(color = "black",size=12))
col2 <-colorRampPalette(brewer.pal(9,"Set1"))(3)
p3 <- ggtree(tree,size=1)+
  geom_tippoint(aes(shape=group,color=group),
                show.legend = T,
                size=4)+
  scale_color_manual(values = col2)
p <- p1%>%insert_left(p3,width = 0.3)
p

