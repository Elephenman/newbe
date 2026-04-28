# 📖 literature-review-matrix

**文献综述矩阵自动生成器**

## 使用方法

```bash
cd literature-review-matrix
python literature_review_matrix.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `文献数据CSV路径` | `papers.csv` |
| 2 | `矩阵维度(逗号分隔)` | `method` |
| 3 | `是否出表格图(yes/no)` | `yes` |

### 交互式输入示例

```
文献数据CSV路径 [默认: papers.csv]: 
矩阵维度(逗号分隔) [默认: method]: 
是否出表格图(yes/no) [默认: yes]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT