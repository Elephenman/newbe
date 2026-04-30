#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CNV分段结果可视化"""
import os, sys
from collections import defaultdict

def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

def plot_cnv(filepath, annotate_regions=True, make_heatmap=False, img_format="png"):
    try:
        import matplotlib; matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
    except: print("需要matplotlib+numpy"); return
    
    # 解析CNV结果(支持seg格式和简化CSV)
    segments = []
    with open(filepath, 'r') as f:
        header = f.readline()  # skip header
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) >= 6:
                # seg格式: ID chrom loc.start loc.end num.mark seg.mean
                segments.append({
                    "sample": fields[0], "chr": fields[1],
                    "start": int(fields[2]), "end": int(fields[3]),
                    "mean": float(fields[5]) if len(fields) > 5 else float(fields[4])
                })
            elif len(fields) >= 4:
                # 简化: chr start end mean
                segments.append({
                    "sample": "all", "chr": fields[0],
                    "start": int(fields[1]), "end": int(fields[2]),
                    "mean": float(fields[3])
                })
    
    if not segments: print("无有效数据"); return
    
    # 分类
    gain = sum(1 for s in segments if s["mean"] > 0.1)
    loss = sum(1 for s in segments if s["mean"] < -0.1)
    neutral = len(segments) - gain - loss
    
    # 染色体分布图
    chr_segments = defaultdict(list)
    for s in segments: chr_segments[s["chr"]].append(s)
    
    # Sort chromosomes naturally (chr1, chr2, ..., chr10, chr11, ..., chrX, chrY)
    def chrom_sort_key(c):
        c_clean = c.replace('chr', '').replace('CHR', '').replace('Chr', '')
        if c_clean.isdigit():
            return (0, int(c_clean))
        elif c_clean in ('X', 'x'):
            return (1, 0)
        elif c_clean in ('Y', 'y'):
            return (1, 1)
        elif c_clean in ('M', 'MT', 'm', 'mt'):
            return (2, 0)
        else:
            return (3, 0)
    chrs = sorted(chr_segments.keys(), key=chrom_sort_key)
    fig, ax = plt.subplots(figsize=(14, 6))
    
    colors = {"gain": "#E64B35", "loss": "#4DBBD5", "neutral": "#AAAAAA"}
    for i, chrom in enumerate(chrs):
        for s in chr_segments[chrom]:
            color = colors["gain"] if s["mean"] > 0.1 else colors["loss"] if s["mean"] < -0.1 else colors["neutral"]
            ax.barh(i, (s["end"]-s["start"])/1e6, left=s["start"]/1e6,
                    height=0.8, color=color, alpha=0.7)
    
    ax.set_yticks(range(len(chrs))); ax.set_yticklabels(chrs)
    ax.set_xlabel('位置 (Mb)'); ax.set_title('CNV分布图')
    ax.legend(handles=[plt.Rectangle((0,0),1,1,color=colors["gain"],label="Gain"),
                       plt.Rectangle((0,0),1,1,color=colors["loss"],label="Loss"),
                       plt.Rectangle((0,0),1,1,color=colors["neutral"],label="Neutral")])
    plt.tight_layout()
    plt.savefig(f"cnv_distribution.{img_format}", dpi=300); plt.close()
    
    print(f"CNV可视化完成")
    print(f"  总分段: {len(segments)}")
    print(f"  Gain: {gain}, Loss: {loss}, Neutral: {neutral}")
    print(f"  图: cnv_distribution.{img_format}")
    
    # 保存统计
    with open("cnv_stats.csv", 'w') as out:
        out.write("指标,值\n")
        out.write(f"总分段,{len(segments)}\n")
        out.write(f"Gain,{gain}\n"); out.write(f"Loss,{loss}\n"); out.write(f"Neutral,{neutral}\n")
        for chrom in chrs:
            n = len(chr_segments[chrom])
            out.write(f"{chrom},{n}\n")
    print("统计CSV: cnv_stats.csv")

def main():
    print("="*50); print("  CNV分段可视化"); print("="*50)
    fp = get_input("CNV结果文件路径(seg/CSV)", "cnv_segments.seg")
    ar = get_input("标注关键区域(yes/no)", "yes")
    mh = get_input("是否出热图(yes/no)", "no")
    im = get_input("图片格式(png/pdf)", "png")
    plot_cnv(fp, ar.lower() in ('yes','y'), mh.lower() in ('yes','y'), im)

if __name__ == "__main__": main()