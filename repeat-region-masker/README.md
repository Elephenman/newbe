# repeat-region-masker

> 基因组重复序列标注+mask文件生成

## 一句话说明

基因组重复序列标注+mask文件生成 — 针对浙大生信研究生+陆慧智课题组（DNA损伤修复）方向优化。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 输入文件路径 | input.txt |
| output_file | 输出文件路径 | output_repeat_region_masker.txt |
| param1 | 主参数（阈值/数值） | 0.05 |
| param2 | 辅参数（模式/格式） | default |

## 使用示例

```bash
# Python工具
cd repeat-region-masker
python repeat_region_masker.py

# R工具
cd repeat-region-masker
Rscript repeat_region_masker.py
```

所有参数通过交互式 `input()` 输入，带默认值可直接回车跳过。

## 输出格式

- TSV表格文件，带注释行
- 包含处理统计摘要

## 依赖

见 [requirements.txt](./requirements.txt)

## 许可

MIT License — [Newbe](https://github.com/Elephenman/newbe)
