#!/usr/bin/env python3
"""结构变异(SV)类型统计+环形图
解析VCF/BEDPE格式的结构变异文件，统计DEL/DUP/INV/TRA/BND类型分布
"""

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


def parse_sv_vcf(filepath):
    """解析VCF格式的SV调用结果"""
    sv_types = defaultdict(int)
    sv_list = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 8:
                continue

            chrom, pos, id_, ref, alt, qual, filter_, info = parts[:8]

            # Determine SV type
            info_dict = {}
            for item in info.split(';'):
                if '=' in item:
                    key, val = item.split('=', 1)
                    info_dict[key] = val
                else:
                    info_dict[item] = True

            svtype = info_dict.get('SVTYPE', '')

            # Fallback: infer from ALT
            if not svtype:
                if alt.startswith('<DEL'):
                    svtype = 'DEL'
                elif alt.startswith('<DUP'):
                    svtype = 'DUP'
                elif alt.startswith('<INV'):
                    svtype = 'INV'
                elif alt.startswith('<TRA') or alt.startswith('<BND'):
                    svtype = 'TRA'
                elif '[' in alt or ']' in alt:
                    svtype = 'BND'
                else:
                    svtype = 'OTHER'

            # Get SV length
            svlen = 0
            if 'SVLEN' in info_dict:
                try:
                    svlen = abs(int(info_dict['SVLEN']))
                except ValueError:
                    pass
            elif 'END' in info_dict:
                try:
                    svlen = abs(int(info_dict['END']) - int(pos))
                except ValueError:
                    pass

            sv_types[svtype] += 1
            sv_list.append({
                'chrom': chrom, 'pos': pos, 'id': id_,
                'svtype': svtype, 'svlen': svlen, 'qual': qual
            })

    return sv_types, sv_list


def parse_bedpe(filepath):
    """解析BEDPE格式的SV"""
    sv_types = defaultdict(int)
    sv_list = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 7:
                continue
            try:
                chrom1, start1, end1, chrom2, start2, end2, name = parts[:7]
                svtype = parts[7] if len(parts) > 7 else 'OTHER'
                svlen = abs(int(end1) - int(start1))
                sv_types[svtype] += 1
                sv_list.append({
                    'chrom': chrom1, 'pos': start1, 'id': name,
                    'svtype': svtype, 'svlen': svlen, 'qual': '.'
                })
            except (ValueError, IndexError):
                continue
    return sv_types, sv_list


def main():
    print("=" * 60)
    print("  结构变异(SV)类型统计+环形图")
    print("=" * 60)
    print()

    input_file = get_input("SV文件路径(VCF/BEDPE)", "sv_calls.vcf")
    output_file = get_input("统计报告输出路径", "sv_summary.tsv")
    make_plot = get_input("是否生成环形图(yes/no)", "yes")
    file_format = get_input("文件格式(vcf/bedpe)", "vcf")

    print()
    print(f"输入:    {input_file}")
    print(f"输出:    {output_file}")
    print(f"格式:    {file_format}")
    print()

    if not os.path.exists(input_file):
        print(f"[ERROR] 输入文件不存在: {input_file}")
        sys.exit(1)

    # Parse SV file
    print("[Processing] 解析SV文件...")
    if file_format == 'bedpe':
        sv_types, sv_list = parse_bedpe(input_file)
    else:
        sv_types, sv_list = parse_sv_vcf(input_file)

    total = len(sv_list)
    print(f"[Processing] 找到 {total} 个结构变异")

    # Statistics
    print("[Processing] 统计SV类型分布...")
    for svtype, count in sorted(sv_types.items(), key=lambda x: -x[1]):
        pct = count / total * 100 if total > 0 else 0
        print(f"  {svtype}: {count} ({pct:.1f}%)")

    # Length statistics by type
    len_stats = {}
    for sv in sv_list:
        svtype = sv['svtype']
        if svtype not in len_stats:
            len_stats[svtype] = []
        if sv['svlen'] > 0:
            len_stats[svtype].append(sv['svlen'])

    # Save summary
    try:
        with open(output_file, 'w') as out:
            out.write("SVType\tCount\tPercentage\tMedianLen\tMeanLen\n")
            for svtype in sorted(sv_types.keys()):
                count = sv_types[svtype]
                pct = count / total * 100 if total > 0 else 0
                lens = len_stats.get(svtype, [])
                median_len = sorted(lens)[len(lens)//2] if lens else 0
                mean_len = sum(lens) / len(lens) if lens else 0
                out.write(f"{svtype}\t{count}\t{pct:.1f}\t{median_len}\t{mean_len:.0f}\n")
    except Exception as e:
        print(f"[ERROR] 写入失败: {e}")
        sys.exit(1)

    # Plot
    if make_plot.lower() in ('yes', 'y'):
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt

            labels = list(sv_types.keys())
            sizes = list(sv_types.values())
            colors = ['#E64B35', '#4DBBD5', '#00A087', '#3C5488', '#F39B7F', '#8491B4']
            colors = colors[:len(labels)]

            fig, ax = plt.subplots(figsize=(8, 8))
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                               autopct='%1.1f%%', pctdistance=0.75,
                                               wedgeprops=dict(width=0.5))
            ax.set_title("Structural Variant Distribution")
            plt.tight_layout()
            plot_path = output_file.rsplit('.', 1)[0] + '_donut.png'
            plt.savefig(plot_path, dpi=300)
            plt.close()
            print(f"  环形图: {plot_path}")
        except ImportError:
            print("[WARN] matplotlib未安装，跳过出图")

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  总SV数:       {total}")
    print(f"  SV类型数:     {len(sv_types)}")
    print(f"  输出文件:     {output_file}")
    print("=" * 60)
    print()
    print("[Done] structural_variant_summarizer completed successfully!")


if __name__ == "__main__":
    main()
