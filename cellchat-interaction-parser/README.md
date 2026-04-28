# 🔬 cellchat-interaction-parser

**CellChat细胞通讯一键分析**

## 使用方法

```bash
cd cellchat-interaction-parser
Rscript cellchat_interaction_parser.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `Seurat对象路径(rds)` | `seurat.rds` |
| 2 | `物种(human/mouse)` | `human` |

### 交互式输入示例

```
Seurat对象路径(rds) [默认: seurat.rds]: 
物种(human/mouse) [默认: human]: 
```

## 依赖

```r
install.packages('CellChat')  # 或 BiocManager::install('CellChat')
install.packages('Seurat')  # 或 BiocManager::install('Seurat')
install.packages('ggplot2')  # 或 BiocManager::install('ggplot2')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT