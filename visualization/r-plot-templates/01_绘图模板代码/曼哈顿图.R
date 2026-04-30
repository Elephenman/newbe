#设置工作环境
rm(list=ls())
setwd("D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\曼哈顿图")

#安装包
# install.packages("qqman")
# install.packages("CMplot")
# install.packages("ggplot2")
# install.packages("tidyverse")
# install.packages("ggforce")
# install.packages("ggprism")
#加载包
library(qqman)
library(CMplot)
library(ggplot2)
library(tidyverse)
library(ggforce)
library(ggprism)
##############1、使用qqman包进行绘制##################
#加载数据——以qqman包自带示例数据gwasresult数据为例
df1 <- gwasResults#数据中SNP为SNP名称，CHR为染色体编号，BP为碱基位置，P为p值
head(df1)#预览数据

manhattan(df1,#数据
          col = c('#30A9DE','#EFDC05','#E53A40','#090707'),#交替使用颜色展示
          suggestiveline = -log10(1e-05),#－log10(1e－5)处添加"suggestive"横线
          genomewideline = -log10(5e-08),#－log10(5e－10)处添加"genome-wide sigificant"横线
          highlight = snpsOfInterest,#内置高亮的snp数据， 也可以对snpOfInterest进行设置
          annotatePval = 0.05,#标记p值小于0.05的点
          annotateTop = T,#如果为T，则仅批注低于注解阈值的每个染色体上的顶部点，为F则标记所有小于注解阈值的点。
          main = "XXXXXXXX"#标题
          )
##可以使用??manhattan查看具体参数

#############2、使用CMplot包进行绘制##################
#加载数据——以CMplot包自带示例数据pig60k数据为例
data(pig60K)#预览数据

CMplot(pig60K,#示例数据
       chr.den.col=c("black","green","red"),#SNP密度展示
       file="jpg",#绘制图片类型
       memo="",#输出文件名中添加一个字符
       dpi = 600)#绘制图片的分辨率

#可以使用??CMplot查看具体参数,根据需要进行设置
CMplot(Pmap,
       col=c("#4197d8", "#f8c120", "#413496", "#495226",
             "#d60b6f", "#e66519", "#d581b7", "#83d3ad", "#7c162c", "#26755d"),
       bin.size=1e6, bin.range=NULL, bin.legend.num=10, pch=19, type="p",
       band=1, H=1.5, ylim=NULL, cex.axis=1, lwd.axis=1.5, cex.lab=1.5,
       plot.type="b", multracks=FALSE, points.alpha=100L, cex=c(0.5,1,1),
       r=0.3, outward=FALSE, ylab=expression(-log[10](italic(p))), 
       ylab.pos=3, xticks.pos=1, mar = c(3,6,3,3), threshold = NULL, 
       threshold.col="red", threshold.lwd=1, threshold.lty=2, 
       amplify= TRUE, signal.cex = 1.5, signal.pch = 19, 
       signal.col=NULL, signal.line=2, highlight=NULL, highlight.cex=1, 
       highlight.pch=19, highlight.type="p", highlight.col="red", 
       highlight.text=NULL, highlight.text.col="black", highlight.text.cex=1, 
       highlight.text.xadj=NULL, highlight.text.yadj=NULL, 
       highlight.text.font=3, chr.labels=NULL, chr.border=FALSE,
       chr.labels.angle=0, chr.den.col="black", chr.pos.max=FALSE, cir.band=1, 
       cir.chr=TRUE, cir.chr.h=1.5, cir.legend=TRUE, cir.legend.cex=0.6, 
       cir.legend.col="black", LOG10=TRUE, box=FALSE, conf.int=TRUE, 
       conf.int.col=NULL, file.output=TRUE, file=c("jpg","pdf","tiff"), 
       dpi=300, height=NULL, width=NULL, memo="", main="", main.cex=1.5, 
       main.font=2, trait.legend.ncol=NULL, verbose=TRUE)

###################3、使用ggplot2包进行绘制################
#数据，同样以qqman包自带数据gwasresult为例
df <- gwasResults
###数据处理
df %>% 
  group_by(CHR) %>% 
  summarise(df_chr_len=max(BP)) %>% #计算染色体长度
  mutate(total = cumsum(df_chr_len) - df_chr_len) %>%
  select(-df_chr_len) %>% #计算染色体初始位置
  left_join(df, ., by="CHR") %>%
  arrange(CHR, BP) %>%
  mutate( BPcum = BP + total)->df_SNP_position#计算累计SNP的位置

head(df_SNP_position)#预览数据

###绘图
#X轴标签位置
X_axis <-  df_SNP_position %>% group_by(CHR) %>% summarize(center=( max(BPcum) +min(BPcum) ) / 2 )
#添加高亮和注释信息：snpsOfInterest中的rs编号和P值大于10的点
data <- df_SNP_position %>%
  mutate( is_highlight=ifelse(SNP %in% snpsOfInterest, "yes", "no")) %>%
  mutate( is_annotate=ifelse(-log10(P)>10, "yes", "no"))
#绘图
ggplot(data, aes(x=BPcum, y=-log10(P))) +
  geom_point(aes(color=as.factor(CHR)),alpha=0.8, size=1.5)+
  scale_color_manual(values = rep(c('#30A9DE','#EFDC05','#E53A40','#090707'), 22 ))+#颜色设置
  scale_x_continuous(label = X_axis$CHR, breaks= X_axis$center)+#设定X轴
  scale_y_continuous(expand = c(0, 0) ) +#去除绘图区和X轴之间的gap
  geom_hline(yintercept = c(6, -log10(0.05/nrow(df_SNP_position))), #添加阈值线
             color = c('green', 'red'),size = 1.2, 
             linetype = c("dotted", "twodash")) + 
  geom_point(data=subset(data, is_highlight=="yes"), color="green", 
             size=2)+facet_zoom(x = BPcum >= 3000 & BPcum <=3500)+#展示某一区域的p值情况
  theme_prism(palette = "flames",#使用ggprism包自带主题
              base_fontface = "plain", 
              base_family = "serif", 
              base_size = 16,  
              base_line_size = 0.8, 
              axis_text_angle = 45)+ 
  theme(legend.position = "none",#去除图例
        panel.grid = element_blank(),
        panel.border = element_blank(),
        axis.line.x = element_line(),
        axis.line.y = element_line())
#参考：https://blog.csdn.net/ddxygq/article/details/103555955
