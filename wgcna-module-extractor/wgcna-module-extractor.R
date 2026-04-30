#!/usr/bin/env Rscript
# WGCNA共表达网络模块识别与可视化

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat("============================================================\n")
cat("  WGCNA共表达网络模块识别\n")
cat("============================================================\n\n")

expr_file <- get_input("表达矩阵CSV(行=基因,列=样本)", "expression.csv")
soft_power <- get_input("软阈值幂次(0=自动)", "0")
min_module_size <- as.integer(get_input("最小模块大小", "30"))
output_dir <- get_input("输出目录", "wgcna_results")

if (!requireNamespace("WGCNA", quietly=TRUE)) { cat("需要WGCNA\n"); quit(status=1) }
library(WGCNA)
options(stringsAsFactors=FALSE)

if (!file.exists(expr_file)) { cat("[ERROR] 表达矩阵不存在\n"); quit(status=1) }

dir.create(output_dir, showWarnings=FALSE, recursive=TRUE)

cat("[Processing] 读取表达矩阵...\n")
dat <- as.data.frame(t(read.csv(expr_file, row.names=1)))
cat("  样本:", nrow(dat), "基因:", ncol(dat), "\n")

# Good samples/genes check
gsg <- goodSamplesGenes(dat, verbose=0)
if (!gsg$allOK) {
  dat <- dat[gsg$goodSamples, gsg$goodGenes]
  cat("  移除低质量样本/基因\n")
}

# Soft threshold selection
pv <- as.numeric(soft_power)
if (pv == 0) {
  cat("[Processing] 自动选择软阈值...\n")
  sft <- pickSoftThreshold(dat, verbose=0)
  pv <- ifelse(is.na(sft$powerEstimate), 6, sft$powerEstimate)
  cat("  选择软阈值:", pv, "\n")
}

# Build network
cat("[Processing] 构建共表达网络...\n")
adj <- adjacency(dat, power=pv)
TOM <- TOMsimilarity(adj)
dissTOM <- 1 - TOM

# Hierarchical clustering
gtree <- hclust(as.dist(dissTOM), method="average")

# Module detection
mods <- cutreeDynamic(dendro=gtree, deepSplit=2, pamRespectsDendro=FALSE,
                      minClusterSize=min_module_size)
mcols <- labels2colors(mods)

n_modules <- length(unique(mcols))
cat("[Processing] 检测到", n_modules, "个模块\n")

# Save results
write.csv(data.frame(Gene=colnames(dat), Module=mcols),
          file.path(output_dir, "module_assignments.csv"), row.names=FALSE)

# Plot dendrogram
pdf(file.path(output_dir, "dendrogram.pdf"), width=12, height=6)
plotDendroAndColors(gtree, mcols, "Module",
                    dendroLabels=FALSE, hang=0.03,
                    addGuide=TRUE, guideHang=0.05)
dev.off()

# Module eigengenes
MEs <- moduleEigengenes(dat, colors=mcols)$eigengenes
write.csv(MEs, file.path(output_dir, "module_eigengenes.csv"))

# Module-trait correlations (if trait data available)
cat("\n============================================================\n")
cat("  RESULTS SUMMARY\n")
cat("============================================================\n")
cat("  Samples:     ", nrow(dat), "\n")
cat("  Genes:       ", ncol(dat), "\n")
cat("  Soft power:  ", pv, "\n")
cat("  Modules:     ", n_modules, "\n")
cat("  Output dir:  ", output_dir, "\n")
cat("============================================================\n\n")
cat("[Done] WGCNA模块识别完成!\n")
