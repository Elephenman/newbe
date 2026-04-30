#!/usr/bin/env Rscript
# 单细胞差异丰度分析(比较组间细胞比例变化)

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat("============================================================\n")
cat("  单细胞差异丰度分析\n")
cat("============================================================\n\n")

rds_file <- get_input("Seurat对象RDS路径", "seurat_obj.rds")
group_col <- get_input("分组列名", "condition")
celltype_col <- get_input("细胞类型列名", "cell_type")
output_file <- get_input("输出CSV路径", "diff_abundance.csv")
test_method <- get_input("统计检验(chisq/fisher/prop)", "chisq")

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
library(Seurat)
library(dplyr)

if (!file.exists(rds_file)) { cat("[ERROR] RDS文件不存在\n"); quit(status=1) }

obj <- readRDS(rds_file)
meta <- obj@meta.data

# Validate columns
if (!(group_col %in% colnames(meta))) {
  cat("[ERROR] 分组列不存在:", group_col, "\n"); quit(status=1)
}
if (!(celltype_col %in% colnames(meta))) {
  cat("[ERROR] 细胞类型列不存在:", celltype_col, "\n"); quit(status=1)
}

cat("[Processing] 计算差异丰度...\n")

# Count cells per group per cell type
counts <- meta %>% group_by(.data[[group_col]], .data[[celltype_col]]) %>% tally()
totals <- meta %>% group_by(.data[[group_col]]) %>% summarise(total=n())
props <- counts %>% left_join(totals, by=group_col) %>% mutate(proportion=n/total)

# Statistical tests for each cell type
celltypes <- unique(meta[[celltype_col]])
groups <- unique(meta[[group_col]])

test_results <- data.frame()
if (length(groups) == 2) {
  for (ct in celltypes) {
    g1_cells <- meta[meta[[group_col]] == groups[1] & meta[[celltype_col]] == ct, ]
    g2_cells <- meta[meta[[group_col]] == groups[2] & meta[[celltype_col]] == ct, ]
    g1_total <- nrow(meta[meta[[group_col]] == groups[1], ])
    g2_total <- nrow(meta[meta[[group_col]] == groups[2], ])

    mat <- matrix(c(nrow(g1_cells), g1_total - nrow(g1_cells),
                    nrow(g2_cells), g2_total - nrow(g2_cells)),
                  nrow=2, byrow=TRUE)

    tryCatch({
      if (test_method == "fisher") {
        test <- fisher.test(mat)
      } else if (test_method == "prop") {
        test <- prop.test(mat)
      } else {
        test <- chisq.test(mat)
      }
      test_results <- rbind(test_results, data.frame(
        CellType=ct,
        Group1=groups[1], Group1_n=nrow(g1_cells), Group1_total=g1_total,
        Group1_prop=round(nrow(g1_cells)/g1_total, 4),
        Group2=groups[2], Group2_n=nrow(g2_cells), Group2_total=g2_total,
        Group2_prop=round(nrow(g2_cells)/g2_total, 4),
        P_value=test$p.value,
        Method=test_method
      ))
    }, error=function(e) {
      cat("  [WARN]", ct, "test failed\n")
    })
  }
}

# Adjust p-values
if (nrow(test_results) > 0) {
  test_results$P_adj <- p.adjust(test_results$P_value, method="BH")
  test_results <- test_results[order(test_results$P_adj), ]
}

# Save
write.csv(props, gsub("\\.csv$", "_proportions.csv", output_file), row.names=FALSE)
if (nrow(test_results) > 0) {
  write.csv(test_results, output_file, row.names=FALSE)
}

cat("\n============================================================\n")
cat("  RESULTS SUMMARY\n")
cat("============================================================\n")
cat("  Cell types:", length(celltypes), "\n")
cat("  Groups:    ", paste(groups, collapse=", "), "\n")
if (nrow(test_results) > 0) {
  sig <- sum(test_results$P_adj < 0.05, na.rm=TRUE)
  cat("  Significant (FDR<0.05):", sig, "\n")
}
cat("  Output:    ", output_file, "\n")
cat("============================================================\n\n")
cat("[Done] Differential abundance analysis completed!\n")
