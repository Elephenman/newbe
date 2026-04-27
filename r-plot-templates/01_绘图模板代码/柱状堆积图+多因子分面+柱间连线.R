rm(list=ls())#clear Global Environment
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/柱状堆积图+多因子分面+柱间连线")

##加载包
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(reshape) # Flexibly Reshape Data
library(ggalluvial) # Alluvial Plots in 'ggplot2'
library(dplyr) # A Grammar of Data Manipulation
# remotes::install_github("teunbrand/ggh4x")
library(ggh4x) # Hacks for 'ggplot2'

##加载数据
df <- read.table("data.txt", check.names = F, header = 1, sep = "\t",row.names = 1)

##计算相对丰度
df2 <- as.data.frame(t(apply(t(df[5:9]),2,function(x) x/sum(x))))
df2$sample <- rownames(df2)
#合并数据
df3 <- df[1:4]
df3$sample <- rownames(df3)
data <- merge(df3, df2, by = "sample")

##变量格式转换,宽数据转化为长数据
data1 <- melt(data,
            id.vars = c("sample","group1","group2","group3","time"), 
            measure.vars = c('SpeciesA','SpeciesB','SpeciesC',
                             'SpeciesD','SpeciesE'))
names(data1)[6] <- 'Species'  #修改列名
data1$time <- factor(data1$time, levels = df$time[1:6])

#####按照分组time绘制未分面柱状堆积图
##计算分组time的均值
df_time <- data1 %>%
  select(time,Species,value) %>%
  group_by(time,Species) %>% 
  summarise_all(mean)# 求均值
##绘图
ggplot(df_time, aes(time, y = value*100,
                    fill = Species,
                    stratum = Species, alluvium = Species))+
  #柱状堆积图+柱间连线
  geom_stratum(width = 0.6, color='white')+
  geom_alluvium(alpha = 0.4,#透明度
                width = 0.6,#宽度
                color='white',#间隔颜色
                linewidth = 1,#间隔宽度
                curve_type = "linear")+
  ##主题相关设置
  scale_y_continuous(expand = c(0,0))+
  labs(y="Relative Abundance(%)")+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.y = element_text(size=10),
        axis.text.x = element_text(size=10, angle = 45, vjust = 1, hjust = 1),
        axis.title = element_text(size=12))+
  guides(fill=guide_legend(keywidth = 1.2, keyheight = 1.2)) +
  #颜色设置
  scale_fill_manual(values = c("#fc636b","#3be8b0","#1aafd0",
                               "#6a67ce","#ffb900"))

#####绘制按照分组time并按照group1进行分面柱状堆积图
df_time_group1 <- data1 %>%
  select(group1,time,Species,value) %>%
  group_by(group1,time,Species) %>% 
  summarise_all(mean)# 求均值
##绘图
ggplot(df_time_group1, aes(time, y = value*100,
                    fill = Species,
                    stratum = Species, alluvium = Species))+
  geom_stratum(width = 0.6, color='white')+
  geom_alluvium(alpha = 0.4,
                width = 0.6,
                color='white',
                linewidth = 1,
                curve_type = "linear")+
  scale_y_continuous(expand = c(0,0))+
  #分面
  facet_grid(~group1)+
  labs(y="Relative Abundance(%)")+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.y = element_text(size=10),
        axis.text.x = element_text(size=10, angle = 45, vjust = 1, hjust = 1),
        axis.title = element_text(size=12),
        strip.text = element_text(color = "black", size = 12),
        strip.background = element_rect(color = "black", fill="grey90"))+
  guides(fill=guide_legend(keywidth = 1.2, keyheight = 1.2)) +
  scale_fill_manual(values = c("#fc636b","#3be8b0","#1aafd0",
                               "#6a67ce","#ffb900"))

#####绘制按照分组time并按照group1+group2进行分面柱状堆积图
df_time_group12 <- data1 %>%
  select(group1,group2,time,Species,value) %>%
  group_by(group1,group2,time,Species) %>% 
  summarise_all(mean)# 求均值
##绘图
ggplot(df_time_group12, aes(time, y = value*100,
                           fill = Species,
                           stratum = Species, alluvium = Species))+
  geom_stratum(width = 0.6, color='white')+
  geom_alluvium(alpha = 0.4,
                width = 0.6,
                color='white',
                linewidth = 1,
                curve_type = "linear")+
  scale_y_continuous(expand = c(0,0))+
  #分面（facet_nested函数可以解决多因子分面过程中分面标签的不同框问题）
  facet_nested(~group1+group2,scales = "free",space = "free")+
  labs(y="Relative Abundance(%)")+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.y = element_text(size=10),
        axis.text.x = element_text(size=10, angle = 45, vjust = 1, hjust = 1),
        axis.title = element_text(size=12),
        strip.text = element_text(color = "black", size = 12),
        strip.background = element_rect(color = "black", fill="grey90"))+
  guides(fill=guide_legend(keywidth = 1.2, keyheight = 1.2)) +
  scale_fill_manual(values = c("#fc636b","#3be8b0","#1aafd0",
                               "#6a67ce","#ffb900"))


#####绘制按照分组time并按照group1+group2+group3进行分面柱状堆积图
df_time_group123 <- data1 %>%
  select(group1,group2,group3,time,Species,value) %>%
  group_by(group1,group2,group3,time,Species) %>% 
  summarise_all(mean)# 求均值
##绘图
ggplot(df_time_group123, aes(time, y = value*100,
                            fill = Species,
                            stratum = Species, alluvium = Species))+
  geom_stratum(width = 0.6, color='white')+
  geom_alluvium(alpha = 0.4,
                width = 0.6,
                color='white',
                linewidth = 1,
                curve_type = "linear")+
  scale_y_continuous(expand = c(0,0))+
  #分面
  facet_nested(~group1+group2+group3,scales = "free",space = "free")+
  labs(y="Relative Abundance(%)")+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text.y = element_text(size=9),
        axis.text.x = element_text(size=9, angle = 45, vjust = 1, hjust = 1),
        axis.title = element_text(size=12),
        strip.text = element_text(color = "black", size = 10),
        strip.background = element_rect(color = "black", fill="grey90"),
        panel.spacing = unit(0.1, "cm"))+
  guides(fill=guide_legend(keywidth = 1.2, keyheight = 1.2)) +
  scale_fill_manual(values = c("#fc636b","#3be8b0","#1aafd0",
                               "#6a67ce","#ffb900"))
