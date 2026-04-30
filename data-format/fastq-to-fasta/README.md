# 🧬 fastq-to-fasta

**FASTQ转FASTA + 可选去冗余**

## 使用方法

```bash
cd fastq-to-fasta
python fastq_to_fasta.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `输入FASTQ文件路径` | `sample.fastq` |
| 2 | `是否去冗余(yes/no)` | `yes` |
| 3 | `输出FASTA路径(留空自动)` | `` |

### 交互式输入示例

```
输入FASTQ文件路径 [默认: sample.fastq]: 
是否去冗余(yes/no) [默认: yes]: 
输出FASTA路径(留空自动) [默认: ]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT