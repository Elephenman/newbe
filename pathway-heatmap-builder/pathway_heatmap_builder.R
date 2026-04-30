# 通路基因集表达热图+分层聚类
# Interactive R script - all parameters via readline()

cat("=", rep("-", 59), "\n", sep="")
cat("  通路基因集表达热图+分层聚类\n")
cat("=", rep("-", 59), "\n", sep="")
cat("\n")

# === Input Parameters ===
get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

expression_file <- get_input("Expression matrix CSV (rows=genes, cols=samples)", "expression.csv")
gene_set_file   <- get_input("Gene set file (one pathway per line: name<tab>gene1,gene2,...)", "pathways.tsv")
output_prefix   <- get_input("Output file prefix", "pathway_heatmap")
scale_data      <- get_input("Scale data (yes/no)", "yes")
show_rownames   <- get_input("Show row names (yes/no)", "no")

# === Validate Input ===
if (!file.exists(expression_file)) {
  cat("[ERROR] Expression file not found:", expression_file, "\n")
  quit(status=1)
}

cat("[Processing] Loading expression data...\n")
expr_data <- read.csv(expression_file, row.names = 1, check.names = FALSE)
cat("[Processing]", nrow(expr_data), "genes x", ncol(expr_data), "samples\n")

# Load gene sets
pathways <- list()
if (file.exists(gene_set_file)) {
  cat("[Processing] Loading gene sets...\n")
  con <- file(gene_set_file, "r")
  while (TRUE) {
    line <- readLines(con, n = 1)
    if (length(line) == 0) break
    if (startsWith(line, "#")) next
    parts <- strsplit(line, "\t")[[1]]
    if (length(parts) >= 2) {
      pw_name <- parts[1]
      pw_genes <- strsplit(parts[2], "[,;/]")[[1]]
      pw_genes <- trimws(pw_genes)
      pathways[[pw_name]] <- pw_genes
    }
  }
  close(con)
  cat("[Processing]", length(pathways), "pathways loaded\n")
} else {
  cat("[WARN] Gene set file not found. Using all genes.\n")
  pathways[["all_genes"]] <- rownames(expr_data)
}

# === Build Pathway Heatmaps ===
suppressPackageStartupMessages({
  library(ggplot2)
  tryCatch(library(pheatmap), error = function(e) {
    cat("[INFO] pheatmap not installed, using basic heatmap\n")
  })
})

do_scale <- tolower(scale_data) == "yes"
do_show_rownames <- tolower(show_rownames) == "yes"

for (pw_name in names(pathways)) {
  pw_genes <- pathways[[pw_name]]
  # Find genes present in expression data
  available_genes <- intersect(pw_genes, rownames(expr_data))

  if (length(available_genes) < 2) {
    cat("[WARN] Pathway '", pw_name, "': only", length(available_genes), "genes found, skipping\n")
    next
  }

  cat("[Processing] Building heatmap for:", pw_name, "(", length(available_genes), "genes)\n")

  # Subset expression data
  mat <- as.matrix(expr_data[available_genes, , drop = FALSE])

  # Scale if requested
  if (do_scale) {
    mat <- t(scale(t(mat)))
    mat[is.na(mat)] <- 0
  }

  safe_name <- gsub("[^A-Za-z0-9_]", "_", pw_name)
  out_png <- paste0(output_prefix, "_", safe_name, ".png")

  tryCatch({
    if ("pheatmap" %in% loadedNamespaces()) {
      pheatmap(mat,
               scale = "none",
               cluster_rows = TRUE,
               cluster_cols = TRUE,
               show_rownames = do_show_rownames || nrow(mat) <= 50,
               show_colnames = TRUE,
               main = paste0("Pathway: ", pw_name),
               filename = out_png,
               width = 10, height = max(6, nrow(mat) * 0.15 + 2),
               dpi = 200)
    } else {
      png(out_png, width = 1200, height = max(600, nrow(mat) * 10 + 200), res = 150)
      heatmap(mat, main = paste0("Pathway: ", pw_name))
      dev.off()
    }
    cat("[Done] Heatmap saved:", out_png, "\n")
  }, error = function(e) {
    cat("[WARN] Failed to create heatmap for", pw_name, ":", e$message, "\n")
  })
}

# === Summary ===
cat("\n", "=", rep("-", 59), "\n", sep="")
cat("  RESULTS SUMMARY\n")
cat("=", rep("-", 59), "\n", sep="")
cat("  Expression matrix: ", nrow(expr_data), "genes x", ncol(expr_data), "samples\n")
cat("  Pathways:          ", length(pathways), "\n")
cat("  Scaled:            ", do_scale, "\n")
cat("  Output prefix:     ", output_prefix, "\n")
cat("=", rep("-", 59), "\n\n", sep="")
cat("[Done] pathway_heatmap_builder completed!\n")
