# 🧪 cnv-segment-plotter

**CNV分段结果可视化**

## 使用方法

```bash
cd cnv-segment-plotter
python cnv_segment_plotter.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `CNV结果文件路径(seg/CSV)` | `cnv_segments.seg` |
| 2 | `标注关键区域(yes/no)` | `yes` |
| 3 | `是否出热图(yes/no)` | `no` |
| 4 | `图片格式(png/pdf)` | `png` |

### 交互式输入示例

```
CNV结果文件路径(seg/CSV) [默认: cnv_segments.seg]: 
标注关键区域(yes/no) [默认: yes]: 
是否出热图(yes/no) [默认: no]: 
图片格式(png/pdf) [默认: png]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT