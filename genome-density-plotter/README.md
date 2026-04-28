# 🧬 genome-density-plotter

**基因/SNP/特征染色体密度图**

## 使用方法

```bash
cd genome-density-plotter
python genome_density_plotter.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `坐标文件路径(BED/TSV)` | `regions.bed` |
| 2 | `bin大小(bp)` | `100000` |
| 3 | `是否出circos风格图(yes/no)` | `no` |
| 4 | `图片格式(png/pdf)` | `png` |

### 交互式输入示例

```
坐标文件路径(BED/TSV) [默认: regions.bed]: 
bin大小(bp) [默认: 100000]: 
是否出circos风格图(yes/no) [默认: no]: 
图片格式(png/pdf) [默认: png]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT