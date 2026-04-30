rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/代码复现/nature文章原图复现系列/代码/不一样的点线图')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics

#加载数据
df <- read.table("data.txt",header = 1,check.names = F,sep="\t")
df$group <- factor(df$group,levels = c("all","WB","PL","IT","IR","AJ","IN","CH","CB","NG"))

#绘图
ggplot(df,aes(sample,value,color=group,group=group))+
  #绘制实线部分的折线
  geom_line(data = df[df$sample==1|df$sample==2|df$sample==3|
                        df$sample==4|df$sample==5,],linewidth=0.5)+
  #绘制虚线部分的折线
  geom_line(data = df[df$sample==5|df$sample==6.5|df$sample==8,],
            linewidth=0.5,linetype=2)+
  #绘制散点
  geom_point(data = df[df$sample==6.5|df$sample==8,],size=1.5)+
  #调整并更改X轴标签
  scale_x_continuous(breaks = c(1,2,3,4,5,6.5,8), labels = c("PCA\n(J=1)","PCA\n(J=5)","PCA\n(J=10)",
                                                 "PCA\n(J=15)","PCA\n(J=20)","GRM\n(PCA SNPs)","GRM\n(PGS SNPs)"))+
  #Y轴范围及标签
  scale_y_continuous(breaks = seq(0, 1, len = 5),limits = c(0,1))+
  #主题
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.x = element_text(color = "black", size = 11),
        axis.text.y = element_text(color = "black",size = 11),
        axis.title = element_text(color = "black",size = 15),
        legend.position = "right",
        legend.title = element_text(color = "black",size = 14),
        legend.text = element_text(color = "black",size = 12))+
  #标题设置
  labs(x="Genetic distance from training data",
       y="UKBB: -cor("*r[i]^2~","~d[i]*")",
       color="ancestry")+
  #颜色
  scale_color_manual(values = c("#000000","#989898","#781a18","#029c6f",
                                "#55b4e4","#d174a8","#e19e09","#dd5b00",
                                "#8562bf","#2d50d9"))
