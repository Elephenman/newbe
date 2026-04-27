rm(list=ls())#clear Global Environment
#加载包
library(ggplot2)
library(reshape2)

# 创建示例数据
df <- data.frame(
  group = c("A", "B", "C","D","F"),
  value1 = c(10, 20, 30, 20, 15),
  value2 = c(15, 25, 35, 15, 20)
)
df1 <- melt(df)
#添加误差数据
df1$sd <- c(1,2,3,2.5,1,1,2,3,2,1.5)
#误差线位置
df1 <- df1 %>% 
  group_by(group) %>% 
  mutate(xx=cumsum(value))
df1$variable <- factor(df1$variable,levels = c("value2","value1"))#保证误差线可以对应其正确位置
# 绘制堆积柱状图
ggplot(df1, aes( x = group,y=value,fill = variable))+
  geom_col(position = 'stack', width = 0.6)+
  geom_errorbar(aes(ymin=xx-sd,ymax=xx+sd),
                width=0.1,linewidth=0.8)+
  scale_y_continuous(expand = c(0,0),limits = c(0,70))+
  labs(x=NULL,y=NULL)+
  theme_bw()+
  theme(panel.grid = element_blank(),
        legend.position = c(0.92,0.88),
        legend.background = element_blank())+
  scale_fill_manual(values = c("#0099cc","#ff9933"))
