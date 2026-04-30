#!/usr/bin/env python3
"""Correlation scatter matrix + regression lines"""

import os
import sys


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def create_scatter_matrix(input_file, output_file, method="pearson", max_vars=10):
    """Create correlation scatter matrix from CSV data."""
    try:
        import pandas as pd
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("[ERROR] pandas, numpy, matplotlib required: pip install pandas numpy matplotlib")
        sys.exit(1)

    # Read data
    df = pd.read_csv(input_file)

    # Select numeric columns only
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_cols:
        print("[ERROR] No numeric columns found in input file")
        sys.exit(1)

    # Limit to max_vars
    if len(numeric_cols) > max_vars:
        print(f"[INFO] Limiting to top {max_vars} numeric columns (out of {len(numeric_cols)})")
        numeric_cols = numeric_cols[:max_vars]

    df_sub = df[numeric_cols].dropna()

    # Compute correlation matrix
    corr_matrix = df_sub.corr(method=method)

    # Create scatter matrix
    n = len(numeric_cols)
    fig, axes = plt.subplots(n, n, figsize=(3*n, 3*n))

    for i in range(n):
        for j in range(n):
            ax = axes[i][j] if n > 1 else axes
            if i == j:
                # Diagonal: histogram
                ax.hist(df_sub[numeric_cols[i]], bins=30, color='#4DBBD5', alpha=0.7)
                ax.set_ylabel('Count', fontsize=7)
            else:
                # Off-diagonal: scatter with regression line
                x = df_sub[numeric_cols[j]]
                y = df_sub[numeric_cols[i]]
                ax.scatter(x, y, alpha=0.3, s=5, color='#3C5488')
                # Regression line
                try:
                    z = np.polyfit(x, y, 1)
                    p = np.poly1d(z)
                    x_sorted = np.sort(x)
                    ax.plot(x_sorted, p(x_sorted), color='#E64B35', linewidth=1.5)
                except Exception:
                    pass
                # Correlation coefficient
                r = corr_matrix.iloc[i, j]
                ax.text(0.05, 0.95, f'r={r:.2f}', transform=ax.transAxes,
                       fontsize=7, verticalalignment='top',
                       color='#E64B35' if abs(r) > 0.5 else 'grey')

            if i == n - 1:
                ax.set_xlabel(numeric_cols[j], fontsize=7)
            else:
                ax.set_xticklabels([])
            if j == 0 and i != j:
                ax.set_ylabel(numeric_cols[i], fontsize=7)
            elif j != 0:
                ax.set_yticklabels([])
            ax.tick_params(labelsize=6)

    plt.suptitle(f'Correlation Scatter Matrix ({method})', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()

    # Save correlation matrix
    corr_file = output_file.rsplit('.', 1)[0] + '_correlation.csv'
    corr_matrix.to_csv(corr_file)

    return {
        "n_vars": len(numeric_cols),
        "n_rows": len(df_sub),
        "method": method,
        "corr_file": corr_file,
    }


def main():
    print("=" * 60)
    print("  Correlation Scatter Matrix + Regression Lines")
    print("=" * 60)
    print()

    input_file = get_input("Input CSV path", "data.csv")
    output_file = get_input("Output plot path", "scatter_matrix.png")
    method = get_input("Correlation method (pearson/spearman)", "pearson")
    max_vars = get_input("Max variables to plot", "10", int)

    if not os.path.exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)

    stats = create_scatter_matrix(input_file, output_file, method, max_vars)

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  Variables:        {stats['n_vars']}")
    print(f"  Data rows:        {stats['n_rows']}")
    print(f"  Method:           {stats['method']}")
    print(f"  Output saved to:  {output_file}")
    print(f"  Correlation CSV:  {stats['corr_file']}")
    print("=" * 60)
    print()
    print("[Done] Correlation scatter matrix completed successfully!")


if __name__ == "__main__":
    main()
