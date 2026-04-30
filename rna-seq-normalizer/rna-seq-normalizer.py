#!/usr/bin/env python3
"""对RNA-seq计数矩阵进行TPM/FPKM/RPKM/CPM标准化"""

import os
import sys


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    try:
        return dtype(val)
    except (ValueError, TypeError):
        return default


def main():
    print("=" * 60)
    print("  RNA-seq计数矩阵标准化")
    print("=" * 60)
    print()

    input_file = get_input("计数矩阵CSV(行=基因,列=样本)", "counts.csv")
    output_file = get_input("标准化输出路径", "normalized.csv")
    method = get_input("方法(tpm/fpkm/rpkm/cpm)", "tpm")
    gene_length_file = get_input("基因长度CSV(基因,长度) [gene_lengths.csv]", "gene_lengths.csv")

    print()
    print(f"输入:    {input_file}")
    print(f"输出:    {output_file}")
    print(f"方法:    {method}")
    print()

    if not os.path.exists(input_file):
        print(f"[ERROR] 计数矩阵不存在: {input_file}")
        sys.exit(1)

    import pandas as pd
    import numpy as np

    df = pd.read_csv(input_file, index_col=0).apply(pd.to_numeric, errors="coerce").fillna(0)

    if method == "cpm":
        # CPM: counts per million
        total_counts = df.sum(axis=0)
        total_counts[total_counts == 0] = 1  # avoid division by zero
        result = df.div(total_counts, axis=1) * 1e6
    else:
        # Methods requiring gene lengths
        if not os.path.exists(gene_length_file):
            print(f"[ERROR] 基因长度文件不存在: {gene_length_file}")
            print("  TPM/FPKM/RPKM需要基因长度信息")
            sys.exit(1)

        gl = pd.read_csv(gene_length_file, index_col=0)
        lengths = gl.reindex(df.index).iloc[:, 0]

        # Check for missing lengths
        missing = lengths.isna().sum()
        if missing > 0:
            print(f"[WARN] {missing} 个基因缺少长度信息，使用默认值1000bp")
            lengths = lengths.fillna(1000)

        lengths = lengths.astype(float)

        if method == "tpm":
            # TPM: RPK normalization then scale to million
            # Step 1: RPK = counts / (length / 1000)
            rpk = df.div(lengths.values / 1000, axis=0)
            # Step 2: Scale to per million
            scaling = rpk.sum(axis=0) / 1e6
            scaling[scaling == 0] = 1
            result = rpk.div(scaling, axis=1)
        elif method == "rpkm":
            # RPKM = (counts / (length/1000)) / (total_counts / 1e6)
            total_counts = df.sum(axis=0)
            total_counts[total_counts == 0] = 1
            rpm = df.div(total_counts / 1e6, axis=1)
            result = rpm.div(lengths.values / 1000, axis=0)
        elif method == "fpkm":
            # FPKM = (counts / (length/1000)) / (total_counts / 1e6)
            # Same formula as RPKM for single-end data
            total_counts = df.sum(axis=0)
            total_counts[total_counts == 0] = 1
            rpm = df.div(total_counts / 1e6, axis=1)
            result = rpm.div(lengths.values / 1000, axis=0)

    result.to_csv(output_file)

    # Summary
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  方法:        {method.upper()}")
    print(f"  基因数:      {len(result)}")
    print(f"  样本数:      {len(result.columns)}")
    print(f"  输出文件:    {output_file}")
    print("=" * 60)
    print()
    print(f"[Done] {method.upper()}标准化完成: {output_file}")


if __name__ == "__main__":
    main()
