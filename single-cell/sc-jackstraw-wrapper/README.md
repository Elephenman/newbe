# sc-jackstraw-wrapper

## 一句话说明
运行JackStraw分析确定单细胞数据中显著的主成分数量。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| Seurat RDS文件 | seurat.rds | R中的Seurat对象 |
| 输出文件 | jackstraw_results.txt | 显著性检验结果 |
| 重复次数 | 100 | JackStraw重采样次数 |

## 使用示例

```bash
python sc_jackstraw_wrapper.py
```
