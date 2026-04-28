# snp-ld-block-extractor

从LD矩阵中提取LD block及其tag SNP

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| ld_file | LD矩阵文件CSV路径 | ld_matrix.csv |
| snp_list_file | SNP列表文件路径 | snps.txt |
| output_file | 输出LD block路径 | ld_blocks.tsv |
| r2_threshold | r2阈值 | 0.8 |

## 使用示例

```bash
python snp-ld-block-extractor.py
```

## 依赖

```
pandas
numpy
```
