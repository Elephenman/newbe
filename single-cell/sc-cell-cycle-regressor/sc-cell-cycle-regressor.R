# 单细胞周期效应回归消除
library(Seurat)

get_input <- function(prompt, default) {
  val <- readline(prompt=paste0(prompt, " [默认: ", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat(paste(rep("=", 60), collapse=""), "\n")
cat("  🔬 单细胞周期效应回归器\n")
cat(paste(rep("=", 60), collapse=""), "\n")

rds_file <- get_input("Seurat对象路径", "seurat_obj.rds")
species <- get_input("物种(human/mouse)", "human")
regress <- get_input("是否回归消除周期效应(yes/no)", "yes")
output_file <- get_input("处理后对象路径", "cycle_regressed.rds")

obj <- readRDS(rds_file)
cat(paste0("\n✅ 加载对象: ", ncol(obj), " cells\n"))

s_genes <- if (species == "human") {
  c("MCM5","PCNA","TYMS","FANCI","MCM2","MCM4","RRM1","UBR1","MCM6","RPA2")
} else {
  c("Mcm5","Pcna","Tyms","Fanci","Mcm2","Mcm4","Rrm1","Ubr1","Mcm6","Rpa2")
}

g2m_genes <- if (species == "human") {
  c("ATAD2","CENPF","CTCF","NEAT1","SLC25A8","MXI1","TOP2A","HJURP","CDK1","NUSAP1")
} else {
  c("Atad2","Cenpf","Ctcf","Neat1","Slc25a8","Mxi1","Top2a","Hjurp","Cdk1","Nusap1")
}

obj <- CellCycleScoring(obj, s.features=s_genes, g2m.features=g2m_genes, set.ident=TRUE)

s_count <- sum(obj$Phase == "S")
g2m_count <- sum(obj$Phase == "G2M")
g1_count <- sum(obj$Phase == "G1")
cat(paste0("  G1: ", g1_count, ", S: ", s_count, ", G2M: ", g2m_count, "\n"))

if (regress == "yes") {
  obj <- ScaleData(obj, vars.to.regress=c("S.Score", "G2M.Score"))
  cat("  ✅ 周期效应已回归消除\n")
}

saveRDS(obj, output_file)
cat(paste0("📄 输出对象: ", output_file, "\n"))