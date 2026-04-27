# 📊 deseq2-result-formatter

**DESeq2结果→发表级表格+火山图** — R脚本，参数全交互

## 功能

- ✅ 读取DESeq2结果CSV
- ✅ 按padj和log2FC阈值过滤
- ✅ 统计上调/下调/稳定基因数
- ✅ 生成ggplot2火山图（标注top基因）
- ✅ 自动识别常见列名别名（logFC/p_val/FDR等）
- ✅ 输出过滤后CSV + 注释完整CSV + 火山图

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| DESeq2结果CSV路径 | 输入文件 | deseq2_results.csv |
| padj阈值 | 显著性阈值 | 0.05 |
| log2FC阈值 | 差异倍数阈值 | 1 |
| 基因名列名 | rowname或具体列名 | rowname |
| 是否生成火山图 | yes/no | yes |
| 标注topN基因 | 火山图标注基因数 | 10 |
| 图片格式 | png/pdf/tiff | png |

## 使用示例

```bash
Rscript deseq2_result_formatter.R
```

交互式输入：
```
输入DESeq2结果CSV路径 [默认: deseq2_results.csv]: /data/deseq2_vs_control.csv
padj阈值 [默认: 0.05]: 0.01
log2FC阈值 [默认: 1]: 2
基因名列名 [默认: rowname]: gene_symbol
是否生成火山图 [默认: yes]: yes
火山图标注topN基因 [默认: 10]: 15
图片格式(png/pdf/tiff) [默认: png]: pdf
```

## 依赖

```
ggplot2>=3.3
dplyr>=1.0  # 可选
```

## 输出

- `{filename}_filtered.csv` — 显著差异基因列表
- `{filename}_annotated.csv` — 完整结果（含category列）
- `{filename}_volcano.png/pdf/tiff` — 火山图

## 火山图配色

- 上调基因：红色 (#E64B35，Nature风格)
- 下调基因：蓝色 (#4DBBD5，Nature风格)
- 稳定基因：灰色背景

## License

MIT