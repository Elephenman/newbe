# 通路交叉对话检测
library(ggplot2)
library(dplyr)

get_input <- function(prompt, default) {
  val <- readline(prompt=paste0(prompt, " [默认: ", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat(paste(rep("=", 60), collapse=""), "\n")
cat("  📊 通路交叉对话检测器\n")
cat(paste(rep("=", 60), collapse=""), "\n")

pathway_file <- get_input("通路基因集文件(GMT)", "pathways.gmt")
min_shared <- as.integer(get_input("最小共享基因数", "3"))
output_file <- get_input("交叉对话结果路径", "crosstalk_results.tsv")
plot_out <- get_input("网络图路径", "crosstalk_network.png")

pathways <- list()
con <- file(pathway_file, "r")
while (TRUE) {
  line <- readLines(con, n=1)
  if (length(line) == 0) break
  parts <- strsplit(line, "\t")[[1]]
  name <- parts[1]
  genes <- parts[3:length(parts)]
  pathways[[name]] <- genes
}
close(con)

cat(paste0("\n✅ 加载 ", length(pathways), " 个通路\n"))

crosstalk <- data.frame()
pnames <- names(pathways)

for (i in 1:(length(pnames)-1)) {
  for (j in (i+1):length(pnames)) {
    shared <- intersect(pathways[[pnames[i]]], pathways[[pnames[j]]])
    if (length(shared) >= min_shared) {
      jaccard <- length(shared) / length(union(pathways[[pnames[i]]], pathways[[pnames[j]]]))
      crosstalk <- rbind(crosstalk, data.frame(
        Pathway_A=pnames[i], Pathway_B=pnames[j],
        Shared_Genes=length(shared), Jaccard=jaccard,
        Shared_List=paste(shared, collapse=",")
      ))
    }
  }
}

crosstalk <- crosstalk %>% arrange(desc(Jaccard))
write.table(crosstalk, output_file, sep="\t", quote=FALSE, row.names=FALSE)

cat(paste0("\n✅ 检测完成: ", nrow(crosstalk), " 对交叉对话\n"))

if (nrow(crosstalk) > 0) {
  top <- head(crosstalk, 50)
  p <- ggplot(top, aes(x=Jaccard, y=Shared_Genes)) +
    geom_point(aes(color=Jaccard), size=2) +
    scale_color_gradient(low="blue", high="red") +
    labs(title="Pathway Cross-talk Network", x="Jaccard Index", y="Shared Genes") +
    theme_bw()
  ggsave(plot_out, p, width=10, height=8)
  cat(paste0("📊 网络图: ", plot_out, "\n"))
}

cat(paste0("📄 结果: ", output_file, "\n"))