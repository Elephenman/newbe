# experiment-design-checker

实验设计检查器(样本量/重复/对照完整性)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 实验设计CSV路径(样本,组,重复,处理) | design.csv |
| output_file | 输出检查报告路径 | design_check.txt |

## 使用示例

```bash
python experiment-design-checker.py
```

## 依赖

```
pandas
```
