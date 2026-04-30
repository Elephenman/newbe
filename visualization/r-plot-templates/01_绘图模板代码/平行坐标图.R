rm(list = ls())

#加载R包
library(GGally)
library(ggthemes)
library(ggprism)
library(scagnostics)
#加载数据，使用R自带数据集iris
df<- iris

####绘图
#可选参数
??ggparcoord#查看该函数下的参数

ggparcoord(data,
           columns = 1:ncol(data),
           groupColumn = NULL,
           scale = "std",
           scaleSummary = "mean",
           centerObsID = 1,
           missing = "exclude",
           order = columns,
           showPoints = FALSE,
           splineFactor = FALSE,
           alphaLines = 1,
           boxplot = FALSE,
           shadeBox = NULL,
           mapping = NULL,
           title = "")
#展示
p1<-ggparcoord(df,
           columns = 1:4, #数据行数
           scale="globalminmax",#No scaling
           groupColumn = "Species",#按照分组显示不同颜色
           order = "anyClass",#水平坐标轴排序，可选参数有'skewness', 'allClass', 'anyClass', 'Outlying', 'Skewed', 'Clumpy', 'Sparse', 'Striated', 'Convex', 'Skinny', 'Stringy', 'Monotonic'
           showPoints = T,#是否显示点 
           title = "Parallel Coordinates chart",#标题
           alphaLines = 0.5) + #线的粗细
  theme_pander()+#模板主题设置
  theme(plot.title = element_text(size=10))+#标题大小设置
  scale_color_prism(palette = "candy_bright")#使用ggrism包的主题颜色
p1

p2<-ggparcoord(df,
               columns = 1:4, #数据行数
               groupColumn = "Species",#按照分组显示不同颜色
               order = "Outlying",#水平坐标轴排序
               showPoints = T,#是否显示点 
               title = "Parallel Coordinates chart",#标题
               scale="uniminmax",#Standardize to Min = 0 and Max = 1
               alphaLines = 0.5) + #线的粗细
  theme_pander()+#模板主题设置
  theme(plot.title = element_text(size=10))+#标题大小设置
  scale_color_prism(palette = "neon")#使用ggrism包的主题颜色
p2

p3<-ggparcoord(df,
               columns = 1:4, #数据行数
               groupColumn = "Species",#按照分组显示不同颜色
               order = "Clumpy",#水平坐标轴排序
               showPoints = T,#是否显示点 
               title = "Parallel Coordinates chart",#标题
               scale="std",#Normalize univariately (substract mean & divide by sd)
               alphaLines = 0.5) + #线的粗细
  theme_pander()+#模板主题设置
  theme(plot.title = element_text(size=10))+#标题大小设置
  scale_color_prism(palette = "autumn_leaves")#使用ggrism包的主题颜色
p3

p4<-ggparcoord(df,
               columns = 1:4, #数据行数
               groupColumn = "Species",#按照分组显示不同颜色
               order = "Sparse",#水平坐标轴排序
               showPoints = T,#是否显示点 
               title = "Parallel Coordinates chart",#标题
               scale="center",#Standardize and center variables
               alphaLines = 0.5) + #线的粗细
  theme_pander()+#模板主题设置
  theme(plot.title = element_text(size=10))+#标题大小设置
  scale_color_prism(palette = "sunny_garden")#使用ggrism包的主题颜色
p4

#拼图
cowplot::plot_grid(p1,p2,p3,p4,ncol=2)

#显示箱线图
ggparcoord(df,
           columns = 1:4, 
           scale="globalminmax",
           groupColumn = "Species",
           showPoints = T,
           title = "Parallel Coordinates chart",
           alphaLines = 0.5,
           boxplot = T) + 
  theme_map()+
  theme(plot.title = element_text(size=10))+
  scale_color_prism(palette = "candy_bright")

#分面显示
p1+facet_wrap(~Species)
p2+facet_wrap(~Species)
p3+facet_wrap(~Species)
p4+facet_wrap(~Species)
