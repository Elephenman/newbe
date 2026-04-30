##清空环境变量并设置工作目录
rm(list = ls())
setwd("D:/桌面/SCI论文写作与绘图/R语言绘图/数据分析及可视化/多序列比对及可视化")

####基于ggmsa包进行多序列比对及可视化
##安装包
# if (!require("BiocManager"))
#   install.packages("BiocManager")
# BiocManager::install("ggmsa")
##加载包
library(ggmsa)
library(ggplot2)
##数据-包括蛋白和核酸两种类型数据
protein_sequences <- system.file("extdata", "sample.fasta", 
                                 package = "ggmsa")
miRNA_sequences <- system.file("extdata", "seedSample.fa", 
                               package = "ggmsa")
nt_sequences <- system.file("extdata", "LeaderRepeat_All.fa", 
                            package = "ggmsa")

##可视化
ggmsa(protein_sequences, 320, 350, color = "Clustal", 
      font = "DroidSansMono", char_width = 0.5, seq_name = TRUE )
ggmsa(miRNA_sequences, color = "Chemistry_AA", 
      font = "DroidSansMono", char_width = 0.5, seq_name = TRUE )
ggmsa(nt_sequences, color = "Chemistry_AA", 
      font = "DroidSansMono", char_width = 0.5, seq_name = TRUE )

###基础参数
##颜色
available_colors()
#> 1.color schemes for nucleotide sequences currently available:
#> Chemistry_NT Shapely_NT Taylor_NT Zappo_NT
#> 2.color schemes for AA sequences currently available:
#> ClustalChemistry_AA Shapely_AA Zappo_AA Taylor_AA LETTER CN6 Hydrophobicity
#Clustal
ggmsa(protein_sequences, start = 320, end = 360, color = "Clustal", show.legend = TRUE)
#Color by Chemistry(Default)
ggmsa(protein_sequences, start = 330, end = 360, color = "Chemistry_AA", show.legend = TRUE)
#Color by Shapely
ggmsa(protein_sequences, start = 330, end = 360, color = "Shapely_AA", show.legend = TRUE)
#Color by Taylor
ggmsa(protein_sequences, start = 330, end = 360, color = "Taylor_AA", show.legend = TRUE)
#Color by Zappo
ggmsa(protein_sequences, start = 330, end = 360, color = "Zappo_AA", show.legend = TRUE)
#Color by LETTER
ggmsa(protein_sequences, start = 330, end = 360, color = "LETTER", show.legend = TRUE)

#Color Customzation
library(RColorBrewer)
library(pals)
my_pal <- colorRampPalette(rev(brewer.pal(n = 9, name = "Reds")))
my_cutstom <- data.frame(names = c(LETTERS[1:26],"-"), 
                         color = my_pal(27), 
                         stringsAsFactors = FALSE)
head(my_cutstom)
#>   names   color
#> 1     A #67000D
#> 2     B #7A040F
#> 3     C #8D0911
#> 4     D #A00D14
#> 5     E #AD1116
#> 6     F #B91319
pals::pal.bands(my_cutstom$color)
ggmsa(protein_sequences, 300, 345, 
      custom_color = my_cutstom, 
      char_width = 0.5, 
      border = "white",
      show.legend = TRUE)


##字体
available_fonts()
#> font families currently available:
#> helvetical mono TimesNewRoman DroidSansMono
ggmsa(protein_sequences, start = 340, end = 360, font = "helvetical")
ggmsa(protein_sequences, start = 340, end = 360, font = "TimesNewRoman")
ggmsa(protein_sequences, start = 340, end = 360, font = "DroidSansMono")
ggmsa(protein_sequences, start = 340, end = 360, font = NULL)


####与ggplot2类似，该包支持MSA注释
##geom_seqlogo
ggmsa(protein_sequences, 320, 350, char_width = 0.5, seq_name = TRUE) + 
  geom_seqlogo(color = "Chemistry_AA")

##geom_GC—使用气泡图显示GC含量
ggmsa(nt_sequences, font = NULL,color = "Chemistry_NT") + 
  geom_seqlogo(color = "Chemistry_NT") + geom_GC() + 
  theme(legend.position = "none")

##geom_seed-突出 miRNA 序列上的 seed 区
#有背景
ggmsa(miRNA_sequences, char_width = 0.5, color = "Chemistry_NT") + 
  geom_seed(seed = "GAGGUAG", star = TRUE)
#去除背景
ggmsa(miRNA_sequences, char_width = 0.5, seq_name = TRUE, none_bg = TRUE) + 
  geom_seed(seed = "GAGGUAG")

##geom_msaBar-用条形图显示序列保守性
ggmsa(protein_sequences, 320, 350, char_width = 0.5, seq_name = TRUE) + 
  geom_msaBar()

