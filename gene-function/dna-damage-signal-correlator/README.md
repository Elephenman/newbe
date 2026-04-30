# dna-damage-signal-correlator

## 一句话说明
分析DNA损伤信号标记(如gammaH2AX/p53)与DDR基因表达的相关性。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 损伤信号文件 | damage_signals.tsv | 损伤标记数据 |
| 表达矩阵文件 | expression.tsv | 基因表达 |
| 输出文件 | damage_signal_correlation.txt | 相关性结果 |

## 使用示例

```bash
python dna_damage_signal_correlator.py
```
