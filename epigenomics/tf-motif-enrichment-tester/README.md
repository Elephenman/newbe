# tf-motif-enrichment-tester

> TF motif富集统计检验

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| target_regions | 目标BED文件路径 | target_regions.bed |
| background_regions | 背景BED文件路径 | background_regions.bed |
| motif_file | motif文件路径(JASPAR) | motifs.meme |
| output_file | 富集结果路径 | motif_enrichment.tsv |


## 使用示例

```bash
cd tf-motif-enrichment-tester
python tf-motif-enrichment-tester.py
```

对目标区域vs背景区域做TF motif富集检验

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
