# bam-mate-pair-resolver

> BAM mate-pair信息解析+配对修复

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_bam | 输入BAM文件路径 | sample.bam |
| output_bam | 输出BAM路径 | resolved.bam |
| fix_mates | 是否修复mate信息 | yes |
| report_file | 配对统计报告路径 | mate_pair_report.txt |


## 使用示例

```bash
cd bam-mate-pair-resolver
python bam-mate-pair-resolver.py
```

解析BAM中mate-pair配对信息，检测并修复异常配对

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
