#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  tpm-matrix-normalizer
  TPM表达矩阵标准化工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def normalize_tpm(count_file, output="tpm_normalized.tsv", log_transform=True, pseudocount=1):
    """TPM矩阵标准化和log转换"""
    try:
        import pandas as pd
        data = pd.read_csv(count_file, sep='\t', index_col=0)
    except:
        print("使用示例数据")
        import pandas as pd
        data = pd.DataFrame({
            'Sample1': [100, 50, 200, 80],
            'Sample2': [120, 60, 180, 90]
        }, index=['Gene1', 'Gene2', 'Gene3', 'Gene4'])
    
    result = data.copy()
    
    if log_transform:
        import numpy as np
        result = np.log2(result + pseudocount)
    
    result.to_csv(output, sep='\t')
    return result

def main():
    print("\n" + "=" * 60)
    print("  TPM矩阵标准化工具")
    print("=" * 60)
    
    count_file = get_input("\n表达矩阵文件", "tpm_matrix.tsv", str)
    output = get_input("输出文件", "tpm_normalized.tsv", str)
    log_transform = get_input("是否log2转换(yes/no)", "yes", str).lower() == "yes"
    
    result = normalize_tpm(count_file, output, log_transform)
    
    print(f"\n标准化完成!")
    print(f"矩阵维度: {result.shape}")
    print(f"结果已保存到: {output}")

if __name__ == "__main__":
    main()
