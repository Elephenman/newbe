rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/散点+多辅助线+特定区域颜色及标签标记")

##加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggrepel) # Automatically Position Non-Overlapping Text Labels with'

##加载数据（随机编写，无实际意义，具体应用场景根据个人数据进行数据分析，这里不做展示）
df <- read.table("data.txt",sep="\t",header = T, check.names = F)

##根据预设辅助线位置及划定区域添加分组信息
df$G <- ifelse(abs(df$x)>=30|abs(df$y)>=30, "Y","N")
#也可以给不同区域划定不同分组
df$G2 <- ifelse(df$x>=30&abs(df$y)<=30, "g1", ifelse(df$x<=-30&abs(df$y)<=30, "g2", ifelse(abs(df$x<=30)&df$y>=30, "g3",ifelse(abs(df$x<=30)&df$y<=-30,"g4", "g5"))))

##根据预设条件为符合的数据添加标签
df$label <- ifelse(abs(df$x)>=40|abs(df$y)>=40, df$sample,"")


##绘图——区域指定统一颜色
p1 <- ggplot(df, aes(x,y))+
  #添加辅助线
  geom_vline(xintercept = 30, lty="dashed", color = "grey50", linewidth = 0.8)+
  geom_vline(xintercept = -30, lty="dashed", color = "grey50", linewidth = 0.8)+
  geom_hline(yintercept = 30, lty="dashed", color = "grey50", linewidth = 0.8)+
  geom_hline(yintercept = -30, lty="dashed", color = "grey50", linewidth = 0.8)+
  #绘制散点图
  geom_point(aes(color = G), shape = 16, size = 4, alpha = 0.8)+
  scale_color_manual(values = c("grey80","#ea4c89"))+
  labs(x = "xxxxxxxxxxx\nxxxxxxx", y = "XXXXXXXXXXXXX\nXXXXXX")+
  #主题相关设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        legend.position = "none")+
  #为特定区域统一添加颜色
  annotate("rect", xmin = -Inf, xmax = -30, ymin = -30, ymax = 30, alpha = 0.2,fill="#ea4c89")+
  annotate("rect", xmin = 30, xmax = Inf, ymin = -30, ymax = 30, alpha = 0.2,fill="#ea4c89")+
  annotate("rect", xmin = -30, xmax = 30, ymin = -Inf, ymax = -30, alpha = 0.2,fill="#ea4c89")+
  annotate("rect", xmin = -30, xmax = 30, ymin = 30, ymax = Inf, alpha = 0.2,fill="#ea4c89")+
  #添加显著性标签
  geom_text_repel(aes(label = label),
                  color="#ea4c89",
                  max.overlaps = 10000,
                  size=4,
                  box.padding=unit(0.8,'lines'),
                  point.padding=unit(0.8, 'lines'),
                  segment.color='black',
                  show.legend=FALSE)
p1

##绘图——区域指定不同颜色
p2 <- ggplot(df, aes(x,y))+
  #添加辅助线
  geom_vline(xintercept = 30, lty="dashed", color = "grey50", linewidth = 0.8)+
  geom_vline(xintercept = -30, lty="dashed", color = "grey50", linewidth = 0.8)+
  geom_hline(yintercept = 30, lty="dashed", color = "grey50", linewidth = 0.8)+
  geom_hline(yintercept = -30, lty="dashed", color = "grey50", linewidth = 0.8)+
  #绘制散点图
  geom_point(aes(color = G2), shape = 16, size = 4, alpha = 0.8)+
  scale_color_manual(values = c("g5"="grey80",
                                "g2"="#4dc9f6",
                                "g1"="#f67019",
                                "g4"="#f53794",
                                "g3"="#acc236"))+
  labs(x = "xxxxxxxxxxx\nxxxxxxx", y = "XXXXXXXXXXXXX\nXXXXXX", color=NULL)+
  #主题相关设置
  theme_bw()+
  theme(panel.grid = element_blank())+
  #为特定区域统一添加颜色
  annotate("rect", xmin = -Inf, xmax = -30, ymin = -30, ymax = 30, alpha = 0.2, fill="#4dc9f6")+
  annotate("rect", xmin = 30, xmax = Inf, ymin = -30, ymax = 30, alpha = 0.2, fill="#f67019")+
  annotate("rect", xmin = -30, xmax = 30, ymin = -Inf, ymax = -30, alpha = 0.2, fill="#f53794")+
  annotate("rect", xmin = -30, xmax = 30, ymin = 30, ymax = Inf, alpha = 0.2, fill="#acc236")+
  #添加显著性标签
  geom_text_repel(aes(label = label,color=G2),
                  max.overlaps = 10000,
                  size=4,
                  box.padding=unit(0.8,'lines'),
                  point.padding=unit(0.8, 'lines'),
                  segment.color='black',
                  show.legend=FALSE)+
  #图例大小设置
  guides(color=guide_legend(override.aes = list(size=5,alpha=1)))
p2  

##拼图
cowplot::plot_grid(p1,p2,rel_widths = c(1,1.2),ncol = 2)

