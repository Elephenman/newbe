#!/usr/bin/env python3
"""DEG方向一致性箭头图"""

# DEG方向一致性箭头图
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("  📊 DEG方向一致性箭头图")
print("=" * 60)

files_str = get_input("DEG结果文件(逗号分隔多个)", "deg1.csv,deg2.csv")
fc_col = get_input("log2FC列名", "log2FoldChange")
gene_col = get_input("基因名列名", "gene")
plot_out = get_input("箭头图输出路径", "deg_direction.png")

files = [f.strip() for f in files_str.split(',')]

dfs = []
for f in files:
    sep = '\t' if f.endswith('.tsv') else ','
    df = pd.read_csv(f, sep=sep)
    dfs.append(df)
    print(f"  加载 {f}: {len(df)} 基因")

common_genes = set(dfs[0][gene_col])
for df in dfs[1:]:
    common_genes &= set(df[gene_col])
common_genes = list(common_genes)
print(f"  共有基因: {len(common_genes)}")

directions = {}
for i, df in enumerate(dfs):
    sub = df[df[gene_col].isin(common_genes)]
    directions[i] = dict(zip(sub[gene_col], sub[fc_col]))

n_files = len(files)
sample_genes = common_genes[:50] if len(common_genes) > 50 else common_genes

fig, ax = plt.subplots(figsize=(12, 10))
for j, gene in enumerate(sample_genes):
    for i in range(n_files - 1):
        fc_start = directions[i].get(gene, 0)
        fc_end = directions[i+1].get(gene, 0)
        color = '#C44E52' if fc_end > fc_start else '#4C72B0' if fc_end < fc_start else '#888888'
        ax.annotate("", xy=(i+1, fc_end), xytext=(i, fc_start),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5))
    ax.plot(range(n_files), [directions[i].get(gene, 0) for i in range(n_files)],
            'o-', color='gray', alpha=0.3, markersize=3)

ax.set_xticks(range(n_files))
ax.set_xticklabels([f.split('/')[-1].split('.')[0] for f in files])
ax.set_ylabel("log2FC")
ax.set_title("DEG Direction Consistency Across Comparisons")
plt.tight_layout()
plt.savefig(plot_out, dpi=150)
print(f"\n📊 箭头图: {plot_out}")
