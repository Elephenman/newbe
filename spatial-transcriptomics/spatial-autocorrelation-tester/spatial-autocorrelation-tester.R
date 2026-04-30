# 空间自相关检验
library(Seurat)

get_input <- function(prompt, default) {
  val <- readline(prompt=paste0(prompt, " [默认: ", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat(paste(rep("=", 60), collapse=""), "\n")
cat("  🔬 空间自相关检验器\n")
cat(paste(rep("=", 60), collapse=""), "\n")

rds_file <- get_input("Seurat空间对象路径", "spatial_obj.rds")
gene_str <- get_input("基因列表(逗号分隔)", "CD68,CD3E,EGFR")
method <- get_input("检验方法(Moran/Geary)", "Moran")
output_file <- get_input("结果输出路径", "autocorrelation_results.tsv")

obj <- readRDS(rds_file)
genes <- strsplit(gene_str, ",")[[1]]
cat(paste0("\n✅ 加载对象: ", ncol(obj), " spots\n"))

coords <- GetTissueCoordinates(obj)
expr <- GetAssayData(obj, slot="data")

results <- data.frame()

for (gene in genes) {
  if (!(gene %in% rownames(expr))) {
    cat(paste0("  ⚠️ ", gene, " 不存在\n"))
    continue
  }
  
  gene_expr <- as.numeric(expr[gene, ])
  
  n <- length(gene_expr)
  mean_e <- mean(gene_expr)
  var_e <- var(gene_expr)
  
  if (method == "Moran") {
    W_sum <- 0
    numerator <- 0
    for (i in 1:(n-1)) {
      for (j in (i+1):n) {
        d <- sqrt((coords[i,1]-coords[j,1])^2 + (coords[i,2]-coords[j,2])^2)
        w <- 1 / max(d, 1)
        numerator <- numerator + w * (gene_expr[i]-mean_e) * (gene_expr[j]-mean_e)
        W_sum <- W_sum + w
      }
    }
    I <- (n / W_sum) * (numerator / (var_e * n))
    results <- rbind(results, data.frame(Gene=gene, Method="Moran", Value=round(I,4)))
  }
}

write.table(results, output_file, sep="\t", quote=FALSE, row.names=FALSE)
cat(paste0("\n✅ 检验完成\n"))
cat(paste0("📄 结果: ", output_file, "\n"))