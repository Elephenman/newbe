#!/usr/bin/env python3
"""VEP/SnpEff结果解析+报告生成
解析VEP或SnpEff的注释输出，汇总变异效应统计
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


def parse_vep_output(filepath):
    """解析VEP标准输出格式"""
    stats = {
        'total': 0,
        'consequence': defaultdict(int),
        'impact': defaultdict(int),
        'biotype': defaultdict(int),
        'chr_dist': defaultdict(int),
        'variant_type': defaultdict(int),
    }
    variants = []

    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 7:
                continue

            stats['total'] += 1
            chrom = parts[0]
            pos = parts[1]
            ref = parts[3]
            alt = parts[4]

            stats['chr_dist'][chrom] += 1

            # Variant type
            if len(ref) == 1 and len(alt) == 1:
                stats['variant_type']['SNP'] += 1
            else:
                stats['variant_type']['INDEL'] += 1

            # Parse consequence (CSQ field or last column)
            if len(parts) >= 8:
                # Try VEP extra field
                extra = parts[7] if len(parts) > 7 else ''
                # Parse consequence from extra
                for item in extra.split(';'):
                    if item.startswith('Consequence='):
                        consequences = item.split('=')[1].split('&')
                        for c in consequences:
                            stats['consequence'][c] += 1
                    elif item.startswith('IMPACT='):
                        impact = item.split('=')[1]
                        stats['impact'][impact] += 1
                    elif item.startswith('BIOTYPE='):
                        biotype = item.split('=')[1]
                        stats['biotype'][biotype] += 1

    return stats


def parse_snpeff_output(filepath):
    """解析SnpEff VCF注释输出"""
    stats = {
        'total': 0,
        'consequence': defaultdict(int),
        'impact': defaultdict(int),
        'biotype': defaultdict(int),
        'chr_dist': defaultdict(int),
        'variant_type': defaultdict(int),
    }

    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 8:
                continue

            stats['total'] += 1
            chrom, pos = parts[0], parts[1]
            ref, alt = parts[3], parts[4]

            stats['chr_dist'][chrom] += 1

            if len(ref) == 1 and len(alt) == 1:
                stats['variant_type']['SNP'] += 1
            else:
                stats['variant_type']['INDEL'] += 1

            # Parse ANN field from INFO
            info = parts[7]
            for item in info.split(';'):
                if item.startswith('ANN=') or item.startswith('EFF='):
                    annotations = item.split('=', 1)[1].split(',')
                    for ann in annotations[:1]:  # Take first annotation
                        fields = ann.split('|')
                        if len(fields) >= 2:
                            effects = fields[1].split('&')
                            for eff in effects:
                                stats['consequence'][eff] += 1
                        if len(fields) >= 3:
                            stats['impact'][fields[2]] += 1
                        if len(fields) >= 7:
                            stats['biotype'][fields[6]] += 1

    return stats


def main():
    print("=" * 60)
    print("  VEP/SnpEff结果解析+报告生成")
    print("=" * 60)
    print()

    input_file = get_input("VEP/SnpEff注释文件路径", "annotated.vcf")
    output_file = get_input("统计报告输出路径", "vep_report.tsv")
    make_plot = get_input("生成效应分布图(yes/no)", "yes")
    tool = get_input("注释工具(vep/snpeff)", "snpeff")

    print()
    print(f"输入:      {input_file}")
    print(f"输出:      {output_file}")
    print(f"工具:      {tool}")
    print()

    if not os.path.exists(input_file):
        print(f"[ERROR] 文件不存在: {input_file}")
        sys.exit(1)

    # Parse
    print("[Processing] 解析注释结果...")
    if tool == 'vep':
        stats = parse_vep_output(input_file)
    else:
        stats = parse_snpeff_output(input_file)

    print(f"[Processing] 找到 {stats['total']} 个注释变异")

    # Print report
    print()
    print("=" * 60)
    print("  变异效应统计")
    print("=" * 60)
    print(f"  总变异数: {stats['total']}")
    print()
    print("  变异类型:")
    for vtype, count in sorted(stats['variant_type'].items(), key=lambda x: -x[1]):
        pct = count / stats['total'] * 100 if stats['total'] else 0
        print(f"    {vtype}: {count} ({pct:.1f}%)")

    print()
    print("  影响级别(Impact):")
    for impact, count in sorted(stats['impact'].items(), key=lambda x: -x[1]):
        pct = count / stats['total'] * 100 if stats['total'] else 0
        print(f"    {impact}: {count} ({pct:.1f}%)")

    print()
    print("  功能效应(Top 15):")
    for conseq, count in sorted(stats['consequence'].items(), key=lambda x: -x[1])[:15]:
        pct = count / stats['total'] * 100 if stats['total'] else 0
        print(f"    {conseq}: {count} ({pct:.1f}%)")

    # Save TSV
    try:
        with open(output_file, 'w') as out:
            out.write("Category\tItem\tCount\tPercentage\n")
            for vtype, count in stats['variant_type'].items():
                pct = count / stats['total'] * 100 if stats['total'] else 0
                out.write(f"VariantType\t{vtype}\t{count}\t{pct:.1f}\n")
            for impact, count in stats['impact'].items():
                pct = count / stats['total'] * 100 if stats['total'] else 0
                out.write(f"Impact\t{impact}\t{count}\t{pct:.1f}\n")
            for conseq, count in stats['consequence'].items():
                pct = count / stats['total'] * 100 if stats['total'] else 0
                out.write(f"Consequence\t{conseq}\t{count}\t{pct:.1f}\n")
            for chrom, count in sorted(stats['chr_dist'].items()):
                pct = count / stats['total'] * 100 if stats['total'] else 0
                out.write(f"Chromosome\t{chrom}\t{count}\t{pct:.1f}\n")
    except Exception as e:
        print(f"[ERROR] 写入失败: {e}")
        sys.exit(1)

    # Plot
    if make_plot.lower() in ('yes', 'y'):
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt

            fig, axes = plt.subplots(1, 2, figsize=(14, 6))

            # Impact pie chart
            if stats['impact']:
                labels = list(stats['impact'].keys())
                sizes = list(stats['impact'].values())
                colors_impact = {'HIGH': '#E64B35', 'MODERATE': '#F39B7F',
                                'LOW': '#4DBBD5', 'MODIFIER': '#8491B4'}
                pie_colors = [colors_impact.get(l, '#CCCCCC') for l in labels]
                axes[0].pie(sizes, labels=labels, colors=pie_colors, autopct='%1.1f%%')
                axes[0].set_title('Impact Distribution')

            # Top consequences bar chart
            if stats['consequence']:
                top_conseq = sorted(stats['consequence'].items(), key=lambda x: -x[1])[:15]
                labels = [c[0] for c in top_conseq]
                counts = [c[1] for c in top_conseq]
                axes[1].barh(range(len(labels)), counts, color='#3C5488')
                axes[1].set_yticks(range(len(labels)))
                axes[1].set_yticklabels(labels, fontsize=8)
                axes[1].set_xlabel('Count')
                axes[1].set_title('Top Consequences')
                axes[1].invert_yaxis()

            plt.tight_layout()
            plot_path = output_file.rsplit('.', 1)[0] + '_plot.png'
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"  统计图: {plot_path}")
        except ImportError:
            print("[WARN] matplotlib未安装，跳过出图")

    print()
    print("[Done] variant_effect_predictor_wrapper completed successfully!")


if __name__ == "__main__":
    main()
