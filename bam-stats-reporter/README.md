# 📊 bam-stats-reporter

**BAM/SAM文件关键指标速查** — pysam封装，5行代码出报告

## 功能

- ✅ 总reads数、mapped率、duplicate率
- ✅ MAPQ分布统计与可视化
- ✅ 插入长度统计（paired-end）
- ✅ 平均覆盖度计算（需提供基因组长度）
- ✅ 终端报告 + 可选CSV统计表

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| BAM/SAM文件路径 | 输入的BAM/SAM文件 | sample.bam |
| 是否计算覆盖度 | yes/no | no |
| 参考基因组总长度(bp) | 覆盖度计算需要 | 3000000000 |
| 是否保存CSV统计表 | yes/no | no |

## 使用示例

```bash
python bam_stats_reporter.py
```

交互式输入：
```
输入BAM/SAM文件路径 [默认: sample.bam]: /data/aligned.bam
是否计算覆盖度(yes/no) [默认: no]: yes
参考基因组总长度(bp) [默认: 3000000000]: 121000000
是否保存CSV统计表 [默认: no]: yes
```

## 依赖

```
pysam>=0.15
```

## 输出

- 终端打印结构化统计报告
- 可选 `{filename}_bam_stats.csv`

## License

MIT