# multi-omics-integration-helper

多组学数据整合辅助(联合矩阵构建+基础分析)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| omics_files | 组学数据文件(逗号分隔CSV) | omics1.csv,omics2.csv |
| output_file | 整合输出矩阵路径 | integrated.csv |
| method | 整合方式(concat/intersect) | intersect |

## 使用示例

```bash
python multi-omics-integration-helper.py
```

## 依赖

```
pandas
numpy
```
