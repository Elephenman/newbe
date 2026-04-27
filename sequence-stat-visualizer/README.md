# 📈 sequence-stat-visualizer

**多序列文件统计+可视化** — 长度/GC/氨基酸一键分析

## 功能

- ✅ 序列长度分布统计（均值/中位数/最大/最小）
- ✅ GC含量分布统计与密度图
- ✅ 自动检测DNA/蛋白质序列类型
- ✅ 氨基酸比例分析（蛋白质序列）
- ✅ 统计表CSV + 可选matplotlib分布图

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| FASTA文件路径 | 输入的FASTA文件 | sequences.fasta |
| 统计维度 | length/gc/aa/all | all |
| 是否出图 | yes/no | yes |
| 图片格式 | png/pdf | png |

## 使用示例

```bash
python sequence_stat_visualizer.py
```

## 依赖

```
matplotlib>=3.0
```

## License

MIT