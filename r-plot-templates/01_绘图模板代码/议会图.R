###########parliament diagrams###################
rm(list = ls())

#安装包
# install.packages("ggparliament")
# install.packages("tidyverse")
#加载包
library(ggparliament)
library(tidyverse)

#数据
df<-election_data %>% 
  filter(country == "Russia" & year == 2016)
#将数据转换成绘图所需格式,可以在type中修改类型
df1 <- parliament_data(election_data = df,
                                 type = "semicircle", # 议会类型
                                 parl_rows = 10,      # 议会的行数
                                 party_seats = df$seats) # 席位
df2 <- parliament_data(election_data = df,
                       type = "circle", # 议会类型
                       parl_rows = 10,      # 议会的行数
                       party_seats = df$seats) # 席位
df3 <- parliament_data(election_data = df,
                       type = "classroom", # 议会类型
                       parl_rows = 11,      # 议会的行数
                       party_seats = df$seats) # 席位
df4 <- parliament_data(election_data = df,
                       type = "horseshoe", # 议会类型
                       parl_rows = 10,      # 议会的行数
                       party_seats = df$seats) # 席位
#绘图
ggplot(df1, aes(x = x, y = y, colour = party_short)) +
  geom_parliament_seats() + 
  geom_highlight_government(government == 1) +
  geom_parliament_bar(colour = colour, party = party_long, label = TRUE) +#使用条形图显示比例
  draw_majoritythreshold(n = 225, label = TRUE, type = "semicircle") +#添加阈值线
  theme_ggparliament() +
  labs(title = "R") +#标题
  scale_colour_manual(values = df1$colour, 
                      limits = df1$party_short) +#颜色
  draw_partylabels(type = "semicircle",   ##标签
                   party_names = party_long,
                   party_seats = seats,
                   party_colours = colour)+
  draw_totalseats(n = 450, type = "semicircle")#标签

#其他类型
ggplot(df2, aes(x = x, y = y, color = party_short)) +
  geom_parliament_seats() + 
  theme_ggparliament() +
  labs(title = "Russia, 2016") +
  scale_colour_manual(values = df1$colour, 
                      limits = df1$party_short)
ggplot(df3, aes(x = x, y = y, color = party_short)) +
  geom_parliament_seats() + 
  theme_ggparliament() +
  labs(title = "Russia, 2016") +
  scale_colour_manual(values = df1$colour, 
                      limits = df1$party_short)
ggplot(df4, aes(x = x, y = y, color = party_short)) +
  geom_parliament_seats() + 
  theme_ggparliament() +
  labs(title = "Russia, 2016") +
  scale_colour_manual(values = df1$colour, 
                      limits = df1$party_short)

#参考：https://r-charts.com/part-whole/ggparliament/