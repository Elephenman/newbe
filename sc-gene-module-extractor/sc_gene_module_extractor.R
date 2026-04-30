# 单细胞基因模块提取+活性评分
# 基于共表达或预定义基因集，计算单细胞模块评分

cat("=", rep("-", 59), "\n", sep="")
cat("  单细胞基因模块提取+活性评分\n")
cat("=", rep("-", 59), "\n", sep="")
cat("\n")

get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

rds_file     <- get_input("Seurat对象RDS路径", "seurat.rds")
module_file  <- get_input("基因模块文件(CSV: module_name,gene1;gene2;...)", "modules.csv")
output_rds   <- get_input("输出RDS路径", "seurat_scored.rds")
method       <- get_input("评分方法(AddModuleScore/UCell)", "AddModuleScore")

cat("\nRDS:     ", rds_file, "\n")
cat("Modules: ", module_file, "\n")
cat("Output:  ", output_rds, "\n")
cat("Method:  ", method, "\n\n")

if (!requireNamespace("Seurat", quietly=TRUE)) { cat("需要Seurat\n"); quit(status=1) }
library(Seurat)

if (!file.exists(rds_file)) { cat("[ERROR] RDS文件不存在\n"); quit(status=1) }
if (!file.exists(module_file)) { cat("[ERROR] 模块文件不存在\n"); quit(status=1) }

obj <- readRDS(rds_file)

# Parse module file
module_df <- read.csv(module_file, stringsAsFactors=FALSE, header=FALSE)
colnames(module_df) <- c("module", "genes")

module_list <- list()
for (i in 1:nrow(module_df)) {
  mod_name <- module_df$module[i]
  gene_str <- module_df$genes[i]
  genes <- unique(strsplit(gene_str, "[;|,]")[[1]])
  genes <- genes[genes != "" & !is.na(genes)]
  module_list[[mod_name]] <- genes
  cat("  Module:", mod_name, "-", length(genes), "genes\n")
}

# Calculate module scores
cat("[Processing] 计算模块评分...\n")

if (method == "UCell" && requireNamespace("UCell", quietly=TRUE)) {
  obj <- UCell::ScoreSignatures_UCell(obj, features=module_list)
} else {
  # Default: AddModuleScore
  for (mod_name in names(module_list)) {
    genes <- module_list[[mod_name]]
    # Filter to genes present in the object
    genes_present <- genes[genes %in% rownames(obj)]
    if (length(genes_present) < 3) {
      cat("  [WARN]", mod_name, "only", length(genes_present), "genes found, skipping\n")
      next
    }
    obj <- AddModuleScore(obj, features=list(genes_present),
                          name=mod_name, ctrl=min(5, length(genes_present)))
    cat("  Scored:", mod_name, "(", length(genes_present), "genes matched)\n")
  }
}

# Save
saveRDS(obj, output_rds)

cat("\n", "=", rep("-", 59), "\n", sep="")
cat("  RESULTS SUMMARY\n")
cat("=", rep("-", 59), "\n", sep="")
cat("  Modules scored: ", length(module_list), "\n")
cat("  Output:         ", output_rds, "\n")
cat("=", rep("-", 59), "\n\n", sep="")
cat("[Done] sc_gene_module_extractor completed!\n")
