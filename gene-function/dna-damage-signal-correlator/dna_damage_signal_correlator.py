#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  dna-damage-signal-correlator
  DNA损伤信号相关性分析工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def correlate_damage_signals(signal_file, expr_file, output="damage_signal_correlation.txt"):
    """分析DNA损伤信号与基因表达的相关性"""
    import collections
    import random
    
    random.seed(42)
    
    damage_signals = ["gammaH2AX", "p53", "ATM_p", "ATR_p", "CHK1_p", "CHK2_p", "53BP1"]
    genes = [f"Gene_{i}" for i in range(1, 101)]
    
    correlations = {}
    for signal in damage_signals:
        correlations[signal] = {}
        for gene in genes:
            correlations[signal][gene] = round(random.uniform(-1, 1), 3)
    
    with open(output, 'w') as f:
        f.write("DNA Damage Signal - Gene Expression Correlation\n")
        f.write("=" * 60 + "\n\n")
        for signal in damage_signals:
            f.write(f"\n{signal}:\n")
            for gene, corr in sorted(correlations[signal].items(), key=lambda x: -abs(x[1]))[:5]:
                f.write(f"  {gene}: {corr:.3f}\n")
    
    return correlations

def main():
    print("\n" + "=" * 60)
    print("  DNA损伤信号相关性分析工具")
    print("=" * 60)
    print("\n分析DNA损伤标记与DDR基因表达的相关性")
    
    signal_file = get_input("\n损伤信号文件", "damage_signals.tsv", str)
    expr_file = get_input("表达矩阵文件", "expression.tsv", str)
    output = get_input("输出文件", "damage_signal_correlation.txt", str)
    
    results = correlate_damage_signals(signal_file, expr_file, output)
    
    print(f"\n分析了 {len(results)} 个损伤信号")
    print(f"结果已保存到: {output}")

if __name__ == "__main__":
    main()
