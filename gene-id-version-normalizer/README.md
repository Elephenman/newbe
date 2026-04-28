# gene-id-version-normalizer

统一基因ID格式(去除版本号/Ensembl转Symbol等)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 输入基因列表(每行一个) | gene_list.txt |
| output_file | 标准化输出路径 | normalized_genes.txt |
| input_type | 输入ID类型(ensembl/entrez/symbol) | ensembl |
| output_type | 输出ID类型(symbol/ensembl/entrez) | symbol |

## 使用示例

```bash
python gene-id-version-normalizer.py
```

## 依赖

```
无额外依赖
```
