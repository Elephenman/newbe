#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多序列文件统计+可视化
解析FASTA，统计长度/GC/氨基酸比例，生成分布图

功能：
- 序列长度分布（均值/中位数/最大/最小）
- GC含量分布
- 氨基酸比例（蛋白质序列）
- 统计表CSV + 可选matplotlib分布图
"""

import os
import sys
from collections import defaultdict

try:
    import matplotlib
    matplotlib.use('Agg')  # 无GUI后端
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False


def get_input(prompt, default=None, type=str):
    val = input(f"{prompt} [默认: {default}]: ").strip()
    if val == "":
        return default
    try:
        return type(val)
    except (ValueError, TypeError):
        print(f"  ⚠ 输入格式错误，使用默认值: {default}")
        return default


def parse_fasta(filepath):
    """解析FASTA文件，返回序列字典"""
    sequences = {}
    current_id = None
    current_seq = []

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_id:
                    sequences[current_id] = ''.join(current_seq)
                current_id = line[1:].split()[0]  # 取第一个word作为ID
                current_seq = []
            elif line and current_id:
                current_seq.append(line.upper())

    if current_id:
        sequences[current_id] = ''.join(current_seq)

    return sequences


def is_protein(sequences):
    """判断是否为蛋白质序列（含有L/I/F/P/Y/W/Q/E/H/K/R/D/N/S/T/V/M/C/A/G以外的字符则不是）"""
    dna_chars = set('ATCGN')
    aa_chars = set('ACDEFGHIKLMNPQRSTVWY*')
    sample_seqs = list(sequences.values())[:10]
    all_chars = set(''.join(sample_seqs))
    # 如果字符集完全是DNA字符，则判断为DNA
    if all_chars <= dna_chars:
        return False
    # 如果包含典型的氨基酸专属字符（如L, I, F, P, Y, W, E, Q, H, K, R, D, M），则判断为蛋白质
    aa_specific = set('LIFPYWEQHKRDM')
    if all_chars & aa_specific:
        return True
    return False


def calculate_stats(sequences):
    """计算统计指标"""
    lengths = [len(s) for s in sequences.values()]
    gc_contents = []
    aa_ratios = defaultdict(list)

    for seq_id, seq in sequences.items():
        seq_len = len(seq)
        if seq_len == 0:
            continue

        # GC含量
        g_count = seq.count('G')
        c_count = seq.count('C')
        gc_pct = round((g_count + c_count) / seq_len * 100, 2)
        gc_contents.append(gc_pct)

        # 氨基酸比例（如果是蛋白质）
        for aa in set(seq):
            aa_ratios[aa].append(round(seq.count(aa) / seq_len * 100, 2))

    stats = {
        "count": len(sequences),
        "total_bases": sum(lengths),
        "min_len": min(lengths) if lengths else 0,
        "max_len": max(lengths) if lengths else 0,
        "mean_len": round(sum(lengths) / len(lengths), 1) if lengths else 0,
        "median_len": sorted(lengths)[len(lengths)//2] if lengths else 0,
        "lengths": lengths,
        "gc_contents": gc_contents,
        "mean_gc": round(sum(gc_contents) / len(gc_contents), 2) if gc_contents else 0,
        "aa_ratios": dict(aa_ratios),
    }
    return stats


def save_csv(stats, sequences, filepath, output_path):
    """保存统计CSV"""
    rows = []
    for seq_id, seq in sequences.items():
        gc = round((seq.count('G') + seq.count('C')) / len(seq) * 100, 2) if len(seq) > 0 else 0
        rows.append(f"{seq_id},{len(seq)},{gc}%")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("序列ID,长度(bp),GC含量\n")
        f.write("\n".join(rows))
    print(f"  ✅ 统计CSV已保存: {output_path}")


def plot_length_distribution(lengths, output_path):
    """绘制长度分布直方图"""
    plt.figure(figsize=(10, 6))
    plt.hist(lengths, bins=50, color='#2196F3', edgecolor='white', alpha=0.8)
    plt.xlabel('序列长度 (bp)', fontsize=12)
    plt.ylabel('频次', fontsize=12)
    plt.title('序列长度分布', fontsize=14, fontweight='bold')
    mean_val = sum(lengths) / len(lengths) if lengths else 0
    plt.axvline(mean_val, color='red', linestyle='--', label=f'均值={mean_val:.0f}')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"  ✅ 长度分布图已保存: {output_path}")


def plot_gc_distribution(gc_contents, output_path):
    """绘制GC含量密度图"""
    plt.figure(figsize=(10, 6))
    plt.hist(gc_contents, bins=50, color='#4CAF50', edgecolor='white', alpha=0.8)
    plt.xlabel('GC含量 (%)', fontsize=12)
    plt.ylabel('频次', fontsize=12)
    plt.title('GC含量分布', fontsize=14, fontweight='bold')
    mean_gc = sum(gc_contents) / len(gc_contents) if gc_contents else 0
    plt.axvline(mean_gc, color='red', linestyle='--', label=f'均值={mean_gc:.1f}%')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"  ✅ GC分布图已保存: {output_path}")


def print_report(stats, filepath, is_protein_flag):
    """终端打印统计报告"""
    seq_type = "蛋白质" if is_protein_flag else "核酸(DNA/RNA)"

    report = f"""
