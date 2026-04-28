# sc-dim-loadings-extractor

## 一句话说明
从单细胞Seurat对象提取PCA等降维的基因载荷信息。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| Seurat RDS文件 | seurat.rds | R中的Seurat对象 |
| 输出文件 | dim_loadings.tsv | 载荷矩阵 |
| 提取的PC数 | 10 | 降维维度数量 |

## 使用示例

```bash
python sc_dim_loadings_extractor.py
```
