# structural-variant-summarizer

> 结构变异(SV)类型统计+环形图

## 一句话说明

结构变异(SV)类型统计+环形图 — 针对浙大生信研究生+陆慧智课题组（DNA损伤修复）方向优化。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 输入文件路径 | input.txt |
| output_file | 输出文件路径 | output_structural_variant_summarizer.txt |
| param1 | 主参数（阈值/数值） | 0.05 |
| param2 | 辅参数（模式/格式） | default |

## 使用示例

```bash
# Python工具
cd structural-variant-summarizer
python structural_variant_summarizer.py

# R工具
cd structural-variant-summarizer
Rscript structural_variant_summarizer.py
```

所有参数通过交互式 `input()` 输入，带默认值可直接回车跳过。

## 输出格式

- TSV表格文件，带注释行
- 包含处理统计摘要

## 依赖

见 [requirements.txt](./requirements.txt)

## 许可

MIT License — [Newbe](https://github.com/Elephenman/newbe)
