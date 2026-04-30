# 🧪 promoter-extractor

**批量提取基因启动子序列+TSS注释**

## 使用方法

```bash
cd promoter-extractor
python promoter_extractor.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `基因列表文件路径` | `gene_list.txt` |
| 2 | `参考基因组FASTA路径` | `genome.fa` |
| 3 | `GTF注释路径` | `annotation.gtf` |
| 4 | `上游长度(bp)` | `2000` |
| 5 | `下游长度(bp)` | `500` |
| 6 | `过滤重叠(yes/no)` | `yes` |

### 交互式输入示例

```
基因列表文件路径 [默认: gene_list.txt]: 
参考基因组FASTA路径 [默认: genome.fa]: 
GTF注释路径 [默认: annotation.gtf]: 
上游长度(bp) [默认: 2000]: 
下游长度(bp) [默认: 500]: 
过滤重叠(yes/no) [默认: yes]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT