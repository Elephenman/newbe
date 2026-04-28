# 🧪 motif-scanner

**DNA序列motif扫描**

## 使用方法

```bash
cd motif-scanner
python motif_scanner.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `序列FASTA路径` | `sequences.fasta` |
| 2 | `motif字典(内置JASPAR/自定义文件路径)` | `JASPAR` |
| 3 | `p-value阈值` | `0.05` |
| 4 | `是否出图(yes/no)` | `no` |

### 交互式输入示例

```
序列FASTA路径 [默认: sequences.fasta]: 
motif字典(内置JASPAR/自定义文件路径) [默认: JASPAR]: 
p-value阈值 [默认: 0.05]: 
是否出图(yes/no) [默认: no]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT