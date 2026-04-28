#!/usr/bin/env python3
"""多组学数据整合辅助(联合矩阵构建+基础分析)"""

def main():
    omics_files = input("组学数据文件(逗号分隔CSV) [omics1.csv,omics2.csv]: ") or "omics1.csv,omics2.csv"
    output_file = input("整合输出矩阵路径 [integrated.csv]: ") or "integrated.csv"
    method = input("整合方式(concat/intersect) [intersect]: ") or "intersect"
    import pandas as pd, numpy as np
    files = [f.strip() for f in omics_files.split(",")]
    dfs = [pd.read_csv(f, index_col=0) for f in files]
    # Prefix columns to avoid collision
    for i, df in enumerate(dfs):
        df.columns = [f"O{i+1}_{c}" for c in df.columns]
    if method == "intersect":
        common = dfs[0].index
        for df in dfs[1:]: common = common.intersection(df.index)
        result = pd.concat([df.loc[common] for df in dfs], axis=1)
    else:
        result = pd.concat(dfs, axis=1)
    result.to_csv(output_file)
    print(f"多组学整合: {result.shape[0]} 样本, {result.shape[1]} features -> {output_file}")


if __name__ == "__main__":
    main()
