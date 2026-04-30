#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""K-mer频次统计与差异比较"""
import os, sys
from collections import defaultdict

def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v=="" or v is None: return d
    try: return t(v)
    except: return d

def count_kmers(filepath, k=5, compare_file=None, top_n=20):
    kmers = defaultdict(int); total = 0
    with open(filepath, 'r') as f:
        seq = ""
        for line in f:
            if line.startswith('>'):
                if seq: 
                    for i in range(len(seq)-k+1): kmers[seq[i:i+k]] += 1; total += 1
                seq = ""
            else: seq += line.strip().upper()
        if seq: 
            for i in range(len(seq)-k+1): kmers[seq[i:i+k]] += 1; total += 1
    
    # 排序top N
    sorted_kmers = sorted(kmers.items(), key=lambda x: -x[1])[:top_n]
    print(f"✅ K-mer统计完成: K={k}, 总计数={total}")
    print(f"   Top {top_n} K-mers:")
    for km, cnt in sorted_kmers:
        pct = cnt/total*100
        bar = "█"*min(int(pct*2),50)
        print(f"   {km}: {cnt} ({pct:.2f}%) {bar}")
    
    # 比较
    if compare_file:
        kmers2 = defaultdict(int); total2 = 0
        with open(compare_file, 'r') as f:
            seq = ""
            for line in f:
                if line.startswith('>'):
                    if seq:
                        for i in range(len(seq)-k+1): kmers2[seq[i:i+k]] += 1
                        total2 += len(seq)-k+1
                    seq = ""
                else: seq += line.strip().upper()
            if seq:
                for i in range(len(seq)-k+1): kmers2[seq[i:i+k]] += 1
                total2 += len(seq)-k+1
        
        print(f"\n   🔍 K-mer差异比较:")
        for km, cnt in sorted_kmers[:top_n]:
            cnt2 = kmers2.get(km, 0)
            pct1 = cnt/total*100; pct2 = cnt2/total2*100 if total2 else 0
            diff = pct1 - pct2
            print(f"   {km}: 文件1={pct1:.2f}% 文件2={pct2:.2f}% 差值={diff:+.2f}%")
    
    # 保存CSV
    with open("kmer_counts.csv", 'w') as out:
        out.write("kmer,count,frequency\n")
        for km, cnt in sorted(kmers.items(), key=lambda x: -x[1]):
            out.write(f"{km},{cnt},{cnt/total*100:.4f}\n")
    print(f"   完整结果: kmer_counts.csv")

def main():
    print("="*50); print("  🧮 K-mer频次统计器"); print("="*50)
    fp=get_input("FASTA文件路径","sequences.fasta")
    k=get_input("K值(4/5/6等)",5,int)
    cf=get_input("对比FASTA路径(留空=无对比)","")
    tn=get_input("展示TopN",20,int)
    count_kmers(fp, k, cf or None, tn)
if __name__=="__main__": main()