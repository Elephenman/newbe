# 📊 tpm-fpkm-calculator

**raw counts → TPM/FPKM/CPM转换器**

## 使用方法

```bash
cd tpm-fpkm-calculator
python tpm_fpkm_calculator.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `count矩阵CSV路径` | `counts.csv` |
| 2 | `基因长度文件路径(基因名+长度,TSV)` | `gene_lengths.tsv` |
| 3 | `转换类型(TPM/FPKM/CPM/all)` | `TPM` |
| 4 | `是否log2转换(yes/no)` | `no` |

### 交互式输入示例

```
count矩阵CSV路径 [默认: counts.csv]: 
基因长度文件路径(基因名+长度,TSV) [默认: gene_lengths.tsv]: 
转换类型(TPM/FPKM/CPM/all) [默认: TPM]: 
是否log2转换(yes/no) [默认: no]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT