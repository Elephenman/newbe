rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/弦图_chord")
#安装、加载包
# install.packages("circlize")
# install.packages("statnet")

library(circlize) # Circular Visualization
library(statnet) # Software Tools for the Statistical Analysis of Network Data

#准备数据
data <- read.table("data.txt",sep="\t",header = T,row.names = 1,check.names = F)
data <- as.matrix(data)
#生成作图数据
df <- data.frame(from = rep(rownames(data), ncol(data)),
                 to = rep(colnames(data), each = nrow(data)),
                 value = as.vector(data))

##颜色设定
color <- NULL
#为“to”列进行颜色赋值
color[c("A","B","C","D","E")] <- c("blue","red","yellow","green","pink")
#为“from”列进行颜色赋值
color[rownames(data)] <- c("#40A4D8","#33BEB7","#B2C224","#FECC2F","#FBA127",
                           "#F66320","#DB3937","#A463D7","#0C5BCE","grey","black")
#绘图
# circos.par(start.degree = 90)#调整放置方向
chordDiagram(df, 
             grid.col =color,#颜色设置
             grid.border=NULL,#边框颜色设置，设置为NULL则默认与填充色一致
             transparency = 0.2,#连接颜色透明度
             link.lwd = 0.01,#线条宽度
             link.lty = 1,    # 线路类型
             link.border = 0,#边框颜色
             directional = -1,#表示线条的方向，0代表没有方向，1代表正向，-1代表反向，2代表双向
             diffHeight = mm_h(2),#外圈和中间连线的间隔
             direction.type = c("diffHeight","arrows"), #线条是否带有箭头
             link.arr.type = "big.arrow")#箭头类型

circos.clear()#重新设置图形参数和内部变量

# 图例制作
legend("right",pch=20,legend=rownames(data),
       col=color[rownames(data)],bty="n",
       cex=1,pt.cex=3,border="black") # 设定图例

# 设置图片文件名、长宽和字体大小
pdf(file="plot.pdf", width=9, height=5, pointsize=8)
# circos.par(start.degree = 90)#调整放置方向
chordDiagram(df, 
             grid.col =color,#颜色设置
             grid.border=NULL,#边框颜色设置，设置为NULL则默认与填充色一致
             transparency = 0.2,#连接颜色透明度
             link.lwd = 0.01,#线条宽度
             link.lty = 1,    # 线路类型
             link.border = 0,#边框颜色
             directional = -1,#表示线条的方向，0代表没有方向，1代表正向，-1代表反向，2代表双向
             diffHeight = mm_h(2),#外圈和中间连线的间隔
             direction.type = c("diffHeight","arrows"), #线条是否带有箭头
             link.arr.type = "big.arrow")#箭头类型
legend("right",pch=20,legend=rownames(data),
       col=color[rownames(data)],bty="n",
       cex=1,pt.cex=3,border="black") # 设定图例
dev.off()

###由于修改文字注释代码的麻烦，所以这里需要后期使用AI软件或PS软件对一些重叠的文字进行调整