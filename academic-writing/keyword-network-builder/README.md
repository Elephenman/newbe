# 🧪 keyword-network-builder

**文献关键词共现网络构建**

## 使用方法

```bash
cd keyword-network-builder
python keyword_network_builder.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `文献列表文件(title+keywords TSV)` | `papers.tsv` |
| 2 | `最小共现次数` | `2` |
| 3 | `出网络图(yes/no)` | `yes` |
| 4 | `布局(force/circular)` | `force` |

### 交互式输入示例

```
文献列表文件(title+keywords TSV) [默认: papers.tsv]: 
最小共现次数 [默认: 2]: 
出网络图(yes/no) [默认: yes]: 
布局(force/circular) [默认: force]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT