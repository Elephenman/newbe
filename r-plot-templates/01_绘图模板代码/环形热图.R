rm(list=ls())#clear Global Environment
setwd('D:\\桌面\\SCI论文写作与绘图\\R语言绘图\\基础图形绘制\\ggtree画环形热图')#设置工作路径

#安装包
if(!requireNamespace("BiocManager", quietly = T))
  install.packages("BiocManager") 
BiocManager::install("ComplexHeatmap")
install.packages("circlize")

#加载包
library(circlize)
library(ComplexHeatmap)


#读取数据
df <- read.table(file="example.txt",sep="\t",header=T,check.names=FALSE,row.names = 1)
#常规热图
Heatmap(df)
###绘制环形热图
#颜色
color <- colorRamp2(c(-5, 0, 5), c("blue", "white", "green"))
circos.par(gap.after = c(20))#空出一段用于添加组名
circos.heatmap(df, #数据
               col = color,#颜色
               dend.side = "inside",#确定聚类结果放在圈内还是圈外
               rownames.side = "outside",#组名
               track.height = 0.4
               # clustering.method = "complete",#归一化处理
               # distance.method = "euclidean"#聚类方法，默认为欧氏距离
               )
#添加组名
circos.track(track.index = get.current.track.index(), panel.fun = function(x, y) {
  if(CELL_META$sector.numeric.index == 1) {
    A = length(colnames(df))
    circos.text(rep(CELL_META$cell.xlim[2], A) + convert_x(0.2, "mm"), #x坐标
                28+(1:A)*10,#y坐标
                colnames(df), #标签
                cex = 0.5, adj = c(0, 1), facing = "inside")
  }
}, bg.border = NA)
##组名的标签位置需要耐心调整参数以到合适的位置，当然也可以导出PDF在AI中进行添加及位置调整
#添加图例
grid.draw(Legend(title = "Title", col_fun = color))

circos.clear()#清除参数，如果前面需要调整参数，必须先执行此命令，否则绘制的新图会和之前的图重叠在一起

#可以再加一个热图
color2=colorRamp2(c(-5, 0, 5), c("green", "white", "red"))
circos.heatmap(df,  col = color, dend.side = "outside")
circos.heatmap(df, col = color2,rownames.side = "inside")

circos.clear()#清除参数，如果前面需要调整参数，必须先执行此命令，否则绘制的新图会和之前的图重叠在一起


#参考资料：https://jokergoo.github.io/circlize_book/book/
??circos.heatmap
circos.heatmap(mat, split = NULL, col, na.col = "grey",
               cell.border = NA, cell.lty = 1, cell.lwd = 1,
               bg.border = NA, bg.lty = par("lty"), bg.lwd = par("lwd"),
               ignore.white = is.na(cell.border),
               cluster = TRUE, clustering.method = "complete", distance.method = "euclidean",
               dend.callback = function(dend, m, si) reorder(dend, rowMeans(m)),
               dend.side = c("none", "outside", "inside"), dend.track.height = 0.1,
               rownames.side = c("none", "outside", "inside"), rownames.cex = 0.5,
               rownames.font = par("font"), rownames.col = "black",
               show.sector.labels = FALSE, cell_width = rep(1, nrow(mat)), ...)
