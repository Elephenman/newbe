# 🧪 ld-decay-calculator

**LD衰减曲线计算与绘图**

## 使用方法

```bash
cd ld-decay-calculator
python ld_decay_calculator.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `VCF文件路径` | `variants.vcf` |
| 2 | `最大距离(kb)` | `500` |
| 3 | `r2阈值` | `0.2` |
| 4 | `是否出图(yes/no)` | `yes` |

### 交互式输入示例

```
VCF文件路径 [默认: variants.vcf]: 
最大距离(kb) [默认: 500]: 
r2阈值 [默认: 0.2]: 
是否出图(yes/no) [默认: yes]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT