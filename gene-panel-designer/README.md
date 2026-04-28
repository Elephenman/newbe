# gene-panel-designer

> 基因Panel设计(靶向测序)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_genes | 目标基因列表文件路径 | target_genes.txt |
| input_gtf | GTF注释路径 | annotation.gtf |
| flank_size | 侧翼区域大小(bp) | 50 |
| min_coverage | 最小覆盖度要求 | 0.8 |
| output_file | Panel设计结果路径 | gene_panel.tsv |


## 使用示例

```bash
cd gene-panel-designer
python gene-panel-designer.py
```

根据目标基因列表设计靶向测序Panel

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
