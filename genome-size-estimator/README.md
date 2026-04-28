# 🧬 genome-size-estimator

**K-mer频率估算基因组大小+杂合度**

## 使用方法

```bash
cd genome-size-estimator
python genome_size_estimator.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `Input file path` | `input.txt` |
| 2 | `Output file path` | `output_genome_size_estimator.txt` |
| 3 | `Main parameter (threshold)` | `0.05` |
| 4 | `Secondary parameter (mode)` | `default` |

### 交互式输入示例

```
Input file path [默认: input.txt]: 
Output file path [默认: output_genome_size_estimator.txt]: 
Main parameter (threshold) [默认: 0.05]: 
Secondary parameter (mode) [默认: default]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT