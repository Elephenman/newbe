#!/usr/bin/env python3
"""箱线图异常值检测与报告"""

def main():
    input_file = input("数据文件CSV路径 [data.csv]: ") or "data.csv"
    output_file = input("异常值报告路径 [outliers.txt]: ") or "outliers.txt"
    column = input("检测列名(留空=所有数值列) []: ") or ""
    method = input("检测方法(iqr/zscore) [iqr]: ") or "iqr"
    import pandas as pd, numpy as np
    df = pd.read_csv(input_file)
    cols = [column] if column and column in df.columns else df.select_dtypes(include=[np.number]).columns.tolist()
    all_outliers = {}
    for col in cols:
        s = df[col].dropna()
        if method == "iqr":
            q1, q3 = s.quantile(0.25), s.quantile(0.75)
            iqr = q3 - q1
            lo, hi = q1 - 1.5*iqr, q3 + 1.5*iqr
            outliers = s[(s < lo) | (s > hi)]
        else:
            z = np.abs((s - s.mean()) / s.std())
            outliers = s[z > 3]
        all_outliers[col] = outliers
    with open(output_file, "w") as out:
        out.write("=== 异常值检测报告 ===\n")
        for col, outliers in all_outliers.items():
            out.write(f"\n{col}: {len(outliers)} 个异常值\n")
            if len(outliers) > 0:
                for idx, val in outliers.items():
                    out.write(f"  行{idx}: {val:.4f}\n")
    total = sum(len(v) for v in all_outliers.values())
    print(f"异常值检测: {len(cols)} 列, 共 {total} 个异常值")


if __name__ == "__main__":
    main()