##geom_helix-用圆弧图表示RNA二级结构
RF03120 <- system.file("extdata/Rfam/RF03120_SS.txt", package="ggmsa")
RF03120_fas <- system.file("extdata/Rfam/RF03120.fasta", package="ggmsa")
SS <- readSSfile(RF03120, type = "Vienna")
ggmsa(RF03120_fas, font = NULL,border = NA, color = "Chemistry_NT", seq_name = FALSE) +
  geom_helix(SS)


###主题修改
##char_width: 字符宽度，默认 0.9
ggmsa(protein_sequences, start = 320, end = 360, char_width = 0.5)

##none_bg = TRUE: 仅显示字符，去除有色背景
ggmsa(protein_sequences, start = 320, end = 360, none_bg = TRUE) + 
  theme_void()

##seq_name = TRUE: 显示序列名称
ggmsa(protein_sequences, 164, 213, seq_name = TRUE)

##show.legend = TRUE: 显示多序列比对图的图例
ggmsa(protein_sequences, 190, 213, font = NULL, show.legend = TRUE)

##border = NA: 去除描边；border = "white": 白色描边
ggmsa(protein_sequences, 164, 213, font = NULL, border = NA)
ggmsa(protein_sequences, 164, 213, font = NULL, border = "white")

##position_highlight: 特定位置高亮
ggmsa(protein_sequences, 164, 213, position_highlight = c(190, 195), char_width = 0.5)

####其他模块
##Sequence logo
seqlogo(protein_sequences, start = 330, end = 350, color = "Chemistry_AA", font = "DroidSansMono")
seqlogo(nt_sequences, start = 1, end = 20, color = "Chemistry_NT", font = "DroidSansMono")

##Sequence Bundles
negative <-  system.file("extdata", "Gram-negative_AKL.fasta", package = "ggmsa")
positive <-  system.file("extdata", "Gram-positive_AKL.fasta", package = "ggmsa")
ggSeqBundle(negative, bundle_color = "red")
ggSeqBundle(msa = c(negative,positive))

##RNA二级结构
transat_file <- system.file("extdata", "helix.txt", package = "R4RNA")
known_file <- system.file("extdata", "vienna.txt", package = "R4RNA")
connect_file <- system.file("extdata", "connect.txt", package = "R4RNA")
known <- readSSfile(known_file, type = "Vienna")
transat <- readSSfile(transat_file, type = "Helix")
connect <- readSSfile(connect_file , type = "Connect")
gghelix(known)
gghelix(list(known = known, predicted = transat), overlap = FALSE)
gghelix(list(known = known, predicted = transat), color_by = "value", overlap = TRUE)
gghelix(list(known = known, predicted = connect), overlap = TRUE)


###查看模式
##四个参数：
# use_dot: 在图中将匹配的字符显示为点
# disagreement: 是否高亮显示不匹配的字符,默认为TRUE
# ignore_gaps: 选择TRUE 时，列中的间隙将被视为该行不存在。
# ref: 指定参考序列（输入参考序列名称即可，必须在输入数据内）

ggmsa(protein_sequences, 330, 350, char_width = 0.5, 
      seq_name = T, consensus_views = T, 
      disagreement = T, use_dot = T)
ggmsa(protein_sequences, 330, 350, char_width = 0.5, 
      seq_name = T, consensus_views = T, 
      disagreement = F, use_dot = F)
ggmsa(protein_sequences, 330, 350, char_width = 0.5, 
      seq_name = T, consensus_views = T, 
      disagreement = F, use_dot = F,
      ignore_gaps = T)
ggmsa(protein_sequences, 330, 350, char_width = 0.5, 
      seq_name = T, consensus_views = T ,
      use_dot = T, ref = "PH4H_Rhizobium_loti")

##根据序列保守性进行着色
ggmsa(protein_sequences, 320, 350, color = "Chemistry_AA", 
      # font = NULL, 
      seq_name = T ,border = "white", by_conservation = TRUE)

######实例操作
##将ggmsa的示例数据下载到本地进行读取
# install.packages ("Biostrings")
library(Biostrings)
fa <- readAAStringSet('sample.fasta')
#个性化绘图模板
ggmsa(fa, #数据文件
      start = 330, end = 360, #显示的位置
      font = "TimesNewRoman",#字体
      color = "Chemistry_AA",#颜色
      char_width = 0.6, #字符宽度
      border = "white",#描边颜色
      show.legend = F
      )+
  #sequenc logo注释
  geom_seqlogo(color = "Chemistry_AA",#配色
               font = "TimesNewRoman",
               adaptive = F)+
  #条形图
  geom_msaBar()


###参考：
# 1）https://yulab-smu.top/ggmsa/articles/ggmsa.html