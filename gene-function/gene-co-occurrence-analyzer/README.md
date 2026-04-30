# gene-co-occurrence-analyzer

> 基因共出现频率分析+网络构建

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 基因列表文件(每行一组基因) | gene_groups.txt |
| min_co_occurrence | 最小共出现次数 | 2 |
| output_file | 网络输出路径 | co_occurrence_network.tsv |
| network_plot | 网络图路径 | co_occurrence_network.png |


## 使用示例

```bash
cd gene-co-occurrence-analyzer
python gene-co-occurrence-analyzer.py
```

分析基因共出现频率并构建共出现网络

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
