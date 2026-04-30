# gtf-exon-extractor

## 一句话说明
从GTF注释文件中提取外显子坐标和长度信息到BED格式。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| GTF文件路径 | annotation.gtf | 基因组注释文件 |
| 输出BED文件 | exons.bed | 外显子坐标输出 |
| 指定基因ID | 留空 | 可选，提取特定基因 |

## 使用示例

```bash
python gtf_exon_extractor.py
```
