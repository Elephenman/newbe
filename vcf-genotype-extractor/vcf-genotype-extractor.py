#!/usr/bin/env python3
"""从VCF文件提取指定样本的基因型矩阵"""

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
    print("  VCF基因型矩阵提取")
    print("=" * 60)
    print()

    input_vcf = get_input("输入VCF文件路径", "input.vcf")
    output_file = get_input("输出基因型矩阵路径", "genotypes.tsv")
    samples_str = get_input("样本名(逗号分隔,留空=全部)", "")
    gt_format = get_input("输出格式(GT/DS/GP)", "GT")

    print()
    print(f"VCF:     {input_vcf}")
    print(f"输出:    {output_file}")
    print(f"格式:    {gt_format}")
    print()

    if not os.path.exists(input_vcf):
        print(f"[ERROR] VCF文件不存在: {input_vcf}")
        sys.exit(1)

    # Parse sample filter
    sf = [s.strip() for s in samples_str.split(",") if s.strip()] if samples_str else []

    sel = []
    data = []
    idx = []
    header_lines = []

    with open(input_vcf) as f:
        for line in f:
            if line.startswith("##"):
                header_lines.append(line.strip())
                continue
            parts = line.strip().split("\t")
            if line.startswith("#CHROM"):
                all_s = parts[9:]
                if sf:
                    idx = [i for i, s in enumerate(all_s) if s in sf]
                    sel = [all_s[i] for i in idx]
                    missing_samples = [s for s in sf if s not in all_s]
                    if missing_samples:
                        print(f"[WARN] 样本不存在: {', '.join(missing_samples)}")
                else:
                    idx = list(range(len(all_s)))
                    sel = all_s
                continue

            if len(parts) < 9:
                continue

            # Get FORMAT field to locate genotype
            fmt_fields = parts[8].split(':') if len(parts) > 8 else []
            gt_idx = None
            target_idx = None

            if gt_format == "GT":
                target_key = "GT"
            elif gt_format == "DS":
                target_key = "DS"
            elif gt_format == "GP":
                target_key = "GP"
            else:
                target_key = "GT"

            if target_key in fmt_fields:
                target_idx = fmt_fields.index(target_key)

            # Extract genotypes
            gts = []
            for i in idx:
                if (9 + i) < len(parts):
                    sample_data = parts[9 + i]
                    if sample_data == '.' or sample_data.startswith('./.'):
                        gts.append('./.')
                    else:
                        fields = sample_data.split(':')
                        if target_idx is not None and target_idx < len(fields):
                            gts.append(fields[target_idx])
                        elif fields:
                            gts.append(fields[0])  # Default to GT
                        else:
                            gts.append('./.')
                else:
                    gts.append('./.')

            # Filter: only multi-allelic if desired
            ref = parts[3]
            alt = parts[4]
            data.append([parts[0], parts[1], parts[2], ref, alt] + gts)

    if not sel:
        print("[ERROR] 未找到样本")
        sys.exit(1)

    # Write output
    try:
        with open(output_file, "w") as out:
            out.write("\t".join(["CHROM", "POS", "ID", "REF", "ALT"] + sel) + "\n")
            for row in data:
                out.write("\t".join(str(x) for x in row) + "\n")
    except Exception as e:
        print(f"[ERROR] 写入失败: {e}")
        sys.exit(1)

    # Summary
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  变异数:    {len(data)}")
    print(f"  样本数:    {len(sel)}")
    print(f"  格式:      {gt_format}")
    print(f"  输出:      {output_file}")
    print("=" * 60)
    print()
    print("[Done] vcf-genotype-extractor completed successfully!")


if __name__ == "__main__":
    main()
