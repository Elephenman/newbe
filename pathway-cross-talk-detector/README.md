# pathway-cross-talk-detector

> 通路交叉对话检测(共享基因分析)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| pathway_file | 通路基因集文件(GMT) | pathways.gmt |
| min_shared | 最小共享基因数 | 3 |
| output_file | 交叉对话结果路径 | crosstalk_results.tsv |
| plot_output | 网络图路径 | crosstalk_network.png |


## 使用示例

```bash
cd pathway-cross-talk-detector
Rscript pathway-cross-talk-detector.R
```

检测通路间的交叉对话(共享基因重叠)

## 依赖

参见 `requirements.txt`（R工具，依赖≤5个包）
