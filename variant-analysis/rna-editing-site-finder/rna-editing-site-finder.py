#!/usr/bin/env python3
"""从RNA-seq VCF中筛选候选RNA编辑位点(A>I/G等)"""

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
    print("  RNA编辑位点筛选")
    print("=" * 60)
    print()

    input_vcf = get_input("RNA-seq变异VCF路径", "rna_variants.vcf")
    output_file = get_input("候选编辑位点输出", "rna_editing.tsv")
    min_alt_freq = get_input("最低变异频率", "0.1", float)
    min_depth = get_input("最低测序深度", "10", int)

    print()
    print(f"输入VCF:  {input_vcf}")
    print(f"输出:     {output_file}")
    print(f"最低AF:   {min_alt_freq}")
    print(f"最低DP:   {min_depth}")
    print()

    if not os.path.exists(input_vcf):
        print(f"[ERROR] VCF文件不存在: {input_vcf}")
        sys.exit(1)

    # RNA editing types: A>I (appears as A>G on + strand, T>C on - strand)
    etypes = {("A", "G"), ("T", "C")}
    res = []
    total_variants = 0

    with open(input_vcf) as f:
        for line in f:
            if line.startswith("#"):
                continue
            p = line.strip().split("\t")
            if len(p) < 8:
                continue
            total_variants += 1
            ref, alt = p[3].upper(), p[4].upper()

            # Skip multi-allelic or non-SNP
            if len(ref) > 1 or len(alt) > 1 or alt == '.':
                continue
            if (ref, alt) not in etypes:
                continue

            # Parse INFO field
            info = {}
            for it in p[7].split(";"):
                if "=" in it:
                    k, v = it.split("=", 1)
                    info[k] = v
                else:
                    info[it] = True

            dp = int(info.get("DP", "0"))

            # Handle AF: could be single value or per-allele
            af = 0.0
            af_str = info.get("AF", "0")
            try:
                # Take first value if comma-separated
                af = float(af_str.split(",")[0])
            except ValueError:
                # Try to compute from sample fields if AF not in INFO
                if len(p) >= 10:
                    ref_count = 0
                    alt_count = 0
                    for sample in p[9:]:
                        if sample == '.' or sample.startswith('./.'):
                            continue
                        gt = sample.split(':')[0]
                        for allele in gt.replace('|', '/').split('/'):
                            if allele == '0':
                                ref_count += 1
                            elif allele == '1':
                                alt_count += 1
                    total_alleles = ref_count + alt_count
                    if total_alleles > 0:
                        af = alt_count / total_alleles

            if dp >= min_depth and af >= min_alt_freq:
                res.append([p[0], p[1], p[2], ref, alt, dp, f"{af:.4f}"])

    # Write output
    with open(output_file, "w") as out:
        out.write("CHROM\tPOS\tID\tREF\tALT\tDepth\tAF\n")
        for r in res:
            out.write("\t".join(str(x) for x in r) + "\n")

    # Summary
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  总变异数:          {total_variants}")
    print(f"  RNA编辑候选位点:   {len(res)}")
    print(f"  过滤条件:          AF>={min_alt_freq}, DP>={min_depth}")
    print(f"  输出文件:          {output_file}")
    print("=" * 60)
    print()
    print("[Done] rna-editing-site-finder completed successfully!")


if __name__ == "__main__":
    main()
