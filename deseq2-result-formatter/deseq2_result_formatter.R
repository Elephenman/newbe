#!/usr/bin/env Rscript
# -*- coding: utf-8 -*-
# ============================================================
# DESeq2结果→发表级表格+火山图
# 
# 功能：
# - 读取DESeq2结果CSV
# - 按padj和log2FC阈值过滤
# - 统计上调/下调/稳定基因数
# - 生成ggplot2火山图（标注top基因）
# - 输出：过滤后CSV + 灭山图PNG + 统计摘要
# ============================================================

# ========== 交互式输入函数 ==========

get_input <- function(prompt, default = NULL, type = "character") {
  val <- readline(prompt = paste0(prompt, " [默认: ", default, "]: "))
  val <- trimws(val)
  
  if (val == "" || is.null(val)) {
    return(default)
  }
  
  if (type == "numeric" || type == "integer") {
    val <- as.numeric(val)
    if (is.na(val)) {
      cat("  ⚠ 输入格式错误，使用默认值:", default, "\n")
      return(default)
    }
  }
  
  return(val)
}

# ========== 主脚本 ==========

cat("============================================================\n")
cat("  📊 DESeq2结果→发表级表格+火山图\n")
cat("============================================================\n\n")

# 交互式参数输入
csv_path <- get_input("输入DESeq2结果CSV路径", default = "deseq2_results.csv")
padj_threshold <- get_input("padj阈值", default = 0.05, type = "numeric")
log2fc_threshold <- get_input("log2FC阈值", default = 1, type = "numeric")
gene_col <- get_input("基因名列名(如rowname/gene_id/symbol)", default = "rowname")
make_volcano <- get_input("是否生成火山图(yes/no)", default = "yes")
top_n <- get_input("火山图标注topN基因", default = 10, type = "numeric")
img_format <- get_input("图片格式(png/pdf/tiff)", default = "png")

# 加载必要包
suppressPackageStartupMessages({
  if (!require(ggplot2)) {
    cat("  ❌ 需要安装ggplot2: install.packages('ggplot2')\n")
    quit(status = 1)
  }
  if (!require(dplyr)) {
    cat("  ⚠ dplyr未安装，使用基础R替代\n")
    has_dplyr <- FALSE
  } else {
    has_dplyr <- TRUE
  }
})

# 读取数据
cat("\n  ⏳ 正在读取DESeq2结果...\n")

if (!file.exists(csv_path)) {
  cat("  ❌ 文件不存在:", csv_path, "\n")
  quit(status = 1)
}

results <- read.csv(csv_path, row.names = 1)

# 处理基因名列
if (gene_col == "rowname") {
  results$gene <- rownames(results)
} else if (gene_col %in% colnames(results)) {
  results$gene <- results[[gene_col]]
} else {
  cat("  ⚠ 基因名列'", gene_col, "'不存在，使用rowname\n")
  results$gene <- rownames(results)
}

# 确认必要列存在
required_cols <- c("log2FoldChange", "pvalue", "padj")
missing_cols <- required_cols[!required_cols %in% colnames(results)]
if (length(missing_cols) > 0) {
  # 尝试别名
  aliases <- list(
    log2FoldChange = c("log2FoldChange", "logFC", "log2FC", "FC"),
    pvalue = c("pvalue", "p_val", "P.Value", "pval", "P"),
    padj = c("padj", "p_adj", "adj.P.Val", "FDR", "padjust")
  )
  
  for (col in missing_cols) {
    for (alias in aliases[[col]]) {
      if (alias %in% colnames(results)) {
        results[[col]] <- results[[alias]]
        cat("  ℹ️ 使用别名:", alias, "→", col, "\n")
        break
      }
    }
  }
  
  # 再次检查
  still_missing <- required_cols[!required_cols %in% colnames(results)]
  if (length(still_missing) > 0) {
    cat("  ❌ 缺少必要列:", still_missing, "\n")
    cat("  可用列:", colnames(results), "\n")
    quit(status = 1)
  }
}

# 过滤
cat("  ⏳ 正在过滤DEGs...\n")

results$category <- "Stable"
results$category[results$log2FoldChange >= log2fc_threshold & results$padj < padj_threshold] <- "Up"
results$category[results$log2FoldChange <= -log2fc_threshold & results$padj < padj_threshold] <- "Down"

up_count <- sum(results$category == "Up")
down_count <- sum(results$category == "Down")
stable_count <- sum(results$category == "Stable")
total_count <- nrow(results)
sig_count <- up_count + down_count

