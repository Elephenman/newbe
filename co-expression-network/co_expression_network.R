#!/usr/bin/env Rscript
# WGCNA简化版一键网络构建
suppressPackageStartupMessages({
  if (!require(WGCNA)) { cat("需要WGCNA\n"); quit(status=1) }
  library(ggplot2)
})

get_input <- function(prompt, default = NULL) {
  val <- readline(prompt = paste0(prompt, " [默认: ", default, "]: "))
  if (val == "" || is.null(val)) return(default); return(val)
}

cat("============================================================\n")
cat("  🕸️ WGCNA简化版\n")
cat("============================================================\n\n")

mat_path <- get_input("表达矩阵CSV路径(行=基因,列=样本)", "expression.csv")
min_mod_size <- as.integer(get_input("最小模块大小", "30"))
soft_power_range <- get_input("软阈值范围(如1-20)", "1-20")
traits_file <- get_input("性状数据文件(留空=无)", "")

mat <- as.matrix(read.csv(mat_path, row.names = 1))
mat[is.na(mat)] <- 0

# 选择软阈值
powers <- c(as.integer(strsplit(soft_power_range, "-")[[1]][1]):as.integer(strsplit(soft_power_range, "-")[[1]][2]))
sft <- pickSoftThreshold(mat, powerVector = powers, verbose = 0)
best_power <- sft$powerEstimate
if (best_power == 0) best_power <- 6
cat("选择软阈值:", best_power, "\n")

# 构建网络
net <- blockwiseModules(mat, power = best_power, minModuleSize = min_mod_size,
                         verbose = 0, saveTomFiles = "none")

# 模块颜色
colors <- net$colors
cat("模块数:", length(unique(colors)), "\n")
for (c in unique(colors)) cat("  ", c, ": ", sum(colors == c), " genes\n")

# 保存结果
out_path <- paste0(tools::file_path_syn_ext(mat_path), "_wgcna_modules.csv")
module_df <- data.frame(gene = rownames(mat), module = colors)
write.csv(module_df, out_path, row.names = FALSE)
cat("✅ 模块结果:", out_path, "\n")