# fastq-subset-sampler

从FASTQ文件中随机采样指定数量或比例的reads

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 输入FASTQ文件路径 | input.fastq |
| output_file | 输出FASTQ路径 | sampled.fastq |
| sample_type | 采样方式(count/ratio) | ratio |
| sample_value | 采样数量或比例 | 0.1 |
| seed | 随机种子 | 42 |

## 使用示例

```bash
python fastq-subset-sampler.py
```

## 依赖

```
无额外依赖
```
