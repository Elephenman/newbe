rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/tree+分支颜色调整+分组注释+热图注释+柱状堆积图注释')#设置工作路径

#加载包
library(ggtree) # an R package for visualization of tree and annotation data
library(ape) # Analyses of Phylogenetics and Evolution
library(vegan) # Community Ecology Package
library(ggtreeExtra) # An R Package To Add Geometric Layers On Circular Or Other Layout Tree Of "ggtree"
library(ggnewscale) # Multiple Fill and Colour Scales in 'ggplot2'
library(ggstar) # Multiple Geometric Shape Point Layer for 'ggplot2'
#读取数据
OTU <- read.table("OTU.txt",check.names = F, row.names = 1, header = 1, sep = "\t")

#计算距离矩阵
df_dist <- vegdist(t(OTU),method = 'bray')#使用bray curtis方法计算距离矩阵
####进行层次聚类,可选择方法有single、complete、median、mcquitty、average 、centroid 、ward 
df_hc <- hclust(df_dist,method="average")#使用类平均法进行聚类
#绘图
plot(as.dendrogram(df_hc),type="rectangle",horiz=T)#实现将垂直的聚类树变成水平聚类树，绘图
# 将聚类结果转成系统发育格式
df_tree <- as.phylo(df_hc)
# 对树分组
sample <- list(A=c("A_1","A_2","A_3","A_4","A_5","A_6","A_7","A_8"),
            B=c("B_1","B_2","B_3","B_4","B_5","B_6","B_7","B_8"),
            C=c("C_1","C_2","C_3","C_4","C_5","C_6","C_7","C_8"),
            D=c("D_1","D_2","D_3","D_4","D_5","D_6","D_7","D_8"),
            E=c("E_1","E_2","E_3","E_4","E_5","E_6","E_7","E_8"),
            F=c("F_1","F_2","F_3","F_4","F_5","F_6","F_7","F_8"),
            G=c("G_1","G_2","G_3","G_4","G_5","G_6","G_7","G_8"))
# 将分组信息和进化树组合到一起
tree<-groupOTU(df_tree,sample)

# ggtree初步展示
ggtree(tree,size=0.8, layout="circular", 
             ladderize=FALSE, branch.length="none", aes(col=group),show.legend = F)+
  geom_tiplab(aes(color=group),size=4,align = F,
              offset = 0.001,show.legend = F)

##读取分组注释信息
group <- read.table("sample.txt",check.names = F, row.names = 1, header = 1, sep = "\t")
group$sample <- rownames(group)

##计算各样本的物种丰度信息
#读取分类信息
tax <- read.table("tax.txt",check.names = F, header = 1, sep = "\t")
#根据OTUID合并OTU数据和分类信息
OTU2 <- OTU
OTU2$OTU_id <- rownames(OTU2)
df <- merge(tax,OTU2,by="OTU_id")
#提取属水平的信息
data_Genus <- df[,c(7,9:64)]
##利用循环处理具有重复的数据
#初始化
data<-aggregate(A_1 ~ Genus,data=data_Genus,sum)
#重命名
colnames(data)[2]<-"example"
for (i in colnames(data_Genus)[2:length(colnames(data_Genus))]){
  #计算每列的和
  data1<-aggregate(data_Genus[,i]~Genus,data=data_Genus,sum)
  colnames(data1)[2]<-i  
  #合并列
  data<-merge(data,data1,by="Genus")
}
df2<-data[,-2]
rownames(df2)=df2$Genus#修改行名
df3=df2[,-1]#删除多的列

#计算物种总丰度并降序排列
df3$rowsum <- apply(df3,1,sum)
df4 <- df3[order (df3$rowsum,decreasing=TRUE),]
df5 = df4[,-57]#删除求和列
#求物种相对丰度
df6 <- apply(df5,2,function(x) x/sum(x))
#由于之间已经按照每行的和进行过升序排列，所以可以直接取前10行
df7 <-  df6[1:10,]
df8 <- 1-apply(df7, 2, sum) #计算剩下物种的总丰度
#合并数据
df9 <- rbind(df7,df8)
row.names(df9)[11]="Others"
df9 <- as.data.frame(df9)
df10 <- as.data.frame(t(df9))
df10$sample <- rownames(df10)

##根据样本名称合并分组与丰度信息
group <- merge(group,df10,by="sample")

