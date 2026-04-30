#加载包
library(UpSetR)
library(RColorBrewer)

#生成作图数据或者导入数据
data <- data.frame(set1 = paste(rep("word_" , 200) , sample(c(1:1000) , 200 , replace=F) , sep=""),
                   set2 = paste(rep("word_" , 200) , sample(c(1:1000) , 200 , replace=F) , sep=""),
                   set3 = paste(rep("word_" , 200) , sample(c(1:1000) , 200 , replace=F) , sep=""),
                   set4 = paste(rep("word_" , 200) , sample(c(1:1000) , 200 , replace=F) , sep=""),
                   set5 = paste(rep("word_" , 200) , sample(c(1:1000) , 200 , replace=F) , sep=""),
                   set6 = paste(rep("word_" , 200) , sample(c(1:1000) , 200 , replace=F) , sep=""))
View(data)
# data <- read.table(file="otu.txt",sep="\t",header=T,check.names=FALSE,row.names = 1)
# data[data>0]=1
#绘图
upset(fromList(data))
#参数调整
upset(fromList(data),
      #显示数据集的所有数据
      nsets = length(data),
      #显示前多少个
      nintersects=30,
      #点点图和条形图的比例
      mb.ratio = c(0.5, 0.5),
      #对集合进行排序
      sets=c("set1","set2","set3","set4","set5","set6"),
      #图中点的大小
      point.size = 3,
      #图中线的粗细
      line.size = 1,  
      #y轴的名称
      mainbar.y.label = "This is y-axis",
      #x轴的名称
      sets.x.label="This is x-axis",      
      #6个参数intersection size title, intersection size tick labels, set size title, set size tick labels, set names, numbers above bars的设置
      text.scale = c(1.5, 1.5, 1.5, 1.5,1.5, 1.5),  
      #图中阴影部分的颜色
      shade.color = "green",
      #柱状图的颜色
      sets.bar.color=brewer.pal(6, "Set1"),
      queries=list(list(query=intersects,params=list("set1","set2"),color="red",active=T),
             list(query=intersects,params=list("set2","set3"),color="blue",active=T),
             list(query=intersects,params=list("set3","set4"),color="green",active=T),
             list(query=intersects,params=list("set4","set5"),color="yellow",active=T)))



