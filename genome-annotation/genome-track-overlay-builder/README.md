# genome-track-overlay-builder

> 基因组多轨道叠加配置生成

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| tracks_config | 轨道配置文件路径 | tracks.json |
| genome_version | 基因组版本 | hg38 |
| region | 显示区域(chr:start-end) | chr1:1000000-2000000 |
| output_file | 叠加配置输出路径 | track_overlay.html |


## 使用示例

```bash
cd genome-track-overlay-builder
python genome-track-overlay-builder.py
```

生成基因组多轨道叠加可视化配置

## 依赖

参见 `requirements.txt`（Python工具，依赖≤5个包）
