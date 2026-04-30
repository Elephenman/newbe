#!/usr/bin/env python3
"""Gene expression correlation matrix + heatmap"""

import os
import sys


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def create_correlation_matrix(input_file, output_file, method="pearson", top_n=50):
    """Create gene expression correlation matrix and heatmap."""
    try:
        import pandas as pd
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("[ERROR] pandas, numpy, matplotlib required: pip install pandas numpy matplotlib")
        sys.exit(1)

    # Read expression matrix (rows=genes, columns=samples)
    df = pd.read_csv(input_file, index_col=0)

    # Take top N most variable genes
    gene_vars = df.var(axis=1)
    top_genes = gene_vars.nlargest(min(top_n, len(df))).index
    df_sub = df.loc[top_genes]

    # Compute gene-gene correlation matrix
    corr_matrix = df_sub.T.corr(method=method)

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(12, 10))
    cax = ax.imshow(corr_matrix.values, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')

    # Add colorbar
    plt.colorbar(cax, label=f'{method.capitalize()} correlation')

    # Labels
    tick_labels = [g[:15] for g in corr_matrix.columns]
    ax.set_xticks(range(len(tick_labels)))
    ax.set_yticks(range(len(tick_labels)))
    if len(tick_labels) <= 30:
        ax.set_xticklabels(tick_labels, rotation=90, fontsize=6)
        ax.set_yticklabels(tick_labels, fontsize=6)

    ax.set_title(f'Gene Expression Correlation Matrix ({method}, top {len(top_genes)} variable genes)')
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()

    # Save correlation matrix
    corr_file = output_file.rsplit('.', 1)[0] + '_matrix.csv'
    corr_matrix.to_csv(corr_file)

    # Compute stats
    upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    high_corr = (upper_tri.abs() > 0.8).sum().sum()
    total_pairs = upper_tri.count().sum()

    return {
        "n_genes": len(top_genes),
        "n_samples": df.shape[1],
        "method": method,
        "high_corr_pairs": high_corr,
        "total_pairs": total_pairs,
        "corr_file": corr_file,
    }


def main():
    print("=" * 60)
    print("  Gene Expression Correlation Matrix + Heatmap")
    print("=" * 60)
    print()

    input_file = get_input("Expression matrix CSV (rows=genes, cols=samples)", "expression.csv")
    output_file = get_input("Output heatmap path", "correlation_heatmap.png")
    method = get_input("Correlation method (pearson/spearman)", "pearson")
    top_n = get_input("Top N variable genes", "50", int)

    if not os.path.exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)

    stats = create_correlation_matrix(input_file, output_file, method, top_n)

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  Genes analyzed:   {stats['n_genes']}")
    print(f"  Samples:          {stats['n_samples']}")
    print(f"  Method:           {stats['method']}")
    print(f"  High corr pairs:  {stats['high_corr_pairs']} (|r|>0.8)")
    print(f"  Total pairs:      {stats['total_pairs']}")
    print(f"  Output saved to:  {output_file}")
    print(f"  Matrix CSV:       {stats['corr_file']}")
    print("=" * 60)
    print()
    print("[Done] Correlation matrix completed successfully!")


if __name__ == "__main__":
    main()
