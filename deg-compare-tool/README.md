# 📊 deg-compare-tool

**多组DEG结果交叉对比**

## 使用方法

```bash
cd deg-compare-tool
python deg_compare_tool.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `DEG结果文件路径(逗号分隔多个)` | `deg1.csv` |
| 2 | `对比模式(Venn/UpSet/bar)` | `Venn` |
| 3 | `基因ID列名` | `gene` |

### 交互式输入示例

```
DEG结果文件路径(逗号分隔多个) [默认: deg1.csv]: 
对比模式(Venn/UpSet/bar) [默认: Venn]: 
基因ID列名 [默认: gene]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT