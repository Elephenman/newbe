rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/半圆进化树+分支颜色+注释+标签颜色')#设置工作路径

#加载包
library(ggtree) # an R package for visualization of tree and annotation data
library(ggtreeExtra) # An R Package To Add Geometric Layers On Circular Or Other Layout Tree Of "ggtree"
library(ggnewscale) # Multiple Fill and Colour Scales in 'ggplot2'
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics 

##数据——随机编写
df_tree <- read.tree(text='((((A_1:1,A_2:1,A_3:3,A_4:2,A_5:1,A_6:6,A_7:4,A_8:5):3,(C_1:3,C_2:2,C_3:3,C_4:1,C_5:3,C_6:4,C_7:6,C_8:5):1):2,(B_1:4,B_2:1,B_3:3,B_4:2,B_5:1,B_6:1,B_7:2,B_8:5):2):4,(D_1:2,D_2:1,D_3:5,D_4:3,D_5:4,D_6:1,D_7:5,D_8:7):5):3;')

# 对树分组
sample <- list(A=c("A_1","A_2","A_3","A_4","A_5","A_6","A_7","A_8"),
               B=c("B_1","B_2","B_3","B_4","B_5","B_6","B_7","B_8"),
               C=c("C_1","C_2","C_3","C_4","C_5","C_6","C_7","C_8"),
               D=c("D_1","D_2","D_3","D_4","D_5","D_6","D_7","D_8"))
# 将分组信息和进化树组合到一起
tree<-groupOTU(df_tree,sample)

#突出显示的标签
df_label <- c("A_6",
             "D_8",
             "C_7",
             "B_8")

#注释信息（随机生成）
df_group <- data.frame(
  sample=c("A_1","A_2","A_3","A_4","A_5","A_6","A_7","A_8",
           "B_1","B_2","B_3","B_4","B_5","B_6","B_7","B_8",
           "C_1","C_2","C_3","C_4","C_5","C_6","C_7","C_8",
           "D_1","D_2","D_3","D_4","D_5","D_6","D_7","D_8"),
  group=rep(c("A","B","C","D"),each=8),
  G=rep(c('group1','group2','group3','group4'),each=3,len=32),
  group2=sample(-50:50, 32, replace = FALSE)
)
df_group$G2 <-ifelse(df_group$group2>0,"Yes","No")

##绘图
ggtree(tree,#文件
       aes(color=group),#支长颜色按照分组进行着色
       layout="fan",#进化树类型
       open.angle=180,#开口角度
       linewidth=0.6,#分支线条粗细
       show.legend = F)+
  geom_tiplab(aes(color = label %in% df_label),#设定标签颜色根据筛选条件突出显示特定标签
              size=3.5,#字体大小
              align = T,#使用虚线连接标签与分支
              linetype = 3,linewidth = 0.4,offset = 12.5,show.legend = F)+
  scale_color_manual(values=c("black","#1aafd0","#6a67ce","#ffb900","#fc636b","#aeb6b8","#e53238"))+
  #添加注释信息-G
  new_scale_fill() +
  geom_fruit(
    data=df_group,
    geom=geom_tile,
    mapping=aes(y=sample, fill=G),
    color="grey10",
    width=1.2,
    offset=0.1)+
  scale_fill_manual(
    values=c("#4285f4", "#34a853", "#fbbc05","#ea4335"),
    guide=guide_legend(keywidth=1, keyheight=1, order=2),
    name="Note01")+
  #添加注释信息-group2
  new_scale_fill() +
  geom_fruit(
    data=df_group,#数据
    geom = geom_col,#绘图类型
    mapping = aes(x = group2,y=sample,fill=G2),
    offset = 0.4,
    pwidth = 0.4,
    width=0.8)+#条形图宽度
  scale_fill_manual(
    values=c("Yes"="#4b1702",
             "No"="#8f9696"),
    guide=guide_legend(keywidth=1, keyheight=1, order=1),
    name="Note02")+
  theme(legend.position = "top")#主题设置
