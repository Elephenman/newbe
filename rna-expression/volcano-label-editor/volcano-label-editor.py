#!/usr/bin/env python3
"""火山图标签编辑器(添加/修改/删除基因标签)
读取现有DEG结果和标签配置，生成交互式或静态火山图
"""

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
    print("  火山图标签编辑器")
    print("=" * 60)
    print()

    input_file = get_input("DEG结果CSV(基因,log2FC,padj)", "deg_results.csv")
    output_plot = get_input("输出火山图路径", "volcano_labeled.png")
    label_genes = get_input("标注基因(逗号分隔)", "TP53,BRCA1,MYC")
    log2fc_threshold = get_input("log2FC阈值", "1", float)
    padj_threshold = get_input("padj阈值", "0.05", float)

    print()
    print(f"输入:      {input_file}")
    print(f"输出:      {output_plot}")
    print(f"标注基因:  {label_genes}")
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

    # Auto-detect columns
    gene_col = df.columns[0]
    log2fc_col = None
    padj_col = None

    for col in df.columns:
        col_lower = col.lower()
        if 'log2fc' in col_lower or 'log2_fc' in col_lower or 'logfc' in col_lower:
            log2fc_col = col
        elif 'padj' in col_lower or 'p_adj' in col_lower or 'fdr' in col_lower or 'q_value' in col_lower:
            padj_col = col
        elif ('pvalue' in col_lower or 'p_value' in col_lower) and padj_col is None:
            padj_col = col

    if log2fc_col is None:
        log2fc_col = df.columns[1]
    if padj_col is None:
        padj_col = df.columns[2]

    l2fc = log2fc_threshold
    pt = padj_threshold

    df["neg_log10p"] = -np.log10(df[padj_col].clip(lower=1e-300))
    df["sig"] = "NS"
    df.loc[(df[log2fc_col] > l2fc) & (df[padj_col] < pt), "sig"] = "Up"
    df.loc[(df[log2fc_col] < -l2fc) & (df[padj_col] < pt), "sig"] = "Down"

    fig, ax = plt.subplots(figsize=(10, 8))
    colors = {"Up": "#E64B35", "Down": "#3C5488", "NS": "#8491B4"}

    for s, sub in df.groupby("sig"):
        ax.scatter(sub[log2fc_col], sub["neg_log10p"], c=colors[s],
                  s=5 if s == "NS" else 15,
                  alpha=0.3 if s == "NS" else 0.7, label=s)

    # Label genes
    lg = [g.strip() for g in label_genes.split(",") if g.strip()]
    labeled_count = 0
    for gene in lg:
        row = df[df[gene_col] == gene]
        if not row.empty:
            r = row.iloc[0]
            ax.annotate(str(gene), (r[log2fc_col], r["neg_log10p"]),
                       xytext=(5, 5), textcoords="offset points",
                       fontsize=8, fontweight="bold",
                       arrowprops=dict(arrowstyle="-", color="gray", lw=0.5))
            labeled_count += 1
        else:
            print(f"  [WARN] 基因未找到: {gene}")

    # Threshold lines
    ax.axhline(-np.log10(pt), linestyle="--", color="black", alpha=0.3)
    ax.axvline(l2fc, linestyle="--", color="black", alpha=0.3)
    ax.axvline(-l2fc, linestyle="--", color="black", alpha=0.3)
    ax.set_xlabel(log2fc_col)
    ax.set_ylabel(f"-log10({padj_col})")
    ax.set_title("Volcano Plot (Labeled)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_plot, dpi=150, bbox_inches='tight')
    plt.close()

    # Save label configuration
    label_config = output_plot.rsplit('.', 1)[0] + '_labels.txt'
    with open(label_config, 'w') as f:
        for g in lg:
            f.write(g + '\n')

    # Summary
    n_up = (df["sig"] == "Up").sum()
    n_down = (df["sig"] == "Down").sum()

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  总基因:      {len(df)}")
    print(f"  Up:          {n_up}")
    print(f"  Down:        {n_down}")
    print(f"  标注基因:    {labeled_count}/{len(lg)}")
    print(f"  输出:        {output_plot}")
    print(f"  标签配置:    {label_config}")
    print("=" * 60)
    print()
    print(f"[Done] 火山图: {output_plot}")


if __name__ == "__main__":
    main()
