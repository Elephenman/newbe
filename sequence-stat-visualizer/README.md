# 🧬 sequence-stat-visualizer

**多序列文件统计+可视化
解析FASTA，统计长度/GC/氨基酸比例，生成分布图

功能：
- 序列长度分布（均值/中位数/最大/最小）
- GC含量分布
- 氨基酸比例（蛋白质序列）
- 统计表CSV + 可选matplotlib分布图**

## 使用方法

```bash
cd sequence-stat-visualizer
python sequence_stat_visualizer.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `输入FASTA文件路径` | `sequences.fasta` |
| 2 | `统计维度(length/gc/aa/all)` | `all` |
| 3 | `是否出图(yes/no)` | `yes` |
| 4 | `图片格式(png/pdf)` | `png` |

### 交互式输入示例

```
输入FASTA文件路径 [默认: sequences.fasta]: 
统计维度(length/gc/aa/all) [默认: all]: 
是否出图(yes/no) [默认: yes]: 
图片格式(png/pdf) [默认: png]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT