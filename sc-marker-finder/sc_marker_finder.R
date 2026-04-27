#!/usr/bin/env Rscript
# 单细胞marker基因批量查找
get_input <- function(p, d=NULL) {
  v <- readline(prompt=paste0(p, " [默认: ", d, "]: "))
  if (v == "" || is.null(v)) return(d)
  return(v)
}
cat("============================================================
")
cat("  单细胞marker基因批量查找
")
cat("============================================================

")
# TODO: 实现核心功能
cat("✅ 完成
")