##第二层注释的数据
data2 <- group[,c(1,4:11)]
data2 <- melt(data2)
data2$`Diet (detailed)` <- as.character(data2$variable)
data2$value <- as.character(data2$value)

##第六层注释的数据
data6 <- group[,c(1,15:25)]
data6 <- melt(data6)

###为进化树添加注释信息
ggtree(tree,size=0.8, layout="circular", 
       ladderize=FALSE, branch.length="none", aes(col=group),show.legend = F)+#图形主体
  geom_tiplab(aes(color=group),size=3,align = F,
              offset = 0.001,show.legend = F)+#分支标签
  scale_color_manual(
    values=c("black", "#0ebeff", "#47cf73","#ae63e4",
             "#fcd000","#ff3c41","#b62b6e","#00b7c9"))+#自定义分支颜色
  #第一层注释_Diet
  new_scale_fill() + 
  geom_fruit(
    data=group,
    geom=geom_tile,
    mapping=aes(y=sample, fill=Diet),
    width = 0.4,#注释的宽度
    offset=0.3 #位置
  )+
  scale_fill_manual(
    values=c("#00ff01", "#fecc32", "#ff0100"),
    guide=guide_legend(keywidth=1, keyheight=1, order=1))+
  #第二层注释_Diet (detailed)
  new_scale_fill() +
  geom_fruit(
    data=data2,
    geom=geom_tile,
    mapping=aes(y=sample, x=`Diet (detailed)`, fill=value),
    color="grey80",
    pwidth=0.8,
    offset=0.05, #位置
    axis.params=list(
      axis="x", # 添加图层的轴文本
      text.angle=0, #x 轴的文本角度
      hjust=0.5,  # 调整文字轴的水平位置
      text.size = 4,#文字大小
      line.alpha = 0
    )
  )+
  scale_fill_manual(
    values=c("#000000", "#a95401", "#ff8000","#ffff00"),
    guide=guide_legend(keywidth=1, keyheight=1, order=2),
    name="Diet (detailed)")+
  #添加第三层注释——Habitat
  new_scale_fill() +
  geom_fruit(data=group,
             geom = geom_star,
             mapping = aes(y=sample,fill = Habitat), 
             starshape = 13, color = NA,
             size = 5, starstroke = 0, pwidth = 2, offset = 0.2,
             grid.params=list(
               linetype=3,
               size=0.4
             ))+
  scale_fill_manual(
    values=c("#ff9901", "#01ccff", "#999601", "#663300"),
    guide=guide_legend(keywidth=1, keyheight=1, order=3)
  )+
  #添加第四层注释——Captive-wild
  new_scale_fill() +
  geom_fruit(data=group,
             geom = geom_star,
             mapping = aes(y=sample,fill = `Captive-wild`), 
             starshape = 13, color = NA,
             size = 5, starstroke = 0, pwidth = 2, offset = 0.2,
             grid.params=list(
               linetype=3,
               size=0.4
             ))+
  scale_fill_manual(
    values=c("#ff9901", "#0000ff", "#009900"),
    guide=guide_legend(keywidth=1, keyheight=1, order=4)
  )+
  #添加第五层注释——Captive-wild
  new_scale_fill() +
  geom_fruit(data=group,
             geom = geom_star,
             mapping = aes(y=sample,fill = `Sample type`), 
             starshape = 13, color = NA,
             size = 5, starstroke = 0, pwidth = 2, offset = 0.2,
             grid.params=list(
               linetype=3,
               size=0.4,
             ))+
  scale_fill_manual(
    values=c("#663300", "#cc9a00"),
    guide=guide_legend(keywidth=1, keyheight=1, order=5)
  )+
  new_scale_fill() +
  geom_fruit(
    data=data6,
    geom=geom_bar,
    mapping=aes(y=sample, x=value, fill=variable),
    pwidth=1,
    width = 0.6,
    offset = 0.1,
    stat="identity",
    orientation="y",
    axis.params = list(axis = "x",
                       text.size = 2,
                       vjust = 0.5,
                       hjust = 0,
                       text.angle = -90,
                       limits = c(0,1)),
    grid.params = list(linetype = 3)
  )+
  scale_fill_manual(
    values=c("#4078c0", "#6cc644", "#bd2c00","#c9510c", "#6e5494",
             "#fbbc05","#ec6400", "#d5df00", "#e30061","#009ee3",
             "#aca6a2"),
    guide=guide_legend(keywidth=1, keyheight=1, order=6),
    name = "Genus"
  )

