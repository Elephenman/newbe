# methylation-beta-calculator

从bedGraph计算甲基化beta值并做基本统计

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 甲基化信号文件(chr,pos,methylated,total) | methylation.bedgraph |
| output_file | 输出beta值路径 | beta_values.tsv |
| min_coverage | 最低覆盖度 | 5 |

## 使用示例

```bash
python methylation-beta-calculator.py
```

## 依赖

```
无额外依赖
```
