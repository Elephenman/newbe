# ZJU Blue Layout变体索引

## 概述

基于实测数据（`zju-blue-tokens.json`），浙大蓝多篇版模板包含 **24个slide**，分为 **8种layout变体**。

所有坐标标注 `data-source="measured"` 表示直接来自模板实测，`data-source="derived"` 表示基于实测推算。

## 变体清单

| 编号 | 类型 | 变体ID | 名称 | 源Slide | 描述 |
|------|------|--------|------|---------|------|
| 功能页 | F1 | F1-cover | 封面页 | Slide 1 | 居中标题+文献列表+校徽+汇报人信息 |
| 功能页 | F2 | F2-toc | 目录页 | Slide 2 | 右上"目录"+编号圆角矩形+论文标题列表 |
| 功能页 | F3 | F3-section-separator | 章节分隔页 | Slide 3/10/15/20 | 右上大字编号+PART标签+左侧编号列表 |
| 功能页 | F4 | F4-ending | 结尾致谢页 | Slide 24 | 类似封面，大字"谢谢聆听" |
| 内容页 | C1 | C1-info | 文献基本信息页 | Slide 4 | 标题栏+左图+右表+关键词+底部内容 |
| 内容页 | C2 | C2-image-text | 左图右文页 | Slide 5 | 标题栏+左大图+右双栏(背景+意义) |
| 内容页 | C3 | C3-flowchart | 流程图页 | Slide 6 | 标题栏+椭圆节点+箭头+标签条 |
| 内容页 | C4 | C4-general | 通用内容页 | Slide 7-9等 | 标题栏+灵活内容区(图表/结果/讨论) |

> **P1-8 FIX**: 变体ID统一使用完整格式（如 `F1-cover` 而非 `F1`），与ppt-architect SKILL.md和ppt-implement LAYOUT_COORDS保持一致。

## 共性组件

所有内容页(C1-C4)共享：
- **标题栏**：编号(29.74pt, 32.35pt, 51.27×36.35pt, 24pt bold) + 标题(79.55pt起, 36.35pt高, 24pt bold) + 分隔线(y≈49pt, 高度1pt)
- **页码Footer**：(706pt, 500.5pt, 216×28.75pt)

## HTML骨架文件

每个变体对应一个HTML文件（960pt×540pt，position:absolute），位于 `zju-blue-layouts/` 目录下：

- `F1-cover.html` — 封面页
- `F2-toc.html` — 目录页
- `F3-section-separator.html` — 章节分隔页
- `F4-ending.html` — 结尾致谢页
- `C1-info.html` — 文献基本信息页
- `C2-image-text.html` — 左图右文页
- `C3-flowchart.html` — 流程图页
- `C4-general.html` — 通用内容页

## 使用方式

1. 选择需要的layout变体（从index中选择F/C编号，使用完整ID如F1-cover）
2. 打开对应HTML文件，替换placeholder内容
3. 浏览器预览确认布局（所有坐标已标注source来源）
4. 如需导出PPTX：按huashu-design的html2pptx.js路线处理（满足4条硬约束），或使用ppt-implement的路线B纯绘制

## 验证注意事项

- 所有坐标来自实测EMU→pt换算（÷12700）
- 模板无渐变（html2pptx兼容）
- 图片是PICTURE shape（img标签兼容，非DIV background-image）
- 颜色使用SCHEME类型（需转换为具体RGB：#003F88等）