#####输出PDF
pdf(file='test.pdf', height=10,width=12)#新建一个PDF文件，设置名称、宽高及字体等
ggtree(tree,size=0.8, layout="circular", 
       ladderize=FALSE, branch.length="none", aes(col=group),show.legend = F)+
  geom_tiplab(aes(color=group),size=3,align = F,
              offset = 0.001,show.legend = F)+
  scale_color_manual(
    values=c("black", "#0ebeff", "#47cf73","#ae63e4",
             "#fcd000","#ff3c41","#b62b6e","#00b7c9"))+
  #第一层注释_Diet
  new_scale_fill() + 
  geom_fruit(
    data=group,
    geom=geom_tile,
    mapping=aes(y=sample, fill=Diet),
    width = 0.4,#注释的宽度
    offset=0.3 #位置
  )+
  scale_fill_manual(
    values=c("#00ff01", "#fecc32", "#ff0100"),
    guide=guide_legend(keywidth=1, keyheight=1, order=1))+
  #第二层注释_Diet (detailed)
  new_scale_fill() +
  geom_fruit(
    data=data2,
    geom=geom_tile,
    mapping=aes(y=sample, x=`Diet (detailed)`, fill=value),
    color="grey80",
    pwidth=0.8,
    offset=0.05, #位置
    axis.params=list(
      axis="x", # 添加图层的轴文本
      text.angle=0, #x 轴的文本角度
      hjust=0.5,  # 调整文字轴的水平位置
      text.size = 4,#文字大小
      line.alpha = 0
    )
  )+
  scale_fill_manual(
    values=c("#000000", "#a95401", "#ff8000","#ffff00"),
    guide=guide_legend(keywidth=1, keyheight=1, order=2),
    name="Diet (detailed)")+
  #添加第三层注释——Habitat
  new_scale_fill() +
  geom_fruit(data=group,
             geom = geom_star,
             mapping = aes(y=sample,fill = Habitat), 
             starshape = 13, color = NA,
             size = 5, starstroke = 0, pwidth = 2, offset = 0.2,
             grid.params=list(
               linetype=3,
               size=0.4
             ))+
  scale_fill_manual(
    values=c("#ff9901", "#01ccff", "#999601", "#663300"),
    guide=guide_legend(keywidth=1, keyheight=1, order=3)
  )+
  #添加第四层注释——Captive-wild
  new_scale_fill() +
  geom_fruit(data=group,
             geom = geom_star,
             mapping = aes(y=sample,fill = `Captive-wild`), 
             starshape = 13, color = NA,
             size = 5, starstroke = 0, pwidth = 2, offset = 0.2,
             grid.params=list(
               linetype=3,
               size=0.4
             ))+
  scale_fill_manual(
    values=c("#ff9901", "#0000ff", "#009900"),
    guide=guide_legend(keywidth=1, keyheight=1, order=4)
  )+
  #添加第五层注释——Captive-wild
  new_scale_fill() +
  geom_fruit(data=group,
             geom = geom_star,
             mapping = aes(y=sample,fill = `Sample type`), 
             starshape = 13, color = NA,
             size = 5, starstroke = 0, pwidth = 2, offset = 0.2,
             grid.params=list(
               linetype=3,
               size=0.4,
             ))+
  scale_fill_manual(
    values=c("#663300", "#cc9a00"),
    guide=guide_legend(keywidth=1, keyheight=1, order=5)
  )+
  new_scale_fill() +
  geom_fruit(
    data=data6,
    geom=geom_bar,
    mapping=aes(y=sample, x=value, fill=variable),
    pwidth=1,
    width = 0.6,
    offset = 0.1,
    stat="identity",
    orientation="y",
    axis.params = list(axis = "x",
                       text.size = 2,
                       vjust = 0.5,
                       hjust = 0,
                       text.angle = -90,
                       limits = c(0,1)),
    grid.params = list(linetype = 3)
  )+
  scale_fill_manual(
    values=c("#4078c0", "#6cc644", "#bd2c00","#c9510c", "#6e5494",
             "#fbbc05","#ec6400", "#d5df00", "#e30061","#009ee3",
             "#aca6a2"),
    guide=guide_legend(keywidth=1, keyheight=1, order=6),
    name = "Genus"
  )
dev.off()#关闭PDF

