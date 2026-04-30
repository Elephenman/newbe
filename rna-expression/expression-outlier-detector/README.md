# expression-outlier-detector

## 一句话说明
检测表达矩阵中的异常样本和基因（IQR/Z-score方法）。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 表达矩阵文件 | expression.tsv | 表达量矩阵 |
| 输出文件 | outliers.txt | 异常值报告 |
| 检测方法 | iqr | iqr或zscore |
| 阈值 | 3 | 异常判定阈值 |

## 使用示例

```bash
python expression_outlier_detector.py
```
