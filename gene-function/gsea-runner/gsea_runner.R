#!/usr/bin/env Rscript
# -*- coding: utf-8 -*-
# GSEA分析一键运行

get_input <- function(prompt, default = NULL) {
  val <- readline(prompt = paste0(prompt, " [默认: ", default, "]: "))
  if (val == "" || is.null(val)) return(default)
  return(val)
}

cat("============================================================\n")
cat("  GSEA分析一键运行\n")
cat("============================================================\n\n")

mat_path <- get_input("表达矩阵路径(行=基因,列=样本)", "expression.csv")
group_file <- get_input("分组标签文件(样本名+分组,逗号分隔)", "groups.txt")
gene_set <- get_input("基因集(KEGG/Reactome/custom)", "KEGG")
p_cutoff <- as.numeric(get_input("pvalue阈值", "0.05"))
species <- get_input("物种(human/mouse)", "human")

suppressPackageStartupMessages({
  if (!require(fgsea)) { cat("需要fgsea: install.packages('fgsea')\n"); quit(status=1) }
  library(ggplot2)
})

# 读取表达矩阵
mat <- as.matrix(read.csv(mat_path, row.names = 1))
groups <- read.csv(group_file, header = FALSE, stringsAsFactors = FALSE)
group_vec <- setNames(groups$V2, groups$V1)

# 计算ranked list (signal-to-noise ratio or t-test statistic)
cat("[Processing] Computing ranked gene list...\n")
group_names <- unique(group_vec)
if (length(group_names) < 2) {
  cat("[ERROR] Need at least 2 groups for GSEA\n")
  quit(status=1)
}

ranked <- sapply(rownames(mat), function(g) {
  g1 <- as.numeric(mat[g, names(group_vec[group_vec == group_names[1]])])
  g2 <- as.numeric(mat[g, names(group_vec[group_vec == group_names[2]])])
  # Remove NA values
  g1 <- g1[!is.na(g1)]
  g2 <- g2[!is.na(g2)]
  if (length(g1) < 2 || length(g2) < 2) return(0)
  # Signal-to-noise ratio (preferred for GSEA)
  snr <- (mean(g1) - mean(g2)) / (sd(g1) + sd(g2))
  if (is.na(snr) || is.infinite(snr)) return(0)
  return(snr)
})
ranked_list <- sort(ranked, decreasing = TRUE)

cat("[Processing] Ranked list: length =", length(ranked_list), "\n")

# 基因集
kegg_org <- if(species == "human") "hsa" else "mmu"

if (gene_set == "KEGG") {
  if (!require(clusterProfiler)) {
    cat("需要clusterProfiler: BiocManager::install('clusterProfiler')\n")
    quit(status=1)
  }
  cat("[Processing] Running GSEA with KEGG pathways...\n")
  result <- tryCatch({
    gseKEGG(geneList = ranked_list, organism = kegg_org, pvalueCutoff = p_cutoff)
  }, error = function(e) {
    cat("[WARN] gseKEGG failed:", e$message, "\n")
    cat("[INFO] Trying fgsea with KEGG pathways...\n")

    # Fallback: use fgsea with KEGG
    if (require(clusterProfiler)) {
      kegg_pathways <- clusterProfiler::download_KEGG(kegg_org)
      pathways_list <- split(kegg_pathways$kegg_pathway$gene, kegg_pathways$kegg_pathway$pathway)
      fgsea(pathways = pathways_list, stats = ranked_list, minSize = 5, maxSize = 500)
    } else {
      NULL
    }
  })
} else if (gene_set == "Reactome") {
  if (!require(ReactomePA)) {
    cat("需要ReactomePA: BiocManager::install('ReactomePA')\n")
    quit(status=1)
  }
  cat("[Processing] Running GSEA with Reactome pathways...\n")
  result <- tryCatch({
    gsePathway(geneList = ranked_list, pvalueCutoff = p_cutoff)
  }, error = function(e) {
    cat("[ERROR] gsePathway failed:", e$message, "\n")
    quit(status=1)
  })
} else {
  # Custom GMT file
  gmt_file <- get_input("自定义GMT文件路径", "custom_pathways.gmt")
  if (!file.exists(gmt_file)) {
    cat("[ERROR] GMT file not found:", gmt_file, "\n")
    quit(status=1)
  }

  cat("[Processing] Parsing custom GMT file...\n")
  pathways_list <- list()
  con <- file(gmt_file, "r")
  while (TRUE) {
    line <- readLines(con, n = 1)
    if (length(line) == 0) break
    parts <- strsplit(line, "\t")[[1]]
    if (length(parts) >= 3) {
      pw_name <- parts[1]
      pw_genes <- parts[3:length(parts)]
      pw_genes <- pw_genes[pw_genes != ""]
      pathways_list[[pw_name]] <- pw_genes
    }
  }
  close(con)

  cat("[Processing] Running fgsea with", length(pathways_list), "custom pathways...\n")
  result <- fgsea(pathways = pathways_list, stats = ranked_list, minSize = 5, maxSize = 500)
}

# 保存结果
if (is.null(result) || (is.data.frame(result) && nrow(result) == 0)) {
  cat("[WARN] No significant pathways found at p <", p_cutoff, "\n")
} else {
  out_path <- paste0(tools::file_path_sans_ext(mat_path), "_GSEA.csv")
  write.csv(as.data.frame(result), out_path, row.names = FALSE)
  cat("GSEA结果:", out_path, "\n")
  cat("   显著通路数:", nrow(as.data.frame(result)), "\n")

  # 绘制enrichment plot for top pathway
  tryCatch({
    if ("pathway" %in% colnames(result)) {
      top_pathway <- result$pathway[1]
      plotGseaTable(ranked_list, result, fgseaRes = result)
      ggsave(paste0(tools::file_path_sans_ext(mat_path), "_GSEA_plot.png"),
             width = 10, height = 8, dpi = 150)
    }
  }, error = function(e) {
    cat("[WARN] Plot failed:", e$message, "\n")
  })
}
