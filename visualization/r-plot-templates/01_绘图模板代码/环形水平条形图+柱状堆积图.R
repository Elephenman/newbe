#########微信公众号：科研后花园
######推文题目：环形水平条形图+柱状堆积图的绘制方法！！！

##清除环境并设置工作目录
rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/水平环形条形图+柱状堆积图")

##加载R包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(dplyr) # A Grammar of Data Manipulation
library(reshape2) # Flexibly Reshape Data: A Reboot of the Reshape Package
library(plyr) # Tools for Splitting, Applying and Combining Data

##加载数据（随机编写，无实际意义）
df <- read.table("data.txt", header = 1, check.names = F, sep = "\t")

###绘制环形水平条形图
##根据value1进行绘制，先将数据按照由小到大进行排序（可视化效果为数据最大柱子的在最外层）
df2 <- df[order(abs(df$value1),decreasing=F),]
##为了达到随意调节环形图内层圈的大小，需要根据排序的sample列增加一列数值型数据
df2$x <- 1:9
##绘图
df2 %>% 
  ggplot(aes(x, value1))+#这里将增加的数值列作为x轴
  #绘制条形图，并按照group进行着色
  geom_col(aes(fill = group))+
  #转换为极坐标
  coord_polar(theta = 'y')+
  #自定义x轴，通过将范围中的最小值设为负数以实现环形内部空白圈大小的目的
  scale_x_continuous(limits = c(-2,9.5))+
  #自定义y轴，通过将范围中的最大值设为大于数据中的最大值以实现环形中水平条形图是否首位相接及首位间的距离
  scale_y_continuous(limits = c(0,130))+
  #添加sample文本
  geom_text(aes(x = x, y = 0, label = sample, color = group),
            hjust = 1, size = 3.5, show.legend = F)+
  #添加各条形图的数值标注
  geom_text(aes(x = x, y = ifelse(x>4, value1+1, value1+3), 
                label = value1, color = group),
            size = 3.5, show.legend = F)+
  #将主题设置为空白,图例放置在空白处
  theme_void()+
  theme(legend.position = c(0.2,0.78),
        legend.text = element_text(size = 10),
        legend.title = element_text(size = 14, color = "red"))+
  guides(fill=guide_legend(ncol = 1, keywidth=1.5, keyheight=1.2))+
  #自定义分组颜色
  scale_fill_manual(values = c("#ec1c24","#fdbd10","#0066b2","#ed7902"))+
  scale_color_manual(values = c("#ec1c24","#fdbd10","#0066b2","#ed7902"))


###绘制环形水平柱状堆积图
##先将宽数据转换为长数据
df3 <- melt(df, id.vars = c("sample","group"), 
            measure.vars = c('value1','value2','value3',
                             'value4','value5'))
df3$group <- factor(df3$group,levels = c("groupA","groupB","groupC","groupD"))
##排序，此时需要根据原始数据计算各样本值和（根据个人需求制定排序方式），并按照值和进行排序：
df4 <- df3 %>%
  select(sample,value) %>%
  group_by(sample) %>% 
  summarise_all(sum)
df4 <- df4[order(abs(df4$value),decreasing=F),]
##为了达到随意调节环形图内层圈的大小，同样需要根据排序的sample列增加一列数值型数据
df4$x <- 1:9
##将绘图数据按照得到的排序顺序进行排序
df3$sample <- factor(df3$sample,levels = df4$sample)
##将数值型列按照sample匹配进作图数据
df3 <- left_join(df3, df4[c(1,3)], by = "sample")
##绘图
df3 %>% 
  ggplot(aes(x, value))+#这里将增加的数值列作为x轴
  #绘制柱状堆积图，并按照variable进行着色
  geom_col(aes(fill = variable))+
  #转换为极坐标
  coord_polar(theta = 'y')+
  #自定义x轴，通过将范围中的最小值设为负数以实现环形内部空白圈大小的目的
  scale_x_continuous(limits = c(-2,9.5))+
  #自定义y轴，通过将范围中的最大值设为大于数据中的样本和最大值以实现环形中水平条形图是否首位相接及首位间的距离
  scale_y_continuous(limits = c(0,500))+
  #添加sample文本
  geom_text(data = df4, aes(x = x, y = 0, label = sample),
            hjust = 1, size = 3.5, show.legend = F)+
  #将主题设置为空白,图例放置在空白处
  theme_void()+
  theme(legend.position = c(0.2,0.78),
        legend.text = element_text(size = 10),
        legend.title = element_text(size = 14, color = "red"))+
  guides(fill=guide_legend(ncol = 1, keywidth=1.3, keyheight=1))+
  #自定义分组颜色
  scale_fill_manual(values = c("#ec1c24","#fdbd10","#0066b2","#ed7902","#acc236"))

###当然，也可以绘制环形水平百分比柱状堆积图
##计算各样本中的百分比情况
df5 <- ddply(df3, 'sample', transform, percent_con = value/sum(value)*100)
##绘图
df5 %>% 
  ggplot(aes(x, percent_con))+#这里将增加的数值列作为x轴
  #绘制柱状堆积图，并按照variable进行着色
  geom_col(aes(fill = variable))+
  #转换为极坐标
  coord_polar(theta = 'y')+
  #自定义x轴，通过将范围中的最小值设为负数以实现环形内部空白圈大小的目的
  scale_x_continuous(limits = c(-2,9.5))+
  #自定义y轴，百分比柱状堆积图y轴范围为（0，100）（%），这里将范围设为大于100即可实现
  scale_y_continuous(limits = c(0,130))+
  #添加sample文本
  geom_text(data = df4, aes(x = x, y = 0, label = sample),
            hjust = 1, size = 3.5, show.legend = F)+
  #将主题设置为空白,图例放置在空白处
  theme_void()+
  theme(legend.position = c(0.2,0.78),
        legend.text = element_text(size = 10),
        legend.title = element_text(size = 14, color = "red"))+
  guides(fill=guide_legend(ncol = 1, keywidth=1.3, keyheight=1))+
  #自定义分组颜色
  scale_fill_manual(values = c("#ec1c24","#fdbd10","#0066b2","#ed7902","#acc236"))



