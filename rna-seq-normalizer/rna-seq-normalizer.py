#!/usr/bin/env python3
"""对RNA-seq计数矩阵进行TPM/FPKM/RPKM/CPM标准化"""

def main():
    input_file = input("计数矩阵CSV(行=基因,列=样本) [counts.csv]: ") or "counts.csv"
    output_file = input("标准化输出路径 [normalized.csv]: ") or "normalized.csv"
    method = input("方法(tpm/fpkm/rpkm/cpm) [tpm]: ") or "tpm"
    gene_length_file = input("基因长度CSV(基因,长度) [gene_lengths.csv]: ") or "gene_lengths.csv"
    import pandas as pd, numpy as np
    df = pd.read_csv(input_file, index_col=0).apply(pd.to_numeric, errors="coerce").fillna(0)
    if method == "cpm":
        result = df.div(df.sum(axis=0), axis=1) * 1e6
    else:
        gl = pd.read_csv(gene_length_file, index_col=0)
        lengths = gl.reindex(df.index).iloc[:, 0].fillna(1000)
        rpk = df.div(lengths.values, axis=0)
        if method == "tpm":
            result = rpk.div(rpk.sum(axis=0) / 1e6, axis=1)
        else:
            rpm = df.div(df.sum(axis=0), axis=1) * 1e6
            result = rpm.div(lengths.values, axis=0) * 1e3
    result.to_csv(output_file)
    print(f"{method.upper()}标准化完成: {output_file}")


if __name__ == "__main__":
    main()
