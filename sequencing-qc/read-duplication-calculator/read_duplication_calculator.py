#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测序reads重复率统计+分布可视化"""
import os, sys
from collections import Counter

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def calculate_read_duplication(fastq_path, output_file=None, make_plot=True, max_reads=0):
    """计算FASTQ文件的reads重复率

    统计相同序列出现的次数，计算重复率和分布
    """
    # 读取序列
    seq_counter = Counter()
    total = 0

    with open(fastq_path, 'r') as f:
        while True:
            header = f.readline()
            if not header:
                break
            seq = f.readline().strip()
            plus = f.readline()
            qual = f.readline()

            seq_counter[seq] += 1
            total += 1

            if max_reads > 0 and total >= max_reads:
                break

    if total == 0:
        print("[ERROR] No reads found in FASTQ file")
        return

    # 计算重复统计
    unique_seqs = len(seq_counter)
    duplicate_seqs = sum(1 for s, c in seq_counter.items() if c > 1)
    duplicate_reads = sum(c - 1 for s, c in seq_counter.items() if c > 1)
    dup_rate = duplicate_reads / total * 100

    # 重复度分布
    dup_distribution = Counter()
    for seq, count in seq_counter.items():
        dup_distribution[count] += 1

    # 输出
    out_path = output_file or os.path.splitext(fastq_path)[0] + "_duplication.tsv"
    with open(out_path, 'w') as out:
        out.write("# Read Duplication Report\n")
        out.write(f"# Input: {fastq_path}\n")
        out.write(f"Total reads\t{total}\n")
        out.write(f"Unique sequences\t{unique_seqs}\n")
        out.write(f"Duplicate sequences (count>1)\t{duplicate_seqs}\n")
        out.write(f"Duplicate reads\t{duplicate_reads}\n")
        out.write(f"Duplication rate\t{dup_rate:.2f}%\n\n")
        out.write("Duplication_count\tNumber_of_sequences\tFraction_of_reads\n")
        for count in sorted(dup_distribution.keys()):
            n_seqs = dup_distribution[count]
            fraction = count * n_seqs / total * 100
            out.write(f"{count}\t{n_seqs}\t{fraction:.2f}%\n")

    # 绘图
    if make_plot:
        try:
            import matplotlib; matplotlib.use('Agg')
            import matplotlib.pyplot as plt

            # 重复度分布图
            counts_sorted = sorted(dup_distribution.keys())
            max_display = min(max(counts_sorted), 50)

            x = list(range(1, max_display + 1))
            y = [dup_distribution.get(i, 0) for i in x]

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

            # Bar plot of duplication count distribution
            ax1.bar(x, y, color='#2196F3', alpha=0.8)
            ax1.set_xlabel('Duplication count')
            ax1.set_ylabel('Number of sequences')
            ax1.set_title('Sequence duplication distribution')
            ax1.set_yscale('log')

            # Pie chart of unique vs duplicate
            labels = ['Unique', 'Duplicated']
            sizes = [total - duplicate_reads, duplicate_reads]
            colors = ['#4CAF50', '#F44336']
            ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax2.set_title(f'Duplication rate: {dup_rate:.1f}%')

            plt.tight_layout()
            plot_path = os.path.splitext(fastq_path)[0] + "_duplication.png"
            plt.savefig(plot_path, dpi=200)
            plt.close()
            print(f"  Duplication plot: {plot_path}")

        except ImportError:
            print("  [INFO] matplotlib required for duplication plot")

    print(f"Read duplication calculation complete")
    print(f"  Total reads: {total:,}")
    print(f"  Unique sequences: {unique_seqs:,}")
    print(f"  Duplicate reads: {duplicate_reads:,}")
    print(f"  Duplication rate: {dup_rate:.2f}%")
    print(f"  Report: {out_path}")

def main():
    print("=" * 60)
    print("  测序reads重复率统计+分布可视化")
    print("=" * 60)
    fastq_path = get_input("FASTQ文件路径", "input.fastq")
    output = get_input("输出文件路径", "")
    plot = get_input("是否出图(yes/no)", "yes")
    max_reads = get_input("最大读取reads数(0=全部)", "0")
    calculate_read_duplication(fastq_path, output or None,
                               plot.lower() in ('yes', 'y'), int(max_reads))

if __name__ == "__main__":
    main()
