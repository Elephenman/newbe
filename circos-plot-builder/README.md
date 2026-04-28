# 🧪 circos-plot-builder

**Circos环形图数据准备+配置生成**

## 使用方法

```bash
cd circos-plot-builder
python circos_plot_builder.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `Input file path` | `input.txt` |
| 2 | `Output file path` | `output_circos_plot_builder.txt` |
| 3 | `Main parameter (threshold)` | `0.05` |
| 4 | `Secondary parameter (mode)` | `default` |

### 交互式输入示例

```
Input file path [默认: input.txt]: 
Output file path [默认: output_circos_plot_builder.txt]: 
Main parameter (threshold) [默认: 0.05]: 
Secondary parameter (mode) [默认: default]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT