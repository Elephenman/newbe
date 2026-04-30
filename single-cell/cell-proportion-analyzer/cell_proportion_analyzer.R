# Cell type proportion change analysis + stacked bar plot
# Interactive R script - all parameters via readline()

cat("=", rep("-", 59), "\n", sep="")
cat("  Cell type proportion change analysis\n")
cat("=", rep("-", 59), "\n", sep="")
cat("\n")

# === Input Parameters ===
get_input <- function(prompt, default) {
  val <- readline(prompt = paste0(prompt, " [", default, "]: "))
  if (val == "") return(default) else return(val)
}

obj_path <- get_input("Seurat object path (rds)", "seurat.rds")
group_by <- get_input("Grouping metadata column (e.g., condition/sample)", "orig.ident")
celltype_col <- get_input("Cell type column (e.g., celltype/seurat_clusters)", "seurat_clusters")
output_file <- get_input("Output CSV path", "cell_proportions.csv")
output_plot <- get_input("Output plot path", "cell_proportions.png")

cat("\nObject:   ", obj_path, "\n")
cat("Group by: ", group_by, "\n")
cat("Cell type:", celltype_col, "\n")
cat("Output:   ", output_file, "\n\n")

# === Load Seurat ===
suppressPackageStartupMessages({
  if (!require(Seurat)) { cat("Need Seurat\n"); quit(status=1) }
  library(ggplot2)
})

if (!file.exists(obj_path)) {
  cat("[ERROR] File not found:", obj_path, "\n")
  quit(status=1)
}

obj <- readRDS(obj_path)

# Validate columns
if (!group_by %in% colnames(obj@meta.data)) {
  cat("[ERROR] Column '", group_by, "' not found in metadata\n", sep="")
  cat("Available columns:", paste(colnames(obj@meta.data), collapse=", "), "\n")
  quit(status=1)
}
if (!celltype_col %in% colnames(obj@meta.data)) {
  cat("[ERROR] Column '", celltype_col, "' not found in metadata\n", sep="")
  cat("Available columns:", paste(colnames(obj@meta.data), collapse=", "), "\n")
  quit(status=1)
}

# === Core Logic ===
cat("[Processing] Computing cell proportions...\n")

# Create proportion table
meta <- obj@meta.data
prop_table <- prop.table(table(meta[[group_by]], meta[[celltype_col]]), margin=1)

# Convert to data frame for ggplot
prop_df <- as.data.frame(prop_table)
colnames(prop_df) <- c("Group", "CellType", "Proportion")
prop_df$Proportion <- round(prop_df$Proportion * 100, 2)

# Statistical test: chi-squared test for proportion differences
chi_result <- chisq.test(prop_table)
cat("[Processing] Chi-squared test: p-value =", format(chi_result$p.value, digits=4), "\n")

# === Generate Output ===
cat("[Processing] Writing output...\n")
write.csv(prop_df, output_file, row.names = FALSE)

# Stacked bar plot
p <- ggplot(prop_df, aes(x = Group, y = Proportion, fill = CellType)) +
  geom_bar(stat = "identity", position = "stack") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  labs(title = "Cell Type Proportions by Group",
       x = group_by, y = "Proportion (%)",
       fill = celltype_col) +
  scale_y_continuous(expand = c(0, 0))

ggsave(output_plot, p, width = 10, height = 6, dpi = 300)

# === Summary Report ===
cat("\n", "=", rep("-", 59), "\n", sep="")
cat("  RESULTS SUMMARY\n")
cat("=", rep("-", 59), "\n", sep="")
cat("  Total cells:       ", ncol(obj), "\n")
cat("  Groups:            ", length(unique(meta[[group_by]])), "\n")
cat("  Cell types:        ", length(unique(meta[[celltype_col]])), "\n")
cat("  Chi-sq p-value:    ", format(chi_result$p.value, digits=4), "\n")
cat("  Proportion CSV:    ", output_file, "\n")
cat("  Plot:              ", output_plot, "\n")
cat("=", rep("-", 59), "\n\n", sep="")
cat("[Done] cell_proportion_analyzer completed!\n")
