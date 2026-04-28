# fastq-barcode-splitter

> FASTQ按barcode/标签拆分文件

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_fastq | 输入FASTQ文件路径 | sample.fastq.gz |
| barcode_file | barcode列表文件路径 | barcodes.txt |
| barcode_position | barcode位置(start/end) | start |
| barcode_length | barcode长度 | 6 |
| output_dir | 输出目录 | split_output |


## 使用示例

```bash
cd fastq-barcode-splitter
python fastq-barcode-splitter.py
```

按barcode标签拆分FASTQ到多个文件

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
