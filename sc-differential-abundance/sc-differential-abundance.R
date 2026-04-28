# 单细胞差异丰度分析(比较组间细胞比例变化)

  rds_file <- ifelse(interactive(), readline("Seurat对象RDS路径 [seurat_obj.rds]: "), "seurat_obj.rds")
  group_col <- ifelse(interactive(), readline("分组列名 [condition]: "), "condition")
  celltype_col <- ifelse(interactive(), readline("细胞类型列名 [cell_type]: "), "cell_type")
  output_file <- ifelse(interactive(), readline("输出CSV路径 [diff_abundance.csv]: "), "diff_abundance.csv")
  library(Seurat); library(dplyr)
  obj <- readRDS(rds_file)
  meta <- obj@meta.data
  counts <- meta %>% group_by(.data[[group_col]], .data[[celltype_col]]) %>% tally()
  totals <- meta %>% group_by(.data[[group_col]]) %>% summarise(total=n())
  props <- counts %>% left_join(totals, by=group_col) %>% mutate(proportion=n/total)
  write.csv(props, output_file, row.names=FALSE)
  cat("差异丰度完成:", output_file, "\n")

