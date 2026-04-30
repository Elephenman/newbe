rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/网络图+微生物丰度与基因间的相关性+正负相关')#Set working path

#加载R包
library(igraph) # Network Analysis and Visualization
library(Hmisc) # Harrell Miscellaneous
library(psych) # Procedures for Psychological, Psychometric, and Personality Research
library(dplyr) # A Grammar of Data Manipulation
library(tidyr) # Tidy Messy Data

##加载OTU数据及基因数据
mic <- read.table("Genus.txt", sep="\t", header=T, check.names=F,row.names = 1)
gene <- read.table("gene.txt", sep="\t", header=T, check.names=F,row.names = 1)
group <- read.table("group.txt", sep="\t", header=T, check.names=F)
##根据样本名合并数据
mic <- as.data.frame(t(mic))
mic$sample <- rownames(mic)
gene$sample <- rownames(gene)
df <- merge(mic, gene, by = "sample")
rownames(df) <- df$sample
df <- df[-1]
head(df)

##转换数据格式
data<-as.matrix(df)

#基于psych包计算相关性并基于Benjamini-Hochberg("FDR-BH")法校正p值
cor<- corr.test(data, method="spearman",adjust="BH")

##提取微生物与基因相关性部分的R值和P值
r.cor<-data.frame(cor$r)[1:11,12:23]
p.cor<-data.frame(cor$p)[1:11,12:23]

##保存数据
write.csv(r.cor,file='cor_r.csv')
write.csv(p.cor,file='cor_p.csv')

###以p>0.05作为筛选阈值,R值不做筛选
r.cor[p.cor>0.05] <- 0

###将数据转换为long format进行合并并添加连接属性
r.cor$from = rownames(r.cor)
p.cor$from = rownames(p.cor)
#将p值转换为long format
p_value <-  p.cor %>% 
  gather(key = "to", value = "p", -from) %>%
  data.frame()
#合并数据并设置阈值、连接线属性等
cor.data<- r.cor %>% 
  gather(key = "to", value = "r", -from) %>%
  data.frame() %>%
  left_join(p_value, by=c("from","to")) %>%
  mutate(
    linecolor = ifelse(r > 0,"positive","negative"), # 设置连接线的属性，可用于设置线型和颜色。
    linesize = abs(r) #设置连接线宽度
  ) # 此输出仍有重复连接，后面需进一步去除。
head(cor.data)

###设置节点属性
vertices <- c(as.character(cor.data$from),as.character(cor.data$to)) %>%
  as_tibble() %>%
  group_by(value) %>% 
  summarise()
colnames(vertices) <- "name"

##添加变量分类属性
vertices <- vertices %>%
  left_join(group,by="name")#将分类属性添加进去

###对节点属性表进行排序
vertices$group <- factor(vertices$group, levels = c("Mic","Gene" ))
vertices <- vertices %>%
  arrange(group) 

###构建graph数据结构
graph <- graph_from_data_frame(cor.data, vertices = vertices, directed = FALSE )
graph

##设置连接线的宽度为r值，并将标签设置为name
E(graph)$weight <- abs(E(graph)$r)
V(graph)$label <- V(graph)$name
###保存数据并基于Gephi进行可视化
write_graph(graph, "net.graphml", format="graphml")

##参考：
# 1）https://blog.csdn.net/qq_39859424/article/details/124462727
