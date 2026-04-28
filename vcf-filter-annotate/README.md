# 🧬 vcf-filter-annotate

**VCF变异过滤+注释格式化**

## 使用方法

```bash
cd vcf-filter-annotate
python vcf_filter_annotate.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `输入VCF文件路径` | `variants.vcf` |
| 2 | `最小QUAL阈值` | `30` |
| 3 | `最小DP阈值` | `10` |
| 4 | `最大缺失率` | `0.5` |
| 5 | `是否保留INDEL(yes/no)` | `yes` |
| 6 | `输出格式(vcf/tsv)` | `tsv` |

### 交互式输入示例

```
输入VCF文件路径 [默认: variants.vcf]: 
最小QUAL阈值 [默认: 30]: 
最小DP阈值 [默认: 10]: 
最大缺失率 [默认: 0.5]: 
是否保留INDEL(yes/no) [默认: yes]: 
输出格式(vcf/tsv) [默认: tsv]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT