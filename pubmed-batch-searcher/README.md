# 📖 pubmed-batch-searcher

**PubMed批量检索+结果导出**

## 使用方法

```bash
cd pubmed-batch-searcher
python pubmed_batch_searcher.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `搜索关键词` | `DNA damage repair` |
| 2 | `最大返回数` | `20` |
| 3 | `日期范围(如2020:2025[dp])` | `` |
| 4 | `只取free-fulltext(yes/no)` | `no` |
| 5 | `导出格式(csv/bibtex)` | `csv` |

### 交互式输入示例

```
搜索关键词 [默认: DNA damage repair]: 
最大返回数 [默认: 20]: 
日期范围(如2020:2025[dp]) [默认: ]: 
只取free-fulltext(yes/no) [默认: no]: 
导出格式(csv/bibtex) [默认: csv]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT