#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""K-mer频率估算基因组大小+杂合度"""
import os, sys
from collections import defaultdict

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def estimate_genome_size(kmer_hist_file, k=21, output_file=None):
    """从k-mer频率直方图估算基因组大小和杂合度

    输入文件格式: kmer_count\tfrequency (如Jellyfish histogram输出)
    或 FASTQ文件直接计算k-mer
    """
    hist = {}  # count -> frequency

    # 检测输入文件类型
    with open(kmer_hist_file, 'r') as f:
        first_line = f.readline().strip()
        f.seek(0)

        if first_line.startswith('@') or first_line.startswith('>'):
            # FASTQ/FASTA输入 -> 直接计算k-mer
            print("Detected FASTQ/FASTA input, computing k-mer frequencies...")
            kmers = defaultdict(int)
            seq = ""
            total_bases = 0
            for line in f:
                if line.startswith('@') or line.startswith('>'):
                    # Process previous sequence
                    if seq:
                        for i in range(len(seq) - k + 1):
                            kmer = seq[i:i+k]
                            if 'N' not in kmer:
                                kmers[kmer] += 1
                    seq = ""
                    if line.startswith('@'):
                        # FASTQ: skip quality lines
                        next(f); next(f)  # skip sequence and +
                    continue
                elif line.startswith('+') and len(line.strip()) == 1:
                    next(f)  # skip quality
                    continue
                else:
                    seq += line.strip().upper()

            # Process last sequence
            if seq:
                for i in range(len(seq) - k + 1):
                    kmer = seq[i:i+k]
                    if 'N' not in kmer:
                        kmers[kmer] += 1

            # Build histogram
            for kmer, count in kmers.items():
                hist[count] = hist.get(count, 0) + 1
            total_bases = sum(len(kmer) * count for kmer, count in kmers.items())
        else:
            # Histogram file (count\tfrequency)
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                fields = line.split()
                if len(fields) >= 2:
                    try:
                        count = int(fields[0])
                        freq = int(float(fields[1]))
                        hist[count] = freq
                    except ValueError:
                        continue

    if not hist:
        print("[ERROR] No k-mer data found in input file")
        return

    # 找主峰 (排除低频k-mer噪声)
    max_count = max(hist.keys())
    peak_count = 0
    peak_freq = 0
    for count in range(2, max_count + 1):
        if hist.get(count, 0) > peak_freq:
            peak_freq = hist[count]
            peak_count = count

    if peak_count == 0:
        print("[ERROR] Could not identify k-mer peak")
        return

    # 估算基因组大小
    # Total unique k-mers / peak_coverage
    total_kmers = sum(count * freq for count, freq in hist.items())
    genome_size = total_kmers / peak_count if peak_count > 0 else 0

    # 估算杂合度 (简化方法)
    # 杂合度 h 使得 (1-h)^k = 主峰比例
    # 这里用主峰和半峰的比例粗估
    half_peak_count = peak_count // 2
    half_peak_freq = hist.get(half_peak_count, 0)

    heterozygosity = 0.0
    if half_peak_freq > 0 and peak_freq > 0:
        ratio = half_peak_freq / peak_freq
        # 粗略估计: 杂合度导致半峰
        import math
        try:
            heterozygosity = -math.log(max(ratio, 0.001)) / k * 0.1
            heterozygosity = min(heterozygosity, 0.1)
        except:
            heterozygosity = 0.0

    # 输出
    out_path = output_file or os.path.splitext(kmer_hist_file)[0] + "_genome_size.txt"
    with open(out_path, 'w') as out:
        out.write(f"# Genome Size Estimation (k={k})\n")
        out.write(f"# Input: {kmer_hist_file}\n")
        out.write(f"Estimated genome size: {genome_size:.0f} bp ({genome_size/1e6:.2f} Mb)\n")
        out.write(f"K-mer peak coverage: {peak_count}\n")
        out.write(f"Total k-mers: {total_kmers}\n")
        out.write(f"Unique k-mers: {sum(hist.values())}\n")
        out.write(f"Estimated heterozygosity: {heterozygosity:.4f}\n")
        out.write(f"\n# K-mer histogram\n")
        out.write("count\tfrequency\n")
        for count in sorted(hist.keys()):
            out.write(f"{count}\t{hist[count]}\n")

    print(f"Genome size estimation complete (k={k})")
    print(f"  Estimated genome size: {genome_size/1e6:.2f} Mb ({genome_size:.0f} bp)")
    print(f"  K-mer peak coverage: {peak_count}x")
    print(f"  Total k-mers: {total_kmers:,}")
    print(f"  Unique k-mers: {sum(hist.values()):,}")
    print(f"  Estimated heterozygosity: {heterozygosity:.4f}")
    print(f"  Output: {out_path}")

def main():
    print("=" * 60)
    print("  K-mer频率估算基因组大小+杂合度")
    print("=" * 60)
    input_file = get_input("K-mer频率直方图或FASTQ文件路径", "kmer.hist")
    k_val = get_input("K值", "21")
    output = get_input("输出文件路径", "")
    estimate_genome_size(input_file, int(k_val), output or None)

if __name__ == "__main__":
    main()
