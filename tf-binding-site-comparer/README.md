# tf-binding-site-comparer

比较两个条件下的TF结合位点差异

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| peak_file1 | 条件1 peak文件BED路径 | cond1_peaks.bed |
| peak_file2 | 条件2 peak文件BED路径 | cond2_peaks.bed |
| output_file | 输出差异peak路径 | diff_peaks.tsv |

## 使用示例

```bash
python tf-binding-site-comparer.py
```

## 依赖

```
无额外依赖
```
