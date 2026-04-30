# haplotype-phaser

## 一句话说明
对VCF变异进行单倍型分型，输出Phased GT字段。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 输入VCF文件 | variants.vcf | 未分型VCF |
| 输出VCF文件 | phased.vcf | 分型后VCF |
| 参考panel | 留空 | 可选的参考面板 |

## 使用示例

```bash
python haplotype_phaser.py
```
