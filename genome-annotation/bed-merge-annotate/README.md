# 🧬 bed-merge-annotate

**BED文件合并+区间注释**

## 使用方法

```bash
cd bed-merge-annotate
python bed_merge_annotate.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `BED文件路径` | `regions.bed` |
| 2 | `合并距离阈值(bp)` | `0` |
| 3 | `注释GTF路径(留空=无)` | `` |
| 4 | `输出格式(bed/csv)` | `bed` |

### 交互式输入示例

```
BED文件路径 [默认: regions.bed]: 
合并距离阈值(bp) [默认: 0]: 
注释GTF路径(留空=无) [默认: ]: 
输出格式(bed/csv) [默认: bed]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT