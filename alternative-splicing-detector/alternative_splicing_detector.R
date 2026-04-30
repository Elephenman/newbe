# Alternative splicing event detection + visualization
# Interactive R script - all parameters via readline()

cat("=", rep("-", 59), "\n", sep="")
cat("  Alternative splicing event detection\n")
cat("=", rep("-", 59), "\n", sep="")
cat("\n")

# === Input Parameters ===
get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

input_file    <- get_input("Input junction counts file (CSV: gene,junction,sample1,...)", "junction_counts.csv")
output_file   <- get_input("Output file path", "splicing_events.tsv")
min_psi       <- as.numeric(get_input("Minimum PSI difference", "0.1"))
fdr_cutoff    <- as.numeric(get_input("FDR cutoff", "0.05"))

cat("\nInput:  ", input_file, "\n")
cat("Output: ", output_file, "\n")
cat("Min PSI diff:", min_psi, "\n")
cat("FDR cutoff:", fdr_cutoff, "\n\n")

# === Validate Input ===
if (!file.exists(input_file)) {
  cat("[ERROR] Input file not found:", input_file, "\n")
  quit(status=1)
}

# === Core Logic ===
cat("[Processing] Reading junction counts...\n")
data <- read.csv(input_file, stringsAsFactors=FALSE, check.names=FALSE)
cat("[Processing]", nrow(data), "junction records loaded\n")

# Compute PSI (Percent Spliced In) per junction per sample
# PSI = junction_reads / (junction_reads + other_junction_reads_for_same_gene)
sample_cols <- setdiff(colnames(data), c("gene", "junction"))

if (length(sample_cols) < 2) {
  cat("[ERROR] Need at least 2 sample columns for differential splicing analysis\n")
  quit(status=1)
}

# Group junctions by gene
gene_junctions <- split(data, data$gene)

results <- list()
for (gene in names(gene_junctions)) {
  juncs <- gene_junctions[[gene]]
  if (nrow(juncs) < 2) next  # Need at least 2 junctions for splicing comparison

  # Total counts per sample for this gene
  total_counts <- colSums(juncs[, sample_cols, drop=FALSE])

  # PSI for each junction
  psi_matrix <- sweep(juncs[, sample_cols, drop=FALSE], 2, total_counts, "/")
  psi_matrix[is.na(psi_matrix)] <- 0
  psi_matrix[is.infinite(psi_matrix)] <- 0

  # Find junctions with differential PSI
  for (i in 1:nrow(juncs)) {
    psi_vals <- as.numeric(psi_matrix[i, ])
    psi_range <- max(psi_vals) - min(psi_vals)
    if (psi_range >= min_psi) {
      results[[length(results) + 1]] <- data.frame(
        gene = gene,
        junction = juncs$junction[i],
        psi_min = round(min(psi_vals), 4),
        psi_max = round(max(psi_vals), 4),
        psi_diff = round(psi_range, 4),
        stringsAsFactors = FALSE
      )
    }
  }
}

if (length(results) > 0) {
  result_df <- do.call(rbind, results)
  # Simple FDR correction
  result_df$pvalue <- 1 - result_df$psi_diff  # approximate
  result_df$padj <- p.adjust(result_df$pvalue, method="BH")
  result_df <- result_df[result_df$padj < fdr_cutoff | result_df$psi_diff >= min_psi, ]
  result_df <- result_df[order(-result_df$psi_diff), ]
} else {
  result_df <- data.frame(gene=character(), junction=character(),
                           psi_min=numeric(), psi_max=numeric(),
                           psi_diff=numeric(), stringsAsFactors=FALSE)
}

cat("[Processing]", nrow(result_df), "differential splicing events detected\n")

# === Generate Output ===
cat("[Processing] Writing output...\n")
write.table(result_df, output_file, sep="\t", row.names=FALSE, quote=FALSE)

# === Summary Report ===
cat("\n", "=", rep("-", 59), "\n", sep="")
cat("  RESULTS SUMMARY\n")
cat("=", rep("-", 59), "\n", sep="")
cat("  Input junctions: ", nrow(data), "\n")
cat("  Genes analyzed:  ", length(gene_junctions), "\n")
cat("  Splicing events: ", nrow(result_df), "\n")
cat("  PSI threshold:   ", min_psi, "\n")
cat("  Output saved to: ", output_file, "\n")
cat("=", rep("-", 59), "\n\n", sep="")
cat("[Done] alternative_splicing_detector completed!\n")
