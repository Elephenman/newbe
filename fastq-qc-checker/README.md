# 🧬 fastq-qc-checker

**FASTQ质量一键体检报告
纯Python解析，不依赖FastQC，3秒出结果

功能：
- reads总数、平均长度、Q20/Q30比例
- GC含量分布、N碱基比例
- adapter残留检测（Illumina TruSeq等常见adapter）
- 终端打印报告 + 可选txt/html报告文件**

## 使用方法

```bash
cd fastq-qc-checker
python fastq_qc_checker.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `输入FASTQ文件路径` | `sample.fastq.gz` |
| 2 | `是否生成报告文件` | `yes` |
| 3 | `报告格式(txt/html)` | `txt` |

### 交互式输入示例

```
输入FASTQ文件路径 [默认: sample.fastq.gz]: 
是否生成报告文件 [默认: yes]: 
报告格式(txt/html) [默认: txt]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT