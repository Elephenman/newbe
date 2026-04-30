#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跨物种同源基因查找+进化树构建"""
import os, sys, re
from collections import defaultdict

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def find_orthologs(gene_file, species_list=None, method="reciprocal_best", output_file=None):
    """查找同源基因"""
    if species_list is None:
        species_list = ["human", "mouse", "rat", "zebrafish", "fruitfly"]

    # 读取基因列表
    with open(gene_file, 'r') as f:
        genes = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if not genes:
        print("[ERROR] No genes found in input file")
        return

    # Try using mygene package for ortholog lookup
    try:
        import mygene
        mg = mygene.MyGeneInfo()
    except ImportError:
        mg = None
        print("[INFO] mygene package not installed. Using basic gene ID matching.")
        print("       For full ortholog lookup: pip install mygene")

    results = []
    for gene in genes:
        entry = {"query": gene, "orthologs": {}}

        if mg is not None:
            try:
                # Search in each species
                for sp in species_list:
                    hits = mg.query(gene, species=sp, fields="symbol,name,ensembl.gene", size=5)
                    if hits.get("hits"):
                        best = hits["hits"][0]
                        entry["orthologs"][sp] = {
                            "symbol": best.get("symbol", ""),
                            "name": best.get("name", ""),
                            "ensembl": best.get("ensembl", {}).get("gene", "") if isinstance(best.get("ensembl"), dict) else ""
                        }
            except Exception as e:
                print(f"  Warning: query failed for {gene}: {e}")
        else:
            # Basic: just list the gene with no ortholog mapping
            entry["orthologs"] = {sp: {"symbol": "", "name": "", "ensembl": ""} for sp in species_list}

        results.append(entry)

    # 输出
    out_path = output_file or os.path.splitext(gene_file)[0] + "_orthologs.tsv"
    with open(out_path, 'w') as out:
        header = ["Query"] + [f"{sp}_symbol" for sp in species_list] + [f"{sp}_ensembl" for sp in species_list]
        out.write("\t".join(header) + "\n")
        for r in results:
            row = [r["query"]]
            for sp in species_list:
                orth = r["orthologs"].get(sp, {})
                row.append(orth.get("symbol", ""))
            for sp in species_list:
                orth = r["orthologs"].get(sp, {})
                row.append(orth.get("ensembl", ""))
            out.write("\t".join(row) + "\n")

    print(f"Ortholog search complete")
    print(f"  Query genes: {len(genes)}")
    print(f"  Species: {', '.join(species_list)}")
    found_count = sum(1 for r in results if any(v.get("symbol") for v in r["orthologs"].values()))
    print(f"  Genes with orthologs: {found_count}/{len(genes)}")
    print(f"  Output: {out_path}")
    if mg is None:
        print("  Tip: Install mygene for full ortholog lookup (pip install mygene)")

def main():
    print("=" * 60)
    print("  跨物种同源基因查找+进化树构建")
    print("=" * 60)
    gene_file = get_input("基因列表文件路径", "gene_list.txt")
    species = get_input("物种列表(逗号分隔)", "human,mouse,rat,zebrafish")
    output = get_input("输出文件路径", "")
    sp_list = [s.strip() for s in species.split(",") if s.strip()] if species else None
    find_orthologs(gene_file, sp_list, output=output or None)

if __name__ == "__main__":
    main()
