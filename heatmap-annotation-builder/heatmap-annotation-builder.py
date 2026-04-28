#!/usr/bin/env python3
"""热图行列注释文件构建器"""

def main():
    sample_file = input("样本信息CSV(样本,组,批次等) [samples.csv]: ") or "samples.csv"
    output_file = input("输出注释文件路径 [heatmap_anno.csv]: ") or "heatmap_anno.csv"
    color_scheme = input("配色方案(set1/set2/dark2) [set1]: ") or "set1"
    import pandas as pd
    df = pd.read_csv(sample_file, index_col=0)
    anno = df.copy()
    with open(output_file, "w") as out:
        anno.to_csv(out)
    n_cols = anno.shape[1]
    n_groups = sum(anno[c].nunique() for c in anno.columns)
    print(f"注释文件: {n_cols} 列, {n_groups} 总分组 -> {output_file}")


if __name__ == "__main__":
    main()
