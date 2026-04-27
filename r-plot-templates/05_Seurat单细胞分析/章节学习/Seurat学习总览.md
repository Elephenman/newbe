# 🧬 Seurat 学习总览

## 📖 Seurat 简介

**Seurat** 是 R 语言中最流行的单细胞 RNA-seq 分析工具包，由 **Satija Lab** 开发和维护。它提供了一套完整的分析流程，从数据导入、质量控制、降维聚类到细胞类型注释，覆盖了单细胞分析的各个环节。

> **官方网址**：https://satijalab.org/seurat/

---

## 🆕 Seurat v5 特性

Seurat v5 带来了多项重要更新：

- **多层架构（Sketch / BPCells）**：支持超大规模数据集（百万级细胞）的高效分析
- **统一的多模态框架**：WNN（Weighted Nearest Neighbor）方法整合多种数据模态
- **改进的整合方法**：支持 Reciprocal PCA (RPCA) 和 Bridge integration 等新方法
- **更快的计算性能**：底层计算优化，支持 on-disk 存储
- **向后兼容**：Seurat v4 的代码可平滑迁移至 v5
- **空间转录组支持增强**：与 Seurat 对象无缝集成

---

## 🗺️ 学习路线图

```
数据准备阶段                核心分析阶段               高级分析阶段
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ 01 安装与环境  │────▶│ 03 质量控制 QC    │────▶│ 11 多样本整合      │
│ 02 数据导入    │     │ 04 数据归一化     │     │ 12 空间转录组      │
└──────────────┘     │ 05 特征选择       │     │ 13 多模态 WNN     │
                     │ 06 缩放与 PCA     │     │ 14 细胞周期评分    │
                     │ 07 UMAP/tSNE     │     └──────────────────┘
                     │ 08 细胞聚类       │
                     │ 09 差异表达       │     ┌──────────────────┐
                     │ 10 细胞类型注释    │────▶│ 15 命令速查表      │
                     └──────────────────┘     │ 16 完整实战案例    │
                                              └──────────────────┘
```

---

## 📚 模块索引

### 第一阶段：数据准备

| 序号 | 模块 | 说明 | 链接 |
|------|------|------|------|
| 01 | 安装与环境配置 | 安装 Seurat 及依赖包，配置分析环境 | [[01_安装与环境配置/安装与环境配置]] |
| 02 | 数据导入与Seurat对象 | 读取 10x 数据，创建 Seurat 对象 | [[02_数据导入与Seurat对象/数据导入与Seurat对象]] |

### 第二阶段：核心分析流程

| 序号 | 模块 | 说明 | 链接 |
|------|------|------|------|
| 03 | 质量控制QC | 过滤低质量细胞和基因，质控指标可视化 | [[03_质量控制QC/质量控制QC]] |
| 04 | 数据归一化 | 消除测序深度差异，LogNormalize 等 | [[04_数据归一化/数据归一化]] |
| 05 | 特征选择 | 选择高变基因（HVG），VariableFeatures | [[05_特征选择/特征选择]] |
| 06 | 数据缩放与线性降维PCA | ScaleData 与 PCA 降维 | [[06_数据缩放与线性降维PCA/数据缩放与线性降维PCA]] |
| 07 | 非线性降维UMAP/tSNE | UMAP 和 t-SNE 可视化 | [[07_非线性降维UMAP_tSNE/非线性降维UMAP_tSNE]] |
| 08 | 细胞聚类 | FindNeighbors 与 FindClusters | [[08_细胞聚类/细胞聚类]] |
| 09 | 差异表达与Marker基因 | FindAllMarkers 与 FindMarkers | [[09_差异表达与Marker基因/差异表达与Marker基因]] |
| 10 | 细胞类型注释 | 基于 Marker 基因的细胞类型鉴定 | [[10_细胞类型注释/细胞类型注释]] |

### 第三阶段：高级分析

| 序号 | 模块 | 说明 | 链接 |
|------|------|------|------|
| 11 | 多样本整合Integration | IntegrateData 整合多样本 | [[11_多样本整合Integration/多样本整合Integration]] |
| 12 | 空间转录组分析 | 空间数据导入与可视化分析 | [[12_空间转录组分析/空间转录组分析]] |
| 13 | 多模态分析WNN | 加权最近邻（WNN）多模态整合 | [[13_多模态分析WNN/多模态分析WNN]] |
| 14 | 细胞周期评分 | CellCycleScoring 回归细胞周期效应 | [[14_细胞周期评分/细胞周期评分]] |

### 第四阶段：总结与实战

| 序号 | 模块 | 说明 | 链接 |
|------|------|------|------|
| 15 | 命令速查表 | Seurat 常用函数速查 | [[15_命令速查表/命令速查表]] |
| 16 | 完整实战案例 | PBMC 3k 数据集完整分析流程 | [[16_完整实战案例/PBMC3k完整流程]] |

---

## 🔗 官方资源

- **Seurat 官方网站**：https://satijalab.org/seurat/
- **Seurat GitHub 仓库**：https://github.com/satijalab/seurat
- **Seurat 官方教程（PBMC3k）**：https://satijalab.org/seurat/articles/pbmc3k_tutorial
- **Seurat v5 快速入门**：https://satijalab.org/seurat/articles/get_started_v5_new
- **Seurat 命令速查表**：https://satijalab.org/seurat/articles/essential_commands
- **安装指南**：https://satijalab.org/seurat/articles/install
- **Satija Lab 主页**：https://satijalab.org/
- **Seurat 论文 (v5)**：Hao et al., Nature Biotechnology 2024

---

## 💡 使用建议

1. **按顺序学习**：模块 01-10 是核心流程，建议按顺序学习
2. **动手实践**：每个模块都包含可运行的代码，建议边学边练
3. **结合实战**：学完基础模块后，用模块 16 的 PBMC3k 案例巩固
4. **善用速查**：模块 15 的命令速查表可作为日常参考
5. **关注版本**：本知识库基于 Seurat v5，部分函数与 v4 有差异
