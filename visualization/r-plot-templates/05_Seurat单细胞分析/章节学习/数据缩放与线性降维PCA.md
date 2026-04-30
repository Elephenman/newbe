# 数据缩放与线性降维PCA

## 📌 本模块目标
理解数据缩放（Z-score标准化）的目的和操作，掌握 PCA 降维的原理和可视化方法，学会确定用于后续分析的 PC 数量。

## 🔧 核心函数
| 函数 | 用途 | 关键参数 |
|------|------|----------|
| `ScaleData()` | 数据缩放（Z-score） | `features`, `vars.to.regress` |
| `RunPCA()` | 主成分分析 | `features`, `npcs` |
| `VizDimLoadings()` | 可视化PC载荷 | `dims`, `reduction` |
| `DimPlot()` | 绘制降维散点图 | `reduction`, `group.by` |
| `DimHeatmap()` | PC热图 | `dims`, `cells`, `balanced` |
| `ElbowPlot()` | 肘部图选PC数 | `ndims` |
| `JackStraw()` | JackStraw显著性检验 | `num.replicate`, `dims` |

## 📝 详细代码与注释

### 1. 数据缩放（Scaling）

```r
# ============================================
# 为什么要缩放？
# ============================================
# PCA 要求数据满足：
#   1. 均值为0（中心化）→ 消除基因表达水平的绝对差异
#   2. 方差为1（标准化）→ 让所有基因在PCA中权重相同
# 否则高表达基因会主导PCA结果
#
# 数学操作：scaled = (x - mean) / sd
# ============================================

# 方法一：只对高变基因缩放（默认，更快）
pbmc <- ScaleData(pbmc)

# 方法二：对所有基因缩放（后续画热图需要）
all.genes <- rownames(pbmc)
pbmc <- ScaleData(pbmc, features = all.genes)

# ============================================
# 回归掉干扰因素（重要！）
# ============================================
# 回归线粒体基因比例 → 去除细胞质量差异
# 回归细胞周期 → 去除细胞周期效应
pbmc <- ScaleData(
  pbmc,
  vars.to.regress = c("percent.mt")  # 回归线粒体比例
)

# 同时回归多个因素
pbmc <- ScaleData(
  pbmc,
  vars.to.regress = c("percent.mt", "nCount_RNA")  # 回归线粒体+测序深度
)

# ⚠️ vars.to.regress 会显著增加计算时间
```

### 2. 缩放结果验证

```r
# ============================================
# 验证缩放后的数据：每行均值为0，方差为1
# ============================================
# 提取缩放后的矩阵前10行
mat <- pbmc[["RNA"]]$scale.data[1:10, ]

# 计算每行的均值和方差
res <- data.frame(
  gene = rownames(mat),
  mean = apply(mat, 1, mean),      # 应该接近 0
  variance = apply(mat, 1, var)     # 应该接近 1
)
print(res)
# 均值 ≈ 0（可能有极小浮点误差）
# 方差 ≈ 1
```

### 3. 运行 PCA

```r
# ============================================
# 主成分分析（PCA）
# ============================================
# 只使用高变基因进行PCA（默认）
pbmc <- RunPCA(
  pbmc,
  features = VariableFeatures(object = pbmc),
  ncp = 50    # 计算50个主成分（默认）
)

# ⭐ 简写形式
pbmc <- RunPCA(pbmc)
```

### 4. 查看 PCA 结果

```r
# ============================================
# 查看前5个主成分的载荷基因
# ============================================
print(pbmc[["pca"]], dims = 1:5, nfeatures = 5)
# PC_ 1 
# Positive:  CST3, TYROBP, LST1, AIF1, FTL     → 髓系细胞标记
# Negative:  MALAT1, LTB, IL32, IL7R, CD2       → T细胞标记
# PC_ 2 
# Positive:  CD79A, MS4A1, TCL1A, HLA-DQA1      → B细胞标记
# Negative:  NKG7, PRF1, CST7, GZMB, GZMA       → NK/CTL标记
# ...

# ============================================
# 解读：每个PC的正/负载荷基因代表了该PC捕捉到的生物学差异
```

### 5. PCA 可视化

```r
# ============================================
# 5.1 PC 载荷基因可视化
# ============================================
VizDimLoadings(pbmc, dims = 1:2, reduction = "pca")
# 显示 PC1 和 PC2 正/负载荷最大的基因

# ============================================
# 5.2 PCA 散点图
# ============================================
DimPlot(pbmc, reduction = "pca") + NoLegend()
# 每个点代表一个细胞，按 PC1 和 PC2 坐标排列

# ============================================
# 5.3 PC 热图（看每个PC的基因表达模式）
# ============================================
# 单个PC的热图
DimHeatmap(pbmc, dims = 1, cells = 500, balanced = TRUE)

# 前15个PC的热图（选择PC数量时参考）
DimHeatmap(pbmc, dims = 1:15, cells = 500, balanced = TRUE)

# 参数详解：
# dims：要绘制的主成分编号
# cells：使用多少个细胞（越多越慢）
# balanced：正负两侧各取等量基因
```

### 6. 确定使用的 PC 数量（关键步骤！）

```r
# ============================================
# 方法一：肘部图（ElbowPlot）— 最常用
# ============================================
ElbowPlot(pbmc)
# 看拐点：PC 数量取拐点前的值
# 拐点 = 标准差下降明显变缓的位置
# 例如拐点在 PC10-12，就选 dims = 1:10

# 指定展示的 PC 数量
ElbowPlot(pbmc, ndims = 30)

# ============================================
# 方法二：JackStraw 检验（更严谨但更慢）
# ============================================
pbmc <- JackStraw(pbmc, num.replicate = 100, dims = 50)
pbmc <- ScoreJackStraw(pbmc, dims = 1:20)

JackStrawPlot(pbmc, dims = 1:20)
# 红线以上的 PC 是显著的
# 显著 PC 的最后一个就是使用数量

# ============================================
# 🎯 选择 PC 数量的经验法则
# ============================================
# 1. ElbowPlot 看拐点
# 2. JackStraw 看显著性
# 3. 热图看生物学意义
# 4. PBMC3k 通常选 10-20 个 PC
# 5. 宁多勿少（多选几个比少选好）
# 6. 不建议超过 30 个 PC
```

## ⚠️ 常见问题与注意事项

- **ScaleData 必须在 RunPCA 之前**：先缩放再降维
- **vars.to.regress 很慢**：大数据集可能需要很长时间，可以用 SCTransform 替代
- **PC 数量很重要**：直接影响后续聚类结果，建议多试几个值
- **不要盲目选 10**：每个数据集最佳 PC 数不同
- **热图看生物学意义**：PC 的载荷基因应该有已知的生物学含义

## 🔗 相关模块
- [[05_特征选择/特征选择]]
- [[07_非线性降维UMAP_tSNE/非线性降维UMAP_tSNE]]
- [[08_细胞聚类/细胞聚类]]
