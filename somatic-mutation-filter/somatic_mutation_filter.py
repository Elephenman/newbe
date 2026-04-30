#!/usr/bin/env python3
"""体细胞变异过滤（肿瘤/正常配对）
从VCF文件中过滤体细胞变异，根据VAF/深度/质量等指标筛选
"""

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


def parse_info_field(info_str):
    """解析VCF INFO字段为字典"""
    info = {}
    for item in info_str.split(';'):
        if '=' in item:
            key, val = item.split('=', 1)
            info[key] = val
        else:
            info[item] = True
    return info


def main():
    print("=" * 60)
    print("  体细胞变异过滤（肿瘤/正常配对）")
    print("=" * 60)
    print()

    input_vcf = get_input("输入体细胞VCF文件路径", "somatic.vcf")
    output_file = get_input("过滤后输出路径", "somatic_filtered.vcf")
    min_vaf = get_input("最低肿瘤VAF", "0.05", float)
    min_tumor_dp = get_input("最低肿瘤深度", "10", int)
    min_normal_dp = get_input("最低正常深度", "5", int)
    max_normal_vaf = get_input("最高正常VAF(排除germline)", "0.02", float)
    min_qual = get_input("最低QUAL", "30", float)
    keep_indel = get_input("保留InDel(yes/no)", "yes")

    print()
    print(f"输入VCF:     {input_vcf}")
    print(f"输出:        {output_file}")
    print(f"最低VAF:     {min_vaf}")
    print(f"肿瘤深度:    {min_tumor_dp}")
    print(f"正常深度:    {min_normal_dp}")
    print(f"正常VAF上限: {max_normal_vaf}")
    print(f"最低QUAL:    {min_qual}")
    print()

    if not os.path.exists(input_vcf):
        print(f"[ERROR] VCF文件不存在: {input_vcf}")
        sys.exit(1)

    keep_ind = keep_indel.lower() in ('yes', 'y')

    # Process VCF
    print("[Processing] 过滤体细胞变异...")
    total = 0
    kept = 0
    filtered_reasons = {'low_qual': 0, 'low_vaf': 0, 'low_tumor_dp': 0,
                        'low_normal_dp': 0, 'high_normal_vaf': 0, 'indel': 0}

    with open(input_vcf, 'r') as fin, open(output_file, 'w') as fout:
        for line in fin:
            # Write header
            if line.startswith('#'):
                fout.write(line)
                continue

            parts = line.strip().split('\t')
            if len(parts) < 8:
                continue

            total += 1
            chrom, pos, id_, ref, alt, qual, filter_, info = parts[:8]

            # Check indel
            is_indel = len(ref) > 1 or len(alt) > 1
            if not keep_ind and is_indel:
                filtered_reasons['indel'] += 1
                continue

            # Check QUAL
            try:
                q = float(qual) if qual != '.' else 0
            except ValueError:
                q = 0
            if q < min_qual:
                filtered_reasons['low_qual'] += 1
                continue

            # Parse INFO
            info_dict = parse_info_field(info)

            # Check VAF
            tumor_vaf = 0.0
            normal_vaf = 0.0
            tumor_dp = 0
            normal_dp = 0

            # Try common VAF/DP fields
            if 'AF' in info_dict:
                try:
                    tumor_vaf = float(info_dict['AF'])
                except ValueError:
                    pass
            if 'DP' in info_dict:
                try:
                    tumor_dp = int(info_dict['DP'])
                except ValueError:
                    pass

            # Try sample-level format fields
            if len(parts) >= 11:
                fmt = parts[8].split(':')
                # Tumor sample (first sample after FORMAT)
                tumor_data = parts[9].split(':')
                # Normal sample (second sample)
                normal_data = parts[10].split(':') if len(parts) > 10 else []

                fmt_dict_t = dict(zip(fmt, tumor_data))
                fmt_dict_n = dict(zip(fmt, normal_data)) if normal_data else {}

                # Extract VAF
                if 'AF' in fmt_dict_t:
                    try:
                        tumor_vaf = float(fmt_dict_t['AF'])
                    except ValueError:
                        pass
                elif 'VAF' in fmt_dict_t:
                    try:
                        tumor_vaf = float(fmt_dict_t['VAF'])
                    except ValueError:
                        pass

                if 'AF' in fmt_dict_n:
                    try:
                        normal_vaf = float(fmt_dict_n['AF'])
                    except ValueError:
                        pass
                elif 'VAF' in fmt_dict_n:
                    try:
                        normal_vaf = float(fmt_dict_n['VAF'])
                    except ValueError:
                        pass

                # Extract depth
                if 'DP' in fmt_dict_t:
                    try:
                        tumor_dp = int(fmt_dict_t['DP'])
                    except ValueError:
                        pass
                if 'DP' in fmt_dict_n:
                    try:
                        normal_dp = int(fmt_dict_n['DP'])
                    except ValueError:
                        pass

            # Apply filters
            if tumor_vaf < min_vaf:
                filtered_reasons['low_vaf'] += 1
                continue
            if tumor_dp < min_tumor_dp:
                filtered_reasons['low_tumor_dp'] += 1
                continue
            if normal_dp < min_normal_dp and normal_dp > 0:
                filtered_reasons['low_normal_dp'] += 1
                continue
            if normal_vaf > max_normal_vaf:
                filtered_reasons['high_normal_vaf'] += 1
                continue

            kept += 1
            fout.write(line)

    # Summary
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  总变异数:        {total}")
    print(f"  保留:            {kept}")
    print(f"  过滤原因:")
    for reason, count in filtered_reasons.items():
        if count > 0:
            print(f"    {reason}: {count}")
    print(f"  输出:            {output_file}")
    print("=" * 60)
    print()
    print("[Done] somatic_mutation_filter completed successfully!")


if __name__ == "__main__":
    main()
