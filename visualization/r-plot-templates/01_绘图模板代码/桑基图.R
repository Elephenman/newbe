rm(list=ls())
#设置工作环境
setwd("D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\桑基图")

#下载包
# install.packages("ggplot2")
# install.packages("ggalluvial")
#载入包
library(ggplot2)
library(ggalluvial)

#加载数据
data <- read.table("data.txt",header = T, check.names = F)

#格式转换
df <- to_lodes_form(data[,1:ncol(data)],
                           axes = 1:ncol(data),
                           id = "value")
print(df)#预览数据

##绘制桑基图（Sankey diagram）
col<- rep(c('#2e1f54', '#52057f', '#bf033b', '#f00a36',
            '#ed3b21', '#ff6908', '#ffc719','#598c14', 
            '#335238', '#4a8594', '#051736', '#dbe0e3'), 3)#自定义颜色

pdf("test.pdf",width = 8, height = 6)#新建一个PDF文件
ggplot(df, aes(x = x, fill=stratum, label=stratum,
               stratum = stratum, alluvium  = value))+#数据
  geom_flow(width = 0.3,#连线宽度
            curve_type = "sigmoid",#曲线形状
            alpha = 0.5,#透明度
            color = 'white',#间隔颜色
            size = 0.1)+#间隔宽度
  geom_stratum(width = 0.28)+#图中方块的宽度
  geom_text(stat = 'stratum', size = 2, color = 'black')+
  scale_fill_manual(values = col)+#自定义颜色
  theme_void()+#主题（无轴及网格线）
  theme(axis.line=element_line(linetype=1,color="grey",size=1.5),#坐标轴粗细、类型及颜色设置
        plot.title = element_text(size=15,hjust = 0.5), #标题大小和位置
        legend.position = 'none')#去除图例
dev.off()#关闭PDF
