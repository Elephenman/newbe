# multi-fasta-concatenator

将多个FASTA文件合并为一个，添加文件名前缀避免ID冲突

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_dir | 输入FASTA目录 | . |
| output_file | 合并输出FASTA路径 | concatenated.fa |
| add_prefix | 添加文件名前缀(yes/no) | yes |
| pattern | 文件匹配模式 | *.fasta |

## 使用示例

```bash
python multi-fasta-concatenator.py
```

## 依赖

```
无额外依赖
```
