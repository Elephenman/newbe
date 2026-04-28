# enhancer-target-linker

基于Hi-C/ChIA-PET数据关联增强子与靶基因

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| interaction_file | 交互文件BEDPE路径 | interactions.bedpe |
| gene_file | 基因注释GTF路径 | genes.gtf |
| output_file | 输出增强子-基因关联路径 | enhancer_gene.tsv |
| max_distance | 最大关联距离(bp) | 1000000 |

## 使用示例

```bash
python enhancer-target-linker.py
```

## 依赖

```
无额外依赖
```
