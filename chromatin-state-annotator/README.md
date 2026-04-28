# chromatin-state-annotator

ChromHMM/Segway染色质状态注释工具

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| state_file | 染色质状态BED路径 | chromatin_states.bed |
| region_file | 目标区域BED路径 | regions.bed |
| output_file | 输出注释路径 | annotated_regions.tsv |

## 使用示例

```bash
python chromatin-state-annotator.py
```

## 依赖

```
无额外依赖
```
