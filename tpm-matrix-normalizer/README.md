# tpm-matrix-normalizer

## 一句话说明
对TPM表达矩阵进行标准化和log2转换处理。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 表达矩阵文件 | tpm_matrix.tsv | TPM表达矩阵 |
| 输出文件 | tpm_normalized.tsv | 标准化结果 |
| 是否log2转换 | yes | yes=log2, no=原始值 |

## 使用示例

```bash
python tpm_matrix_normalizer.py
```
