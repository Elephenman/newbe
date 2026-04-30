# 🧪 snp-stats-reporter

**SNP/InDel变异统计一键报告**

## 使用方法

```bash
cd snp-stats-reporter
python snp_stats_reporter.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `VCF文件路径` | `variants.vcf` |
| 2 | `是否按染色体分组(yes/no)` | `yes` |
| 3 | `是否计算MAF(yes/no)` | `yes` |
| 4 | `是否出图(yes/no)` | `no` |

### 交互式输入示例

```
VCF文件路径 [默认: variants.vcf]: 
是否按染色体分组(yes/no) [默认: yes]: 
是否计算MAF(yes/no) [默认: yes]: 
是否出图(yes/no) [默认: no]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT