# splice-junction-counter

从STAR SJ.out.tab统计剪接junction并注释已知/新颖

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | STAR SJ.out.tab路径 | SJ.out.tab |
| output_file | 输出统计路径 | junction_counts.tsv |
| min_count | 最低junction read数 | 5 |

## 使用示例

```bash
python splice-junction-counter.py
```

## 依赖

```
无额外依赖
```
