rm(list=ls())

#安装包
# install.packages("ggseqlogo")
#加载包
library(ggseqlogo)

#数据——支持序列与矩阵两种格式的文件
#以ggseqlogo包自带示例数据ggseqlogo_sample为例
data(ggseqlogo_sample)
#DNA数据
df1<-pfms_dna
#氨基酸数据
df2<-seqs_aa
#序列格式
df3<-seqs_dna$MA0011.1
#矩阵格式——代表碱基位置及相应碱基在该位置的出现次数
df4<-pfms_dna$MA0031.1

###使用函数ggseqlogo()进行展示
??ggseqlogo#查看参数
ggseqlogo(data, facet = "wrap", scales = "free_x", ncol = NULL,
          nrow = NULL, ...)
#基本绘图
ggseqlogo(df1)
ggseqlogo(df3)

#方法的选择——bits(默认)和probability
p1<-ggseqlogo(df3,method="bits")
p2<-ggseqlogo(df3,method="probability")
cowplot::plot_grid(p1,p2,ncol=1)

#绘制多个图时通过facet与ncol控制
ggseqlogo(df1, facet = "wrap",ncol = 1)
ggseqlogo(df1, facet = "wrap",ncol = 2)

#序列类型的指定——通过seq_type参数指定序列类型，默认为“auto”自动识别
ggseqlogo(df1, facet = "wrap",ncol = 2, seq_type="dna")#"aa"、"dna"、"rna"
ggseqlogo(df2, facet = "wrap",ncol = 2, seq_type="aa")

#配色方案——col_scheme参数设置，具体配色方案通过?list_col_schemes查看
list_col_schemes(v = T)#展示配色方案
ggseqlogo(df1,col_scheme='clustalx')
ggseqlogo(df1,col_scheme='taylor')
###自定义配色——make_col_scheme参数实现
#离散型配色
col1<-make_col_scheme(chars = c("A","G", "T", "C"), 
                        groups = c("g1","g2", "g3","g4"),
                        cols = c("red","green","blue","yellow"))
ggseqlogo(df1,col_scheme=col1)
#连续型配色
col2<-make_col_scheme(chars=c("A","G", "T", "C"),
                      values=1:4,
                      name='group')
ggseqlogo(df1,col_scheme=col2)

##设置字体——通过font参数实现，?list_fonts查看内置字体
list_fonts(v = T)#查看内置字体
a<-ggseqlogo(df3,font="xkcd_regular")
b<-ggseqlogo(df3,font="roboto_slab_regular")
c<-ggseqlogo(df3,font="helvetica_regular")
d<-ggseqlogo(df3,font="helvetica_light")
cowplot::plot_grid(a,b,c,d,ncol=2)

##字母宽度——stack_width参数设置
a<-ggseqlogo(df3,stack_width=1)
b<-ggseqlogo(df3,stack_width=0.5)
cowplot::plot_grid(a,b,ncol=1)

##注释——与ggplot2注释类似
p1<-ggplot2::ggplot()+geom_logo(df3)+theme_logo()#可视化
p1
#添加文字注释
p1+ggplot2::annotate("text", x=6, y=1, label="This is a text\n annotation!")
#添加线条
p1+ggplot2::annotate("segment", x=1, xend = 3, y=1.5, yend = 1.5, size=3)
#添加图形注释
p1+ggplot2::annotate("rect", xmin = 6.5, xmax = 7.5, ymin = -0.05, ymax = 0.8, 
                     alpha=0.2, col="grey", fill="green")


###模板代码
library(ggplot2)
col1<-make_col_scheme(chars = c("A","G", "T", "C"), 
                      groups = c("g1","g2", "g3","g4"),
                      cols = c("red","green","blue","yellow"))#自定义配色
ggplot()+geom_logo(df1$MA0018.2,#数据
                            method="bits",#方法
                            seq_type="dna",#序列类型
                            col_scheme=col1,#配色方案
                            font="xkcd_regular",#字体
                            stack_width=0.8#字母宽度
                            )+
  annotate("text", x=5.5, y=2, color='red',label="This is a text\n annotation!")+
  annotate("segment", x=4.5, xend = 6.5, y=1.6, yend = 1.6, size=3)+
  annotate("rect", xmin = 2.5, xmax = 3.5, ymin = -0.05, ymax = 2.05, 
           alpha=0.2, col="grey", fill="green")+
  theme_logo()
#参考:https://omarwagih.github.io/ggseqlogo/