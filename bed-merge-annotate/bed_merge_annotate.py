#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BED文件合并+区间注释"""
import os, sys
from collections import defaultdict

def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v=="" or v is None: return d
    try: return t(v)
    except: return d

def merge_bed(filepath, merge_dist=0, gtf_file=None, output_format="bed"):
    # 解析BED
    intervals = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#') or line.strip()=='': continue
            fields = line.strip().split('\t')
            if len(fields) >= 3:
                intervals.append((fields[0], int(fields[1]), int(fields[2]), fields[3] if len(fields)>3 else '.'))
    
    # 按染色体排序+贪心合并
    intervals.sort(key=lambda x: (x[0], x[1]))
    merged = []; current = None
    for iv in intervals:
        if current is None: current = iv; continue
        if iv[0] == current[0] and iv[1] <= current[2] + merge_dist:
            current = (current[0], current[1], max(current[2], iv[2]), current[3])
        else:
            merged.append(current); current = iv
    if current: merged.append(current)
    
    # GTF注释（可选）
    annotations = {}
    if gtf_file and os.path.exists(gtf_file):
        genes = []
        with open(gtf_file, 'r') as f:
            for line in f:
                if line.startswith('#'): continue
                fields = line.strip().split('\t')
                if len(fields) < 9: continue
                if fields[2] == 'gene':
                    import re
                    name = re.search(r'gene_name "([^"]+)"', fields[8])
                    gname = name.group(1) if name else fields[8].split(';')[0]
                    genes.append((fields[0], int(fields[3]), int(fields[4]), gname))
        
        for iv in merged:
            overlap_genes = []
            for g in genes:
                if g[0] == iv[0] and g[1] < iv[2] and g[2] > iv[1]:
                    overlap_genes.append(g[3])
            annotations[iv] = overlap_genes
    
    # 输出
    sep = '\t' if output_format == 'bed' else ','
    out_path = filepath.replace('.bed','') + '_merged.bed'
    with open(out_path, 'w') as out:
        for iv in merged:
            line = sep.join([str(x) for x in iv[:4]])
            if gtf_file and iv in annotations:
                line += sep + '|'.join(annotations[iv])
            out.write(line + '\n')
    
    print(f"✅ BED合并完成: {out_path}")
    print(f"   原始区间: {len(intervals)}, 合并后: {len(merged)}")
    if annotations:
        annotated = sum(1 for v in annotations.values() if v)
        print(f"   有基因注释: {annotated}")

def main():
    print("="*50); print("  🧬 BED合并+注释"); print("="*50)
    fp=get_input("BED文件路径","regions.bed")
    md=get_input("合并距离阈值(bp)",0,int)
    gf=get_input("注释GTF路径(留空=无)","")
    of=get_input("输出格式(bed/csv)","bed")
    merge_bed(fp, md, gf or None, of)
if __name__=="__main__": main()