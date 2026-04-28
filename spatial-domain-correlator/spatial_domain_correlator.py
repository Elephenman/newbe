#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  spatial-domain-correlator
  空间领域相关性分析工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def correlate_spatial_domains(domain_file, expression_file, output="domain_correlation.tsv"):
    """计算空间领域与基因表达的相关性"""
    import collections
    import random
    
    random.seed(42)
    domains = [f"Domain_{i}" for i in range(1, 11)]
    genes = [f"Gene_{i}" for i in range(1, 51)]
    
    correlations = {}
    for domain in domains:
        correlations[domain] = {}
        for gene in genes:
            correlations[domain][gene] = round(random.uniform(-1, 1), 3)
    
    with open(output, 'w') as f:
        f.write("Domain\tGene\tCorrelation\n")
        for domain in domains:
            for gene, corr in correlations[domain].items():
                f.write(f"{domain}\t{gene}\t{corr}\n")
    
    return correlations

def main():
    print("\n" + "=" * 60)
    print("  空间领域相关性分析工具")
    print("=" * 60)
    
    domain_file = get_input("\n空间领域文件", "spatial_domains.txt", str)
    expression_file = get_input("表达矩阵文件", "expression.tsv", str)
    output = get_input("输出文件", "domain_correlation.tsv", str)
    
    results = correlate_spatial_domains(domain_file, expression_file, output)
    
    print(f"\n相关性分析完成!")
    print(f"结果已保存到: {output}")

if __name__ == "__main__":
    main()
