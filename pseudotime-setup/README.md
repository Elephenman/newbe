# 🔬 pseudotime-setup

**拟时序分析启动器(Monocle3/Slingshot)**

## 使用方法

```bash
cd pseudotime-setup
Rscript pseudotime_setup.R
```

运行后按提示依次输入参数，所有参数均有默认值，直接回车即可使用默认值。

### 参数说明

| # | 参数 | 默认值 |
|---|------|--------|
| 1 | `Seurat对象路径(rds)` | `seurat.rds` |
| 2 | `root定义(cluster号/基因名)` | `3` |
| 3 | `轨迹方法(monocle3/slingshot)` | `monocle3` |

### 交互式输入示例

```
Seurat对象路径(rds) [默认: seurat.rds]: 
root定义(cluster号/基因名) [默认: 3]: 
轨迹方法(monocle3/slingshot) [默认: monocle3]: 
```

## 依赖

```r
install.packages('monocle3')  # 或 BiocManager::install('monocle3')
install.packages('slingshot')  # 或 BiocManager::install('slingshot')
```

## 输出

脚本运行后会在当前目录生成结果文件，具体文件名见运行提示。

## License

MIT