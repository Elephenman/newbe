#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hi-C接触矩阵可视化+TAD标注"""
import os, sys
from collections import defaultdict

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def map_hic_contacts(matrix_file, resolution=10000, output_file=None, make_plot=True, tad_file=None):
    """可视化Hi-C接触矩阵

    输入格式1 (dense matrix): 行列为genomic bins, 值为接触频率
    输入格式2 (sparse): chr1,pos1,chr2,pos2,count
    """
    try:
        import numpy as np
        import matplotlib; matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("[ERROR] Requires numpy and matplotlib")
        return

    # 检测文件格式并读取
    with open(matrix_file, 'r') as f:
        first_line = f.readline().strip()
        f.seek(0)

        if first_line.startswith('#') or ',' in first_line:
            # Sparse format: chr1,start1,chr2,start2,count
            contacts = defaultdict(lambda: defaultdict(float))
            bins = set()
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                fields = line.replace(',', '\t').split('\t')
                if len(fields) >= 5:
                    try:
                        bin1 = f"{fields[0]}:{int(fields[1])//resolution}"
                        bin2 = f"{fields[2]}:{int(fields[3])//resolution}"
                        count = float(fields[4])
                        contacts[bin1][bin2] = count
                        contacts[bin2][bin1] = count
                        bins.add(bin1)
                        bins.add(bin2)
                    except (ValueError, IndexError):
                        continue

            if not bins:
                print("[ERROR] No valid contacts found in sparse format")
                return

            sorted_bins = sorted(bins)
            bin_idx = {b: i for i, b in enumerate(sorted_bins)}
            n = len(sorted_bins)
            matrix = np.zeros((n, n))
            for b1 in sorted_bins:
                for b2, count in contacts[b1].items():
                    if b2 in bin_idx:
                        matrix[bin_idx[b1]][bin_idx[b2]] = count
            bin_labels = sorted_bins

        else:
            # Dense matrix format
            rows = []
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                fields = line.split('\t') if '\t' in line else line.split()
                try:
                    rows.append([float(x) for x in fields])
                except ValueError:
                    continue
            if not rows:
                print("[ERROR] No valid matrix data found")
                return
            matrix = np.array(rows)
            n = matrix.shape[0]
            bin_labels = [f"bin_{i}" for i in range(n)]

    # Log transform for visualization
    matrix_log = np.log1p(matrix)

    # 绘图
    if make_plot:
        fig, ax = plt.subplots(figsize=(10, 10))
        im = ax.imshow(matrix_log, cmap='Reds', aspect='auto', interpolation='nearest')
        plt.colorbar(im, ax=ax, label='Log(contact+1)')

        # TAD边界标注
        if tad_file and os.path.exists(tad_file):
            with open(tad_file, 'r') as tf:
                for line in tf:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    fields = line.split('\t')
                    if len(fields) >= 3:
                        try:
                            tad_start = int(fields[1]) // resolution
                            tad_end = int(fields[2]) // resolution
                            rect = plt.Rectangle((tad_start, tad_start),
                                                tad_end - tad_start, tad_end - tad_start,
                                                fill=False, edgecolor='blue', linewidth=1.5)
                            ax.add_patch(rect)
                        except (ValueError, IndexError):
                            continue

        ax.set_xlabel('Genomic bin')
        ax.set_ylabel('Genomic bin')
        ax.set_title(f'Hi-C Contact Map (resolution={resolution})')
        plt.tight_layout()

        plot_path = os.path.splitext(matrix_file)[0] + "_hic_map.png"
        plt.savefig(plot_path, dpi=200)
        plt.close()
        print(f"  Contact map: {plot_path}")

    # 保存处理后的矩阵
    out_path = output_file or os.path.splitext(matrix_file)[0] + "_normalized.tsv"
    with open(out_path, 'w') as out:
        out.write("\t".join(bin_labels) + "\n")
        for i in range(matrix.shape[0]):
            out.write("\t".join(f"{matrix[i][j]:.4f}" for j in range(matrix.shape[1])) + "\n")

    print(f"Hi-C contact mapping complete")
    print(f"  Matrix size: {matrix.shape[0]}x{matrix.shape[1]}")
    print(f"  Resolution: {resolution}bp")
    print(f"  Total contacts: {np.sum(matrix):.0f}")
    if tad_file:
        print(f"  TAD annotations: {tad_file}")
    print(f"  Normalized matrix: {out_path}")

def main():
    print("=" * 60)
    print("  Hi-C接触矩阵可视化+TAD标注")
    print("=" * 60)
    matrix_file = get_input("接触矩阵文件路径", "hic_contacts.tsv")
    resolution = get_input("分辨率(bp)", "10000")
    output = get_input("输出文件路径", "")
    plot = get_input("是否出图(yes/no)", "yes")
    tad = get_input("TAD边界文件路径(可选)", "")
    map_hic_contacts(matrix_file, int(resolution), output or None,
                     plot.lower() in ('yes', 'y'), tad or None)

if __name__ == "__main__":
    main()
