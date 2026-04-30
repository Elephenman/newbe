#!/usr/bin/env python3
"""基因表达百分位排名+分箱"""

# 基因表达百分位排名
import pandas as pd
import numpy as np

print("=" * 60)
print("  📊 基因表达百分位排名器")
print("=" * 60)

input_file = get_input("表达矩阵文件路径", "expression_matrix.csv")
gene_list_file = get_input("目标基因列表(NA=全部)", "NA")
percentiles_str = get_input("百分位阈值(逗号分隔)", "25,50,75,90")
output_file = get_input("排名结果路径", "percentile_rank.tsv")

percentiles = [float(p.strip()) for p in percentiles_str.split(',')]

sep = '\t' if input_file.endswith('.tsv') else ','
df = pd.read_csv(input_file, sep=sep, index_col=0)
print(f"✅ 加载矩阵: {df.shape[0]} genes x {df.shape[1]} samples")

if gene_list_file != 'NA':
    genes = [line.strip() for line in open(gene_list_file)]
    df = df.loc[df.index.intersection(genes)]

rank_df = df.rank(pct=True) * 100

for p in percentiles:
    rank_df[f'above_{int(p)}th_pct'] = (rank_df.mean(axis=1) >= p)

summary = pd.DataFrame({
    'gene': df.index,
    'mean_expression': df.mean(axis=1),
    'mean_percentile': rank_df.mean(axis=1)
})

for p in percentiles:
    col_name = f'above_{int(p)}th_pct'
    counts = rank_df[col_name].sum()
    summary[col_name] = rank_df[col_name]
    print(f"  >={p}th百分位基因数: {counts}")

summary.to_csv(output_file, sep='\t')
print(f"\n📄 结果: {output_file}")
