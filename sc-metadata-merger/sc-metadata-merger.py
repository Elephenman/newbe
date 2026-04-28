#!/usr/bin/env python3
"""单细胞metadata与表达矩阵合并"""

# 单细胞metadata与表达矩阵合并
import pandas as pd

print("=" * 60)
print("  🔬 单细胞Metadata合并器")
print("=" * 60)

matrix_file = get_input("表达矩阵路径", "matrix.csv")
metadata_file = get_input("metadata文件路径", "metadata.csv")
merge_key = get_input("合并键列名", "cell_id")
output_file = get_input("合并结果路径", "merged_data.tsv")

sep_m = '\t' if matrix_file.endswith('.tsv') else ','
sep_meta = '\t' if metadata_file.endswith('.tsv') else ','

matrix = pd.read_csv(matrix_file, sep=sep_m, index_col=0)
metadata = pd.read_csv(metadata_file, sep=sep_meta)

print(f"✅ 表达矩阵: {matrix.shape[0]} cells x {matrix.shape[1]} genes")
print(f"✅ Metadata: {len(metadata)} 条记录, {len(metadata.columns)} 列")

merged = matrix.merge(metadata, left_index=True, right_on=merge_key, how='inner')
print(f"  合并后: {merged.shape[0]} cells")

merged.to_csv(output_file, sep='\t', index=False)
print(f"\n📄 合并结果: {output_file}")
