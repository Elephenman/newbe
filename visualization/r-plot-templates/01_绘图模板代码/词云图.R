rm(list = ls())
#安装R包
# install.packages("wordcloud2")
#加载R包
library(wordcloud2)

#数据——以示例数据为例
df1<-demoFreq
df2<-demoFreqC
#基础绘图
wordcloud2(df2, #数据
           size=1.5,#字体大小
           fontFamily = 'Segoe UI',#字体
           fontWeight = 'bold',#字体粗细
           color='random-light',#字体颜色设置
           backgroundColor="black"#背景颜色设置
           )
#改变词云方向
wordcloud2(df1, size = 2, minRotation = -pi/6, maxRotation = -pi/6,#文本旋转角度范围
           rotateRatio = 0.5)#文本选择概率

#####更改形状
##常规形状——'star'、'circle'、'cardioid'、'diamond'、'triangle-forward'、'triangle'、'pentagon'
wordcloud2(df1,size=1.5,color='random-light',backgroundColor="black",
           shape = 'star')#改变形状
wordcloud2(df1,size=1.5,color='random-light',backgroundColor="black",
           shape = 'circle')#改变形状
wordcloud2(df1,size=1.5,color='random-light',backgroundColor="black",
           shape = 'cardioid')#改变形状
wordcloud2(df1,size=1.5,color='random-light',backgroundColor="black",
           shape = 'diamond')#改变形状
wordcloud2(df1,size=1.5,color='random-light',backgroundColor="black",
           shape = 'triangle-forward')#改变形状
wordcloud2(df1,size=1.5,color='random-light',backgroundColor="black",
           shape = 'triangle')#改变形状
wordcloud2(df1,size=1.5,color='random-light',backgroundColor="black",
           shape = 'pentagon')#改变形状
###新版本wordcloud2包已经不支持自定义形状，大家如果需要可根据这个博主的推文进行操作：https://blog.csdn.net/tandelin/article/details/103977242


#参考：https://r-graph-gallery.com/196-the-wordcloud2-library.html