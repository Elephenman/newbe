# enhancer-signal-quantifier

> 增强子信号定量(ATAC/H3K27ac)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| enhancer_bed | 增强子BED文件路径 | enhancers.bed |
| signal_file | 信号文件路径(BEDGRAPH) | signal.bedgraph |
| output_file | 定量结果路径 | enhancer_signal.tsv |
| normalize | 是否标准化(RPKM) | yes |


## 使用示例

```bash
cd enhancer-signal-quantifier
python enhancer-signal-quantifier.py
```

定量增强子区域的ATAC/H3K27ac信号强度

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
