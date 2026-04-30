# 🛠️ conda-env-checker

**项目环境依赖一致性检查**

## 使用方法

```bash
cd conda-env-checker
python conda_env_checker.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `conda环境名或env.yml路径` | `base` |
| 2 | `项目脚本目录` | `` |
| 3 | `生成lock文件(yes/no)` | `yes` |
| 4 | `检测版本冲突(yes/no)` | `yes` |

### 交互式输入示例

```
conda环境名或env.yml路径 [默认: base]: 
项目脚本目录 [默认: ]: 
生成lock文件(yes/no) [默认: yes]: 
检测版本冲突(yes/no) [默认: yes]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT