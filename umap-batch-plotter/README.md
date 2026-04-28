# 🔬 umap-batch-plotter

**UMAP按多维度批量分色绘图**

## 使用方法

```bash
cd umap-batch-plotter
Rscript umap_batch_plotter.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `Seurat对象路径(rds)` | `seurat.rds` |
| 2 | `分组维度列表(逗号分隔)` | `cluster,celltype,sample` |
| 3 | `是否组合大图(yes/no)` | `yes` |
| 4 | `配色方案(Set2/Paired/Nature)` | `Set2` |

### 交互式输入示例

```
Seurat对象路径(rds) [默认: seurat.rds]: 
分组维度列表(逗号分隔) [默认: cluster,celltype,sample]: 
是否组合大图(yes/no) [默认: yes]: 
配色方案(Set2/Paired/Nature) [默认: Set2]: 
```

## 依赖

```r
install.packages('Seurat')  # 或 BiocManager::install('Seurat')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT