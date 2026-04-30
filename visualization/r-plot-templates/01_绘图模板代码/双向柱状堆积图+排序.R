#设置工作环境
rm(list=ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/双向柱状堆积图+排序")

#加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(dplyr) # A Grammar of Data Manipulation

#加载数据
df <- read.table("data.txt",header = T,sep='\t')

#将宽数据转变为长数据
df2 <- melt(df, id.vars = c("sample","group"), 
            measure.vars = c('value5','value4','value3',
                             'value2','value1'))
df2$group <- factor(df$group,levels = c("group1","group2"))
df2$sample <- factor(df$sample,levels = c("OR4K2","OR4K1","GRPIN2","OR9G1","SULT1A3","OR4Q3",
                                         "PDPR","CYP2D6","PRAMEF18"))

#数据处理——将其中一组的数据转换为负值
df2$value <- ifelse(df2$group=="group2",-df2$value,df2$value)

#双向柱状堆积图
df2 %>% 
  ggplot()+
  #柱状图
  geom_col(aes(sample, value, fill = variable), width = 0.9)+
  #坐标转换
  coord_flip()+
  #自定义颜色
  scale_fill_manual(values = c(value1="#d20962", 
                               value2="#f47721", 
                               value3="#7ac143", 
                               value4="#00a78e", 
                               value5="#00bce4"))+
  #标注y=0刻度线
  geom_hline(yintercept = 0, 
             color = "black", linetype = 1,linewidth=0.6)+
  #主题设置
  theme_bw()+
  theme(panel.grid.major.y = element_blank(),
        axis.text.x = element_text(color = "black", size = 13),
        axis.text.y = element_text(color = "black",size = 14,face = "italic"),
        axis.title = element_text(color = "black",size = 16),
        legend.position = "top",
        legend.title = element_blank(),
        legend.text = element_text(color = "black",size = 15))+
  #标题设置
  labs(x=NULL,y="Frequency")+
  #y轴范围设置
  scale_y_continuous(breaks = seq(-400, 400, 200), 
                     labels = as.character(abs(seq(-400, 400, 200))),
                     limits = c(-480, 480))->p1
p1

####排序-金字塔型
#根据原始数据计算各样本值和（根据个人需求制定排序方式）
df3 <- df %>%
  melt(id.vars = c("sample","group"), 
       measure.vars = c('value5','value4','value3',
                        'value2','value1')) %>% 
  select(sample,value) %>%
  group_by(sample) %>% 
  summarise_all(sum)
#排序
df3 <- df3[order(abs(df3$value),decreasing=TRUE),]

#将绘图数据按照得到的排序顺序进行排序
df2$sample <- factor(df$sample,levels = df3$sample)

#重新绘图
df2 %>% 
  ggplot()+
  #柱状图
  geom_col(aes(sample, value, fill = variable), width = 0.9)+
  #坐标转换
  coord_flip()+
  #自定义颜色
  scale_fill_manual(values = c(value1="#d20962", 
                               value2="#f47721", 
                               value3="#7ac143", 
                               value4="#00a78e", 
                               value5="#00bce4"))+
  #标注y=0刻度线
  geom_hline(yintercept = 0, 
             color = "black", linetype = 1,linewidth=0.6)+
  #主题设置
  theme_bw()+
  theme(panel.grid.major.y = element_blank(),
        axis.text.x = element_text(color = "black", size = 13),
        axis.text.y = element_text(color = "black",size = 14,face = "italic"),
        axis.title = element_text(color = "black",size = 16),
        legend.position = "top",
        legend.title = element_blank(),
        legend.text = element_text(color = "black",size = 15))+
  #标题设置
  labs(x=NULL,y="Frequency")+
  #y轴范围设置
  scale_y_continuous(breaks = seq(-400, 400, 200), 
                     labels = as.character(abs(seq(-400, 400, 200))),
                     limits = c(-480, 480))->p2
p2

###排序——倒金字塔型
df2$sample <- factor(df$sample,levels = rev(df3$sample))
df2 %>% 
  ggplot()+
  #柱状图
  geom_col(aes(sample, value, fill = variable), width = 0.9)+
  #坐标转换
  coord_flip()+
  #自定义颜色
  scale_fill_manual(values = c(value1="#d20962", 
                               value2="#f47721", 
                               value3="#7ac143", 
                               value4="#00a78e", 
                               value5="#00bce4"))+
  #标注y=0刻度线
  geom_hline(yintercept = 0, 
             color = "black", linetype = 1,linewidth=0.6)+
  #主题设置
  theme_bw()+
  theme(panel.grid.major.y = element_blank(),
        axis.text.x = element_text(color = "black", size = 13),
        axis.text.y = element_text(color = "black",size = 14,face = "italic"),
        axis.title = element_text(color = "black",size = 16),
        legend.position = "top",
        legend.title = element_blank(),
        legend.text = element_text(color = "black",size = 15))+
  #标题设置
  labs(x=NULL,y="Frequency")+
  #y轴范围设置
  scale_y_continuous(breaks = seq(-400, 400, 200), 
                     labels = as.character(abs(seq(-400, 400, 200))),
                     limits = c(-480, 480))->p3
p3


###排序——中间值最大，两端最小
# 在排序数据基础上添加一列数据，这列数据按照最大值在中间，其他值依次向两端延续
# 如 计算的df3中有9行数据，则最大值对于新的排序序号就是5，然后临近两个依次降低的排序为4和6
df3$x <- c(5,4,6,3,7,2,8,1,9)
#按照新的列排序
df4 <- df3[order(df3$x),]
df2$sample <- factor(df$sample,levels = df4$sample)
#重新绘图
df2 %>% 
  ggplot()+
  #柱状图
  geom_col(aes(sample, value, fill = variable), width = 0.9)+
  #坐标转换
  coord_flip()+
  #自定义颜色
  scale_fill_manual(values = c(value1="#d20962", 
                               value2="#f47721", 
                               value3="#7ac143", 
                               value4="#00a78e", 
                               value5="#00bce4"))+
  #标注y=0刻度线
  geom_hline(yintercept = 0, 
             color = "black", linetype = 1,linewidth=0.6)+
  #主题设置
  theme_bw()+
  theme(panel.grid.major.y = element_blank(),
        axis.text.x = element_text(color = "black", size = 13),
        axis.text.y = element_text(color = "black",size = 14,face = "italic"),
        axis.title = element_text(color = "black",size = 16),
        legend.position = "top",
        legend.title = element_blank(),
        legend.text = element_text(color = "black",size = 15))+
  #标题设置
  labs(x=NULL,y="Frequency")+
  #y轴范围设置
  scale_y_continuous(breaks = seq(-400, 400, 200), 
                     labels = as.character(abs(seq(-400, 400, 200))),
                     limits = c(-480, 480))->p4
p4


###排序——两端值最大，中间最小
# 在排序数据基础上添加一列数据，这列数据按照最小值在两端，其他值按照由小到大依次向两端延续
# 如计算的df3中有9行数据，则最小值对于新的排序序号就是5，然后临近两个依次降低的排序为4和6
df3$x2 <- c(1,9,2,8,3,7,4,6,5)
#按照新的列排序
df5 <- df3[order(df3$x2),]
df2$sample <- factor(df$sample,levels = df5$sample)
#重新绘图
df2 %>% 
  ggplot()+
  #柱状图
  geom_col(aes(sample, value, fill = variable), width = 0.9)+
  #坐标转换
  coord_flip()+
  #自定义颜色
  scale_fill_manual(values = c(value1="#d20962", 
                               value2="#f47721", 
                               value3="#7ac143", 
                               value4="#00a78e", 
                               value5="#00bce4"))+
  #标注y=0刻度线
  geom_hline(yintercept = 0, 
             color = "black", linetype = 1,linewidth=0.6)+
  #主题设置
  theme_bw()+
  theme(panel.grid.major.y = element_blank(),
        axis.text.x = element_text(color = "black", size = 13),
        axis.text.y = element_text(color = "black",size = 14,face = "italic"),
        axis.title = element_text(color = "black",size = 16),
        legend.position = "top",
        legend.title = element_blank(),
        legend.text = element_text(color = "black",size = 15))+
  #标题设置
  labs(x=NULL,y="Frequency")+
  #y轴范围设置
  scale_y_continuous(breaks = seq(-400, 400, 200), 
                     labels = as.character(abs(seq(-400, 400, 200))),
                     limits = c(-480, 480))->p5
p5

###拼图
library(patchwork)
patch <- (p2+p3)/(p4+p5)
guide_area()/(p1+patch+plot_layout(widths = c(1.5,2)))+
  plot_layout(heights = c(0.2,2))+
  plot_layout(guides = 'collect')+
  plot_annotation(
    tag_levels = c('A', '1'), 
    tag_prefix = 'Fig. ',
    tag_sep = '.',
  ) & theme(plot.tag.position = c(0, 1.05),
            plot.tag = element_text(size = 15, hjust = 0, vjust = 0,color="red")
  )