cat("\n")
cat("╔══════════════════════════════════════════════════════════╗\n")
cat("║            DESeq2结果统计摘要                           ║\n")
cat("╠══════════════════════════════════════════════════════════╣\n")
cat("║  总基因数:     ", total_count, "\n")
cat("║  显著差异基因: ", sig_count, "\n")
cat("║  上调基因:     ", up_count, " (log2FC≥", log2fc_threshold, ", padj<", padj_threshold, ")\n")
cat("║  下调基因:     ", down_count, " (log2FC≤-", log2fc_threshold, ", padj<", padj_threshold, ")\n")
cat("║  稳定基因:     ", stable_count, "\n")
cat("╚══════════════════════════════════════════════════════════╝\n\n")

# 保存过滤后CSV
deg_results <- results[results$category != "Stable", ]
deg_results <- deg_results[order(deg_results$padj), ]

output_csv <- paste0(tools::file_path_sans_ext(csv_path), "_filtered.csv")
write.csv(deg_results, output_csv, row.names = FALSE)
cat("  ✅ 过滤后DEG列表已保存:", output_csv, "\n")

# 保存完整结果（含category列）
full_output <- paste0(tools::file_path_sans_ext(csv_path), "_annotated.csv")
write.csv(results, full_output, row.names = FALSE)
cat("  ✅ 注释完整结果已保存:", full_output, "\n")

# 生成火山图
if (make_volcano == "yes" || make_volcano == "y") {
  cat("  ⏳ 正在生成火山图...\n")
  
  # 准备数据
  plot_data <- results
  plot_data$neg_log10_padj <- -log10(plot_data$padj)
  
  # 标注top基因
  top_genes_up <- head(plot_data[plot_data$category == "Up", ][order(plot_data$category == "Up" & plot_data$neg_log10_padj, decreasing = TRUE), ], top_n)
  top_genes_down <- head(plot_data[plot_data$category == "Down", ][order(plot_data$category == "Down" & plot_data$neg_log10_padj, decreasing = TRUE), ], top_n)
  
  # 简化版：按绝对值排序取top
  top_up <- plot_data %>>% 
    filter(category == "Up") %>%
    arrange(desc(neg_log10_padj)) %>%
    head(top_n)
  
  top_down <- plot_data %>%
    filter(category == "Down") %>%
    arrange(desc(neg_log10_padj)) %>%
    head(top_n)
  
  label_data <- rbind(top_up, top_down)
  
  # 绘图
  p <- ggplot(plot_data, aes(x = log2FoldChange, y = neg_log10_padj)) +
    # 背景：所有基因
    geom_point(data = plot_data[plot_data$category == "Stable", ], 
               color = "grey70", alpha = 0.5, size = 1) +
    # 上调
    geom_point(data = plot_data[plot_data$category == "Up", ], 
               color = "#E64B35", alpha = 0.7, size = 1.5) +
    # 下调
    geom_point(data = plot_data[plot_data$category == "Down", ], 
               color = "#4DBBD5", alpha = 0.7, size = 1.5) +
    # 阈值线
    geom_hline(yintercept = -log10(padj_threshold), linetype = "dashed", color = "grey40") +
    geom_vline(xintercept = log2fc_threshold, linetype = "dashed", color = "grey40") +
    geom_vline(xintercept = -log2fc_threshold, linetype = "dashed", color = "grey40") +
    # 标注top基因
    geom_text(data = label_data, aes(label = gene), 
              size = 3, hjust = -0.1, vjust = 0.5, check_overlap = TRUE) +
    # 标签和主题
    labs(
      title = "Volcano Plot - DESeq2 Results",
      x = "log2(Fold Change)",
      y = "-log10(adjusted p-value)",
      subtitle = paste0("Up: ", up_count, " | Down: ", down_count, " | padj<", padj_threshold, " | |log2FC|>", log2fc_threshold)
    ) +
    theme_classic() +
    theme(
      plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
      plot.subtitle = element_text(hjust = 0.5, size = 10, color = "grey40"),
      axis.title = element_text(size = 12),
      legend.position = "none"
    ) +
    # 限制显示范围（避免极端值拉长图）
    coord_cartesian(xlim = c(max(-10, min(plot_data$log2FoldChange)), min(10, max(plot_data$log2FoldChange))))
  
  # 保存图片
  output_img <- paste0(tools::file_path_sans_ext(csv_path), "_volcano.", img_format)
  
  if (img_format == "png") {
    ggsave(output_img, p, width = 10, height = 8, dpi = 300)
  } else if (img_format == "pdf") {
    ggsave(output_img, p, width = 10, height = 8)
  } else if (img_format == "tiff") {
    ggsave(output_img, p, width = 10, height = 8, dpi = 300, compression = "lzw")
  }
  
  cat("  ✅ 火山图已保存:", output_img, "\n")
}

cat("\n  ✅ DESeq2结果格式化完成！\n")