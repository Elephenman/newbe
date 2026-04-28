#!/usr/bin/env python3
"""从LD矩阵中提取LD block及其tag SNP"""

def main():
    ld_file = input("LD矩阵文件CSV路径 [ld_matrix.csv]: ") or "ld_matrix.csv"
    snp_list_file = input("SNP列表文件路径 [snps.txt]: ") or "snps.txt"
    output_file = input("输出LD block路径 [ld_blocks.tsv]: ") or "ld_blocks.tsv"
    r2_threshold = input("r2阈值 [0.8]: ") or "0.8"
    import pandas as pd, numpy as np
    r2_thr = float(r2_threshold)
    ld = pd.read_csv(ld_file, index_col=0).apply(pd.to_numeric, errors="coerce").fillna(0)
    with open(snp_list_file) as f: snps = [l.strip() for l in f if l.strip()]
    visited = set(); blocks = []
    for s in snps:
        if s in visited or s not in ld.index: continue
        block = [s2 for s2 in ld.index if s2 in ld.columns and ld.loc[s, s2] >= r2_thr]
        visited.update(block)
        blocks.append((s, len(block), ",".join(block[:10])))
    with open(output_file, "w") as out:
        out.write("Tag_SNP\tBlock_Size\tMembers\n")
        for r in blocks: out.write("\t".join(str(x) for x in r)+"\n")
    print(f"LD blocks: {len(blocks)}")


if __name__ == "__main__":
    main()
