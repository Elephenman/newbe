rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/不同组散点+回归曲线+多项式拟合+线性拟合')#设置工作路径

#加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(ggpmisc) # Miscellaneous Extensions to 'ggplot2'

#读取数据——以Chiplot绘图平台数据为例
df <- read.table("data.txt",sep = "\t",header=1,check.names=FALSE)

######绘图#######
#绘制基础散点图
ggplot(df,aes(x,y))+
  geom_point(aes(fill=group),shape=21,size=3,alpha=0.5)

##为了方便展示，在X=6.25处将图形分割成两部分，并对X<6.25和X>6.25的数据分别添加拟合曲线
#在X=6.25处添加辅助线进区分
ggplot(df,aes(x,y))+
  geom_point(aes(fill=group),shape=21,size=3,alpha=0.5)+
  geom_vline(xintercept = 6.25, linetype = 2, color = "#08538c",linewidth=0.8)
#对X<6.25的散点进行线性拟合
ggplot(df,aes(x,y))+
  geom_point(aes(fill=group),shape=21,size=3,alpha=0.5)+
  geom_vline(xintercept = 6.25, linetype = 2, color = "#08538c",linewidth=0.8)+
  geom_smooth(data = df[df$x<6.25,],
              method = "lm", color = "red", 
              formula = y ~ x,
              linetype=1,alpha=0.5,linewidth = 0.8)
#对X>6.25的散点进行二次拟合
ggplot(df,aes(x,y))+
  geom_point(aes(fill=group),shape=21,size=3,alpha=0.5)+
  geom_vline(xintercept = 6.25, linetype = 2, color = "#08538c",linewidth=0.8)+
  geom_smooth(data = df[df$x<6.25,],
              method = "lm", color = "red", 
              formula = y ~ x,
              linetype=1,alpha=0.5,linewidth = 0.8)+
  geom_smooth(data = df[df$x>6.25,],
              method = "lm", color = "red", 
              formula = y ~ poly(x, 2, raw = TRUE),
              linetype=1,alpha=0.5,linewidth = 0.8)
#分别对两次拟合添加回归方程
ggplot(df,aes(x,y))+
  geom_point(aes(fill=group),shape=21,size=3,alpha=0.5)+
  geom_vline(xintercept = 6.25, linetype = 2, color = "#08538c",linewidth=0.8)+
  geom_smooth(data = df[df$x<6.25,],
              method = "lm", color = "red", 
              formula = y ~ x,
              linetype=1,alpha=0.5,linewidth = 0.8)+
  geom_smooth(data = df[df$x>6.25,],
              method = "lm", color = "red", 
              formula = y ~ poly(x, 2, raw = TRUE),
              linetype=1,alpha=0.5,linewidth = 0.8)+
  stat_poly_eq(data = df[df$x<6.25,],
               formula = y ~ x, 
               aes(label = paste(after_stat(eq.label),
                                 after_stat(adj.rr.label),
                                 sep = "~~~")), 
               parse = TRUE,label.x = "left")+
  stat_poly_eq(data = df[df$x<6.25,],
               formula = y ~ poly(x, 2, raw = TRUE), 
               aes(label = paste(after_stat(eq.label),
                                 after_stat(adj.rr.label),
                                 sep = "~~~")), 
               parse = TRUE,label.x = "right")

####个性化绘图模板
#自定义颜色
col<-c("#ec1c24", "#fdbd10", "#0066b2", "#ed7902")
##绘图
ggplot(df,aes(x,y))+
  #绘制基础散点图
  geom_point(aes(fill=group),shape=21,size=5,alpha=0.7)+
  #在X=6.25处添加辅助线进区分
  geom_vline(xintercept = 6.25, linetype = 2, color = "#08538c",linewidth=0.8)+
  # 对X<6.25的散点进行线性拟合
  geom_smooth(data = df[df$x<6.25,],
              method = "lm", color = "#84754e", 
              formula = y ~ x,
              linetype=1,alpha=0.5,linewidth = 0.8)+
  # 对X>6.25的散点进行线性拟合
  geom_smooth(data = df[df$x>6.25,],
              method = "lm", color = "#bc0024", 
              formula = y ~ poly(x, 2, raw = TRUE),
              linetype=1,alpha=0.5,linewidth = 0.8)+
  # 对X<6.25散点的线性拟合曲线添加回归方程
  stat_poly_eq(data = df[df$x<6.25,],
               formula = y ~ x, 
               aes(label = paste(after_stat(eq.label),
                                 after_stat(adj.rr.label),
                                 sep = "~~~")), 
               parse = TRUE,label.x = 0.05, label.y = 0.95,
               color = "#84754e")+
  # 对X>6.25散点的二次拟合曲线添加回归方程
  stat_poly_eq(data = df[df$x<6.25,],
               formula = y ~ poly(x, 2, raw = TRUE), 
               aes(label = paste(after_stat(eq.label),
                                 after_stat(adj.rr.label),
                                 sep = "~~~")), 
               parse = TRUE,label.x = 0.05, label.y = 0.9,
               color = "#bc0024")+
  #自定义颜色
  scale_fill_manual(values = col)+
  #对主题进行一些修改
  theme_bw()+
  theme(axis.text=element_text(color='black',size=14),
        legend.text = element_text(color='black',size=14),
        axis.title = element_text(color='black',size=15),
        panel.grid = element_blank(),
        legend.title = element_blank(),
        legend.position = c(0.9,0.2))+
  labs(x = "XXXXXXX", y = "XXXXXXX\n(XXXXXXXXXXXXX)", fill = NULL)+
  scale_x_continuous(expand = c(0,0))

#保存图片
ggsave(filename = "test.png", #文件名称及其类型，一般通过改变后缀生成相应格式的图片
       width = 7,#宽
       height = 6, #高
       units = "in",#单位
       dpi = 300)#设置分辨率

