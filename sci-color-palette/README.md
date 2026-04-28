# 🎨 sci-color-palette

**科研绘图配色方案生成器**

## 使用方法

```bash
cd sci-color-palette
python sci_color_palette.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `颜色数量` | `8` |
| 2 | `用途(连续/离散/heatmap)` | `discrete` |
| 3 | `参考期刊(Nature/Science/Cell/NEJM)` | `Nature` |
| 4 | `色盲友好(yes/no)` | `yes` |
| 5 | `展示图(yes/no)` | `yes` |

### 交互式输入示例

```
颜色数量 [默认: 8]: 
用途(连续/离散/heatmap) [默认: discrete]: 
参考期刊(Nature/Science/Cell/NEJM) [默认: Nature]: 
色盲友好(yes/no) [默认: yes]: 
展示图(yes/no) [默认: yes]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT