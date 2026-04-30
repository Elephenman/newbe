#!/usr/bin/env python3
"""DEG效应量计算(log2FC置信区间+效应量)"""

# DEG效应量计算
import pandas as pd
import numpy as np

print("=" * 60)
print("  📊 DEG效应量计算器")
print("=" * 60)

input_file = get_input("DEG结果文件路径(CSV/TSV)", "deg_results.csv")
fc_col = get_input("log2FC列名", "log2FoldChange")
pval_col = get_input("p值列名", "pvalue")
se_col = get_input("标准误列名(可选，NA表示无)", "lfcSE")
output_file = get_input("输出路径", "effect_size_results.tsv")

sep = '\t' if input_file.endswith('.tsv') else ','
df = pd.read_csv(input_file, sep=sep)
print(f"✅ 加载 {len(df)} 条记录")

df['effect_size'] = df[fc_col].abs()
df['direction'] = df[fc_col].apply(lambda x: 'up' if x > 0 else 'down' if x < 0 else 'neutral')

if se_col != 'NA' and se_col in df.columns:
    ci_95_low = df[fc_col] - 1.96 * df[se_col]
    ci_95_high = df[fc_col] + 1.96 * df[se_col]
    df['CI_95_low'] = ci_95_low
    df['CI_95_high'] = ci_95_high
    df['CI_width'] = ci_95_high - ci_95_low
    print("  ✅ 置信区间已计算")

df['abs_log2FC'] = df[fc_col].abs()
sig = df[(df[pval_col] < 0.05) & (df['abs_log2FC'] > 1)]
print(f"  显著DEG(|FC|>1, p<0.05): {len(sig)}")
print(f"  上调: {len(sig[sig['direction']=='up'])}")
print(f"  下调: {len(sig[sig['direction']=='down'])}")

df.to_csv(output_file, sep='\t', index=False)
print(f"\n📄 结果已保存到: {output_file}")
