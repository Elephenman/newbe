#!/usr/bin/env python3
"""单细胞新型基因发现(未注释表达特征)"""

# 单细胞新型基因发现
import pandas as pd
import numpy as np

print("=" * 60)
print("  🔬 单细胞新型基因发现器")
print("=" * 60)

input_file = get_input("表达矩阵路径", "matrix.csv")
ann_file = get_input("基因注释文件路径", "gene_annotations.tsv")
min_expr = float(get_input("最小表达阈值", "1"))
min_cells = int(get_input("最少表达细胞数", "10"))
output_file = get_input("新型基因列表路径", "novel_genes.tsv")

sep = '\t' if input_file.endswith('.tsv') else ','
df = pd.read_csv(input_file, sep=sep, index_col=0)
ann = pd.read_csv(ann_file, sep='\t')

matrix_genes = set(df.index)
annotated_genes = set(ann.iloc[:, 0]) if len(ann.columns) > 0 else set()

novel = matrix_genes - annotated_genes
print(f"  矩阵基因数: {len(matrix_genes)}")
print(f"  已注释基因数: {len(annotated_genes)}")
print(f"  未注释基因数: {len(novel)}")

expressed_novel = []
for gene in novel:
    expr_vals = df.loc[gene]
    high_cells = (expr_vals >= min_expr).sum()
    if high_cells >= min_cells:
        expressed_novel.append({
            'gene': gene,
            'expressed_cells': high_cells,
            'mean_expr': expr_vals.mean(),
            'max_expr': expr_vals.max(),
            'cell_pct': high_cells / len(expr_vals) * 100
        })

result = pd.DataFrame(expressed_novel)
if len(result) > 0:
    result = result.sort_values('expressed_cells', ascending=False)
    result.to_csv(output_file, sep='\t', index=False)
    print(f"\n✅ 发现 {len(result)} 个新型表达基因")
else:
    print("\n⚠️ 未发现新型表达基因")
    result.to_csv(output_file, sep='\t', index=False)
print(f"📄 结果: {output_file}")
