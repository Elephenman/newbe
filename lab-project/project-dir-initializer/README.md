# 🛠️ project-dir-initializer

**科研项目目录一键初始化**

## 使用方法

```bash
cd project-dir-initializer
python project_dir_initializer.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `项目名称` | `my_project` |
| 2 | `数据类型(RNA-seq/scRNA-seq/WGS/ChIP-seq/general)` | `RNA-seq` |
| 3 | `生成README(yes/no)` | `yes` |
| 4 | `git init(yes/no)` | `yes` |

### 交互式输入示例

```
项目名称 [默认: my_project]: 
数据类型(RNA-seq/scRNA-seq/WGS/ChIP-seq/general) [默认: RNA-seq]: 
生成README(yes/no) [默认: yes]: 
git init(yes/no) [默认: yes]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT