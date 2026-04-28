# fasta-alignment-viewer

> FASTA多序列比对可视化

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | FASTA比对文件路径 | alignment.fasta |
| output_file | 可视化图路径 | alignment_view.png |
| color_scheme | 配色方案(clustal/blast) | clustal |
| max_seqs | 最大显示序列数 | 50 |


## 使用示例

```bash
cd fasta-alignment-viewer
python fasta-alignment-viewer.py
```

将FASTA多序列比对结果可视化展示

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
