#!/usr/bin/env python3
"""复制时序(Repli-seq)数据可视化"""

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
    print("  复制时序(Repli-seq)数据可视化")
    print("=" * 60)
    print()

    input_file = get_input("Repli-seq信号文件(CSV: chr,start,end,early,late)", "repliseq.csv")
    output_plot = get_input("输出图片路径", "replication_timing.png")
    chrom = get_input("指定染色体(留空=全部)", "chr1")

    print()
    print(f"输入:    {input_file}")
    print(f"输出:    {output_plot}")
    print(f"染色体:  {chrom}")
    print()

    if not os.path.exists(input_file):
        print(f"[ERROR] 文件不存在: {input_file}")
        sys.exit(1)

    import pandas as pd
    import numpy as np

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("[ERROR] 需要matplotlib")
        sys.exit(1)

    df = pd.read_csv(input_file)

    # Validate required columns
    required = ['chr', 'start', 'early', 'late']
    for col in required:
        if col not in df.columns:
            print(f"[ERROR] 缺少必需列: {col}")
            print(f"  可用列: {', '.join(df.columns)}")
            sys.exit(1)

    # Calculate early/late ratio
    # Add pseudocount to avoid division by zero
    df["ratio"] = (df["early"] + 1) / (df["late"] + 1)

    # Filter by chromosome
    if chrom and chrom in df["chr"].values:
        sub = df[df["chr"] == chrom].copy()
    elif chrom and chrom not in df["chr"].values:
        print(f"[WARN] 染色体 {chrom} 不在数据中，使用全部数据")
        sub = df.copy()
    else:
        sub = df.copy()

    # Sort by position
    sub = sub.sort_values("start")

    # Plot
    fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # Top: Early/Late ratio
    axes[0].plot(sub["start"], sub["ratio"], alpha=0.7, linewidth=0.5, color="#3C5488")
    axes[0].axhline(y=1, color="red", linestyle="--", alpha=0.5, label="Ratio=1 (Early=Late)")
    axes[0].set_ylabel("Early/Late Ratio")
    axes[0].set_title(f"Replication Timing - {chrom if chrom else 'All'}")
    axes[0].legend()

    # Bottom: Early and Late signals
    axes[1].plot(sub["start"], sub["early"], alpha=0.7, linewidth=0.5, color="#E64B35", label="Early")
    axes[1].plot(sub["start"], sub["late"], alpha=0.7, linewidth=0.5, color="#4DBBD5", label="Late")
    axes[1].set_xlabel("Position")
    axes[1].set_ylabel("Signal")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(output_plot, dpi=150)
    plt.close()

    # Summary
    n_chroms = df["chr"].nunique()
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  染色体数:        {n_chroms}")
    print(f"  总区间数:        {len(df)}")
    print(f"  当前区间数:      {len(sub)}")
    print(f"  Ratio均值:       {sub['ratio'].mean():.4f}")
    print(f"  输出图片:        {output_plot}")
    print("=" * 60)
    print()
    print(f"[Done] 复制时序图: {output_plot}")


if __name__ == "__main__":
    main()
