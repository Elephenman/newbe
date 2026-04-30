# 🧪 dna-damage-gene-collector

**DNA损伤修复相关基因集收集器
🔥 针对陆慧智课题组（DNA损伤修复方向）

功能：
- 预置7大修复通路基因字典（HR/NHEJ/BER/MMR/SSB/FA/p53）
- 支持多通路选择和交叉分析
- 可选PubMed API补充搜索
- 输出CSV(符号+Ensembl) + Venn交叉图 + 基因功能简述**

## 使用方法

```bash
cd dna-damage-gene-collector
python dna_damage_gene_collector.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `选择通路(多选，逗号分隔，如HR,NHEJ,BER)` | `HR` |
| 2 | `物种(human/mouse)` | `human` |
| 3 | `是否PubMed补充搜索(yes/no)` | `no` |
| 4 | `是否包含p53通路(yes/no)` | `no` |
| 5 | `是否绘制通路交叉Venn图(yes/no)` | `yes` |

### 交互式输入示例

```
选择通路(多选，逗号分隔，如HR,NHEJ,BER) [默认: HR]: 
物种(human/mouse) [默认: human]: 
是否PubMed补充搜索(yes/no) [默认: no]: 
是否包含p53通路(yes/no) [默认: no]: 
是否绘制通路交叉Venn图(yes/no) [默认: yes]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT