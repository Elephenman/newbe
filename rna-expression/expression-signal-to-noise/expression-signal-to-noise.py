#!/usr/bin/env python3
"""表达信噪比计算+低质量基因过滤"""

# 表达信噪比计算
import pandas as pd
import numpy as np

print("=" * 60)
print("  📊 表达信噪比计算器")
print("=" * 60)

input_file = get_input("表达矩阵文件路径", "expression_matrix.csv")
snr_threshold = float(get_input("信噪比阈值", "2"))
output_file = get_input("过滤后矩阵路径", "snr_filtered_matrix.tsv")
report_file = get_input("统计报告路径", "snr_report.txt")

sep = '\t' if input_file.endswith('.tsv') else ','
df = pd.read_csv(input_file, sep=sep, index_col=0)
print(f"✅ 加载矩阵: {df.shape[0]} genes x {df.shape[1]} samples")

gene_means = df.mean(axis=1)
gene_stds = df.std(axis=1)
snr = gene_means / gene_stds.replace(0, np.nan)
snr = snr.fillna(0)

high_snr = snr[snr >= snr_threshold]
low_snr = snr[snr < snr_threshold]

print(f"  高SNR基因(>={snr_threshold}): {len(high_snr)}")
print(f"  低SNR基因(<{snr_threshold}): {len(low_snr)}")

filtered_df = df.loc[high_snr.index]
filtered_df.to_csv(output_file, sep='\t')

with open(report_file, 'w') as f:
    f.write(f"Signal-to-Noise Ratio Report\n")
    f.write(f"Input genes: {df.shape[0]}\n")
    f.write(f"SNR threshold: {snr_threshold}\n")
    f.write(f"High SNR genes: {len(high_snr)}\n")
    f.write(f"Low SNR genes (filtered): {len(low_snr)}\n")
    f.write(f"Mean SNR: {snr.mean():.2f}\n")

print(f"\n✅ 过滤完成")
print(f"  输出矩阵: {output_file}")
print(f"  报告: {report_file}")
