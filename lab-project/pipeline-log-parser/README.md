# 🛠️ pipeline-log-parser

**分析流程日志解析+耗时统计**

## 使用方法

```bash
cd pipeline-log-parser
python pipeline_log_parser.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `日志文件路径` | `pipeline.log` |
| 2 | `出时间线图(yes/no)` | `yes` |
| 3 | `检测失败步骤(yes/no)` | `yes` |

### 交互式输入示例

```
日志文件路径 [默认: pipeline.log]: 
出时间线图(yes/no) [默认: yes]: 
检测失败步骤(yes/no) [默认: yes]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT