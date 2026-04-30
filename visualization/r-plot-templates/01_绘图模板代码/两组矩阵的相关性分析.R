rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/R绘图模板合集/两组矩阵的相关性分析')#设置工作路径


#加载包
library(psych)
library(circlize)
#加载数据
#OTU表格
df1 <- read.table("otu.txt",sep="\t",header = T,row.names = 1,check.names = F)
df1 <- as.data.frame(t(df1)) 
#环境因子
df2 <- read.table("data.txt",sep="\t",header = T,row.names = 1,check.names = F)

#相关性计算
data <- corr.test(df1,df2,use = "pairwise",
                  method="spearman",#指定方法
                  adjust="BH",#矫正P值,"holm", "hochberg", "hommel", "bonferroni", "BH", "BY", "fdr", "none"
                  alpha=0.05,#指定显著性阈值
                  minlength=3)#指定缩写最小长度
#查看p、r值并提取p、r值
# df_p <- data$p#未矫正
df_p <- data$p.adj
df_r <- data$r
#确定存在相互作用关系的阈值，将相关性R矩阵内不符合的数据转换为0
df_r[abs(df_r)<0.3] = 0
df_r <- t(df_r)#转置矩阵为作图要求格式
###可视化
#pheatmap包
library(pheatmap)
pheatmap(df_r,
         angle_col = "45",
         cellwidth=12, cellheight=17,
         cluster_rows=F, treeheight_col = 30,
         fontsize=5,
         color = colorRampPalette(c("navy", "white", "firebrick3"))(50))

###ComplexHeatmap包
library(ComplexHeatmap)
#颜色
col_fun <- colorRamp2(
  c(-1, 0, 1),
  c("navy", "white", "firebrick3"))
col <- col_fun(seq(-1, 1))
#绘图
Heatmap(df_r,
        col = col,#颜色设置
        # show_row_dend = T,#取消行聚类
        rect_gp = gpar(col = "white", lwd = 1),#网格颜色、宽度
        row_names_side = "right",#行名显示在左或右
        # cluster_rows = FALSE,#取消行聚类，保证行名顺序不变
        clustering_distance_columns = "euclidean",#聚类方法
        #图例设置
        heatmap_legend_param = list(
          # at = c(-1, 0, 1),
          # labels = c("low", "zero", "high"),``
          title = NULL,
          legend_height = unit(4, "cm"),
          title_position = "lefttop-rot"),
        # 居中对齐
        row_names_centered = F,
        column_names_centered = F,
        # 设置选择角度
        row_names_rot = 0,
        column_names_rot = 45,
        # 设置标签字体大小
        row_names_gp = gpar(
          col = "black",
          fontsize = 8
        ),
        column_names_gp = gpar(
          col = "black",
          fontsize = 8
        ),
        #热图整体长宽
        width = unit(25, "cm"),
        height = unit(17, "cm"),
        #设置显示r绝对值大于等于0.5的数据
        cell_fun = function(j, i, x, y, width, height, fill) {
          if(df_r[i, j] >= 0.5 |df_r[i, j] <= -0.5)
            grid.text(sprintf("*", df_r[i, j]), x, y, gp = gpar(fontsize = 15))
        }
)
