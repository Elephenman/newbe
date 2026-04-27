#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""基因/SNP/特征染色体密度图"""
import os, sys
from collections import defaultdict

def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

def plot_genome_density(filepath, bin_size=100000, circos_style=False, img_format="png"):
    try:
        import matplotlib; matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
    except: print("需要matplotlib+numpy"); return
    
    # 加载坐标
    chr_coords = defaultdict(list)
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#') or line.strip() == '': continue
            fields = line.strip().split('\t')
            if len(fields) >= 3:
                chrom, start, end = fields[0], int(fields[1]), int(fields[2])
                chr_coords[chrom].append((start, end))
    
    # 计算密度
    chr_density = {}
    for chrom, coords in chr_coords.items():
        max_pos = max(c[1] for c in coords)
        bins = int(max_pos / bin_size) + 1
        density = np.zeros(bins)
        for start, end in coords:
            bin_idx = int(start / bin_size)
            density[bin_idx] += 1
        chr_density[chrom] = density
    
    chrs = sorted(chr_density.keys())
    base = os.path.splitext(os.path.basename(filepath))[0]
    
    if circos_style:
        # 简化circos风格(线性排列多染色体)
        fig, axes = plt.subplots(len(chrs), 1, figsize=(14, len(chrs)*1.2), sharex=False)
        if len(chrs) == 1: axes = [axes]
        colors = plt.cm.Set2(len(chrs))
        for i, chrom in enumerate(chrs):
            d = chr_density[chrom]
            x = np.arange(len(d)) * bin_size / 1e6
            axes[i].fill_between(x, d, alpha=0.7, color=colors[i])
            axes[i].set_ylabel(chrom, rotation=0, labelpad=40)
            axes[i].set_xlim(0, x[-1])
        axes[-1].set_xlabel('位置 (Mb)')
        plt.suptitle('基因组特征密度分布 (Circos风格)', fontsize=14)
        plt.tight_layout()
        plt.savefig(f"{base}_density_circos.{img_format}", dpi=300); plt.close()
    else:
        # 线性密度图
        fig, ax = plt.subplots(figsize=(14, 6))
        for i, chrom in enumerate(chrs):
            d = chr_density[chrom]
            x = np.arange(len(d)) * bin_size / 1e6
            ax.plot(x, d, label=chrom, alpha=0.8)
        ax.set_xlabel('位置 (Mb)'); ax.set_ylabel('密度')
        ax.legend(); ax.set_title('基因组特征密度分布')
        plt.tight_layout()
        plt.savefig(f"{base}_density_linear.{img_format}", dpi=300); plt.close()
    
    # 保存密度表
    with open(f"{base}_density.csv", 'w') as out:
        out.write("chrom,bin_start,density\n")
        for chrom in chrs:
            for i, d in enumerate(chr_density[chrom]):
                out.write(f"{chrom},{i*bin_size},{d}\n")
    
    print(f"密度图已保存: {base}_density_{'circos' if circos_style else 'linear'}.{img_format}")
    print(f"密度CSV: {base}_density.csv")
    print(f"染色体数: {len(chrs)}, 总特征数: {sum(len(v) for v in chr_coords.values())}")

def main():
    print("="*50); print("  染色体密度图"); print("="*50)
    fp = get_input("坐标文件路径(BED/TSV)", "regions.bed")
    bs = get_input("bin大小(bp)", 100000, int)
    cs = get_input("是否出circos风格图(yes/no)", "no")
    im = get_input("图片格式(png/pdf)", "png")
    plot_genome_density(fp, bs, cs.lower() in ('yes','y'), im)

if __name__ == "__main__": main()