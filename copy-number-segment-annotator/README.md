# copy-number-segment-annotator

拷贝数变异片段基因注释

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| cnv_file | CNV片段文件(TSV: chr,start,end,cn) | cnv_segments.tsv |
| gene_file | 基因注释GTF路径 | genes.gtf |
| output_file | 输出注释路径 | cnv_annotated.tsv |

## 使用示例

```bash
python copy-number-segment-annotator.py
```

## 依赖

```
无额外依赖
```
