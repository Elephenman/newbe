# 🧬 fastq-qc-checker

**FASTQ质量一键体检报告** — 纯Python解析，不依赖FastQC，3秒出结果

## 功能

- ✅ reads总数、平均长度统计
- ✅ Q20/Q30质量比例计算
- ✅ GC含量分布可视化
- ✅ N碱基比例检测
- ✅ Illumina/Nextera adapter残留检测
- ✅ 终端报告 + 可选txt/html报告文件

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| FASTQ文件路径 | 输入的FASTQ文件 | sample.fastq.gz |
| 是否生成报告文件 | yes/no | yes |
| 报告格式 | txt 或 html | txt |

## 使用示例

```bash
python fastq_qc_checker.py
```

交互式输入示例：
```
输入FASTQ文件路径 [默认: sample.fastq.gz]: /data/sample_R1.fastq
是否生成报告文件 [默认: yes]: yes
报告格式(txt/html) [默认: txt]: html
```

## 依赖

```
# requirements.txt — 无外部依赖，纯Python标准库
```

## 输出

- 终端打印彩色结构化报告
- 可选 `{filename}_qc_report.txt` 或 `{filename}_qc_report.html`

## 质量评估标准

| 指标 | 优秀 | 一般 | 较差 |
|------|------|------|------|
| Q20 | ≥90% | 80-90% | <80% |
| Q30 | ≥85% | 70-85% | <70% |
| N碱基 | <0.5% | - | ≥0.5% |
| Adapter | <1% | - | ≥1% |

## License

MIT