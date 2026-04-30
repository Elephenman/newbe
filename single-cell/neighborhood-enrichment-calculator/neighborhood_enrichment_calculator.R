# 细胞邻域富集分析（空间邻近偏好）
# Interactive R script - all parameters via readline()

cat("=", rep("-", 59), "\n", sep="")
cat("  细胞邻域富集分析（空间邻近偏好）\n")
cat("=", rep("-", 59), "\n", sep="")
cat("\n")

# === Input Parameters ===
get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

spatial_file <- get_input("Spatial data file (CSV: cell_id,x,y,cell_type)", "spatial.csv")
output_file  <- get_input("Output file path", "neighborhood_enrichment.tsv")
n_perm       <- as.integer(get_input("Number of permutations", "1000"))
radius       <- as.numeric(get_input("Neighborhood radius", "50"))

# === Validate Input ===
if (!file.exists(spatial_file)) {
  cat("[ERROR] Input file not found:", spatial_file, "\n")
  cat("Expected format: CSV with columns: cell_id, x, y, cell_type\n")
  quit(status=1)
}

# === Load Data ===
cat("[Processing] Loading spatial data...\n")
data <- read.csv(spatial_file, stringsAsFactors = FALSE)

# Validate required columns
required_cols <- c("x", "y", "cell_type")
missing_cols <- setdiff(required_cols, colnames(data))
if (length(missing_cols) > 0) {
  cat("[ERROR] Missing required columns:", paste(missing_cols, collapse=", "), "\n")
  cat("Expected: cell_id, x, y, cell_type\n")
  quit(status=1)
}

cat("[Processing]", nrow(data), "cells loaded\n")
cat("[Processing]", length(unique(data$cell_type)), "cell types\n")

# === Compute Neighborhood Enrichment ===
cell_types <- unique(data$cell_type)
n_types <- length(cell_types)

cat("[Processing] Computing pairwise neighborhood enrichment...\n")
cat("[Processing] Radius:", radius, ", Permutations:", n_perm, "\n")

# Build distance matrix and find neighbors
coords <- as.matrix(data[, c("x", "y")])
type_labels <- data$cell_type

# Observed neighborhood counts
observed <- matrix(0, nrow = n_types, ncol = n_types)
rownames(observed) <- cell_types
colnames(observed) <- cell_types

n_cells <- nrow(data)
for (i in 1:min(n_cells, 5000)) {  # Limit for performance
  dists <- sqrt((coords[,1] - coords[i,1])^2 + (coords[,2] - coords[i,2])^2)
  neighbors <- which(dists <= radius & (1:n_cells) != i)
  if (length(neighbors) > 0) {
    source_type <- type_labels[i]
    for (j in neighbors) {
      neighbor_type <- type_labels[j]
      observed[source_type, neighbor_type] <- observed[source_type, neighbor_type] + 1
    }
  }
}

# Permutation test
perm_counts <- array(0, dim = c(n_types, n_types, n_perm))
for (p in 1:n_perm) {
  perm_labels <- sample(type_labels)
  for (i in 1:min(n_cells, 5000)) {
    dists <- sqrt((coords[,1] - coords[i,1])^2 + (coords[,2] - coords[i,2])^2)
    neighbors <- which(dists <= radius & (1:n_cells) != i)
    if (length(neighbors) > 0) {
      source_type <- perm_labels[i]
      for (j in neighbors) {
        neighbor_type <- perm_labels[j]
        perm_counts[source_type, neighbor_type, p] <- perm_counts[source_type, neighbor_type, p] + 1
      }
    }
  }
}

# Calculate z-scores
z_scores <- matrix(0, nrow = n_types, ncol = n_types)
rownames(z_scores) <- cell_types
colnames(z_scores) <- cell_types

p_values <- matrix(1, nrow = n_types, ncol = n_types)
rownames(p_values) <- cell_types
colnames(p_values) <- cell_types

for (i in 1:n_types) {
  for (j in 1:n_types) {
    perm_dist <- perm_counts[i, j, ]
    perm_mean <- mean(perm_dist)
    perm_sd <- sd(perm_dist)
    if (perm_sd > 0) {
      z_scores[i, j] <- (observed[i, j] - perm_mean) / perm_sd
    }
    # One-sided p-value (enrichment)
    p_values[i, j] <- sum(perm_dist >= observed[i, j]) / n_perm
  }
}

# === Generate Output ===
cat("[Processing] Writing output...\n")

# Save results
result_df <- data.frame(
  source_type = rep(rownames(z_scores), times = n_types),
  neighbor_type = rep(colnames(z_scores), each = n_types),
  observed_count = as.vector(observed),
  z_score = round(as.vector(z_scores), 3),
  p_value = round(as.vector(p_values), 4)
)
write.table(result_df, output_file, sep="\t", row.names=FALSE, quote=FALSE)

# Heatmap
tryCatch({
  library(ggplot2)
  library(reshape2)

  z_melt <- melt(z_scores)
  colnames(z_melt) <- c("source", "neighbor", "z_score")

  p <- ggplot(z_melt, aes(x = neighbor, y = source, fill = z_score)) +
    geom_tile() +
    scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0) +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
    labs(title = "Neighborhood Enrichment Z-scores", fill = "Z-score") +
    coord_fixed()
  ggsave("neighborhood_enrichment_heatmap.png", p, width = 8, height = 7, dpi = 200)
  cat("[Done] Heatmap saved: neighborhood_enrichment_heatmap.png\n")
}, error = function(e) {
  cat("[WARN] Plotting failed:", e$message, "\n")
})

# === Summary Report ===
cat("\n", "=", rep("-", 59), "\n", sep="")
cat("  RESULTS SUMMARY\n")
cat("=", rep("-", 59), "\n", sep="")
cat("  Cells analyzed:  ", nrow(data), "\n")
cat("  Cell types:      ", n_types, "\n")
cat("  Radius:          ", radius, "\n")
cat("  Permutations:    ", n_perm, "\n")

# Top enriched pairs
top_pairs <- result_df[order(-result_df$z_score), ]
cat("\n  Top enriched neighborhoods:\n")
for (i in 1:min(5, nrow(top_pairs))) {
  cat("    ", top_pairs$source_type[i], "->", top_pairs$neighbor_type[i],
      " z=", top_pairs$z_score[i], " p=", top_pairs$p_value[i], "\n")
}
cat("\n  Output saved to: ", output_file, "\n")
cat("=", rep("-", 59), "\n\n", sep="")
cat("[Done] neighborhood_enrichment_calculator completed!\n")
