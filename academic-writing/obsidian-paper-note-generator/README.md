# 📖 obsidian-paper-note-generator

**Generate Obsidian paper note templates from DOI or PDF**

## 使用方法

```bash
cd obsidian-paper-note-generator
python obsidian_paper_note_generator.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `PDF path or DOI` | `10.1038/nature12373` |
| 2 | `Template type (minimal/detailed/meeting)` | `minimal` |
| 3 | `Auto-fill metadata (yes/no)` | `yes` |
| 4 | `Obsidian vault path` | `.` |

### 交互式输入示例

```
PDF path or DOI [默认: 10.1038/nature12373]: 
Template type (minimal/detailed/meeting) [默认: minimal]: 
Auto-fill metadata (yes/no) [默认: yes]: 
Obsidian vault path [默认: .]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT