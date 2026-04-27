#!/usr/bin/env Rscript
# 基因表达与生存关联分析
suppressPackageStartupMessages({
  if (!require(survival)) { cat("需要survival\n"); quit(status=1) }
  if (!require(survminer)) { cat("需要survminer\n"); quit(status=1) }
  library(ggplot2)
})

get_input <- function(prompt, default = NULL) {
  val <- readline(prompt = paste0(prompt, " [默认: ", default, "]: "))
  if (val == "" || is.null(val)) return(default); return(val)
}

cat("============================================================\n")
cat("  📈 生存表达关联分析\n")
cat("============================================================\n\n")

expr_path <- get_input("表达矩阵CSV路径(行=基因,列=样本)", "expression.csv")
clin_path <- get_input("临床数据CSV路径(含OS时间+事件)", "clinical.csv")
genes_str <- get_input("候选基因(逗号分隔)", "BRCA1,BRCA2,TP53")
group_method <- get_input("分组方法(median/quantile/optimal)", "median")
make_km <- get_input("是否出KM曲线(yes/no)", "yes")

expr <- as.matrix(read.csv(expr_path, row.names = 1))
clin <- read.csv(clin_path, row.names = 1)
genes <- strsplit(genes_str, ",")[[1]]

results <- data.frame(gene=character(), p.value=numeric(), HR=numeric(), n_low=integer(), n_high=integer())

for (gene in genes) {
  if (!(gene %in% rownames(expr))) { cat("⚠", gene, "不存在\n"); continue }
  expr_vals <- expr[gene, ]
  if (group_method == "median") {
    group <- ifelse(expr_vals > median(expr_vals), "High", "Low")
  } else if (group_method == "quantile") {
    q75 <- quantile(expr_vals, 0.75); q25 <- quantile(expr_vals, 0.25)
    group <- ifelse(expr_vals > q75, "High", ifelse(expr_vals < q25, "Low", "Mid"))
    group[group == "Mid"] <- NA
  } else {
    # optimal cutpoint用surv_cutpoint
    if (require(survminer)) {
      cut <- surv_cutpoint(clin, time = "OS_time", event = "OS_event", variable = gene)
      group <- ifelse(expr_vals > cut$cutpoint$cutpoint, "High", "Low")
    } else { group <- ifelse(expr_vals > median(expr_vals), "High", "Low") }
  }
  
  clin$group <- group[rownames(clin)]
  clin_sub <- clin[!is.na(clin$group), ]
  
  fit <- survfit(Surv(OS_time, OS_event) ~ group, data = clin_sub)
  sdiff <- survdiff(Surv(OS_time, OS_event) ~ group, data = clin_sub)
  p_val <- format.pval(pchisq(sdiff$chisq, df = 1, lower.tail = FALSE), digits = 3)
  HR <- exp(coef(coxph(Surv(OS_time, OS_event) ~ group, data = clin_sub)))
  
  results <- rbind(results, data.frame(gene=gene, p.value=p_val, HR=HR,
                                        n_low=sum(clin_sub$group=="Low"), n_high=sum(clin_sub$group=="High")))
  
  if (make_km == "yes" || make_km == "y") {
    p <- ggsurvplot(fit, data = clin_sub, pval = TRUE, risk.table = TRUE,
                    title = paste0("KM曲线 - ", gene),
                    palette = c("#E64B35", "#4DBBD5"))
    ggsave(paste0("KM_", gene, ".png"), p$plot, width = 8, height = 6, dpi = 300)
  }
}

write.csv(results, "survival_results.csv", row.names = FALSE)
cat("✅ 生存分析完成: survival_results.csv\n")
cat("   分析基因数:", nrow(results), "\n")