# 🔧 batch-effect-inspector

**批次效应检测+可视化**

## 使用方法

```bash
cd batch-effect-inspector
python batch_effect_inspector.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `表达矩阵CSV路径` | `expression.csv` |
| 2 | `批次信息文件(留空=无)` | `` |
| 3 | `检测方法(PCA/boxplot)` | `PCA` |

### 交互式输入示例

```
表达矩阵CSV路径 [默认: expression.csv]: 
批次信息文件(留空=无) [默认: ]: 
检测方法(PCA/boxplot) [默认: PCA]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT