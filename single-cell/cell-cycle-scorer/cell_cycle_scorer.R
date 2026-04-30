# Single-cell cycle scoring + G1/S/G2M classification
# Interactive R script - all parameters via readline()

cat("=", rep("-", 59), "\n", sep="")
cat("  Single-cell cycle scoring + G1/S/G2M classification\n")
cat("=", rep("-", 59), "\n", sep="")
cat("\n")

# === Input Parameters ===
get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

obj_path <- get_input("Seurat object path (rds)", "seurat.rds")
s_genes <- get_input("S-phase genes file (one per line, or 'default')", "default")
g2m_genes <- get_input("G2M-phase genes file (one per line, or 'default')", "default")
output_file <- get_input("Output CSV path", "cell_cycle_scores.csv")

cat("\nObject:  ", obj_path, "\n")
cat("Output:  ", output_file, "\n\n")

# === Load Seurat ===
suppressPackageStartupMessages({
  if (!require(Seurat)) { cat("Need Seurat\n"); quit(status=1) }
})

if (!file.exists(obj_path)) {
  cat("[ERROR] File not found:", obj_path, "\n")
  quit(status=1)
}

obj <- readRDS(obj_path)

# === Cell cycle scoring ===
# Default S and G2M gene sets (human)
if (s_genes == "default") {
  s_genes_vec <- c("MCM5","PCNA","TYMS","FANCI","MCM2","MCM4","RRM1","UNG","GINS2",
                   "MCM6","CDCA7","DTL","PRIM1","UHRF1","CENPU","HELLS","RFC2","RPA2",
                   "NASP","RAD51AP1","GMNN","WDR76","SLBP","CCNE2","UBR7","POLD3",
                   "MSH2","ATAD2","RAD51","RRM2","CDC45","CDC6","EXO1","TIPIN","DSCC1",
                   "BLM","CASP8AP2","USP1","CLSPN","POLA1","CHAF1B","BRIP1","E2F8")
} else {
  s_genes_vec <- readLines(s_genes)
  s_genes_vec <- trimws(s_genes_vec[s_genes_vec != ""])
}

if (g2m_genes == "default") {
  g2m_genes_vec <- c("HMGB2","CDK1","NUSAP1","UICC1","KIF11","CKAP2","CKAP2L",
                      "GTSE1","TUBB4B","TOP2A","NDC80","KNL1","CKS1B","CENPF",
                      "ANP32E","SMC4","CCNB2","CKAP5","BIRC5","CDCA3","HJURP",
                      "ANLN","CCNA2","CDCA2","CDK2","CDC20","KIF23","CTCF",
                      "AURKB","CENPE","TACC3","G2E3","BUB1","KIF2C","RANGAP1",
                      "INCENP","CDCA8","HMMR","AURKA","BUB1B","CDC25C","PKMYT1",
                      "KIF20B","MKI67","TMEM99","MLF1IP","CENPA","DEPDC1")
} else {
  g2m_genes_vec <- readLines(g2m_genes)
  g2m_genes_vec <- trimws(g2m_genes_vec[g2m_genes_vec != ""])
}

# Ensure normalized data exists
if (is.null(obj@assays$RNA@data) || sum(obj@assays$RNA@data) == 0) {
  cat("[Processing] Running normalization...\n")
  obj <- NormalizeData(obj)
}

# Run cell cycle scoring
cat("[Processing] Scoring cell cycle phases...\n")
obj <- CellCycleScoring(obj, s.features = s_genes_vec, g2m.features = g2m_genes_vec, set.ident = TRUE)

# Summary
phase_counts <- table(obj$Phase)
cat("[Processing] Cell cycle scoring complete\n")
for (phase in names(phase_counts)) {
  cat("  ", phase, ": ", phase_counts[phase], " cells (", round(phase_counts[phase]/length(obj$Phase)*100, 1), "%)\n", sep="")
}

# === Generate Output ===
cat("[Processing] Writing output...\n")
cycle_df <- data.frame(
  cell = colnames(obj),
  phase = obj$Phase,
  S_score = obj$S.Score,
  G2M_score = obj$G2M.Score,
  stringsAsFactors = FALSE
)
write.csv(cycle_df, output_file, row.names = FALSE)

# Save annotated object
saveRDS(obj, "seurat_cellcycle.rds")

# === Summary Report ===
cat("\n", "=", rep("-", 59), "\n", sep="")
cat("  RESULTS SUMMARY\n")
cat("=", rep("-", 59), "\n", sep="")
cat("  Total cells:     ", ncol(obj), "\n")
cat("  G1 cells:        ", phase_counts["G1"], "\n")
cat("  S cells:         ", phase_counts["S"], "\n")
cat("  G2M cells:       ", phase_counts["G2M"], "\n")
cat("  Output CSV:      ", output_file, "\n")
cat("  Seurat object:   seurat_cellcycle.rds\n")
cat("=", rep("-", 59), "\n\n", sep="")
cat("[Done] cell_cycle_scorer completed!\n")
