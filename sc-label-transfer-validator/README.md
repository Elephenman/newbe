# sc-label-transfer-validator

## 一句话说明
验证单细狍标签转移结果的准确性和一致性。

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 参考标签文件 | ref_labels.txt | 已知细胞类型标签 |
| 查询标签文件 | query_labels.txt | 转移后的标签 |
| 输出文件 | transfer_validation.txt | 验证报告 |

## 使用示例

```bash
python sc_label_transfer_validator.py
```
