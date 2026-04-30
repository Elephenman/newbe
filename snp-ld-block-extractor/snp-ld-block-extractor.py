#!/usr/bin/env python3
"""从LD矩阵中提取LD block及其tag SNP"""

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
    print("  LD Block提取器")
    print("=" * 60)
    print()

    ld_file = get_input("LD矩阵文件CSV路径", "ld_matrix.csv")
    snp_list_file = get_input("SNP列表文件路径", "snps.txt")
    output_file = get_input("输出LD block路径", "ld_blocks.tsv")
    r2_threshold = get_input("r2阈值", "0.8", float)

    print()
    print(f"LD矩阵:   {ld_file}")
    print(f"SNP列表:  {snp_list_file}")
    print(f"输出:     {output_file}")
    print(f"r2阈值:   {r2_threshold}")
    print()

    if not os.path.exists(ld_file):
        print(f"[ERROR] LD矩阵文件不存在: {ld_file}")
        sys.exit(1)
    if not os.path.exists(snp_list_file):
        print(f"[ERROR] SNP列表文件不存在: {snp_list_file}")
        sys.exit(1)

    import pandas as pd
    import numpy as np

    print("[Processing] 读取LD矩阵...")
    ld = pd.read_csv(ld_file, index_col=0).apply(pd.to_numeric, errors="coerce").fillna(0)

    print("[Processing] 读取SNP列表...")
    with open(snp_list_file) as f:
        snps = [l.strip() for l in f if l.strip()]

    # Validate SNPs in matrix
    snps_in_matrix = [s for s in snps if s in ld.index]
    snps_missing = [s for s in snps if s not in ld.index]
    if snps_missing:
        print(f"[WARN] {len(snps_missing)} SNPs不在LD矩阵中")
    if not snps_in_matrix:
        print("[ERROR] 无有效SNP")
        sys.exit(1)

    # Extract LD blocks using greedy clustering
    print("[Processing] 提取LD blocks...")
    visited = set()
    blocks = []

    # Also check column names match
    common_snps = [s for s in snps_in_matrix if s in ld.columns]
    if not common_snps:
        print("[ERROR] SNP名称在行和列中不匹配")
        sys.exit(1)

    for s in common_snps:
        if s in visited:
            continue

        # Find all SNPs in LD with this one
        block = []
        for s2 in ld.columns:
            if s2 in ld.index:
                try:
                    r2_val = ld.loc[s, s2]
                    if r2_val >= r2_threshold:
                        block.append(s2)
                except KeyError:
                    continue

        visited.update(block)

        # Tag SNP is the one with highest average r2 to others
        if len(block) > 1:
            avg_r2 = {}
            sub_matrix = ld.loc[block, block]
            for s2 in block:
                if s2 in sub_matrix.index:
                    avg_r2[s2] = sub_matrix.loc[s2, block].mean()
            tag_snp = max(avg_r2, key=avg_r2.get)
        else:
            tag_snp = s

        blocks.append({
            'tag': tag_snp,
            'size': len(block),
            'members': block
        })

    # Write output
    try:
        with open(output_file, "w") as out:
            out.write("Tag_SNP\tBlock_Size\tMembers\n")
            for b in blocks:
                members_str = ",".join(b['members'][:20])
                if len(b['members']) > 20:
                    members_str += f"...({len(b['members'])} total)"
                out.write(f"{b['tag']}\t{b['size']}\t{members_str}\n")
    except Exception as e:
        print(f"[ERROR] 写入失败: {e}")
        sys.exit(1)

    # Summary
    singletons = sum(1 for b in blocks if b['size'] == 1)
    multi = sum(1 for b in blocks if b['size'] > 1)

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  输入SNPs:        {len(snps)}")
    print(f"  有效SNPs:        {len(snps_in_matrix)}")
    print(f"  LD blocks:       {len(blocks)}")
    print(f"  单SNP blocks:    {singletons}")
    print(f"  多SNP blocks:    {multi}")
    print(f"  r2阈值:          {r2_threshold}")
    print(f"  输出:            {output_file}")
    print("=" * 60)
    print()
    print("[Done] snp-ld-block-extractor completed successfully!")


if __name__ == "__main__":
    main()
