# 📊 co-expression-network

**WGCNA简化版一键网络构建**

## 使用方法

```bash
cd co-expression-network
Rscript co_expression_network.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `表达矩阵CSV路径(行=基因,列=样本)` | `expression.csv` |
| 2 | `最小模块大小` | `30` |
| 3 | `软阈值范围(如1-20)` | `1-20` |

### 交互式输入示例

```
表达矩阵CSV路径(行=基因,列=样本) [默认: expression.csv]: 
最小模块大小 [默认: 30]: 
软阈值范围(如1-20) [默认: 1-20]: 
```

## 依赖

```r
install.packages('WGCNA')  # 或 BiocManager::install('WGCNA')
install.packages('ggplot2')  # 或 BiocManager::install('ggplot2')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT