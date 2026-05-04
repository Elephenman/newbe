# ZJU Blue 图片处理策略

## 源文件

模板路径：`A:\kuake\文献汇报01-浙大蓝-多篇版.pptx`

## 校徽处理

### 提取方式
1. 打开模板 → 视图 → 幻灯片母版 → 找到校徽组合图形 → 右键另存为图片
2. 或用python-pptx提取PICTURE shape的image blob：
   ```python
   from pptx import Presentation
   from pptx.enum.shapes import MSO_SHAPE_TYPE

   def extract_images_from_slide(slide, output_dir='extracted_images'):
       """提取slide中所有图片（包括GROUP内的嵌套图片）"""
       import os
       os.makedirs(output_dir, exist_ok=True)
       count = 0
       for shape in slide.shapes:
           count += _extract_from_shape(shape, output_dir, count)
       return count

   def _extract_from_shape(shape, output_dir, count):
       """递归提取shape中的图片（处理PICTURE和GROUP两种类型）"""
       if shape.shape_type == 13:  # MSO_SHAPE_TYPE.PICTURE
           with open(f'{output_dir}/img_{shape.name}_{count}.png', 'wb') as f:
               f.write(shape.image.blob)
           return 1
       elif shape.shape_type == 6:  # MSO_SHAPE_TYPE.GROUP
           # GROUP shape包含子shape，需递归遍历
           sub_count = 0
           for child in shape.shapes:
               sub_count += _extract_from_shape(child, output_dir, count + sub_count)
           return sub_count
       return 0

   # 使用示例
   prs = Presentation(template_path)
   for slide_idx, slide in enumerate(prs.slides):
       n = extract_images_from_slide(slide, f'extracted_slide_{slide_idx}')
       print(f'Slide {slide_idx}: extracted {n} images')
   ```

> **⚠️ GROUP shape注意事项**：封面页校徽是GROUP组合图形（6个子shape），不是单个PICTURE。
> 必须使用上述递归提取函数，而非仅遍历 `slide.shapes` 中 `shape_type == 13` 的元素。
> 忽略此点会导致封面校徽无法提取。

### 校徽变体
| 用途 | 尺寸(pt) | 位置 | 文件 |
|------|---------|------|------|
| 封面页底部小图标 | 22.68×22.68 | (278.47pt, 462.57pt) | zju_emblem_small.png |
| 封面页顶部组合图 | 220.22×50.18 (含文字) | (369.89pt, 57.52pt) | zju_emblem_group.png |
| 章节分隔页右上角 | 需从母版确认 | 右上角区域 | 同上 |

### 校徽使用规则（浙大品牌规范）
- 禁止变形、拉伸、旋转
- 禁止更改颜色
- 保留原始比例（宽高比1:1或按原始比例）
- 周围留白不小于校徽宽度的1/4

## 论文图片嵌入策略

### 来源分类
| 来源 | 处理方式 | 说明 |
|------|---------|------|
| paper-deep-read提取的论文原图 | 直接引用 | 来自images/目录，保持原始分辨率 |
| 用户自制的数据图表 | 占位框+说明 | 暂用灰色占位区，标注"插入XXX图表" |
| 模板内置装饰图 | 按需使用 | 如背景矩形、图标等 |

### 图片尺寸规范（基于实测）

| 页面类型 | 图片区域 | 建议图片尺寸(pt) |
|---------|---------|-----------------|
| 左图右文(Slide 5) | 左侧 | 439.01×292.2 (最大)，实际可用439×292 |
| 大图+信息表(Slide 4) | 左侧 | 562.26×273.08 (最大) |
| 全宽图片 | 全内容区 | ~(828-868)×(342-400) |
| 双图对比 | 各半 | ~(439)×(292) 每侧 |

### 图片格式要求
- 接受格式：PNG (首选)、JPEG (次要)
- DPI：模板内置图片72-192 DPI，建议输出≥150 DPI
- 裁剪：保持原比例，不要拉伸变形
- 去白边：论文截图建议裁掉多余白边

## 图片占位框设计

当无实际图片时，使用灰色占位框：

```python
# python-pptx占位框代码
shape = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE,
    left, top, width, height
)
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0xD9, 0xD9, 0xD9)  # #D9D9D9
shape.line.fill.background()
# 在占位框中心添加提示文字
tf = shape.text_frame
tf.text = "插入[图片描述]"
```

## Caption规范

基于实测：caption位置在图片下方，字号14pt，格式：

```
图1  输入图示标题及标注
```

位置示例：(164.41pt, 462.61pt)，宽度约169.67pt，高度24.23pt

## 关键词标签

基于实测：圆角矩形标签，用于文献标签和关键词：

| 类型 | 尺寸(pt) | 字号(pt) | 填充 |
|------|---------|---------|------|
| 文献标签(文献一/二/三) | 86.25×29.08 | 继承主题 | SCHEME(2)填充 |
| 编号标签(01-04) | 52.64×50.14 | 28pt bold | SCHEME(2)填充 |
| 关键词标签 | 124.77×32.25 | 继承主题 | SCHEME(2)或透明