# genomic-coordinate-converter

基因组坐标系统转换(hg19->hg38等,基于chain文件)

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 输入坐标BED路径 | coords_hg19.bed |
| output_file | 输出转换后BED路径 | coords_hg38.bed |
| from_build | 源基因组版本 | hg19 |
| to_build | 目标基因组版本 | hg38 |

## 使用示例

```bash
python genomic-coordinate-converter.py
```

## 依赖

```
无额外依赖
```
