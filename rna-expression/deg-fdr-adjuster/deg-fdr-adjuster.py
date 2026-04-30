#!/usr/bin/env python3
"""DEG多重检验校正对比(BH/BY/Q值)"""

# DEG多重检验校正对比
import pandas as pd
import numpy as np
from statsmodels.stats.multitest import multipletests

print("=" * 60)
print("  📊 DEG多重检验校正对比器")
print("=" * 60)

input_file = get_input("DEG结果文件路径", "deg_results.csv")
pval_col = get_input("原始p值列名", "pvalue")
methods_str = get_input("校正方法(BH,BY,bonferroni)", "BH,BY,bonferroni")
alpha = float(get_input("显著性阈值", "0.05"))
output_file = get_input("校正结果输出路径", "fdr_adjusted_results.tsv")

methods = [m.strip() for m in methods_str.split(',')]

sep = '\t' if input_file.endswith('.tsv') else ','
df = pd.read_csv(input_file, sep=sep)
pvals = df[pval_col].values
pvals = np.clip(pvals, 1e-300, 1.0)

print(f"✅ 加载 {len(df)} 条记录, {len(methods)} 种校正方法")

method_map = {'BH': 'fdr_bh', 'BY': 'fdr_by', 'bonferroni': 'bonferroni'}

results = {}
for method in methods:
    sm_method = method_map.get(method, method)
    try:
        reject, pval_corr, _, _ = multipletests(pvals, alpha=alpha, method=sm_method)
        df[f'pval_{method}'] = pval_corr
        df[f'significant_{method}'] = reject
        sig_count = sum(reject)
        results[method] = sig_count
        print(f"  {method}: {sig_count} 显著 (阈值{alpha})")
    except Exception as e:
        print(f"  ⚠️ {method} 失败: {e}")

df.to_csv(output_file, sep='\t', index=False)
print(f"\n✅ 校正完成, 结果保存到: {output_file}")

print("\n📊 各方法对比:")
for m, c in sorted(results.items(), key=lambda x: -x[1]):
    print(f"  {m}: {c} 显著DEG")
