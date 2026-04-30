# 📖 paper-pdf-meta-extractor

**PDF论文元数据自动提取**

## 使用方法

```bash
cd paper-pdf-meta-extractor
python paper_pdf_meta_extractor.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `PDF文件/目录路径` | `paper.pdf` |
| 2 | `提取维度(all/title/authors/doi/abstract)` | `all` |
| 3 | `生成Obsidian笔记(yes/no)` | `no` |
| 4 | `Obsidian vault路径` | `.` |

### 交互式输入示例

```
PDF文件/目录路径 [默认: paper.pdf]: 
提取维度(all/title/authors/doi/abstract) [默认: all]: 
生成Obsidian笔记(yes/no) [默认: no]: 
Obsidian vault路径 [默认: .]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT