# 🔬 sc-cluster-stability-checker

**单细胞聚类稳定性评估+分辨率优化**

## 使用方法

```bash
cd sc-cluster-stability-checker
Rscript sc_cluster_stability_checker.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `Input file path` | `input.txt` |
| 2 | `Output file path` | `output_sc_cluster_stability_checker.txt` |
| 3 | `Main parameter (threshold)` | `0.05` |
| 4 | `Secondary parameter (mode)` | `default` |

### 交互式输入示例

```
Input file path [默认: input.txt]: 
Output file path [默认: output_sc_cluster_stability_checker.txt]: 
Main parameter (threshold) [默认: 0.05]: 
Secondary parameter (mode) [默认: default]: 
```

## 依赖

请参考脚本中的 library() 调用

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT