#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从VCF提取突变特征(SBS96谱)并可视化"""
import os, sys, csv
from collections import defaultdict

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def extract_sbs96(input_vcf, ref_fasta=None, output_plot=None, output_file=None):
    """从VCF提取SBS96突变特征谱

    如果提供参考基因组FASTA，则计算完整的SBS96（含trinucleotide context）
    否则计算SBS6（6种碱基替换类型）的简化版
    """
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    bases = ["A","C","G","T"]
    pyrimidine_subs = ["CA","CG","CT","TA","TC","TG"]

    # 初始化SBS96计数
    sbs96 = {}
    for sub in pyrimidine_subs:
        for b5 in bases:
            for b3 in bases:
                sbs96[f"{b5}[{sub}]{b3}"] = 0

    # 如果有参考基因组，加载它
    genome = None
    if ref_fasta and os.path.exists(ref_fasta):
        print("Loading reference genome for trinucleotide context...")
        genome = {}; current_chr = None; current_seq = []
        with open(ref_fasta, 'r') as f:
            for line in f:
                if line.startswith('>'):
                    if current_chr: genome[current_chr] = ''.join(current_seq)
                    current_chr = line.strip()[1:].split()[0]; current_seq = []
                else: current_seq.append(line.strip().upper())
        if current_chr: genome[current_chr] = ''.join(current_seq)

    complement = {"A":"T","T":"A","C":"G","G":"C"}
    total_variants = 0

    with open(input_vcf) as f:
        for line in f:
            if line.startswith("#"): continue
            p = line.strip().split("\t")
            if len(p) < 5: continue
            chrom = p[0]
            pos = int(p[1]) if p[1].isdigit() else int(p[2]) if p[2] != '.' else 0
            ref, alt = p[3].upper(), p[4].upper()
            if len(ref) != 1 or len(alt) != 1: continue

            total_variants += 1

            # 规范化到嘧啶上下文
            r, a = ref, alt
            is_complemented = False
            if (r, a) in [("A","C"),("A","G"),("A","T"),("G","A"),("G","C"),("G","T")]:
                r, a = complement[a], complement[r]
                is_complemented = True

            sub_key = f"{r}{a}"

            # 获取trinucleotide context
            if genome and chrom in genome and pos > 0:
                seq = genome[chrom]
                # VCF uses 1-based coordinates
                idx = pos - 1  # 0-based index
                if idx > 0 and idx < len(seq) - 1:
                    if is_complemented:
                        # Get complement of flanking bases
                        b5 = complement.get(seq[idx - 1], 'N')
                        b3 = complement.get(seq[idx + 1], 'N')
                    else:
                        b5 = seq[idx - 1]
                        b3 = seq[idx + 1]

                    ctx = f"{b5}[{sub_key}]{b3}"
                    if ctx in sbs96:
                        sbs96[ctx] += 1
                    else:
                        # Unknown context, still count
                        sbs96[ctx] = sbs96.get(ctx, 0) + 1
            else:
                # No reference: use SBS6 (just substitution type without context)
                # Store in N[XY]N placeholder
                ctx = f"N[{sub_key}]N"
                sbs96[ctx] = sbs96.get(ctx, 0) + 1

    # 准备绘图数据
    cats = list(sbs96.keys())
    vals = [sbs96[c] for c in cats]

    # 绘图
    out_plot = output_plot or "sbs96.png"
    fig, ax = plt.subplots(figsize=(15, 4))

    # SBS96颜色方案: C>T蓝色, C>A红色, C>G黄色, T>A灰色, T>C绿色, T>G粉色
    color_map = {
        "[CA]": "#1a9850", "[CG]": "#fee08b", "[CT]": "#3288bd",
        "[TA]": "#999999", "[TC]": "#66c2a5", "[TG]": "#d53e4f"
    }
    colors = []
    for c in cats:
        found = False
        for key, color in color_map.items():
            if key in c:
                colors.append(color)
                found = True
                break
        if not found:
            colors.append("#999999")

    ax.bar(range(len(cats)), vals, color=colors)
    ax.set_xlabel("SBS96 Context" if genome else "SBS6 Substitution Type")
    ax.set_ylabel("Count")
    ax.set_title(f"SBS96 Spectrum (n={total_variants} SNVs)" if genome else f"SBS6 Substitution Spectrum (n={total_variants} SNVs)")
    if len(cats) > 30:
        ax.set_xticks(range(0, len(cats), 16))
    plt.tight_layout()
    plt.savefig(out_plot, dpi=150)
    plt.close()

    # 保存CSV
    out_csv = output_file or "sbs96_counts.csv"
    with open(out_csv, "w", newline="") as out:
        w = csv.writer(out); w.writerow(["Context","Count"])
        for c, v in zip(cats, vals): w.writerow([c, v])

    print(f"SBS spectrum extraction complete")
    print(f"  Total SNVs: {total_variants}")
    print(f"  Context: {'SBS96 (trinucleotide)' if genome else 'SBS6 (substitution only, provide --ref for SBS96)'}")
    print(f"  Plot: {out_plot}")
    print(f"  CSV: {out_csv}")

def main():
    input_vcf = get_input("输入VCF文件路径", "somatic.vcf")
    ref_fasta = get_input("参考基因组FASTA路径(可选，留空=SBS6)", "")
    output_plot = get_input("输出SBS谱图片路径", "sbs96.png")
    output_file = get_input("输出SBS计数CSV", "sbs96_counts.csv")
    extract_sbs96(input_vcf, ref_fasta or None, output_plot, output_file)

if __name__ == "__main__":
    main()
