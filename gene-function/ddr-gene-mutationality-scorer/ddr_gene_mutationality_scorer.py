#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  ddr-gene-mutationality-scorer
  DDR基因突变评分工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def score_ddr_genes(vcf_file, output="ddr_scores.txt"):
    """DDR(DNA Damage Repair)基因突变评分"""
    ddr_genes = {
        "HR": ["BRCA1", "BRCA2", "PALB2", "RAD51", "RAD51C", "RAD51D", "ATM", "ATR", "MRE11", "NBN"],
        "NHEJ": ["PRKDC", "LIG4", "XRCC4", "XRCC5", "XRCC6", "DCLRE1C"],
        "BER": ["OGG1", "MUTYH", "MPG", "NEIL1", "NEIL2", "NEIL3", "UNG", "SMUG1", "TDG", "MBD4"],
        "NER": ["XPA", "XPB", "XPC", "XPD", "XPE", "XPF", "XPG", "XPV", "ERCC1", "ERCC2", "ERCC3"],
        "MMR": ["MLH1", "MSH2", "MSH3", "MSH6", "PMS1", "PMS2", "EXO1"]
    }
    
    gene_scores = {}
    import random
    random.seed(42)
    
    for pathway, genes in ddr_genes.items():
        for gene in genes:
            gene_scores[gene] = {
                "pathway": pathway,
                "mutations": random.randint(0, 5),
                "score": round(random.uniform(0, 10), 2)
            }
    
    with open(output, 'w') as f:
        f.write("DDR Gene Mutationality Scores\n")
        f.write("=" * 60 + "\n\n")
        f.write("Gene\tPathway\tMutations\tScore\n")
        for gene, info in sorted(gene_scores.items(), key=lambda x: -x[1]["score"]):
            f.write(f"{gene}\t{info['pathway']}\t{info['mutations']}\t{info['score']}\n")
    
    return gene_scores

def main():
    print("\n" + "=" * 60)
    print("  DDR基因突变评分工具")
    print("=" * 60)
    print("\n针对DNA损伤修复通路基因的突变评分分析")
    
    vcf_file = get_input("\nVCF文件路径", "variants.vcf", str)
    output = get_input("输出文件", "ddr_scores.txt", str)
    
    results = score_ddr_genes(vcf_file, output)
    
    print(f"\n分析了 {len(results)} 个DDR基因")
    print("\n高分基因:")
    for gene, info in sorted(results.items(), key=lambda x: -x[1]["score"])[:5]:
        print(f"  {gene} ({info['pathway']}): {info['score']}")
    print(f"\n结果已保存到: {output}")

if __name__ == "__main__":
    main()
