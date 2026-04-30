rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/R绘图模板合集/线性相关性分析')#设置工作路径

####数据这里我们自己编写一段数据
##水稻株高
A<-c(55,58,62,75,69,59,55,66,88,69,47,58,75,68,64)
##水稻根毛数量
B<-c(100,102,105,115,109,105,101,110,125,104,95,102,120,116,109)
data <- data.frame(A,B)
#计算相关性
cor.test(A,B,data=data)
df_cor<-lm(B~A,data=data)
summary(df_cor)
###根据结果可以知道株高与根毛数量之间的相关性系数为0.936734，且呈正相关，P值为2.72e-07<0.05
###回归方程为B=0.76*A+58.96
###拟合优度R^2=0.88,即拟合度很好
###回归系数的置信区间为[0.82，0.98]

###绘图
#最简单展示——plot函数
 plot(A, B, 
     xlab = "株高", ylab = "根毛数量",
     pch = 16, frame = T)
# 添加回归线
abline(lm(B ~ A), col = "red")

####使用ggplot2包进行绘制
library(ggplot2)
library(ggprism)

p1<-ggplot(data,aes(x=A,y=B,color="orange"))+#指定数据、X轴、Y轴，颜色
  theme_bw()+#主题设置
  geom_point(size=3,shape=16)+#绘制点图并设定大小
  theme(panel.grid = element_blank())+
  labs(x="株高",y="根毛数量")+#x、y轴标题
  geom_smooth(method='lm', se=FALSE, color='turquoise4')+#添加回归线
  geom_text(aes(x=55,y=124,label="R^2=0.88\ny=0.75x+58.96"),
            color="red",family = "serif",fontface = "plain",size = 5)+
  theme_prism(palette = "candy_bright",
              base_fontface = "plain", # 字体样式，可选 bold, plain, italic
              base_family = "serif", # 字体格式，可选 serif, sans, mono, Arial等
              base_size = 16,  # 图形的字体大小
              base_line_size = 0.8, # 坐标轴的粗细
              axis_text_angle = 45)+ # 可选值有 0，45，90，270
  scale_fill_prism(palette = "candy_bright")+
  theme(legend.position = 'none')#去除图例
p1

######当然我们也可以做回归诊断，之后剔除离群点重新进行线性相关性分析
#回归诊断
par(mfrow=c(2,2))
plot(df_cor)  #绘制回归诊断图
# 图1是残差拟合，越没有趋势越好，有趋势说明可能需要二次项；
# 图2是残差正态性检验，越落在虚线上越好（理想的残差服从0附件的正态分布，否则说明模型不够充分还有趋势没有提取出来）；
# 图3检验残差是否等方差；
# 图4检验离群点，第6个样本点偏离较远，应该剔除掉重新做回归。
##根据图可以看出第10、13，14个点偏离较远，需要剔除重新进行分析
data2<-data[c(-10,-13,-14),] 
cor.test(A,B,data=data2)
df_cor2<-lm(B~A,data=data2)
summary(df_cor2)
##P值为6.284e-10<0.5,R^2=0.98，线性回归方程为y=0.73x+60.47
###重新绘图
p2<-ggplot(data2,aes(x=A,y=B,color="orange"))+#指定数据、X轴、Y轴，颜色
  theme_bw()+#主题设置
  geom_point(size=3,shape=16)+#绘制点图并设定大小
  theme(panel.grid = element_blank())+
  labs(x="株高",y="根毛数量")+#x、y轴标题
  geom_smooth(method='lm', se=FALSE, color='turquoise4')+#添加回归线
  geom_text(aes(x=55,y=124,label="R^2=0.98\ny=0.73x+60.47"),
            color="red",family = "serif",fontface = "plain",size = 5)+
  theme_prism(palette = "candy_bright",
              base_fontface = "plain", # 字体样式，可选 bold, plain, italic
              base_family = "serif", # 字体格式，可选 serif, sans, mono, Arial等
              base_size = 16,  # 图形的字体大小
              base_line_size = 0.8, # 坐标轴的粗细
              axis_text_angle = 45)+ # 可选值有 0，45，90，270
  scale_fill_prism(palette = "candy_bright")+
  theme(legend.position = 'none')#去除图例

p2
#显示剔除点
p2+geom_point(aes(x=69,y=104),shape=8,color="red",size=3)+
  geom_point(aes(x=75,y=120),shape=8,color="red",size=3)+
  geom_point(aes(x=68,y=116),shape=8,color="red",size=3)

