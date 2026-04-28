# 📊 pca-tsne-umap-plotter

**表达矩阵降维可视化三合一**

## 使用方法

```bash
cd pca-tsne-umap-plotter
python pca_tsne_umap_plotter.py
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `表达矩阵CSV路径` | `expression.csv` |
| 2 | `分组标签文件路径(留空=无分组)` | `` |
| 3 | `降维方法(PCA/tSNE/UMAP/all)` | `all` |
| 4 | `是否标注样本名(yes/no)` | `no` |
| 5 | `配色方案(default/Set2/tab10)` | `default` |

### 交互式输入示例

```
表达矩阵CSV路径 [默认: expression.csv]: 
分组标签文件路径(留空=无分组) [默认: ]: 
降维方法(PCA/tSNE/UMAP/all) [默认: all]: 
是否标注样本名(yes/no) [默认: no]: 
配色方案(default/Set2/tab10) [默认: default]: 
```

## 依赖

无外部依赖，纯Python标准库

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT