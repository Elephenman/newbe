#!/usr/bin/env python3
"""比较两个VCF文件的变异一致性，输出concordance统计"""

import os
import sys
from collections import defaultdict


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    try:
        return dtype(val)
    except (ValueError, TypeError):
        return default


def parse_vcf(path):
    """解析VCF文件，返回变异集合和详细信息"""
    variants = set()
    variant_info = defaultdict(list)
    with open(path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            p = line.strip().split("\t")
            if len(p) >= 5:
                chrom, pos, id_, ref, alt = p[0], p[1], p[2], p[3], p[4]
                # Handle multi-allelic: split on comma
                for a in alt.split(","):
                    if a != ".":
                        key = (chrom, pos, ref, a)
                        variants.add(key)
                        variant_info[(chrom, pos)].append((ref, a))
    return variants, variant_info


def main():
    print("=" * 60)
    print("  VCF一致性检查")
    print("=" * 60)
    print()

    vcf1 = get_input("第一个VCF文件路径", "sample1.vcf")
    vcf2 = get_input("第二个VCF文件路径", "sample2.vcf")
    output_file = get_input("输出报告路径", "concordance.txt")

    print()
    print(f"VCF1:  {vcf1}")
    print(f"VCF2:  {vcf2}")
    print(f"输出:  {output_file}")
    print()

    if not os.path.exists(vcf1):
        print(f"[ERROR] VCF1不存在: {vcf1}")
        sys.exit(1)
    if not os.path.exists(vcf2):
        print(f"[ERROR] VCF2不存在: {vcf2}")
        sys.exit(1)

    s1, info1 = parse_vcf(vcf1)
    s2, info2 = parse_vcf(vcf2)

    shared = s1 & s2
    only1 = s1 - s2
    only2 = s2 - s1
    union = s1 | s2

    # Calculate metrics
    jaccard = len(shared) / len(union) if union else 0
    sensitivity = len(shared) / len(s1) if s1 else 0
    precision = len(shared) / len(s2) if s2 else 0
    f1 = 2 * precision * sensitivity / (precision + sensitivity) if (precision + sensitivity) > 0 else 0

    # Per-chromosome concordance
    chr_stats = defaultdict(lambda: {'s1': 0, 's2': 0, 'shared': 0})
    for v in s1:
        chr_stats[v[0]]['s1'] += 1
    for v in s2:
        chr_stats[v[0]]['s2'] += 1
    for v in shared:
        chr_stats[v[0]]['shared'] += 1

    # Write report
    try:
        with open(output_file, "w") as out:
            out.write("VCF Concordance Report\n")
            out.write("=" * 50 + "\n\n")
            out.write(f"VCF1:          {vcf1}\n")
            out.write(f"VCF2:          {vcf2}\n\n")
            out.write(f"VCF1 variants: {len(s1)}\n")
            out.write(f"VCF2 variants: {len(s2)}\n")
            out.write(f"Shared:        {len(shared)}\n")
            out.write(f"Only in VCF1:  {len(only1)}\n")
            out.write(f"Only in VCF2:  {len(only2)}\n\n")
            out.write(f"Jaccard Index: {jaccard:.4f}\n")
            out.write(f"Sensitivity:   {sensitivity:.4f}\n")
            out.write(f"Precision:     {precision:.4f}\n")
            out.write(f"F1 Score:      {f1:.4f}\n\n")

            out.write("Per-Chromosome Concordance:\n")
            out.write(f"{'Chr':<10} {'VCF1':>10} {'VCF2':>10} {'Shared':>10} {'Jaccard':>10}\n")
            for chrom in sorted(chr_stats.keys()):
                st = chr_stats[chrom]
                chr_jaccard = st['shared'] / max(st['s1'] + st['s2'] - st['shared'], 1)
                out.write(f"{chrom:<10} {st['s1']:>10} {st['s2']:>10} {st['shared']:>10} {chr_jaccard:>10.4f}\n")

            # Write discordant variants
            out.write("\n\nDiscordant variants (first 100 from each):\n")
            for label, variants in [("Only_VCF1", sorted(only1)[:100]), ("Only_VCF2", sorted(only2)[:100])]:
                for v in variants:
                    out.write(f"{label}\t{v[0]}\t{v[1]}\t{v[2]}\t{v[3]}\n")
    except Exception as e:
        print(f"[ERROR] 写入报告失败: {e}")
        sys.exit(1)

    # Summary
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  VCF1 variants:  {len(s1)}")
    print(f"  VCF2 variants:  {len(s2)}")
    print(f"  Shared:         {len(shared)}")
    print(f"  Only VCF1:      {len(only1)}")
    print(f"  Only VCF2:      {len(only2)}")
    print(f"  Jaccard:        {jaccard:.4f}")
    print(f"  F1 Score:       {f1:.4f}")
    print(f"  Report:         {output_file}")
    print("=" * 60)
    print()
    print("[Done] vcf-concordance-checker completed successfully!")


if __name__ == "__main__":
    main()
