rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/mantel test')#设置工作路径

#加载包
library(vegan)
library(dplyr)
library(ggcor)
library(ggplot2)

#加载数据
#OTU表格，并根据绘图需求对其进行编辑和转换
df <- read.table("otu.txt",header = 1,row.names = 1,check.names = F,sep = "\t")
df <-data.frame(t(df))
df <- df[c(1,3,4,2,8,10,6,9,7,11,5,12),]
#环境因子数据
env <- read.table("env.txt",sep="\t",header = T,row.names = 1,check.names = F)

#绘制环境因子间相关性热图，pearson方法
p <- quickcor(env,#数据
              type = "upper",#绘制上半部分
              method = "pearson",#方法
              show.diag = T) +#是否显示对角线
  geom_square()+#类型
  scale_fill_gradient2( high = '#fe6263', mid = 'white',low = '#7caaff')  #颜色设置
p
#计算OTU与环境因子之间的mantel test的r值和p值并定义OTU数据分组
df_mantel <- mantel_test(df, env, #数据
                         mantel.fun = 'mantel',#方法
                         spec.dist.method = 'bray', 
                         env.dist.method = 'euclidean',
                         spec.select = list("Yield components" = 1:4,
                                            "Wheat growth indicators" = 5:8,
                                            "Yield" = 9:12))#将群落数据按组进行分开
#定义标签,即对mantel分析后的数据按照个人需求进行分割
df_mantel <- df_mantel %>%
  mutate(df_r = cut(r, breaks = c(-Inf, 0.25, 0.5, Inf),
                labels = c("< 0.25", "0.25 - 0.5", ">= 0.5")),#定义Mantel的R值范围标签
         df_p = cut(p.value, breaks = c(-Inf, 0.01, 0.05, Inf),
                    labels = c("< 0.01", "0.01 - 0.05", ">= 0.05")))#定义Mantel的P值范围标签
#自定义连线类型
df_mantel$linetype <- ifelse(df_mantel$p.value>=0.05,2,1)
df_mantel$linetype <- factor(df_mantel$linetype,levels = c("1","2"))
###在热图基础上添加mantel test数据
quickcor(env, type = "upper",method = "pearson",show.diag = T,cor.test = T) +
  geom_square()+
  scale_fill_gradient2( high = '#fe6263', mid = 'white',low = '#7caaff')+
  geom_square() +
  geom_mark(r = NA,sig.thres = 0.05, size = 6, color = "black")+#显著性标签
  anno_link(df_mantel, aes(color = df_p,
                           size = df_r,
                           linetype = linetype),
            label.size = 4,
            label.fontface = 1,
            curvature = 0.2,#连接线变为曲线
            nudge_x =0.2)+#标签位置
  scale_size_manual(values = c(0.8, 1.4, 2))+#连线粗细设置
  scale_color_manual(values = c("#ffa83a","#dc4fff","#cacdd2"))+#线条颜色设置
  scale_linetype_manual(values = c(1,2))+
  guides(fill = guide_colorbar(title = "Pearson's r", order = 1),#图例相关设置
         size = guide_legend(title = "Mantel's r",order = 2),
         color = guide_legend(title = "p-value", order = 3),
         linetype = "none") # 设置线条粗细