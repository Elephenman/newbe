---
tags:
  - tidyverse
  - R
  - 数据处理
  - 可视化
  - 实战代码
  - 一键运行
aliases:
  - tidyverse代码库
  - dplyr速查
  - ggplot2实战
  - R数据处理宝典
created: 2026-04-20
updated: 2026-04-20
version: tidyverse 2.x
description: R语言tidyverse生态实战级代码库，涵盖dplyr/ggplot2/tidyr/readr/purrr/stringr/forcats，封装函数+生信场景，改参数即跑
---

# 📊 Tidyverse 实战代码库

> **定位**：复制→改参数→直接跑。覆盖生信数据处理90%场景，从数据清洗到发文级可视化。
> 包含 **dplyr**（数据处理）+ **ggplot2**（可视化）+ **tidyr**（整洁数据）+ **purrr**（函数式编程）+ **stringr**（字符串）+ **forcats**（因子）+ **readr**（读取）。

---

## 📑 快速导航

| 需求 | 跳转 |
|------|------|
| 环境安装 | [[#📦 环境安装]] |
| 数据读取与导出 | [[#📂 数据读取与导出]] |
| dplyr 数据处理 | [[#🔧 dplyr 数据处理核心]] |
| tidyr 数据整形 | [[#🔄 tidyr 数据整形]] |
| stringr 字符串处理 | [[#✂️ stringr 字符串处理]] |
| forcats 因子处理 | [[#🎭 forcats 因子处理]] |
| purrr 函数式编程 | [[#🔁 purrr 函数式编程]] |
| ggplot2 基础可视化 | [[#🎨 ggplot2 基础可视化体系]] |
| ggplot2 发文级模板 | [[#🏆 ggplot2 发文级模板]] |
| 生信实战场景 | [[#🧬 生信实战场景封装]] |
| 一键处理流水线 | [[#🚀 一键数据处理流水线]] |
| 函数速查表 | [[#📋 函数速查表]] |

---

## 📦 环境安装

```r
# ============================================================
# tidyverse 全家桶安装 + 生信常用扩展
# ============================================================
install_if_missing <- function(pkgs, bio = FALSE) {
  for (pkg in pkgs) {
    if (!requireNamespace(pkg, quietly = TRUE)) {
      cat("安装:", pkg, "\n")
      if (bio) {
        BiocManager::install(pkg, ask = FALSE, update = FALSE)
      } else {
        install.packages(pkg)
      }
    } else {
      cat("✅", pkg, as.character(packageVersion(pkg)), "\n")
    }
  }
}

# 核心包（一次装齐）
install.packages("tidyverse")  # 包含 dplyr/ggplot2/tidyr/purrr/stringr/forcats/readr/tibble

# 生信增强包
install_if_missing(c(
  "readxl", "writexl", "haven",         # 数据读取
  "ggpubr", "ggsci", "ggrepel",          # 可视化增强
  "patchwork", "cowplot",                 # 拼图
  "scales", "viridis", "RColorBrewer",   # 配色
  "broom", "modelr",                      # 建模
  "janitor",                              # 数据清洗
  "glue"                                  # 字符串胶水
))

# 加载
library(tidyverse)   # 一行加载全部
library(ggpubr)      # 发文级统计图
library(ggsci)       # SCI配色
library(patchwork)   # 拼图
library(ggrepel)     # 标签防重叠
library(janitor)     # 清洗工具
```

---

## 📂 数据读取与导出

```r
# ============================================================
# 通用读取函数 —— 自动识别格式
# ============================================================
smart_read <- function(file, sheet = 1, ...) {
  ext <- tolower(tools::file_ext(file))
  switch(ext,
    csv  = readr::read_csv(file, ...),
    tsv  = readr::read_tsv(file, ...),
    txt  = readr::read_tsv(file, ...),
    xlsx = readxl::read_excel(file, sheet = sheet, ...),
    xls  = readxl::read_excel(file, sheet = sheet, ...),
    rds  = readRDS(file),
    rdata = {load(file); get(ls()[1])},
    stop("不支持的格式: ", ext)
  )
}

# 使用示例
# df <- smart_read("counts.csv")
# df <- smart_read("data.xlsx", sheet = "Sheet1")
# df <- smart_read("results.tsv")

# ============================================================
# 通用导出函数 —— 按扩展名自动选格式
# ============================================================
smart_write <- function(df, file, ...) {
  ext <- tolower(tools::file_ext(file))
  switch(ext,
    csv  = readr::write_csv(df, file, ...),
    tsv  = readr::write_tsv(df, file, ...),
    xlsx = writexl::write_xlsx(df, file, ...),
    rds  = saveRDS(df, file),
    stop("不支持的格式: ", ext)
  )
  cat("✅ 已保存:", file, "\n")
}

# ============================================================
# 批量读取同一目录下的文件
# ============================================================
batch_read <- function(dir_path, pattern = "\\.csv$", bind = TRUE, ...) {
  files <- list.files(dir_path, pattern = pattern, full.names = TRUE)
  if (length(files) == 0) stop("未找到匹配文件")
  
  cat("找到", length(files), "个文件\n")
  dfs <- purrr::map(files, ~ smart_read(.x, ...))
  names(dfs) <- basename(files)
  
  if (bind) {
    # 添加来源列后合并
    dfs <- purrr::imap_dfr(dfs, ~ dplyr::mutate(.x, source_file = .y))
  }
  dfs
}

# 使用示例
# all_samples <- batch_read("./counts/", pattern = "\\.csv$")

# ============================================================
# 读取常见生信格式
# ============================================================

# 读取 GTF/GFF 基因注释
read_gtf <- function(file) {
  readr::read_tsv(file, comment = "#",
    col_names = c("seqname","source","feature","start","end","score","strand","frame","attribute"),
    col_types = cols(.default = "c", start = "i", end = "i")
  ) %>%
    tidyr::separate_rows(attribute, sep = ";") %>%
    tidyr::separate(attribute, into = c("key", "value"), sep = "=", fill = "right") %>%
    dplyr::mutate(key = stringr::str_trim(key), value = stringr::str_trim(value)) %>%
    tidyr::pivot_wider(names_from = key, values_from = value)
}

# 读取 GSEA 的 GMT 基因集文件
read_gmt <- function(file) {
  lines <- readr::read_lines(file)
  purrr::map_dfr(lines, function(line) {
    parts <- stringr::str_split(line, "\\t")[[1]]
    tibble(geneset = parts[1], description = parts[2], gene = parts[-(1:2)])
  })
}

# 读取 FASTA 文件为 tibble
read_fasta <- function(file) {
  lines <- readr::read_lines(file)
  is_header <- stringr::str_detect(lines, "^>")
  headers <- lines[is_header]
  sequences <- lines[!is_header]
  
  # 简化版：假设单行序列
  tibble(
    header = stringr::str_remove(headers, "^>"),
    sequence = sequences
  )
}
```

---

## 🔧 dplyr 数据处理核心

### 1. 筛选：filter / slice

```r
# ============================================================
# filter —— 行筛选（保留满足条件的行）
# ============================================================

# 基础筛选
df %>% filter(gene == "TP53")                     # 精确匹配
df %>% filter(pvalue < 0.05)                      # 数值条件
df %>% filter(log2FC > 1 | log2FC < -1)           # 或条件
df %>% filter(log2FC > 1 & pvalue < 0.05)         # 且条件

# 多值匹配
df %>% filter(gene %in% c("TP53", "BRCA1", "EGFR"))   # in 匹配
df %>% filter(!gene %in% c("ACTB", "GAPDH"))           # 排除

# 模糊匹配
df %>% filter(str_detect(gene, "^MT-"))           # 正则匹配
df %>% filter(str_detect(pathway, "immune"))       # 包含某字符串
df %>% filter(str_detect(gene, "^RP[SL]"))         # 核糖体基因

# 缺失值处理
df %>% filter(!is.na(pvalue))                     # 去除NA
df %>% filter(complete.cases(across(everything()))) # 全列无NA

# 数值范围
df %>% filter(between(log2FC, -2, 2))             # 范围筛选
df %>% filter(near(pvalue, 0.05, tol = 0.001))    # 近似等于

# 按分组筛选 top N
df %>% group_by(cluster) %>% filter(row_number() <= 10)   # 每组前10行
df %>% group_by(cluster) %>% filter(avg_log2FC == max(avg_log2FC))  # 每组最大值

# ============================================================
# slice —— 按位置选行
# ============================================================
df %>% slice(1:10)                     # 前10行
df %>% slice_head(n = 5)               # 头5行
df %>% slice_tail(n = 5)               # 尾5行
df %>% slice_sample(n = 100)           # 随机抽100行
df %>% slice_max(avg_log2FC, n = 10)   # 最大的10行
df %>% slice_min(pvalue, n = 10)       # 最小的10行

# 分组取 top N
df %>% group_by(cluster) %>% slice_max(avg_log2FC, n = 5) %>% ungroup()
```

### 2. 选择列：select / relocate / rename

```r
# ============================================================
# select —— 列选择
# ============================================================

# 基础
df %>% select(gene, log2FC, pvalue)               # 选指定列
df %>% select(-c(1:3))                            # 排除前3列
df %>% select(!c(contains("raw")))                # 排除含raw的列

# 辅助函数
df %>% select(starts_with("nCount"))              # 前缀匹配
df %>% select(ends_with("_score"))                # 后缀匹配
df %>% select(contains("RNA"))                    # 包含匹配
df %>% select(matches("^PC\\d+$"))                # 正则匹配
df %>% select(num_range("PC", 1:10))              # PC1-PC10
df %>% select(where(is.numeric))                  # 所有数值列
df %>% select(where(is.character))                # 所有字符列

# everything() 排列顺序
df %>% select(gene, log2FC, everything())         # 关键列放前面

# ============================================================
# rename / relocate
# ============================================================
df %>% rename(avg_log2FC = avg_logFC)              # 重命名
df %>% rename_with(toupper)                        # 全部大写
df %>% rename_with(~str_replace(.x, "\\.", "_"))   # 点替换为下划线

df %>% relocate(celltype, .before = 1)             # 移到第一列
df %>% relocate(starts_with("PC"), .after = gene)  # PC列移到gene后面
```

### 3. 新增列：mutate / transmute

```r
# ============================================================
# mutate —— 新增/修改列（核心函数，最常用）
# ============================================================

# 基础运算
df %>% mutate(fold_change = 2^log2FC)                      # 转换
df %>% mutate(sig = ifelse(pvalue < 0.05, "yes", "no"))   # 条件判断
df %>% mutate(direction = case_when(
  log2FC > 1 & pvalue < 0.05 ~ "up",
  log2FC < -1 & pvalue < 0.05 ~ "down",
  TRUE ~ "ns"
))

# 生信常用
df %>% mutate(nlog10p = -log10(pvalue))                    # 火山图y轴
df %>% mutate(gene_label = ifelse(abs(log2FC) > 2, gene, ""))  # 标签列

# 分组运算（超常用）
df %>% group_by(cluster) %>%
  mutate(z_score = scale(avg_log2FC)[,1]) %>%              # 组内Z-score
  ungroup()

df %>% group_by(cluster) %>%
  mutate(pct_within = n / sum(n)) %>%                      # 组内百分比
  ungroup()

df %>% group_by(cluster) %>%
  mutate(rank = row_number(desc(avg_log2FC))) %>%          # 组内排名
  ungroup()

# 多列同时运算
df %>% mutate(across(contains("count"), ~ .x / sum(.x) * 100))  # 所有count列转百分比
df %>% mutate(across(where(is.numeric), ~ replace_na(.x, 0)))   # 所有数值列NA填0
df %>% mutate(across(where(is.numeric), scale))                 # 所有数值列标准化

# 条件式多列运算
df %>% mutate(across(starts_with("PC"), ~ .x * 100, .names = "{.col}_pct"))
# 原列保留，新列 PC1_pct, PC2_pct ...

# ============================================================
# transmute —— 只保留新创建的列
# ============================================================
df %>% transmute(gene_id = gene, log2FC, sig = pvalue < 0.05)
```

### 4. 汇总：summarise / count

```r
# ============================================================
# summarise —— 分组汇总
# ============================================================

# 单变量
df %>% summarise(mean_fc = mean(log2FC, na.rm = TRUE))
df %>% summarise(med = median(log2FC), sd = sd(log2FC))

# 分组汇总（最常用模式）
df %>% group_by(cluster) %>%
  summarise(
    n = n(),                                    # 计数
    mean_fc = mean(log2FC, na.rm = TRUE),       # 均值
    median_fc = median(log2FC, na.rm = TRUE),   # 中位数
    sd_fc = sd(log2FC, na.rm = TRUE),           # 标准差
    n_up = sum(log2FC > 0),                     # 上调数
    n_sig = sum(pvalue < 0.05),                 # 显著数
    top_gene = gene[which.max(avg_log2FC)],      # top基因
    .groups = "drop"
  )

# 多列汇总
df %>% group_by(cluster) %>%
  summarise(across(where(is.numeric), list(mean = mean, sd = sd), na.rm = TRUE))

# ============================================================
# count —— 快速计数
# ============================================================
df %>% count(cluster)                            # 等价于 group_by + summarise(n=n())
df %>% count(cluster, sort = TRUE)               # 按频次排序
df %>% count(cluster, direction)                 # 交叉计数
df %>% count(cluster, wt = nCount_RNA)           # 加权计数（求和）

# 比例
df %>% count(cluster) %>% mutate(pct = n / sum(n) * 100)

# 累积计数
df %>% count(cluster) %>% mutate(cum_n = cumsum(n))
```

### 5. 排序与去重

```r
# ============================================================
# arrange —— 排序
# ============================================================
df %>% arrange(desc(log2FC))                     # 降序
df %>% arrange(pvalue, desc(log2FC))             # 多列排序
df %>% arrange(cluster, desc(avg_log2FC))        # 组内排序

# ============================================================
# distinct / anti_join / semi_join —— 去重与连接过滤
# ============================================================
df %>% distinct(gene, .keep_all = TRUE)          # 按列去重保留首个
df %>% distinct()                                 # 完全去重

# 取两个数据框的差集/交集
anti_df <- df1 %>% anti_join(df2, by = "gene")   # df1中有但df2中没有
semi_df <- df1 %>% semi_join(df2, by = "gene")   # df1中也在df2中的
```

### 6. 连接：join 系列

```r
# ============================================================
# join —— 表连接（生信极常用）
# ============================================================

# 四种连接
df1 %>% inner_join(df2, by = "gene")             # 交集
df1 %>% left_join(df2, by = "gene")              # 左连接（保留左表所有行）
df1 %>% right_join(df2, by = "gene")             # 右连接
df1 %>% full_join(df2, by = "gene")              # 全连接

# 多列连接
df1 %>% left_join(df2, by = c("gene_id" = "ensembl_id"))

# 列名不同时连接
df1 %>% left_join(df2, by = c("gene" = "symbol"))

# 连接后处理重复列名
df1 %>% left_join(df2, by = "gene", suffix = c("_ctrl", "_treat"))

# 批量连接（连接多个表）
purrr::reduce(list(df1, df2, df3), ~ left_join(.x, .y, by = "gene"))
```

### 7. 窗口函数

```r
# ============================================================
# 窗口函数 —— 排名、累积、偏移
# ============================================================

# 排名
df %>% mutate(rank = row_number(desc(log2FC)))        # 不并列
df %>% mutate(rank = min_rank(desc(log2FC)))          # 跳跃排名
df %>% mutate(rank = dense_rank(desc(log2FC)))        # 连续排名
df %>% mutate(ntile = ntile(desc(log2FC), 4))         # 四分位分组

# 累积
df %>% mutate(cum_sum = cumsum(n))
df %>% mutate(cum_max = cummax(log2FC))
df %>% mutate(run_avg = slider::slide_dbl(log2FC, mean, .before = 2, .after = 2))

# 偏移
df %>% mutate(prev = lag(log2FC))                     # 前一行
df %>% mutate(next = lead(log2FC))                    # 后一行
df %>% mutate(diff = log2FC - lag(log2FC))            # 差分
```

### 8. 封装：生信数据处理工具箱

```r
# ============================================================
# auto_diff_filter —— 自动筛选差异基因
# ============================================================
auto_diff_filter <- function(df,
                              gene_col = "gene",
                              fc_col = "log2FoldChange",
                              pval_col = "pvalue",
                              padj_col = "padj",
                              fc_cutoff = 1,
                              padj_cutoff = 0.05) {
  
  df %>%
    filter(!is.na(!!sym(padj_col))) %>%
    mutate(direction = case_when(
      !!sym(fc_col) > fc_cutoff & !!sym(padj_col) < padj_cutoff ~ "up",
      !!sym(fc_col) < -fc_cutoff & !!sym(padj_col) < padj_cutoff ~ "down",
      TRUE ~ "ns"
    )) %>%
    mutate(label = ifelse(direction != "ns", !!sym(gene_col), ""))
}

# 使用示例
# degs <- auto_diff_filter(results_df, fc_cutoff = 1, padj_cutoff = 0.05)

# ============================================================
# auto_annotation_map —— 自动匹配基因注释
# ============================================================
auto_annotate <- function(gene_list,
                           from_type = "SYMBOL",
                           to_type = c("ENTREZID", "ENSEMBL", "GENENAME"),
                           species = "human") {
  
  pkg <- if (species == "human") "org.Hs.eg.db" else "org.Mm.eg.db"
  if (!requireNamespace(pkg, quietly = TRUE)) {
    BiocManager::install(pkg, ask = FALSE)
  }
  
  AnnotationDbi::bitr(gene_list,
    fromType = from_type,
    toType = to_type,
    OrgDb = pkg
  )
}

# 使用示例
# ids <- auto_annotate(c("TP53", "BRCA1", "EGFR"), to_type = c("ENTREZID", "ENSEMBL"))

# ============================================================
# auto_expression_matrix —— 表达矩阵标准化
# ============================================================
auto_normalize_matrix <- function(mat, method = "cpm") {
  library_size <- colSums(mat)
  
  switch(method,
    cpm = t(t(mat) / library_size * 1e6),
    tpm = { # 需要基因长度信息
      warning("TPM需要基因长度，请确保已提供")
      t(t(mat) / library_size * 1e6)
    },
    rpkm = t(t(mat) / library_size * 1e6),
    log2cpm = {
      cpm <- t(t(mat) / library_size * 1e6)
      log2(cpm + 1)
    },
    zscore = t(scale(t(mat))),
    quantile = {
      preprocessCore::normalize.quantiles(as.matrix(mat))
    },
    stop("不支持的方法: ", method)
  )
}

# ============================================================
# batch_bind_rows —— 批量合并数据框（自动添加来源标识）
# ============================================================
batch_bind_rows <- function(df_list, id_col = "sample") {
  purrr::imap_dfr(df_list, ~ mutate(.x, !!id_col := .y))
}

# ============================================================
# auto_outlier_remove —— MAD法自动去除离群值
# ============================================================
auto_outlier_remove <- function(df, col, k = 3, group_col = NULL) {
  if (is.null(group_col)) {
    med <- median(df[[col]], na.rm = TRUE)
    mad_val <- mad(df[[col]], na.rm = TRUE)
    df %>% filter(between(!!sym(col), med - k * mad_val, med + k * mad_val))
  } else {
    df %>%
      group_by(!!sym(group_col)) %>%
      filter(between(!!sym(col),
                     median(!!sym(col), na.rm = TRUE) - k * mad(!!sym(col), na.rm = TRUE),
                     median(!!sym(col), na.rm = TRUE) + k * mad(!!sym(col), na.rm = TRUE))) %>%
      ungroup()
  }
}

# ============================================================
# quick_summary —— 数据框快速概览
# ============================================================
quick_summary <- function(df, group_col = NULL) {
  if (is.null(group_col)) {
    df %>%
      summarise(across(where(is.numeric), list(
        min = ~min(.x, na.rm = TRUE),
        median = ~median(.x, na.rm = TRUE),
        mean = ~mean(.x, na.rm = TRUE),
        max = ~max(.x, na.rm = TRUE),
        sd = ~sd(.x, na.rm = TRUE),
        n_missing = ~sum(is.na(.x))
      ))) %>%
      pivot_longer(everything(), names_to = c("variable", ".value"), names_sep = "_")
  } else {
    df %>%
      group_by(!!sym(group_col)) %>%
      summarise(across(where(is.numeric), list(
        mean = ~mean(.x, na.rm = TRUE),
        sd = ~sd(.x, na.rm = TRUE),
        n = ~sum(!is.na(.x))
      ), .names = "{.col}_{.fn}")) %>%
      ungroup()
  }
}
```

---

## 🔄 tidyr 数据整形

```r
# ============================================================
# pivot_longer —— 宽变长（生信最常用）
# ============================================================

# 基础：表达矩阵宽→长
# 原始: gene | sample1 | sample2 | sample3
# 目标: gene | sample | expression
expr_long <- expr_wide %>%
  pivot_longer(
    cols = -gene,                    # 除了gene列都转
    names_to = "sample",
    values_to = "expression"
  )

# 多列同时转换
# 原始: gene | ctrl_mean | ctrl_sd | treat_mean | treat_sd
# 目标: gene | group | mean | sd
df_long <- df_wide %>%
  pivot_longer(
    cols = -gene,
    names_to = c("group", ".value"),    # .value保留原列名
    names_sep = "_"
  )

# 正则提取列名信息
# 原始: gene | ctrl_24h | ctrl_48h | treat_24h | treat_48h
df_long <- df_wide %>%
  pivot_longer(
    cols = -gene,
    names_to = c("treatment", "time"),
    names_pattern = "(.*)_(.*)",
    values_to = "expression"
  )

# ============================================================
# pivot_wider —— 长变宽
# ============================================================

# 基础
expr_wide <- expr_long %>%
  pivot_wider(
    names_from = sample,
    values_from = expression
  )

# 聚合后再变宽
df_wide <- df_long %>%
  group_by(gene, cluster) %>%
  summarise(mean_exp = mean(expression, na.rm = TRUE), .groups = "drop") %>%
  pivot_wider(
    names_from = cluster,
    values_from = mean_exp,
    names_prefix = "cluster_"
  )

# ============================================================
# separate / unite —— 拆分与合并列
# ============================================================

# 拆分
df %>% separate(col, into = c("chr", "pos"), sep = ":")        # 按分隔符
df %>% separate(col, into = c("pre", "suf"), sep = -4)         # 按位置
df %>% separate(sample, into = c("treatment", "rep"), sep = "_") # "ctrl_1" → "ctrl", "1"

# 合并
df %>% unite("new_col", c("chr", "pos"), sep = ":")            # 合并为 "chr1:12345"
df %>% unite("sample_id", c("treatment", "rep"), sep = "_")    # "ctrl_1"

# ============================================================
# complete / fill / replace_na —— 填充缺失
# ============================================================

# 补全所有组合
df %>% complete(gene, cluster)                   # 补全 gene × cluster 的所有组合

# 前向填充
df %>% arrange(gene) %>% fill(expression)        # NA用前一个非NA值填充

# 指定值填充
df %>% replace_na(list(expression = 0, pvalue = 1))

# ============================================================
# nest / unnest —— 嵌套操作
# ============================================================

# 嵌套：每个组变成一个tibble列
nested <- df %>% nest(data = -cluster)
# cluster | data
# 0       | <tibble [100×5]>
# 1       | <tibble [80×5]>

# 在嵌套数据上操作
nested %>%
  mutate(cor_test = map(data, ~ cor.test(.x$gene1, .x$gene2))) %>%
  mutate(tidy = map(cor_test, broom::tidy)) %>%
  unnest(tidy)

# 反嵌套
nested %>% unnest(data)

# ============================================================
# 封装：宽长转换工具
# ============================================================

# 表达矩阵 ↔ 长格式 一键转换
expr_to_long <- function(mat, gene_col = "gene") {
  if (is.matrix(mat)) mat <- as.data.frame(mat)
  if (!gene_col %in% names(mat)) {
    mat[[gene_col]] <- rownames(mat)
    rownames(mat) <- NULL
  }
  pivot_longer(mat, -!!sym(gene_col), names_to = "sample", values_to = "expression")
}

expr_to_wide <- function(df, gene_col = "gene", sample_col = "sample", value_col = "expression") {
  pivot_wider(df, names_from = !!sym(sample_col), values_from = !!sym(value_col)) %>%
    column_to_rownames(gene_col) %>%
    as.matrix()
}
```

---

## ✂️ stringr 字符串处理

```r
# ============================================================
# 基础操作
# ============================================================
str_detect("TP53", "P53")           # 是否匹配 → TRUE
str_which(c("TP53","BRCA1"), "P53") # 匹配位置 → 1
str_count("ATCGATCG", "AT")         # 匹配次数 → 2
str_locate("chr1:12345", ":")       # 匹配位置 → 5 5
str_extract("chr1:12345", "\\d+")   # 提取匹配 → "1"
str_extract_all("chr1:12345", "\\d+")  # 全部提取 → c("1","12345")

# 替换
str_replace("TP53", "P", "p")      # 替换第一个 → "Tp53"
str_replace_all("ATCG", "A|T", "X") # 替换全部 → "XXCG"
str_remove("gene_name", "_name")   # 删除匹配 → "gene"
str_remove_all("AATTCC", "A|T")    # 删除全部 → "CC"

# 截取
str_sub("TP53", 1, 2)              # 子串 → "TP"
str_sub("TP53", -2, -1)            # 尾部 → "53"

# 分割
str_split("chr1:12345-12600", ":")  # → c("chr1","12345-12600")
str_split_fixed("chr1:12345", ":", 2) # → matrix 2列

# 长度与大小写
str_length("TP53")                  # → 4
str_to_upper("tp53")               # → "TP53"
str_to_lower("TP53")               # → "tp53"
str_to_title("tp53")               # → "Tp53"

# 去除空白
str_trim("  TP53  ")               # → "TP53"
str_squish("  TP  53  ")           # → "TP 53"（多个空格变一个）

# ============================================================
# 生信常用字符串处理
# ============================================================

# 基因ID转换
str_replace("ENSG00000141510", "ENSG", "Gene")   # Ensembl → 自定义前缀
str_extract("ENST00000012345.5", "ENST\\d+")      # 去版本号
str_remove("TP53-1", "-\\d+$")                     # 去转录本后缀

# 染色体名标准化
chr_standardize <- function(chr) {
  chr %>%
    str_replace("chr", "") %>%
    str_replace("X", "23") %>%
    str_replace("Y", "24") %>%
    str_replace("MT", "25") %>%
    str_replace("M", "25")
}

# 从GTF attribute中提取gene_name
extract_gene_name <- function(attribute_str) {
  str_match(attribute_str, 'gene_name "([^"]+)"')[, 2]
}

# FASTA header 解析
parse_fasta_header <- function(header) {
  header %>%
    str_remove("^>") %>%
    str_split("\\|") %>%
    purrr::map(~ tibble(
      accession = .x[1],
      gene = ifelse(length(.x) > 2, .x[3], NA),
      description = ifelse(length(.x) > 4, .x[5], NA)
    )) %>%
    bind_rows()
}

# 向量化字符串处理
df %>%
  mutate(gene_short = str_extract(gene_id, "^[^.]+")) %>%    # 去版本号
  mutate(chromosome = str_remove(chrom, "^chr")) %>%          # 去chr前缀
  filter(str_detect(gene, "^RP[SL]", negate = TRUE))         # 排除核糖体基因
```

---

## 🎭 forcats 因子处理

```r
# ============================================================
# 因子排序（生信可视化核心！）
# ============================================================

# 手动指定顺序
df %>% mutate(cluster = fct_relevel(cluster, "T cells", "B cells", "Mono"))

# 按另一列排序
df %>% mutate(gene = fct_reorder(gene, avg_log2FC))               # 按值升序
df %>% mutate(gene = fct_reorder(gene, avg_log2FC, .desc = TRUE)) # 按值降序
df %>% mutate(cluster = fct_reorder(cluster, n, .fun = sum))      # 按汇总值

# 按首次出现排序
df %>% mutate(cluster = fct_inorder(cluster))

# 按频次排序
df %>% mutate(celltype = fct_infreq(celltype))

# ============================================================
# 因子合并与重编码
# ============================================================

# 合并小类别为"Other"
df %>% mutate(celltype = fct_lump_n(celltype, n = 8))            # 保留前8类
df %>% mutate(celltype = fct_lump_min(celltype, min = 50))       # 保留≥50的类
df %>% mutate(celltype = fct_lump_prop(celltype, prop = 0.05))   # 保留≥5%的类

# 重编码
df %>% mutate(phase = fct_recode(phase,
  "G1_phase" = "G1",
  "S_phase" = "S",
  "G2M_phase" = "G2M"
))

# 反转因子顺序
df %>% mutate(gene = fct_rev(gene))

# 丢弃未使用的水平
df %>% mutate(cluster = fct_drop(cluster))
```

---

## 🔁 purrr 函数式编程

```r
# ============================================================
# map 系列 —— 向量化操作（替代for循环）
# ============================================================

# 基础 map
map(1:3, ~ .x * 10)                     # list(10, 20, 30)
map_dbl(1:3, ~ .x * 10)                 # double向量 c(10, 20, 30)
map_int(1:3, ~ .x * 10)                 # integer向量
map_chr(c("TP53","BRCA1"), ~ str_sub(.x, 1, 2))  # 字符向量
map_lgl(c(1, NA, 3), ~ !is.na(.x))      # 逻辑向量

# map2 —— 两个输入
map2_dbl(c(1,2,3), c(10,20,30), ~ .x + .y)  # c(11, 22, 33)

# pmap —— 多个输入
pmap_dfr(list(a = 1:3, b = 4:6, c = 7:9), function(a, b, c) {
  tibble(sum = a + b + c, prod = a * b * c)
})

# walk —— 副作用（保存文件等，不返回值）
walk(file_list, ~ ggsave(paste0(.x, ".png"), plot = my_plot))

# ============================================================
# 生信常用：批量处理样本
# ============================================================

# 批量读取 + 处理
sample_files <- list.files("./data/", pattern = "\\.csv$", full.names = TRUE)
names(sample_files) <- basename(sample_files)

all_data <- map(sample_files, ~ read_csv(.x, show_col_types = FALSE)) %>%
  map2(names(.), ~ mutate(.x, sample = .y)) %>%
  list_rbind()

# 批量做统计检验
results <- df %>%
  group_by(gene) %>%
  nest() %>%
  mutate(test = map(data, ~ t.test(.x$control, .x$treatment))) %>%
  mutate(tidy = map(test, broom::tidy)) %>%
  unnest(tidy) %>%
  select(gene, estimate, p.value, conf.low, conf.high)

# 批量出图（最常用！）
plot_list <- unique(df$cluster) %>%
  map(~ {
    df_sub <- filter(df, cluster == .x)
    ggplot(df_sub, aes(x = gene, y = expression)) +
      geom_boxplot() +
      ggtitle(.x)
  })

# 批量保存图
walk2(plot_list, names(plot_list),
      ~ ggsave(paste0(.y, ".pdf"), .x, width = 8, height = 6))

# ============================================================
# safely / possibly —— 容错处理
# ============================================================

# safely：捕获错误不中断
safe_t_test <- safely(t.test)
results <- map(data_list, safe_t_test)
# results[[1]]$result → 成功结果
# results[[1]]$error → NULL（成功时）或错误信息

# possibly：失败返回默认值
safe_cor <- possibly(cor, otherwise = NA)
cor_values <- map_dbl(gene_pairs, ~ safe_cor(expr[.x[1],], expr[.x[2],]))

# quietly：捕获输出和消息
quiet_read <- quietly(read_csv)
```

---

## 🎨 ggplot2 基础可视化体系

### 1. 基础模板

```r
# ============================================================
# ggplot2 七大图层
# ============================================================
# data      → 数据
# aesthetics → aes(x, y, color, fill, size, shape, group)
# geoms     → 几何对象（点、线、柱、箱线...）
# facets    → 分面
# stats     → 统计变换
# scales    → 标度（颜色、坐标轴）
# coords    → 坐标系
# theme     → 主题

# 通用模板
ggplot(data, aes(x = ..., y = ..., color = ...)) +
  geom_XXX(...) +          # 几何图层
  labs(title = "...", x = "...", y = "...") +  # 标签
  scale_color_XXX(...) +   # 颜色标度
  theme_XXX() +            # 主题
  facet_wrap(~group)       # 分面
```

### 2. 常用 geom 速查

```r
# ============================================================
# 散点图
# ============================================================
ggplot(df, aes(x = log2FC, y = -log10(pvalue))) +
  geom_point(aes(color = direction), size = 1, alpha = 0.6) +
  scale_color_manual(values = c(down = "blue", ns = "grey", up = "red"))

# 大数据散点（性能优化）
ggplot(big_df, aes(x, y)) +
  geom_point(size = 0.1, alpha = 0.3, shape = 16)   # 小尺寸+透明
# 或用 geom_hex / geom_bin2d 替代

# ============================================================
# 箱线图 + 小提琴图
# ============================================================
ggplot(df, aes(x = cluster, y = expression, fill = cluster)) +
  geom_violin(width = 0.8, alpha = 0.5) +
  geom_boxplot(width = 0.15, outlier.size = 0.5) +
  stat_compare_means(method = "wilcox.test", label = "p.signif")  # ggpubr统计

# 配对箱线图
ggplot(df, aes(x = timepoint, y = value, fill = group)) +
  geom_boxplot(position = position_dodge(0.8)) +
  geom_line(aes(group = patient_id), alpha = 0.3)    # 连线

# ============================================================
# 柱状图
# ============================================================
# 计数柱状图
ggplot(df, aes(x = celltype, fill = direction)) +
  geom_bar(position = "stack")                        # 堆叠
  # geom_bar(position = "fill")                       # 百分比堆叠
  # geom_bar(position = "dodge")                      # 并排

# 预计算柱状图
ggplot(summary_df, aes(x = celltype, y = mean_exp, fill = group)) +
  geom_col(position = position_dodge(0.8), width = 0.7) +
  geom_errorbar(aes(ymin = mean_exp - sd, ymax = mean_exp + sd),
                position = position_dodge(0.8), width = 0.25)

# ============================================================
# 折线图
# ============================================================
ggplot(df, aes(x = time, y = expression, color = gene, group = gene)) +
  geom_line(size = 1) +
  geom_point(size = 2)

# 平滑曲线
ggplot(df, aes(x = x, y = y)) +
  geom_smooth(method = "lm", se = TRUE, color = "red") +   # 线性拟合
  geom_smooth(method = "loess", se = TRUE, color = "blue")  # 局部回归

# ============================================================
# 热图（ggplot2版，替代pheatmap）
# ============================================================
ggplot(heatmap_df, aes(x = sample, y = gene, fill = expression)) +
  geom_tile() +
  scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# ============================================================
# 密度图
# ============================================================
ggplot(df, aes(x = expression, fill = cluster)) +
  geom_density(alpha = 0.5) +
  # geom_histogram(aes(y = after_stat(density)), bins = 50, alpha = 0.5)  # 直方图

# ============================================================
# 分面
# ============================================================
ggplot(df, aes(x = x, y = y)) +
  geom_point() +
  facet_wrap(~cluster, ncol = 3, scales = "free")       # 单变量分面
  # facet_grid(rows = vars(treatment), cols = vars(time))  # 双变量分面
```

### 3. 标度系统

```r
# ============================================================
# 颜色标度
# ============================================================

# 离散颜色
scale_color_manual(values = c("red", "blue", "green"))      # 手动
scale_color_brewer(palette = "Set1")                          # ColorBrewer
scale_color_npg()                                             # ggsci: Nature配色
scale_color_aaas()                                            # ggsci: Science配色
scale_color_lancet()                                          # ggsci: Lancet配色
scale_color_jco()                                             # ggsci: JCO配色
scale_color_igv()                                             # ggsci: IGV配色
scale_color_d3("category20")                                  # ggsci: D3配色

# 连续颜色
scale_color_gradient(low = "blue", high = "red")              # 两色渐变
scale_color_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0)  # 三色
scale_color_gradientn(colors = viridis::viridis(100))         # 多色渐变
scale_color_viridis_c()                                       # viridis色带

# ============================================================
# 坐标轴标度
# ============================================================
scale_x_log10()                                               # log10坐标
scale_y_continuous(breaks = seq(0, 100, 20), labels = scales::percent)  # 百分比
scale_x_discrete(limits = c("T cells", "B cells", "Mono"))   # 指定顺序
coord_flip()                                                   # 翻转
coord_fixed(ratio = 1)                                         # 等比例
xlim(0, 100) / ylim(0, 50)                                    # 范围限制

# ============================================================
# 大小 / 形状标度
# ============================================================
scale_size_continuous(range = c(1, 5))                        # 点大小范围
scale_shape_manual(values = c(16, 17, 15, 18))               # 点形状
```

### 4. 主题系统

```r
# ============================================================
# 内置主题
# ============================================================
theme_gray()        # 默认
theme_bw()          # 黑白边框（最常用）
theme_minimal()     # 极简
theme_classic()     # 经典（无网格线）
theme_void()        # 空白（适合地图/注释）
theme_dark()        # 深色背景

# ============================================================
# 自定义主题（发文级）
# ============================================================
theme_publication <- function(base_size = 12, base_family = "Arial") {
  theme_bw(base_size = base_size, base_family = base_family) +
    theme(
      # 标题
      plot.title = element_text(size = base_size + 2, face = "bold", hjust = 0.5),
      plot.subtitle = element_text(size = base_size, hjust = 0.5, color = "grey40"),
      # 坐标轴
      axis.title = element_text(size = base_size, face = "bold"),
      axis.text = element_text(size = base_size - 2, color = "black"),
      axis.line = element_line(color = "black", linewidth = 0.5),
      # 去除多余元素
      panel.grid.minor = element_blank(),
      panel.grid.major = element_line(color = "grey90", linewidth = 0.3),
      panel.border = element_rect(color = "black", linewidth = 0.5),
      # 图例
      legend.title = element_text(size = base_size - 1, face = "bold"),
      legend.text = element_text(size = base_size - 2),
      legend.position = "right",
      legend.background = element_rect(fill = "transparent"),
      # 分面
      strip.text = element_text(size = base_size - 1, face = "bold"),
      strip.background = element_rect(fill = "grey90"),
      # 边距
      plot.margin = margin(10, 10, 10, 10)
    )
}

# 使用
# ggplot(...) + theme_publication()
```

---

## 🏆 ggplot2 发文级模板

```r
# ============================================================
# 火山图 —— 标准发文级
# ============================================================
plot_volcano <- function(df,
                          fc_col = "log2FoldChange",
                          pval_col = "padj",
                          gene_col = "gene",
                          fc_cut = 1,
                          pval_cut = 0.05,
                          top_n = 10,
                          title = "Volcano Plot") {
  
  df <- df %>%
    mutate(
      sig = case_when(
        !!sym(fc_col) > fc_cut & !!sym(pval_col) < pval_cut ~ "Up",
        !!sym(fc_col) < -fc_cut & !!sym(pval_col) < pval_cut ~ "Down",
        TRUE ~ "NS"
      ),
      nlog10p = -log10(!!sym(pval_col))
    )
  
  # 自动标注 top 基因
  top_genes <- df %>%
    group_by(sig) %>%
    slice_max(order_by = !!sym(fc_col) * sign(!!sym(fc_col)), n = top_n) %>%
    ungroup() %>%
    filter(sig != "NS")
  
  ggplot(df, aes(x = !!sym(fc_col), y = nlog10p, color = sig)) +
    geom_point(size = 0.8, alpha = 0.5) +
    geom_point(data = filter(df, sig != "NS"), size = 1.2, alpha = 0.8) +
    ggrepel::geom_text_repel(
      data = top_genes,
      aes(label = !!sym(gene_col)),
      size = 3, max.overlaps = 20, color = "black"
    ) +
    geom_hline(yintercept = -log10(pval_cut), linetype = "dashed", color = "grey50") +
    geom_vline(xintercept = c(-fc_cut, fc_cut), linetype = "dashed", color = "grey50") +
    scale_color_manual(values = c(Down = "#2166AC", NS = "#BEBEBE", Up = "#B2182B")) +
    labs(title = title, x = expression(log[2]~Fold~Change), y = expression(-log[10](P[adj]))) +
    theme_publication() +
    theme(legend.position = "bottom")
}

# 使用: plot_volcano(degs, fc_col = "log2FoldChange", pval_col = "padj")

# ============================================================
# MA图
# ============================================================
plot_ma <- function(df,
                     base_mean_col = "baseMean",
                     fc_col = "log2FoldChange",
                     pval_col = "padj",
                     pval_cut = 0.05) {
  df %>%
    mutate(sig = !!sym(pval_col) < pval_cut) %>%
    ggplot(aes(x = log10(!!sym(base_mean_col) + 1),
               y = !!sym(fc_col), color = sig)) +
    geom_point(size = 0.5, alpha = 0.4) +
    scale_color_manual(values = c("grey60", "red3"), labels = c("NS", "Sig")) +
    geom_hline(yintercept = 0, linetype = "dashed") +
    labs(x = expression(log[10]~Mean~Expression), y = expression(log[2]~Fold~Change)) +
    theme_publication()
}

# ============================================================
# 表达热图（ggplot2版，轻量替代ComplexHeatmap）
# ============================================================
plot_heatmap <- function(mat, genes = NULL, samples = NULL,
                          cluster_rows = TRUE, cluster_cols = TRUE,
                          color_range = c("navy", "white", "firebrick3"),
                          show_rownames = TRUE, show_colnames = TRUE) {
  
  if (!is.null(genes)) mat <- mat[intersect(genes, rownames(mat)), ]
  if (!is.null(samples)) mat <- mat[, intersect(samples, colnames(mat))]
  
  # Z-score 标准化
  mat_scaled <- t(scale(t(mat)))
  
  # 聚类排序
  if (cluster_rows) {
    row_order <- hclust(dist(mat_scaled))$order
    mat_scaled <- mat_scaled[row_order, ]
  }
  if (cluster_cols) {
    col_order <- hclust(dist(t(mat_scaled)))$order
    mat_scaled <- mat_scaled[, col_order]
  }
  
  # 转长格式
  heatmap_df <- as.data.frame(mat_scaled) %>%
    rownames_to_column("gene") %>%
    pivot_longer(-gene, names_to = "sample", values_to = "zscore") %>%
    mutate(gene = fct_inorder(gene), sample = fct_inorder(sample))
  
  ggplot(heatmap_df, aes(x = sample, y = gene, fill = zscore)) +
    geom_tile() +
    scale_fill_gradient2(low = color_range[1], mid = color_range[2],
                          high = color_range[3], midpoint = 0,
                          limits = c(-2, 2), oob = scales::squish) +
    labs(x = "", y = "", fill = "Z-score") +
    theme_minimal() +
    theme(
      axis.text.x = element_text(angle = 45, hjust = 1, size = 8),
      axis.text.y = element_text(size = 6),
      axis.ticks = element_blank(),
      panel.grid = element_blank(),
      legend.position = "right"
    ) +
    (if (!show_rownames) theme(axis.text.y = element_blank()) else list()) +
    (if (!show_colnames) theme(axis.text.x = element_blank()) else list())
}

# 使用: plot_heatmap(expr_matrix, genes = top20_genes)

# ============================================================
# 多组比较柱状图 + 统计检验
# ============================================================
plot_grouped_bar <- function(df, x_col, y_col, fill_col,
                              method = "wilcox.test", palette = "npg") {
  
  ggplot(df, aes(x = !!sym(x_col), y = !!sym(y_col), fill = !!sym(fill_col))) +
    geom_bar(stat = "summary", fun = "mean", position = position_dodge(0.8), width = 0.7) +
    geom_errorbar(stat = "summary", fun.data = mean_se,
                  position = position_dodge(0.8), width = 0.25) +
    geom_jitter(aes(color = !!sym(fill_col)), position = position_jitterdodge(dodge.width = 0.8),
                size = 1, alpha = 0.3) +
    ggpubr::stat_compare_means(aes(group = !!sym(fill_col)), method = method, label = "p.signif") +
    scale_fill_brewer(palette = "Set2") +
    labs(y = y_col) +
    theme_publication()
}

# ============================================================
# 发文级 UMAP/TSNE 散点图
# ============================================================
plot_dim <- function(obj, reduction = "umap", group_by = "celltype",
                     palette = "npg", label = TRUE, pt_size = 0.5,
                     title = NULL) {
  
  emb <- as.data.frame(Embeddings(obj, reduction))
  emb[[group_by]] <- obj@meta.data[[group_by]]
  colnames(emb)[1:2] <- c("Dim1", "Dim2")
  
  n_groups <- length(unique(emb[[group_by]]))
  
  p <- ggplot(emb, aes(x = Dim1, y = Dim2, color = !!sym(group_by))) +
    geom_point(size = pt_size, alpha = 0.7) +
    theme_classic() +
    labs(x = paste0(toupper(reduction), " 1"), y = paste0(toupper(reduction), " 2"),
         title = title) +
    theme(
      legend.position = "right",
      axis.text = element_text(color = "black"),
      axis.title = element_text(face = "bold")
    )
  
  # 配色
  if (palette == "npg") p <- p + scale_color_npg()
  else if (palette == "aaas") p <- p + scale_color_aaas()
  else if (palette == "lancet") p <- p + scale_color_lancet()
  else if (palette == "jco") p <- p + scale_color_jco()
  else if (palette == "igv") p <- p + scale_color_igv()
  
  # 标签
  if (label) {
    label_pos <- emb %>%
      group_by(!!sym(group_by)) %>%
      summarise(Dim1 = median(Dim1), Dim2 = median(Dim2), .groups = "drop")
    p <- p + ggrepel::geom_text_repel(
      data = label_pos, aes(label = !!sym(group_by)),
      size = 3.5, fontface = "bold", color = "black",
      max.overlaps = 20, box.padding = 0.5
    )
  }
  p
}

# ============================================================
# 拼图
# ============================================================
# patchwork 最简用法
# p1 + p2 + p3                    # 横向排列
# p1 / p2 / p3                    # 纵向排列
# (p1 | p2) / p3                  # 组合布局
# (p1 + p2 + p3) + plot_layout(guides = "collect")  # 共享图例
# p1 + p2 + plot_annotation(title = "Main Title", tag_levels = "A")  # 加标签

# 批量拼图
combine_plots <- function(plot_list, ncol = 3, byrow = TRUE, 
                           title = NULL, tag_levels = "A") {
  wrapped <- purrr::map(plot_list, ~ .x + theme(plot.title = element_text(size = 10)))
  combined <- wrap_plots(wrapped, ncol = ncol, byrow = byrow) +
    plot_annotation(title = title, tag_levels = tag_levels) &
    theme(plot.tag = element_text(face = "bold", size = 14))
  combined
}
```

---

## 🧬 生信实战场景封装

### 1. DESeq2 结果一键处理

```r
# ============================================================
# deseq2_post_analysis —— DESeq2结果后处理全套
# ============================================================
deseq2_post_analysis <- function(dds, contrast,
                                  fc_cutoff = 1, padj_cutoff = 0.05,
                                  top_n = 20, save_dir = ".") {
  
  library(DESeq2)
  library(ggrepel)
  
  # 提取结果
  res <- results(dds, contrast = contrast, alpha = padj_cutoff)
  res <- lfcShrink(dds, contrast = contrast, res = res, type = "apeglm")
  res_df <- as.data.frame(res) %>% rownames_to_column("gene")
  
  # 标注上调/下调
  res_df <- res_df %>%
    mutate(direction = case_when(
      log2FoldChange > fc_cutoff & padj < padj_cutoff ~ "Up",
      log2FoldChange < -fc_cutoff & padj < padj_cutoff ~ "Down",
      TRUE ~ "NS"
    ))
  
  # 统计
  cat("=== 差异基因统计 ===\n")
  cat("总基因数:", nrow(res_df), "\n")
  cat("上调:", sum(res_df$direction == "Up"), "\n")
  cat("下调:", sum(res_df$direction == "Down"), "\n")
  cat("不显著:", sum(res_df$direction == "NS"), "\n")
  
  # 火山图
  p_volcano <- plot_volcano(res_df, fc_col = "log2FoldChange", pval_col = "padj",
                             gene_col = "gene", fc_cut = fc_cutoff, pval_cut = padj_cutoff,
                             top_n = top_n)
  
  # MA图
  p_ma <- plot_ma(res_df, base_mean_col = "baseMean", fc_col = "log2FoldChange", pval_col = "padj")
  
  # 保存
  if (save_dir != ".") dir.create(save_dir, showWarnings = FALSE, recursive = TRUE)
  ggsave(file.path(save_dir, "volcano.png"), p_volcano, width = 8, height = 6, dpi = 300)
  ggsave(file.path(save_dir, "MA_plot.png"), p_ma, width = 8, height = 6, dpi = 300)
  write_csv(res_df, file.path(save_dir, "DEG_results.csv"))
  
  # 返回
  list(results = res_df, volcano = p_volcano, ma = p_ma)
}
```

### 2. 多组差异分析

```r
# ============================================================
# multi_group_degs —— 多组间两两比较
# ============================================================
multi_group_degs <- function(count_mat, sample_info,
                              group_col = "condition",
                              comparisons = "all",
                              fc_cutoff = 1, padj_cutoff = 0.05) {
  
  library(DESeq2)
  
  # 创建 DESeq2 对象
  dds <- DESeqDataSetFromMatrix(
    countData = count_mat,
    colData = sample_info,
    design = as.formula(paste0("~", group_col))
  )
  dds <- DESeq(dds)
  
  groups <- unique(sample_info[[group_col]])
  
  # 生成比较对
  if (identical(comparisons, "all")) {
    comparisons <- combn(groups, 2, simplify = FALSE)
  }
  
  # 逐对比较
  all_results <- purrr::imap_dfr(comparisons, function(comp, i) {
    contrast <- c(group_col, comp[1], comp[2])
    res <- results(dds, contrast = contrast, alpha = padj_cutoff)
    res_df <- as.data.frame(res) %>% rownames_to_column("gene")
    res_df <- res_df %>%
      mutate(
        direction = case_when(
          log2FoldChange > fc_cutoff & padj < padj_cutoff ~ "Up",
          log2FoldChange < -fc_cutoff & padj < padj_cutoff ~ "Down",
          TRUE ~ "NS"
        ),
        comparison = paste(comp[1], "vs", comp[2])
      )
    res_df
  })
  
  # 汇总统计
  summary <- all_results %>%
    group_by(comparison, direction) %>%
    summarise(n = n(), .groups = "drop") %>%
    filter(direction != "NS") %>%
    pivot_wider(names_from = direction, values_from = n, values_fill = 0)
  
  cat("=== 各比较组差异基因数 ===\n")
  print(summary)
  
  list(results = all_results, summary = summary, dds = dds)
}
```

### 3. 基因集打分

```r
# ============================================================
# gene_set_score —— 基因集打分（类似AUCell/AddModuleScore）
# ============================================================
gene_set_score <- function(expr_mat, gene_set, method = "mean") {
  common_genes <- intersect(gene_set, rownames(expr_mat))
  if (length(common_genes) == 0) stop("基因集与表达矩阵无交集")
  cat("使用", length(common_genes), "/", length(gene_set), "个基因\n")
  
  sub_mat <- expr_mat[common_genes, , drop = FALSE]
  
  switch(method,
    mean = colMeans(sub_mat, na.rm = TRUE),
    median = matrixStats::colMedians(as.matrix(sub_mat), na.rm = TRUE),
    sum = colSums(sub_mat, na.rm = TRUE),
    zscore = {
      z <- t(scale(t(sub_mat)))
      colMeans(z, na.rm = TRUE)
    },
    ssgsea = GSVA::gsva(as.matrix(sub_mat), list(gene_set), method = "ssgsea")[1,],
    stop("不支持的方法: ", method)
  )
}
```

### 4. 表达矩阵批量统计

```r
# ============================================================
# batch_expression_stats —— 批量计算基因表达统计
# ============================================================
batch_expression_stats <- function(expr_mat, group_info,
                                    group_col = "condition",
                                    stats = c("mean", "sd", "pct_expressed")) {
  
  groups <- split(colnames(expr_mat), group_info[[group_col]])
  
  purrr::map_dfr(rownames(expr_mat), function(gene) {
    gene_exp <- expr_mat[gene, ]
    
    result <- tibble(gene = gene)
    
    if ("mean" %in% stats) {
      for (g in names(groups)) {
        result[[paste0("mean_", g)]] <- mean(gene_exp[groups[[g]]], na.rm = TRUE)
      }
    }
    if ("sd" %in% stats) {
      for (g in names(groups)) {
        result[[paste0("sd_", g)]] <- sd(gene_exp[groups[[g]]], na.rm = TRUE)
      }
    }
    if ("pct_expressed" %in% stats) {
      for (g in names(groups)) {
        result[[paste0("pct_", g)]] <- mean(gene_exp[groups[[g]]] > 0, na.rm = TRUE)
      }
    }
    result
  })
}
```

---

## 🚀 一键数据处理流水线

```r
# ============================================================
# run_rnaseq_pipeline —— RNA-seq 数据处理全流程
# 从原始计数到差异基因 + 可视化
# ============================================================
run_rnaseq_pipeline <- function(count_file,
                                 sample_file,
                                 group_col = "condition",
                                 fc_cutoff = 1,
                                 padj_cutoff = 0.05,
                                 save_dir = "rnaseq_results") {
  
  cat("🚀 开始 RNA-seq 分析流程\n")
  dir.create(save_dir, showWarnings = FALSE, recursive = TRUE)
  
  # 1. 读取数据
  cat("📂 读取数据...\n")
  count_mat <- smart_read(count_file) %>% column_to_rownames(1) %>% as.matrix()
  sample_info <- smart_read(sample_file)
  
  # 2. 预过滤
  cat("🔧 预过滤...\n")
  keep <- rowSums(count_mat >= 10) >= ncol(count_mat) * 0.1
  count_mat <- count_mat[keep, ]
  cat("  保留基因:", nrow(count_mat), "\n")
  
  # 3. DESeq2 分析
  cat("🧬 DESeq2 差异分析...\n")
  dds <- DESeqDataSetFromMatrix(count_mat, sample_info, 
                                 design = as.formula(paste0("~", group_col)))
  dds <- DESeq(dds)
  
  # 4. 提取所有比较
  groups <- unique(sample_info[[group_col]])
  comparisons <- if (length(groups) == 2) {
    list(c(groups[1], groups[2]))
  } else {
    combn(groups, 2, simplify = FALSE)
  }
  
  # 5. 逐对分析
  all_results <- list()
  for (comp in comparisons) {
    comp_name <- paste(comp[1], "vs", comp[2])
    cat("  分析:", comp_name, "\n")
    
    contrast <- c(group_col, comp[1], comp[2])
    res <- results(dds, contrast = contrast, alpha = padj_cutoff)
    res_df <- as.data.frame(res) %>% rownames_to_column("gene") %>%
      mutate(
        direction = case_when(
          log2FoldChange > fc_cutoff & padj < padj_cutoff ~ "Up",
          log2FoldChange < -fc_cutoff & padj < padj_cutoff ~ "Down",
          TRUE ~ "NS"
        ),
        comparison = comp_name
      )
    
    # 火山图
    p <- plot_volcano(res_df, fc_col = "log2FoldChange", pval_col = "padj",
                       gene_col = "gene", title = comp_name)
    ggsave(file.path(save_dir, paste0("volcano_", gsub(" ", "_", comp_name), ".png")),
           p, width = 8, height = 6, dpi = 300)
    
    all_results[[comp_name]] <- res_df
  }
  
  # 6. 合并保存
  combined <- bind_rows(all_results, .id = "comparison")
  write_csv(combined, file.path(save_dir, "all_DEG_results.csv"))
  
  # 7. 汇总统计
  summary <- combined %>%
    group_by(comparison, direction) %>%
    summarise(n = n(), .groups = "drop") %>%
    filter(direction != "NS") %>%
    pivot_wider(names_from = direction, values_from = n, values_fill = 0)
  
  cat("\n✅ 分析完成！结果保存在:", save_dir, "\n")
  print(summary)
  
  list(results = all_results, combined = combined, summary = summary, dds = dds)
}

# 使用示例：
# results <- run_rnaseq_pipeline("counts.csv", "samples.csv", group_col = "treatment")
```

---

## 📋 函数速查表

### 封装函数速查

| 函数 | 用途 | 调用示例 |
|------|------|----------|
| `smart_read()` | 智能读取 | `smart_read("data.csv")` |
| `smart_write()` | 智能导出 | `smart_write(df, "out.xlsx")` |
| `batch_read()` | 批量读取 | `batch_read("./data/")` |
| `auto_diff_filter()` | 差异基因筛选 | `auto_diff_filter(df, fc_cutoff=1)` |
| `auto_annotate()` | 基因ID转换 | `auto_annotate(genes, to_type="ENTREZID")` |
| `auto_normalize_matrix()` | 表达矩阵标准化 | `auto_normalize_matrix(mat, "log2cpm")` |
| `auto_outlier_remove()` | 离群值去除 | `auto_outlier_remove(df, "nCount_RNA")` |
| `quick_summary()` | 快速统计概览 | `quick_summary(df, group_col="cluster")` |
| `expr_to_long()` | 矩阵宽→长 | `expr_to_long(mat)` |
| `expr_to_wide()` | 长格式→矩阵 | `expr_to_wide(df)` |
| `plot_volcano()` | 火山图 | `plot_volcano(df, fc_col="log2FC")` |
| `plot_ma()` | MA图 | `plot_ma(df)` |
| `plot_heatmap()` | 表达热图 | `plot_heatmap(mat, genes=top20)` |
| `plot_dim()` | UMAP/tSNE | `plot_dim(obj, "umap", "celltype")` |
| `plot_grouped_bar()` | 多组柱状图 | `plot_grouped_bar(df, "gene","exp","group")` |
| `combine_plots()` | 批量拼图 | `combine_plots(plot_list, ncol=3)` |
| `gene_set_score()` | 基因集打分 | `gene_set_score(mat, gene_set)` |
| `deseq2_post_analysis()` | DESeq2后处理 | `deseq2_post_analysis(dds, contrast)` |
| `multi_group_degs()` | 多组比较 | `multi_group_degs(mat, info)` |
| `run_rnaseq_pipeline()` | RNA-seq全流程 | `run_rnaseq_pipeline("counts.csv","samples.csv")` |

### dplyr 核心动词速查

```
filter()     → 行筛选       select()    → 列选择
mutate()     → 新增/修改列   summarise() → 汇总统计
arrange()    → 排序         group_by()  → 分组
join()       → 表连接       bind_rows() → 纵向合并
slice()      → 按位置选行   rename()    → 重命名
relocate()   → 列顺序       distinct()  → 去重
count()      → 快速计数     pull()      → 提取向量
across()     → 多列操作     where()     → 按类型选列
```

### tidyr 核心函数速查

```
pivot_longer()  → 宽变长       pivot_wider()   → 长变宽
separate()      → 拆分列       unite()         → 合并列
nest()          → 嵌套         unnest()        → 反嵌套
complete()      → 补全组合     fill()          → 前向填充
replace_na()    → 替换NA       drop_na()       → 删除NA行
expand()        → 生成组合     crossing()      → 交叉组合
```

### ggplot2 图层速查

```
geom_point()    → 散点         geom_line()      → 折线
geom_bar()      → 柱状图       geom_boxplot()   → 箱线图
geom_violin()   → 小提琴       geom_tile()      → 热图
geom_density()  → 密度图       geom_histogram() → 直方图
geom_smooth()   → 拟合线       geom_text()      → 文本
geom_hline()    → 水平线       geom_vline()     → 垂直线
facet_wrap()    → 分面         coord_flip()     → 翻转
scale_color_()  → 颜色         scale_fill_()    → 填充色
theme_bw()      → 黑白主题     theme_minimal()  → 极简主题
```

---

> 📌 **核心原则**：所有函数参数有默认值，复制改参数即跑。`run_rnaseq_pipeline()` 一行完成 RNA-seq 全流程。
> 生信可视化首选 `plot_volcano()` / `plot_heatmap()` / `plot_dim()`，自动生成发文级图表。
