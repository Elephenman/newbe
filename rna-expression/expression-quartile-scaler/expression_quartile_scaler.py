#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  expression-quartile-scaler
  表达矩阵分位数标准化工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def quantile_normalize(expr_file, output="quantile_normalized.tsv"):
    """分位数标准化"""
    try:
        import pandas as pd
        import numpy as np
        
        data = pd.read_csv(expr_file, sep='\t', index_col=0)
    except:
        print("使用示例数据")
        import pandas as pd
        import numpy as np
        data = pd.DataFrame(np.random.randn(100, 5) * 10 + 50,
                           columns=['S1', 'S2', 'S3', 'S4', 'S5'])
    
    rank_mean = data.stack().groupby(data.rank(method='first').stack().astype(int)).mean()
    result = data.rank(method='first').stack().astype(int).map(rank_mean).unstack()
    
    result.to_csv(output, sep='\t')
    return result

def main():
    print("\n" + "=" * 60)
    print("  表达矩阵分位数标准化工具")
    print("=" * 60)
    
    expr_file = get_input("\n表达矩阵文件", "expression.tsv", str)
    output = get_input("输出文件", "quantile_normalized.tsv", str)
    
    result = quantile_normalize(expr_file, output)
    
    print(f"\n分位数标准化完成!")
    print(f"矩阵维度: {result.shape}")
    print(f"结果已保存到: {output}")

if __name__ == "__main__":
    main()
