# RNA-seq样本量/功效计算

get_input <- function(prompt, default) {
  val <- readline(prompt=paste0(prompt, " [默认: ", default, "]: "))
  if (val == "") return(default) else return(val)
}

cat(paste(rep("=", 60), collapse=""), "\n")
cat("  📊 RNA-seq样本量/功效计算器\n")
cat(paste(rep("=", 60), collapse=""), "\n")

effect_size <- as.numeric(get_input("预期效应量(log2FC)", "1"))
n_samples <- as.integer(get_input("每组样本数(0=计算所需)", "0"))
alpha <- as.numeric(get_input("显著性水平", "0.05"))
power_target <- as.numeric(get_input("目标功效", "0.8"))
output_file <- get_input("结果输出路径", "power_analysis.tsv")

d <- abs(effect_size) / 1.4142

if (n_samples == 0) {
  z_alpha <- qnorm(1 - alpha/2)
  z_beta <- qnorm(power_target)
  n_needed <- ((z_alpha + z_beta)^2) / (d^2)
  n_needed <- ceiling(n_needed)
  cat(paste0("\n✅ 计算结果:\n"))
  cat(paste0("  效应量: ", effect_size, "\n"))
  cat(paste0("  每组所需样本数: ", n_needed, "\n"))
  cat(paste0("  总样本数: ", n_needed * 2, "\n"))
  
  results <- data.frame(
    Effect_Size=effect_size, Alpha=alpha, Power=power_target,
    N_Per_Group=n_needed, N_Total=n_needed*2
  )
} else {
  z_alpha <- qnorm(1 - alpha/2)
  achieved_power <- pnorm(d * sqrt(n_samples) - z_alpha)
  cat(paste0("\n✅ 计算结果:\n"))
  cat(paste0("  效应量: ", effect_size, "\n"))
  cat(paste0("  当前样本数: ", n_samples, "\n"))
  cat(paste0("  达到功效: ", round(achieved_power, 3), "\n"))
  
  results <- data.frame(
    Effect_Size=effect_size, Alpha=alpha, N_Per_Group=n_samples,
    Achieved_Power=round(achieved_power, 3)
  )
}

write.table(results, output_file, sep="\t", quote=FALSE, row.names=FALSE)
cat(paste0("📄 结果: ", output_file, "\n"))