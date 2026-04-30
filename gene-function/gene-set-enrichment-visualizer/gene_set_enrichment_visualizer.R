# 富集结果多维度可视化（气泡/条形/网络）
# Interactive R script - all parameters via readline()

cat("=", rep("-", 59), "\n", sep="")
cat("  富集结果多维度可视化（气泡/条形/网络）\n")
cat("=", rep("-", 59), "\n", sep="")
cat("\n")

# === Input Parameters ===
get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

input_file    <- get_input("Enrichment result file (TSV: term/pvalue/gene_ratio/count)", "enrichment_results.tsv")
output_prefix <- get_input("Output file prefix", "enrichment_viz")
p_cutoff      <- as.numeric(get_input("p-value cutoff", "0.05"))
plot_type     <- get_input("Plot type (bubble/bar/network/all)", "all")

# === Validate Input ===
if (!file.exists(input_file)) {
  cat("[ERROR] Input file not found:", input_file, "\n")
  cat("Expected format: TSV with columns: term, pvalue, gene_ratio, count\n")
  quit(status=1)
}

# === Load Data ===
cat("[Processing] Reading enrichment results...\n")
data <- read.table(input_file, header=TRUE, sep="\t", stringsAsFactors=FALSE, quote="")

# Validate required columns
required_cols <- c("term", "pvalue")
missing_cols <- setdiff(required_cols, colnames(data))
if (length(missing_cols) > 0) {
  cat("[ERROR] Missing required columns:", paste(missing_cols, collapse=", "), "\n")
  cat("Expected columns: term, pvalue, gene_ratio (optional), count (optional)\n")
  quit(status=1)
}

# Filter by p-value
data <- data[data$pvalue <= p_cutoff, ]
cat("[Processing]", nrow(data), "pathways passed p-value cutoff", p_cutoff, "\n")

if (nrow(data) == 0) {
  cat("[WARN] No pathways passed the p-value cutoff. Try a larger cutoff.\n")
  quit(status=0)
}

# Add derived columns if missing
if (!"gene_ratio" %in% colnames(data) && "count" %in% colnames(data)) {
  data$gene_ratio <- data$count / max(data$count, na.rm=TRUE)
}
if (!"neg_log10_p" %in% colnames(data)) {
  data$neg_log10_p <- -log10(data$pvalue)
}

# === Generate Plots ===
suppressPackageStartupMessages({
  library(ggplot2)
})

# Take top 20 for visualization
top_data <- head(data[order(data$pvalue), ], 20)

if (plot_type %in% c("bubble", "all")) {
  # Bubble plot
  p <- ggplot(top_data, aes(x = gene_ratio, y = reorder(term, -pvalue),
                             size = count, color = neg_log10_p)) +
    geom_point(alpha = 0.8) +
    scale_color_gradient(low = "blue", high = "red", name = "-log10(p)") +
    scale_size_continuous(name = "Gene count") +
    theme_bw() +
    labs(x = "Gene ratio", y = "", title = "Enrichment Bubble Plot") +
    theme(axis.text.y = element_text(size = 8))
  ggsave(paste0(output_prefix, "_bubble.png"), p, width = 10, height = 8, dpi = 300)
  cat("[Done] Bubble plot saved:", paste0(output_prefix, "_bubble.png"), "\n")
}

if (plot_type %in% c("bar", "all")) {
  # Bar plot
  p <- ggplot(top_data, aes(x = reorder(term, -neg_log10_p), y = neg_log10_p, fill = neg_log10_p)) +
    geom_bar(stat = "identity") +
    coord_flip() +
    scale_fill_gradient(low = "blue", high = "red", name = "-log10(p)") +
    theme_bw() +
    labs(x = "", y = "-log10(p-value)", title = "Enrichment Bar Plot") +
    theme(axis.text.y = element_text(size = 8))
  ggsave(paste0(output_prefix, "_bar.png"), p, width = 10, height = 8, dpi = 300)
  cat("[Done] Bar plot saved:", paste0(output_prefix, "_bar.png"), "\n")
}

if (plot_type %in% c("network", "all")) {
  # Network plot (gene-term bipartite)
  tryCatch({
    if (!require(igraph)) install.packages("igraph")
    library(igraph)

    # Build edges from gene lists
    edges <- data.frame(from = character(), to = character(), stringsAsFactors = FALSE)
    if ("genes" %in% colnames(data)) {
      for (i in seq_len(min(nrow(top_data), 15))) {
        gene_list <- strsplit(top_data$genes[i], "[/;,]")[[1]]
        for (g in gene_list) {
          edges <- rbind(edges, data.frame(from = top_data$term[i], to = trimws(g)))
        }
      }
    }

    if (nrow(edges) > 0) {
      g <- graph_from_data_frame(edges, directed = FALSE)
      V(g)$type <- V(g)$name %in% top_data$term

      png(paste0(output_prefix, "_network.png"), width = 1200, height = 1000, res = 150)
      plot(g, vertex.size = ifelse(V(g)$type, 15, 5),
           vertex.color = ifelse(V(g)$type, "lightblue", "orange"),
           vertex.label.cex = 0.6,
           edge.color = "gray80", edge.width = 0.5,
           layout = layout_with_fr)
      dev.off()
      cat("[Done] Network plot saved:", paste0(output_prefix, "_network.png"), "\n")
    } else {
      cat("[INFO] No 'genes' column found, skipping network plot.\n")
    }
  }, error = function(e) {
    cat("[WARN] Network plot failed:", e$message, "\n")
  })
}

# === Summary ===
cat("\n", "=", rep("-", 59), "\n", sep="")
cat("  RESULTS SUMMARY\n")
cat("=", rep("-", 59), "\n", sep="")
cat("  Input:           ", input_file, "\n")
cat("  Pathways shown:  ", nrow(top_data), "\n")
cat("  p-value cutoff:  ", p_cutoff, "\n")
cat("  Output prefix:   ", output_prefix, "\n")
cat("=", rep("-", 59), "\n\n", sep="")
cat("[Done] gene_set_enrichment_visualizer completed!\n")
