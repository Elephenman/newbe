# genome-synteny-block-detector

> 基因组同线性区块检测

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 同线性数据文件路径 | synteny_data.tsv |
| min_block_size | 最小区块大小(bp) | 100000 |
| min_genes | 最小区块基因数 | 5 |
| output_file | 检测结果路径 | synteny_blocks.tsv |


## 使用示例

```bash
cd genome-synteny-block-detector
python genome-synteny-block-detector.py
```

检测基因组间的同线性保守区块

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
