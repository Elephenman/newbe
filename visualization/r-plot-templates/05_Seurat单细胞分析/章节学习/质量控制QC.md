# 质量控制QC

## 📌 本模块目标
学会计算和可视化单细胞数据的质量控制指标（线粒体百分比、基因数、UMI数），并根据这些指标过滤低质量细胞。

## 🔧 核心函数
| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `PercentageFeatureSet()` | 计算某类基因的百分比 | `pattern`, `features` |
| `VlnPlot()` | 小提琴图展示QC指标 | `features`, `ncol`, `pt.size` |
| `RidgePlot()` | 山峦图展示QC指标 | `features`, `ncol` |
| `FeatureScatter()` | 散点图看指标相关性 | `feature1`, `feature2` |
| `subset()` | 按条件过滤细胞 | `subset` |

## 📝 详细代码与注释

### 1. 计算线粒体基因百分比

```r
# ============================================
# 为什么关注线粒体基因？
# → 线粒体基因占比高 = 细胞膜破裂，细胞质RNA流失，只剩线粒体RNA
# → 这些是低质量/死细胞，需要去除
# ============================================

# 方法一：用正则表达式匹配（推荐）
pbmc[["percent.mt"]] <- PercentageFeatureSet(
  pbmc,
  pattern = "^MT-"    # 匹配以 MT- 开头的基因（人类）
)

# 方法二：自定义基因列表
MT_geneSet <- str_subset(rownames(pbmc.data), "^MT-")
pbmc[["percent.mt"]] <- PercentageFeatureSet(
  pbmc,
  features = MT_geneSet
)

# ============================================
# 不同物种的线粒体基因前缀
# ============================================
# 人类（Human）："^MT-"
# 小鼠（Mouse）："^mt-"
# 大鼠（Rat）："^mt-"
# 斑马鱼（Zebrafish）："^mt-"
# 果蝇（Drosophila）："^mt:"

# 同时计算核糖体基因百分比（可选）
pbmc[["percent.rb"]] <- PercentageFeatureSet(pbmc, pattern = "^RP[SL]")
```

### 2. 查看 QC 指标

```r
# ============================================
# 查看所有 QC 指标
# ============================================
head(pbmc[[]])
# orig.ident nCount_RNA nFeature_RNA percent.mt
# AAACATACAACCAC-1    pbmc3k       2419          779   3.017765
# AAACATTGAGCTAC-1    pbmc3k       4903         1352   3.793596
# AAACATTGATCAGC-1    pbmc3k       3147         1129   0.889736
# ...

# 统计摘要
summary(pbmc$nCount_RNA)
summary(pbmc$nFeature_RNA)
summary(pbmc$percent.mt)
```

### 3. QC 指标可视化

```r
# ============================================
# 小提琴图 — 最常用的 QC 可视化
# ============================================
VlnPlot(pbmc,
  features = c("nFeature_RNA", "nCount_RNA", "percent.mt"),
  ncol = 3,        # 每行3个图
  pt.size = 0.01   # 点的大小（0=不显示点）
)

# ✅ 小提琴图的优势：
# 相比箱线图，可以更直观地看到数据分布形态（单峰、多峰、偏态）
```

```r
# ============================================
# 山峦图（Ridge Plot）— 多组比较时更直观
# ============================================
RidgePlot(pbmc,
  features = c("nFeature_RNA", "nCount_RNA", "percent.mt"),
  ncol = 1
)

# ✅ 山峦图优势：
# 能够清晰展示多个分组的分布差异
# 适合单细胞测序中不同细胞类型/状态的比较
```

```r
# ============================================
# 散点图 — 查看指标间的相关性
# ============================================
# 基因数量 vs 转录本数量（期望正相关）
p1 <- FeatureScatter(pbmc,
  feature1 = "nCount_RNA",
  feature2 = "nFeature_RNA"
)

# 线粒体百分比 vs 转录本数量（期望无/负相关）
p2 <- FeatureScatter(pbmc,
  feature1 = "nCount_RNA",
  feature2 = "percent.mt"
)

p1 + p2
```

### 4. 过滤低质量细胞

```r
# ============================================
# 过滤标准详解
# ============================================
# nFeature_RNA > 200：去除基因数太少的细胞（死细胞/空液滴）
# nFeature_RNA < 2500：去除基因数太多的细胞（可能doublets多细胞融合）
# percent.mt < 5：去除线粒体占比过高的细胞（细胞膜破裂）

# 注意：阈值因数据集而异，需要根据小提琴图调整！

pbmc <- subset(pbmc,
  subset = nFeature_RNA > 200 &
           nFeature_RNA < 2500 &
           percent.mt < 5
)

# 查看过滤后的细胞数
dim(pbmc)
# 过滤前 2700 → 过滤后约 2638
```

### 5. 高级 QC：检测 Doublets

```r
# ============================================
# 方法一：基于 nFeature_RNA 极端值（简单快速）
# ============================================
# nFeature_RNA 异常高的细胞可能是 doublets
# 通常设阈值为中位数 + 3*MAD

upper_threshold <- median(pbmc$nFeature_RNA) + 3 * mad(pbmc$nFeature_RNA)
cat("Doublet阈值:", upper_threshold, "\n")

# ============================================
# 方法二：使用 DoubletFinder 包（更准确）
# ============================================
# install.packages("DoubletFinder")
library(DoubletFinder)

# 预估 doublet 比例（通常 5-10%）
# 具体用法见 DoubletFinder 文档
```

### 6. 保存过滤后的数据

```r
# ============================================
# 保存过滤后的 Seurat 对象
# ============================================
save(pbmc, file = "./pbmc_after_qc.rdata")

# 下次直接加载
load("./pbmc_after_qc.rdata")
```

## ⚠️ 常见问题与注意事项

- **阈值不是固定的**：每个数据集的 QC 阈值不同，必须看小提琴图再决定
- **线粒体阈值**：5% 是 PBMC 的常用值，其他组织可能不同（如脑组织可放宽到 10%）
- **不要过度过滤**：宁可保留稍多一些，也不要丢失稀有细胞类型
- **小鼠线粒体前缀是小写**：`"^mt-"` 不是 `"^MT-"`
- **Doublets**：细胞数异常高（nFeature_RNA > 中位数+3MAD）的细胞可能是双细胞

## 🔗 相关模块
- [[02_数据导入与Seurat对象/数据导入与Seurat对象]]
- [[04_数据归一化/数据归一化]]
