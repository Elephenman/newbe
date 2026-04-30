# replication-origin-predictor

> 复制起始点预测与注释

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_fasta | 基因组FASTA路径 | genome.fa |
| input_data | Repli-seq或ori数据路径(可选) | NA |
| window_size | 搜索窗口大小(bp) | 1000 |
| output_file | 预测结果路径 | replication_origins.tsv |


## 使用示例

```bash
cd replication-origin-predictor
python replication-origin-predictor.py
```

基于AT富集和序列特征预测复制起始点

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
