# 🔬 dna-damage-gene-collector

**DNA损伤修复相关基因集收集器** — 🔥针对陆慧智课题组（DNA损伤修复方向）

## 功能

- ✅ 预置7大修复通路基因字典（HR/NHEJ/BER/MMR/SSB/FA/p53）
- ✅ 多通路选择和交叉基因分析
- ✅ 可选PubMed API补充搜索新发现基因
- ✅ 输出CSV(符号+Ensembl+功能) + Venn交叉图 + 候选基因列表

## 支持通路

| 代码 | 通路 | 基因数 | 说明 |
|------|------|--------|------|
| HR | 同源重组 | ~20 | 利用同源模板精确修复DSB |
| NHEJ | 同源末端连接 | ~14 | 无模板直接连接DSB末端 |
| BER | 碱基切除修复 | ~14 | 修复单碱基损伤 |
| MMR | 错配修复 | ~13 | 修复复制错配 |
| SSB | 单链断裂修复 | ~10 | 修复单链断裂 |
| FA | 范可尼贫血通路 | ~14 | 修复DNA交联 |
| p53 | p53通路 | ~11 | DNA损伤响应与细胞命运 |

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 选择通路 | 多选，逗号分隔 | HR,NHEJ,BER |
| 物种 | human/mouse | human |
| PubMed补充搜索 | yes/no | no |
| 包含p53通路 | yes/no | no |
| 是否绘制Venn图 | yes/no | yes |

## 使用示例

```bash
python dna_damage_gene_collector.py
```

交互式输入：
```
选择通路(多选，逗号分隔) [默认: HR,NHEJ,BER]: HR,NHEJ,MMR,p53
物种(human/mouse) [默认: human]: human
是否PubMed补充搜索 [默认: no]: yes
是否包含p53通路 [默认: no]: yes
是否绘制通路交叉Venn图 [默认: yes]: yes
```

## 依赖

```
matplotlib>=3.0
matplotlib-venn>=0.11
requests>=2.20  # PubMed搜索可选
```

## 输出

- `dna_damage_genes_HR,NHEJ,BER.csv` — 基因列表
- `dna_damage_genes_pubmed_candidates.csv` — PubMed候选基因
- `dna_damage_genes_venn.png` — 通路交叉Venn图

## License

MIT