# 🎨 figure-size-checker

**论文图片尺寸/格式合规检查**

## 使用方法

```bash
cd figure-size-checker
python figure_size_checker.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `图片文件/目录路径` | `figures/` |
| 2 | `目标期刊(Nature/Cell/Science/custom)` | `Nature` |
| 3 | `检查维度(DPI/尺寸/格式/all)` | `all` |

### 交互式输入示例

```
图片文件/目录路径 [默认: figures/]: 
目标期刊(Nature/Cell/Science/custom) [默认: Nature]: 
检查维度(DPI/尺寸/格式/all) [默认: all]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT