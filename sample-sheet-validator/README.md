# 🧬 sample-sheet-validator

**实验样本表格式校验器**

## 使用方法

```bash
cd sample-sheet-validator
python sample_sheet_validator.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `样本表CSV路径` | `sample_sheet.csv` |
| 2 | `必填列(逗号分隔)` | `sample_id` |
| 3 | `物种(human/mouse)` | `human` |
| 4 | `出校验报告(yes/no)` | `yes` |

### 交互式输入示例

```
样本表CSV路径 [默认: sample_sheet.csv]: 
必填列(逗号分隔) [默认: sample_id]: 
物种(human/mouse) [默认: human]: 
出校验报告(yes/no) [默认: yes]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT