#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从参考基因组按坐标切片提取序列"""
import os, sys

def get_input(prompt, default=None, type=str):
    val = input(f"{prompt} [默认: {default}]: ").strip()
    if val == "" or val is None: return default
    try: return type(val)
    except: return default

def parse_bed(bed_path):
    coords = []
    with open(bed_path, 'r') as f:
        for line in f:
            if line.startswith('#') or line.strip() == '': continue
            fields = line.strip().split('\t')
            if len(fields) >= 3:
                coords.append((fields[0], int(fields[1]), int(fields[2]), fields[3] if len(fields)>3 else f"{fields[0]}:{fields[1]}-{fields[2]}"))
    return coords

def slice_genome(fasta_path, coords, flank=0, output_path=None):
    # 简单FASTA索引（内存映射方式）
    genome = {}; current_chr = None; current_seq = []
    with open(fasta_path, 'r') as f:
        for line in f:
            if line.startswith('>'):
                if current_chr: genome[current_chr] = ''.join(current_seq)
                current_chr = line.strip()[1:].split()[0]
                current_seq = []
            else: current_seq.append(line.strip())
    if current_chr: genome[current_chr] = ''.join(current_seq)
    
    out_path = output_path or "genome_slices.fasta"
    with open(out_path, 'w') as out:
        for chrom, start, end, name in coords:
            if chrom not in genome:
                print(f"  ⚠ {chrom} 不在参考基因组中，跳过")
                continue
            seq_len = len(genome[chrom])
            s = max(0, start - flank); e = min(seq_len, end + flank)
            seq = genome[chrom][s:e]
            out.write(f">{name} {chrom}:{s}-{e}\n{seq}\n")
    
    print(f"✅ 切片完成: {out_path} ({len(coords)} 个区域)")

def main():
    print("="*50); print("  🧬 基因组序列切片器"); print("="*50)
    fp = get_input("参考基因组FASTA路径", "genome.fa")
    bp = get_input("坐标文件路径(BED/TSV)", "regions.bed")
    fl = get_input("上下游flank长度(bp)", 0, int)
    op = get_input("输出FASTA路径", "genome_slices.fasta")
    coords = parse_bed(bp)
    slice_genome(fp, coords, fl, op)

if __name__ == "__main__": main()