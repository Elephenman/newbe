# 空间共表达基因地图
library(Seurat)
library(ggplot2)

get_input <- function(prompt, default) {
  val <- readline(prompt=paste0(prompt, " [默认: ", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat(paste(rep("=", 60), collapse=""), "\n")
cat("  🔬 空间共表达基因地图\n")
cat(paste(rep("=", 60), collapse=""), "\n")

rds_file <- get_input("空间Seurat对象路径", "spatial_obj.rds")
gene_a <- get_input("基因A", "CD68")
gene_b <- get_input("基因B", "CD3E")
output_file <- get_input("共表达图路径", "coexpression_map.png")

obj <- readRDS(rds_file)
cat(paste0("\n✅ 加载对象: ", ncol(obj), " spots\n"))

expr <- GetAssayData(obj, slot="data")
if (!(gene_a %in% rownames(expr)) | !(gene_b %in% rownames(expr))) {
  cat("⚠️ 基因不在表达矩阵中\n")
  quit(status=1)
}

coords <- GetTissueCoordinates(obj)
df <- data.frame(
  x=coords[,1], y=coords[,2],
  geneA=as.numeric(expr[gene_a,]),
  geneB=as.numeric(expr[gene_b,]),
  coexpression=as.numeric(expr[gene_a,]) * as.numeric(expr[gene_b,])
)

p <- ggplot(df, aes(x=x, y=y)) +
  geom_point(aes(color=coexpression), size=1.5) +
  scale_color_gradient2(low="blue", mid="white", high="red", midpoint=0) +
  labs(title=paste0(gene_a, " x ", gene_b, " Co-expression"),
       subtitle=paste0("Correlation: ", round(cor(df$geneA, df$geneB), 3))) +
  theme_void() + theme(plot.title=element_text(hjust=0.5))

ggsave(output_file, p, width=8, height=8, dpi=200)
cat(paste0("\n✅ 共表达图: ", output_file, "\n"))