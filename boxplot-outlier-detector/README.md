# boxplot-outlier-detector

箱线图异常值检测与报告

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 数据文件CSV路径 | data.csv |
| output_file | 异常值报告路径 | outliers.txt |
| column | 检测列名(留空=所有数值列) |  |
| method | 检测方法(iqr/zscore) | iqr |

## 使用示例

```bash
python boxplot-outlier-detector.py
```

## 依赖

```
pandas
numpy
```
