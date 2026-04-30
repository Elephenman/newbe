#!/usr/bin/env python3
"""火山图增强版（标注+配色+阈值线）
读取DEG结果，生成增强版火山图，支持多阈值线、分类标注、自定义配色
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
    print("  火山图增强版（标注+配色+阈值线）")
    print("=" * 60)
    print()

    input_file = get_input("DEG结果CSV路径(基因,log2FC,padj)", "deg_results.csv")
    output_plot = get_input("输出火山图路径", "volcano_enhanced.png")
    label_genes = get_input("标注基因(逗号分隔,留空=自动标注top基因)", "")
    log2fc_thr = get_input("log2FC阈值", "1", float)
    padj_thr = get_input("padj阈值", "0.05", float)
    color_scheme = get_input("配色方案(Nature/Science/Custom)", "Nature")
    show_threshold_lines = get_input("显示阈值线(yes/no)", "yes")

    print()
    print(f"输入:      {input_file}")
    print(f"输出:      {output_plot}")
    print(f"log2FC:     {log2fc_thr}")
    print(f"padj:       {padj_thr}")
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

    # Read data
    df = pd.read_csv(input_file)
    # Auto-detect columns
    gene_col = df.columns[0]
    log2fc_col = None
    padj_col = None

    for col in df.columns:
        if 'log2fc' in col.lower() or 'log2_fc' in col.lower() or 'logfc' in col.lower():
            log2fc_col = col
        elif 'padj' in col.lower() or 'p_adj' in col.lower() or 'fdr' in col.lower() or 'q_value' in col.lower():
            padj_col = col
        elif 'pvalue' in col.lower() or 'p_value' in col.lower() or 'pval' in col.lower():
            if padj_col is None:
                padj_col = col

    if log2fc_col is None:
        log2fc_col = df.columns[1]
    if padj_col is None:
        padj_col = df.columns[2]

    print(f"[Processing] 使用列: {gene_col}, {log2fc_col}, {padj_col}")

    # Calculate -log10(padj)
    df['neg_log10p'] = -np.log10(df[padj_col].clip(lower=1e-300))

    # Classify
    df['significance'] = 'NS'
    df.loc[(df[log2fc_col] > log2fc_thr) & (df[padj_col] < padj_thr), 'significance'] = 'Up'
    df.loc[(df[log2fc_col] < -log2fc_thr) & (df[padj_col] < padj_thr), 'significance'] = 'Down'

    n_up = (df['significance'] == 'Up').sum()
    n_down = (df['significance'] == 'Down').sum()
    n_ns = (df['significance'] == 'NS').sum()
    print(f"[Processing] Up: {n_up}, Down: {n_down}, NS: {n_ns}")

    # Color scheme
    if color_scheme == 'Nature':
        colors = {'Up': '#E64B35', 'Down': '#3C5488', 'NS': '#8491B4'}
    elif color_scheme == 'Science':
        colors = {'Up': '#E3120B', 'Down': '#0C5B3F', 'NS': '#A1C7ED'}
    else:
        colors = {'Up': 'red', 'Down': 'blue', 'NS': 'gray'}

    # Plot
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot NS first, then significant
    for sig in ['NS', 'Up', 'Down']:
        sub = df[df['significance'] == sig]
        ax.scatter(sub[log2fc_col], sub['neg_log10p'],
                  c=colors[sig], s=5 if sig == 'NS' else 15,
                  alpha=0.3 if sig == 'NS' else 0.7, label=f'{sig} ({(sig=="Up" and n_up) or (sig=="Down" and n_down) or n_ns})')

    # Threshold lines
    if show_threshold_lines.lower() in ('yes', 'y'):
        ax.axhline(-np.log10(padj_thr), linestyle='--', color='black', alpha=0.3, linewidth=0.8)
        ax.axvline(log2fc_thr, linestyle='--', color='black', alpha=0.3, linewidth=0.8)
        ax.axvline(-log2fc_thr, linestyle='--', color='black', alpha=0.3, linewidth=0.8)

    # Label genes
    if label_genes:
        genes_to_label = [g.strip() for g in label_genes.split(',') if g.strip()]
    else:
        # Auto-label: top 10 Up and top 10 Down
        top_up = df[df['significance'] == 'Up'].nlargest(10, log2fc_col)
        top_down = df[df['significance'] == 'Down'].nsmallest(10, log2fc_col)
        genes_to_label = list(top_up[gene_col]) + list(top_down[gene_col])

    for gene in genes_to_label:
        row = df[df[gene_col] == gene]
        if not row.empty:
            r = row.iloc[0]
            ax.annotate(str(gene), (r[log2fc_col], r['neg_log10p']),
                       xytext=(5, 5), textcoords='offset points', fontsize=7,
                       fontweight='bold', color='black',
                       arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))

    ax.set_xlabel(f'{log2fc_col}')
    ax.set_ylabel(f'-log10({padj_col})')
    ax.set_title('Volcano Plot (Enhanced)')
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(output_plot, dpi=300, bbox_inches='tight')
    plt.close()

    # Summary
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  总基因数:    {len(df)}")
    print(f"  Up:          {n_up}")
    print(f"  Down:        {n_down}")
    print(f"  标注基因:    {len(genes_to_label)}")
    print(f"  输出:        {output_plot}")
    print("=" * 60)
    print()
    print("[Done] volcano_plot_enhancer completed successfully!")


if __name__ == "__main__":
    main()
