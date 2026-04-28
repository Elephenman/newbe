# rna-seq-normalizer

对RNA-seq计数矩阵进行TPM/FPKM/RPKM/CPM标准化

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 计数矩阵CSV(行=基因,列=样本) | counts.csv |
| output_file | 标准化输出路径 | normalized.csv |
| method | 方法(tpm/fpkm/rpkm/cpm) | tpm |
| gene_length_file | 基因长度CSV(基因,长度) | gene_lengths.csv |

## 使用示例

```bash
python rna-seq-normalizer.py
```

## 依赖

```
pandas
numpy
```
