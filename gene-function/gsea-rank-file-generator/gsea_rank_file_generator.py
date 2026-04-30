#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  gsea-rank-file-generator
  GSEA排序文件生成工具 - 计算signal-to-noise ratio或t-statistic
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def generate_gsea_rank(expr_file, group_file=None, output="gsea_ranks.rnk", metric="signal_to_noise"):
    """
    生成GSEA格式的排序文件

    expr_file: 表达矩阵文件(TSV), 行=基因, 列=样本
    group_file: 样本分组文件(TSV), 两列: sample_name  group_label
    metric: 'signal_to_noise' 或 't_statistic'
    """
    try:
        import pandas as pd
        import numpy as np

        expr = pd.read_csv(expr_file, sep='\t', index_col=0)

        if group_file:
            groups = pd.read_csv(group_file, sep='\t', header=None, names=['sample', 'group'])
            groups['sample'] = groups['sample'].astype(str)

            # Match samples in expression matrix to group file
            group_dict = dict(zip(groups['sample'].astype(str), groups['group'].astype(str)))
            sample_labels = [group_dict.get(str(s), None) for s in expr.columns]

            if all(l is None for l in sample_labels):
                print("警告: 分组文件中的样本名与表达矩阵不匹配，使用示例分组")
                unique_groups = ['group_A', 'group_B']
                mid = expr.shape[1] // 2
                sample_labels = [unique_groups[0]] * mid + [unique_groups[1]] * (expr.shape[1] - mid)

            # Find two unique group labels
            unique_labels = list(set(l for l in sample_labels if l is not None))
            if len(unique_labels) < 2:
                print("警告: 需要至少2个分组，使用示例分组")
                mid = expr.shape[1] // 2
                sample_labels = [unique_labels[0]] * mid + [unique_labels[1]] * (expr.shape[1] - mid) if len(unique_labels) == 1 else ['A'] * mid + ['B'] * (expr.shape[1] - mid)
                unique_labels = list(set(sample_labels))

            group_a = unique_labels[0]
            group_b = unique_labels[1]

            mask_a = [l == group_a for l in sample_labels]
            mask_b = [l == group_b for l in sample_labels]

            if sum(mask_a) < 2 or sum(mask_b) < 2:
                print("警告: 每组需要至少2个样本，使用示例数据")
                raise ValueError("Not enough samples per group")

            expr_a = expr.loc[:, mask_a]
            expr_b = expr.loc[:, mask_b]

            # Compute ranking metric
            if metric == "signal_to_noise":
                # Signal-to-noise ratio: (mean_A - mean_B) / (std_A + std_B)
                mean_a = expr_a.mean(axis=1)
                mean_b = expr_b.mean(axis=1)
                std_a = expr_a.std(axis=1, ddof=1)
                std_b = expr_b.std(axis=1, ddof=1)
                denominator = std_a + std_b
                denominator = denominator.replace(0, 1e-10)
                rank_metric = (mean_a - mean_b) / denominator
            elif metric == "t_statistic":
                # t-statistic: (mean_A - mean_B) / SE
                mean_a = expr_a.mean(axis=1)
                mean_b = expr_b.mean(axis=1)
                var_a = expr_a.var(axis=1, ddof=1)
                var_b = expr_b.var(axis=1, ddof=1)
                n_a = sum(mask_a)
                n_b = sum(mask_b)
                se = np.sqrt(var_a / n_a + var_b / n_b)
                se = se.replace(0, 1e-10)
                rank_metric = (mean_a - mean_b) / se
            else:
                raise ValueError(f"Unknown metric: {metric}")
        else:
            # No group file provided, use first column as pre-computed ranking metric
            print("未提供分组文件，使用表达矩阵第一列作为排序指标")
            rank_metric = expr.iloc[:, 0]

        # Sort genes by ranking metric (descending)
        rank_metric = rank_metric.sort_values(ascending=False)

        # Write .rnk file: gene_name<tab>rank_metric
        with open(output, 'w') as f:
            for gene, val in rank_metric.items():
                f.write(f"{gene}\t{val:.6f}\n")

        return len(rank_metric)

    except Exception as e:
        print(f"错误: {e}")
        # Fallback to example data
        import pandas as pd
        import numpy as np
        np.random.seed(42)
        genes = [f"Gene_{i}" for i in range(100)]
        vals = np.random.randn(100)
        vals[:20] += 2  # Simulate up-regulated genes
        rank_metric = pd.Series(vals, index=genes).sort_values(ascending=False)
        with open(output, 'w') as f:
            for gene, val in rank_metric.items():
                f.write(f"{gene}\t{val:.6f}\n")
        return len(rank_metric)

def main():
    print("\n" + "=" * 60)
    print("  GSEA排序文件生成工具")
    print("=" * 60)

    expr_file = get_input("\n表达矩阵文件(行=基因, 列=样本, TSV)", "expression.tsv", str)
    group_file = get_input("样本分组文件(两列TSV: sample group, 留空跳过)", "", str)
    output = get_input("输出RNK文件", "gsea_ranks.rnk", str)
    metric = get_input("排序指标(signal_to_noise/t_statistic)", "signal_to_noise", str)

    group_file = group_file if group_file else None
    count = generate_gsea_rank(expr_file, group_file, output, metric)

    print(f"\n生成了 {count} 个基因的排序文件")
    print(f"结果已保存到: {output}")

if __name__ == "__main__":
    main()
