# 📖 reference-cleaner

**参考文献格式统一清洗器**

## 使用方法

```bash
cd reference-cleaner
python reference_cleaner.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `引文文件路径(bib/ris/csv)` | `references.bib` |
| 2 | `目标格式(APA/MLA/GB-T7714/BibTeX)` | `APA` |
| 3 | `检查DOI有效性(yes/no)` | `yes` |
| 4 | `补全缺失字段(yes/no)` | `yes` |

### 交互式输入示例

```
引文文件路径(bib/ris/csv) [默认: references.bib]: 
目标格式(APA/MLA/GB-T7714/BibTeX) [默认: APA]: 
检查DOI有效性(yes/no) [默认: yes]: 
补全缺失字段(yes/no) [默认: yes]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT