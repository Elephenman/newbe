# lab-protocol-versioner

> 实验protocol版本管理

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| protocol_dir | protocol目录路径 | protocols |
| action | 操作(list/create/update/diff) | list |
| output_file | 版本报告路径 | protocol_versions.txt |


## 使用示例

```bash
cd lab-protocol-versioner
python lab-protocol-versioner.py
```

管理实验protocol的版本和变更记录

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
