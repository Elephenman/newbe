#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  rpkm-to-tpm-converter
  RPKM转TPM工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def convert_rpkm_to_tpm(rpkm_file, output="tpm_matrix.tsv", gene_length_file=""):
    """RPKM转TPM"""
    try:
        import pandas as pd
        rpkm_data = pd.read_csv(rpkm_file, sep='\t', index_col=0)
    except:
        print("使用示例数据")
        import pandas as pd
        rpkm_data = pd.DataFrame({
            'Sample1': [100.5, 50.2, 200.1],
            'Sample2': [120.3, 60.1, 180.5]
        }, index=['Gene1', 'Gene2', 'Gene3'])
    
    tpm_data = rpkm_data.copy()
    
    for col in tpm_data.columns:
        tpm_data[col] = rpkm_data[col] / rpkm_data[col].sum() * 1e6
    
    tpm_data.to_csv(output, sep='\t')
    return tpm_data

def main():
    print("\n" + "=" * 60)
    print("  RPKM转TPM工具")
    print("=" * 60)
    
    rpkm_file = get_input("\nRPKM矩阵文件", "rpkm_matrix.tsv", str)
    output = get_input("输出TPM文件", "tpm_matrix.tsv", str)
    
    tpm_data = convert_rpkm_to_tpm(rpkm_file, output)
    
    print(f"\n转换完成!")
    print(f"矩阵维度: {tpm_data.shape}")
    print(f"\n前几行数据预览:")
    print(tpm_data.head())
    print(f"\n结果已保存到: {output}")

if __name__ == "__main__":
    main()
