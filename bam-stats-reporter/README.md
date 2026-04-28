# 🧬 bam-stats-reporter

**BAM/SAM文件关键指标速查
pysam封装，5行代码出报告

功能：
- 总reads数、mapped率、duplicate率
- 平均覆盖度、插入长度分布、MAPQ分布
- 终端打印 + 可选CSV统计表**

## 使用方法

```bash
cd bam-stats-reporter
python bam_stats_reporter.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `输入BAM/SAM文件路径` | `sample.bam` |
| 2 | `是否计算覆盖度(yes/no)` | `no` |
| 3 | `参考基因组总长度(bp)` | `3000000000` |
| 4 | `是否保存CSV统计表` | `no` |

### 交互式输入示例

```
输入BAM/SAM文件路径 [默认: sample.bam]: 
是否计算覆盖度(yes/no) [默认: no]: 
参考基因组总长度(bp) [默认: 3000000000]: 
是否保存CSV统计表 [默认: no]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT