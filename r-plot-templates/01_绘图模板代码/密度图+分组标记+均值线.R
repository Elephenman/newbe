rm(list=ls())#clear Global Environment
setwd('D:/桌面/SCI论文写作与绘图/R语言绘图/基础图形绘制/密度图+分组标记+均值线')#Set working path

##加载R包
#remotes::install_github("AllanCameron/geomtextpath")
library(geomtextpath) # Curved Text in 'ggplot2'
library(tidyverse) # Easily Install and Load the 'Tidyverse'
library(ggplot2) # Create Elegant Data Visualisations Using the Grammar of Graphics
library(palmerpenguins) # Palmer Archipelago (Antarctica) Penguin Data
library(ggridges) # Ridgeline Plots in 'ggplot2'

##加载数据（以palmerpenguins包中的penguins数据集为例）
df <- read.table("data.txt", sep="\t", header=T, check.names=F)
# data(penguins)

##去除数据中的NA值
df <- df %>%
  drop_na()

###绘图
#绘制常规密度图-无填充
p1 <- df %>% 
  ggplot(aes(x = body_mass_g, color = species)) +
  #绘制密度图
  geom_density(linewidth=1.5)+
  #主题设置
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(size = 10),
        axis.title = element_text(size = 14))+
  #颜色设置
  scale_color_manual(values = c("#0099e5","#ff4c4c","#34bf49"))
p1

#绘制密度图+均值线-无填充
p2 <- df %>% 
  ggplot(aes(x = body_mass_g, color = species)) +
  geom_density(linewidth=1.5)+
  #添加均值线
  geom_vline(xintercept = mean(df[df$species=="Adelie",]$body_mass_g), 
             color = "#0099e5", linetype = "dashed",linewidth=0.6) +
  geom_vline(xintercept = mean(df[df$species=="Chinstrap",]$body_mass_g), 
             color = "#ff4c4c", linetype = "dashed",linewidth=0.6)+
  geom_vline(xintercept = mean(df[df$species=="Gentoo",]$body_mass_g), 
             color = "#34bf49", linetype = "dashed",linewidth=0.6)+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(size = 10),
        axis.title = element_text(size = 14))+
  scale_color_manual(values = c("#0099e5","#ff4c4c","#34bf49"))
p2

#绘制密度图+均值线+分组标记（直接在线上标记）-无填充
p3 <- df %>% 
  ggplot(aes(x = body_mass_g, color = species)) +
  #利用geom_textdensity函数绘制带标签的密度图
  geom_textdensity(aes(label = species),#标签
                   fontface = 3, #字体
                   linewidth=1.5,
                   hjust = 0.5, vjust = 0.5)+#位置
  geom_vline(xintercept = mean(df[df$species=="Adelie",]$body_mass_g), 
             color = "#0099e5", linetype = "dashed",linewidth=0.6) +
  geom_vline(xintercept = mean(df[df$species=="Chinstrap",]$body_mass_g), 
             color = "#ff4c4c", linetype = "dashed",linewidth=0.6)+
  geom_vline(xintercept = mean(df[df$species=="Gentoo",]$body_mass_g), 
             color = "#34bf49", linetype = "dashed",linewidth=0.6)+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(size = 10),
        axis.title = element_text(size = 14),
        legend.position = "none")+
  scale_color_manual(values = c("#0099e5","#ff4c4c","#34bf49"))
p3

#绘制密度图+均值线+分组标记（直接在线上标记）-有填充
p4 <- df %>% 
  ggplot(aes(x = body_mass_g, fill = species, color = species)) +
  #绘制带填充的密度图，设置线为0以去除线条
  geom_density(linewidth=0,alpha = 0.6)+
  #只需要标签，故设置线条粗细为0
  geom_textdensity(aes(label = species),
                   fontface = 3, linewidth=0,
                   hjust = 0.5, vjust = -0.5)+
  scale_y_continuous(expand = c(0,0))+
  geom_vline(xintercept = mean(df[df$species=="Adelie",]$body_mass_g), 
             color = "#0099e5", linetype = "dashed",linewidth=0.6) +
  geom_vline(xintercept = mean(df[df$species=="Chinstrap",]$body_mass_g), 
             color = "#ff4c4c", linetype = "dashed",linewidth=0.6)+
  geom_vline(xintercept = mean(df[df$species=="Gentoo",]$body_mass_g), 
             color = "#34bf49", linetype = "dashed",linewidth=0.6)+
  theme_bw()+
  theme(panel.grid = element_blank(),
        axis.text = element_text(size = 10),
        axis.title = element_text(size = 14),
        legend.position = "none")+
  scale_fill_manual(values = c("#0099e5","#ff4c4c","#34bf49"))+
  scale_color_manual(values = c("#0099e5","#ff4c4c","#34bf49"))
p4

###拼图
library(patchwork)
(p1+p3)/(p2+p4)
