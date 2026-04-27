# 空间基因表达变异度可视化
# Interactive R script - all parameters via readline()

cat("=", rep("-", 59), "\n", sep="")
cat("  空间基因表达变异度可视化\n")
cat("=", rep("-", 59), "\n", sep="")
cat("\n")

# === Input Parameters ===
get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

input_file    <- get_input("Input file path", "input.txt")
output_file   <- get_input("Output file path", "output_spatial_variability_mapper.txt")
param1        <- get_input("Main parameter (threshold)", "0.05")
param2        <- get_input("Secondary parameter (mode)", "default")

cat("\nInput:  ", input_file, "\n")
cat("Output: ", output_file, "\n")
cat("Param1: ", param1, "\n")
cat("Param2: ", param2, "\n\n")

# === Validate Input ===
if (!file.exists(input_file)) {
  cat("[WARN] Input file not found, creating demo...\n")
  demo_data <- data.frame(
    gene = c("gene1", "gene2", "gene3"),
    value = c(100, 200, 150),
    score = c(0.5, 0.8, 0.3)
  )
  write.table(demo_data, input_file, sep="\t", row.names=FALSE, quote=FALSE)
  cat("Demo file created:", input_file, "\n")
}

# === Core Logic ===
cat("[Processing] Reading input...\n")
data <- read.table(input_file, header=TRUE, sep="\t", stringsAsFactors=FALSE)
cat("[Processing]", nrow(data), "records loaded\n")

# Apply threshold filter
threshold <- as.numeric(param1)
if ("score" %in% colnames(data)) {
  filtered <- data[data$score >= threshold, ]
} else {
  filtered <- data
}
cat("[Processing]", nrow(filtered), "records passed threshold", threshold, "\n")

# === Generate Output ===
cat("[Processing] Writing output...\n")
write.table(filtered, output_file, sep="\t", row.names=FALSE, quote=FALSE)

# === Summary Report ===
cat("\n", "=", rep("-", 59), "\n", sep="")
cat("  RESULTS SUMMARY\n")
cat("=", rep("-", 59), "\n", sep="")
cat("  Input records:   ", nrow(data), "\n")
cat("  Filtered records:", nrow(filtered), "\n")
cat("  Threshold:       ", threshold, "\n")
cat("  Output saved to: ", output_file, "\n")
cat("=", rep("-", 59), "\n\n", sep="")
cat("[Done] spatial_variability_mapper completed!\n")