╔══════════════════════════════════════════════════════════════╗
║              序列统计可视化报告                               ║
╠══════════════════════════════════════════════════════════════╣
║ 文件: {os.path.basename(filepath)}
║ 类型: {seq_type}
║══════════════════════════════════════════════════════════════║
║ 【长度统计】
║   序列数量:     {stats['count']}
║   总碱基数:     {stats['total_bases']}
║   平均长度:     {stats['mean_len']} bp
║   中位数长度:   {stats['median_len']} bp
║   最短序列:     {stats['min_len']} bp
║   最长序列:     {stats['max_len']} bp
║══════════════════════════════════════════════════════════════║
║ 【GC含量】
║   平均GC%:      {stats['mean_gc']}%
"""
    if is_protein_flag and stats['aa_ratios']:
        # 显示top10氨基酸
        aa_means = {}
        for aa, ratios in stats['aa_ratios'].items():
            aa_means[aa] = round(sum(ratios) / len(ratios), 2)
        sorted_aa = sorted(aa_means.items(), key=lambda x: -x[1])[:10]
        report += "║══════════════════════════════════════════════════════════════║\n"
        report += "║ 【氨基酸比例(top10)】\n"
        for aa, pct in sorted_aa:
            report += f"║   {aa}: {pct}%\n"

    report += "╚══════════════════════════════════════════════════════════════╝\n"
    return report


def main():
    print("=" * 60)
    print("  📈 序列统计+可视化")
    print("=" * 60)

    filepath = get_input("输入FASTA文件路径", default="sequences.fasta")
    if not os.path.exists(filepath):
        print(f"  ❌ 文件不存在: {filepath}")
        sys.exit(1)

    stats_dims = get_input("统计维度(length/gc/aa/all)", default="all")
    make_plot = get_input("是否出图(yes/no)", default="yes")
    plot_flag = make_plot.lower() in ('yes', 'y', '1', 'true')

    img_format = get_input("图片格式(png/pdf)", default="png") if plot_flag else "png"

    print(f"\n  ⏳ 正在解析FASTA文件: {filepath} ...")
    sequences = parse_fasta(filepath)

    if not sequences:
        print("  ❌ 未解析到任何序列，请检查文件格式")
        sys.exit(1)

    is_protein_flag = is_protein(sequences)
    stats = calculate_stats(sequences)

    # 打印报告
    report = print_report(stats, filepath, is_protein_flag)
    print(report)

    # 保存CSV
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_dir = os.path.dirname(filepath) or "."
    csv_path = os.path.join(output_dir, f"{base_name}_stats.csv")
    save_csv(stats, sequences, filepath, csv_path)

    # 绘图
    if plot_flag and HAS_MPL:
        dims = stats_dims.split(',') if stats_dims != 'all' else ['length', 'gc']
        if 'all' in dims:
            dims = ['length', 'gc']

        if 'length' in dims:
            ext = img_format.lower()
            length_plot_path = os.path.join(output_dir, f"{base_name}_length_dist.{ext}")
            plot_length_distribution(stats['lengths'], length_plot_path)

        if 'gc' in dims and not is_protein_flag:
            gc_plot_path = os.path.join(output_dir, f"{base_name}_gc_dist.{ext}")
            plot_gc_distribution(stats['gc_contents'], gc_plot_path)

    elif plot_flag and not HAS_MPL:
        print("  ⚠ matplotlib未安装，无法出图。请运行: pip install matplotlib")

    print("  ✅ 序列统计完成！")


if __name__ == "__main__":
    main()