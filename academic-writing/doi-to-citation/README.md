# 📖 doi-to-citation

**DOI转多格式引用**

## 使用方法

```bash
cd doi-to-citation
python doi_to_citation.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `DOI列表(逗号分隔或文件路径)` | `10.1038/nature12373` |
| 2 | `格式(APA/MLA/GB-T7714/BibTeX)` | `APA` |

### 交互式输入示例

```
DOI列表(逗号分隔或文件路径) [默认: 10.1038/nature12373]: 
格式(APA/MLA/GB-T7714/BibTeX) [默认: APA]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT