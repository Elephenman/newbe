#!/usr/bin/env python3
"""统计摘要表一键生成（均值/SD/检验）
读取数值数据，分组计算统计量，生成摘要表
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
    print("  统计摘要表一键生成（均值/SD/检验）")
    print("=" * 60)
    print()

    input_file = get_input("输入CSV/TSV文件路径", "data.csv")
    output_file = get_input("输出统计表路径", "stats_summary.csv")
    group_col = get_input("分组列名(留空=不分组的整体统计)", "")
    value_cols = get_input("数值列名(逗号分隔,留空=自动检测所有数值列)", "")
    test_method = get_input("组间检验方法(ttest/mannwhitney/anova/kruskal)", "ttest")

    print()
    print(f"输入:    {input_file}")
    print(f"输出:    {output_file}")
    print(f"分组列:  {group_col or '(无)'}")
    print()

    if not os.path.exists(input_file):
        print(f"[ERROR] 输入文件不存在: {input_file}")
        sys.exit(1)

    import pandas as pd
    import numpy as np

    # Read data
    sep = '\t' if input_file.endswith('.tsv') else ','
    df = pd.read_csv(input_file, sep=sep)

    # Determine value columns
    if value_cols:
        val_cols = [c.strip() for c in value_cols.split(',') if c.strip() in df.columns]
    else:
        val_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if not val_cols:
        print("[ERROR] 无数值列可统计")
        sys.exit(1)

    print(f"[Processing] 统计 {len(val_cols)} 个数值列")

    # Overall statistics
    overall_stats = []
    for col in val_cols:
        vals = df[col].dropna()
        overall_stats.append({
            'Variable': col,
            'Group': 'Overall',
            'N': len(vals),
            'Mean': round(vals.mean(), 4),
            'SD': round(vals.std(), 4),
            'Median': round(vals.median(), 4),
            'Min': round(vals.min(), 4),
            'Max': round(vals.max(), 4),
            'Q25': round(vals.quantile(0.25), 4),
            'Q75': round(vals.quantile(0.75), 4)
        })

    # Group statistics
    group_stats = []
    if group_col and group_col in df.columns:
        for col in val_cols:
            for grp_name, grp_df in df.groupby(group_col):
                vals = grp_df[col].dropna()
                group_stats.append({
                    'Variable': col,
                    'Group': str(grp_name),
                    'N': len(vals),
                    'Mean': round(vals.mean(), 4),
                    'SD': round(vals.std(), 4),
                    'Median': round(vals.median(), 4),
                    'Min': round(vals.min(), 4),
                    'Max': round(vals.max(), 4),
                    'Q25': round(vals.quantile(0.25), 4),
                    'Q75': round(vals.quantile(0.75), 4)
                })

        # Statistical tests between groups
        from scipy import stats as sp_stats

        test_results = []
        groups = df[group_col].unique()
        if len(groups) == 2:
            for col in val_cols:
                g1 = df[df[group_col] == groups[0]][col].dropna()
                g2 = df[df[group_col] == groups[1]][col].dropna()
                if len(g1) < 2 or len(g2) < 2:
                    continue
                try:
                    if test_method == 'ttest':
                        stat_val, p_val = sp_stats.ttest_ind(g1, g2)
                        test_name = 't-test'
                    elif test_method == 'mannwhitney':
                        stat_val, p_val = sp_stats.mannwhitneyu(g1, g2, alternative='two-sided')
                        test_name = 'Mann-Whitney U'
                    else:
                        stat_val, p_val = sp_stats.ttest_ind(g1, g2)
                        test_name = 't-test'
                    test_results.append({
                        'Variable': col,
                        'Test': test_name,
                        'Group1': str(groups[0]),
                        'Group2': str(groups[1]),
                        'Statistic': round(stat_val, 4),
                        'P_value': p_val,
                        'Significant': 'Yes' if p_val < 0.05 else 'No'
                    })
                except Exception:
                    continue
        elif len(groups) > 2:
            for col in val_cols:
                group_data = [g[col].dropna() for _, g in df.groupby(group_col)]
                group_data = [g for g in group_data if len(g) >= 2]
                if len(group_data) < 2:
                    continue
                try:
                    if test_method in ('anova', 'ttest'):
                        stat_val, p_val = sp_stats.f_oneway(*group_data)
                        test_name = 'ANOVA'
                    else:
                        stat_val, p_val = sp_stats.kruskal(*group_data)
                        test_name = 'Kruskal-Wallis'
                    test_results.append({
                        'Variable': col,
                        'Test': test_name,
                        'Groups': ','.join(str(g) for g in groups),
                        'Statistic': round(stat_val, 4),
                        'P_value': p_val,
                        'Significant': 'Yes' if p_val < 0.05 else 'No'
                    })
                except Exception:
                    continue

    # Save results
    all_stats = overall_stats + group_stats
    stats_df = pd.DataFrame(all_stats)
    try:
        stats_df.to_csv(output_file, index=False)
    except Exception as e:
        print(f"[ERROR] 写入失败: {e}")
        sys.exit(1)

    # Save test results separately if available
    if group_col and group_col in df.columns and 'test_results' in dir() and test_results:
        test_df = pd.DataFrame(test_results)
        test_path = output_file.rsplit('.', 1)[0] + '_tests.csv'
        test_df.to_csv(test_path, index=False)
        print(f"  检验结果: {test_path}")

    # Summary
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  数值列:        {len(val_cols)}")
    print(f"  分组数:        {len(df[group_col].unique()) if group_col and group_col in df.columns else 'N/A'}")
    print(f"  统计行数:      {len(all_stats)}")
    print(f"  输出文件:      {output_file}")
    print("=" * 60)
    print()
    print("[Done] stats_summary_table_maker completed successfully!")


if __name__ == "__main__":
    main()
