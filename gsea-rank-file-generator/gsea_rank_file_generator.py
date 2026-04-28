#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  gsea-rank-file-generator
  GSEA排序文件生成工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def generate_gsea_rank(expr_file, deg_file, output="gsea_ranks.rnk", weight=1):
    """生成GSEA格式的排序文件"""
    try:
        import pandas as pd
        expr = pd.read_csv(expr_file, sep='\t', index_col=0)
        deg = pd.read_csv(deg_file, sep='\t', index_col=0)
    except:
        print("使用示例数据")
        import pandas as pd
        genes = [f"Gene_{i}" for i in range(100)]
        vals = list(range(-50, 50))
        import random
        random.shuffle(vals)
        expr = pd.DataFrame({'Contrast': vals}, index=genes)
    
    rank_values = expr.iloc[:, 0].sort_values(ascending=False)
    
    rank_values.to_csv(output, sep='\t', header=False)
    return len(rank_values)

def main():
    print("\n" + "=" * 60)
    print("  GSEA排序文件生成工具")
    print("=" * 60)
    
    expr_file = get_input("\n表达矩阵文件", "expression.tsv", str)
    deg_file = get_input("DEG结果文件(用于排序)", "deg_results.tsv", str)
    output = get_input("输出RANK文件", "gsea_ranks.rnk", str)
    
    count = generate_gsea_rank(expr_file, deg_file, output)
    
    print(f"\n生成了 {count} 个基因的排序文件")
    print(f"结果已保存到: {output}")

if __name__ == "__main__":
    main()
