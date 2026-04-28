#!/usr/bin/env python3
"""表达矩阵Z-score标准化+热图"""

# 表达矩阵Z-score标准化
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 60)
print("  📊 表达矩阵Z-score标准化")
print("=" * 60)

input_file = get_input("表达矩阵文件路径", "expression_matrix.csv")
gene_list_file = get_input("目标基因列表文件(NA表示全部)", "NA")
center = get_input("中心化方法(mean/median)", "mean")
output_matrix = get_input("输出矩阵路径", "zscore_matrix.tsv")
heatmap_out = get_input("热图路径", "zscore_heatmap.png")

sep = '\t' if input_file.endswith('.tsv') else ','
df = pd.read_csv(input_file, sep=sep, index_col=0)
print(f"✅ 加载矩阵: {df.shape[0]} genes x {df.shape[1]} samples")

if gene_list_file != 'NA':
    genes = [line.strip() for line in open(gene_list_file)]
    df = df.loc[df.index.intersection(genes)]
    print(f"  过滤到 {len(df)} 目标基因")

if center == "median":
    zscore = (df - df.median(axis=1).values.reshape(-1,1)) / df.std(axis=1).values.reshape(-1,1)
else:
    zscore = df.sub(df.mean(axis=1), axis=0).div(df.std(axis=1), axis=0)

zscore = zscore.fillna(0)
zscore.to_csv(output_matrix, sep='\t')

top_var = zscore.var(axis=1).nlargest(50).index
plot_df = zscore.loc[top_var]

plt.figure(figsize=(12, max(6, len(plot_df)*0.15)))
sns.heatmap(plot_df, cmap='RdBu_r', center=0, linewidths=0.5)
plt.title("Z-score Expression Heatmap (Top 50 variable genes)")
plt.tight_layout()
plt.savefig(heatmap_out, dpi=150)

print(f"\n✅ Z-score标准化完成")
print(f"  输出矩阵: {output_matrix}")
print(f"  热图: {heatmap_out}")
