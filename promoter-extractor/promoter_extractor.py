#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量提取基因启动子序列+TSS注释"""
import os, sys, re
from collections import defaultdict

def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

def extract_promoters(gene_file, fasta_path, gtf_path, upstream=2000, downstream=500, filter_overlap=True):
    # 加载基因组
    genome = {}; current_chr = None; current_seq = []
    with open(fasta_path, 'r') as f:
        for line in f:
            if line.startswith('>'):
                if current_chr: genome[current_chr] = ''.join(current_seq)
                current_chr = line.strip()[1:].split()[0]; current_seq = []
            else: current_seq.append(line.strip().upper())
    if current_chr: genome[current_chr] = ''.join(current_seq)
    
    # 加载基因列表
    target_genes = set()
    with open(gene_file, 'r') as f:
        for line in f: target_genes.add(line.strip().upper())
    
    # 解析GTF获取TSS
    gene_info = {}
    with open(gtf_path, 'r') as f:
        for line in f:
            if line.startswith('#'): continue
            fields = line.strip().split('\t')
            if len(fields) < 9 or fields[2] != 'gene': continue
            chrom, start, end, strand = fields[0], int(fields[3]), int(fields[4]), fields[6]
            # 提取基因名
            name_match = re.search(r'gene_name "([^"]+)"', fields[8])
            if not name_match: name_match = re.search(r'gene_id "([^"]+)"', fields[8])
            gene_name = name_match.group(1) if name_match else ""
            
            if gene_name.upper() not in target_genes: continue
            
            tss = start if strand == '+' else end  # TSS位置
            gene_info[gene_name] = {"chr": chrom, "tss": tss, "strand": strand,
                                     "start": start, "end": end}
    
    # 提取启动子
    out_path = "promoter_sequences.fasta"
    stats_path = "promoter_coordinates.csv"
    extracted = 0; skipped = 0
    
    with open(out_path, 'w') as out_f, open(stats_path, 'w') as out_s:
        out_s.write("gene,chr,tss,strand,promoter_start,promoter_end,length\n")
        
        for gene_name, info in gene_info.items():
            chrom = info["chr"]; tss = info["tss"]; strand = info["strand"]
            seq_len = len(genome.get(chrom, ""))
            
            if strand == '+':
                p_start = max(0, tss - upstream)
                p_end = min(seq_len, tss + downstream)
            else:
                p_start = max(0, tss - downstream)
                p_end = min(seq_len, tss + upstream)
            
            if chrom not in genome:
                skipped += 1; continue
            
            seq = genome[chrom][p_start:p_end]
            if len(seq) < 10:
                skipped += 1; continue
            
            # 反向互补（如果基因在负链）
            if strand == '-':
                complement = {'A':'T','T':'A','G':'C','C':'G','N':'N'}
                seq = ''.join(complement.get(c, 'N') for c in reversed(seq))
            
            out_f.write(f">{gene_name} {chrom}:{p_start}-{p_end} strand={strand}\n{seq}\n")
            out_s.write(f"{gene_name},{chrom},{tss},{strand},{p_start},{p_end},{len(seq)}\n")
            extracted += 1
    
    print(f"启动子提取完成")
    print(f"  目标基因数: {len(target_genes)}")
    print(f"  成功提取: {extracted}")
    print(f"  跳过: {skipped}")
    print(f"  上游: {upstream}bp, 下游: {downstream}bp")
    print(f"  FASTA: {out_path}")
    print(f"  坐标表: {stats_path}")
    
    missing = target_genes - set(g.upper() for g in gene_info.keys())
    if missing: print(f"  未找到基因: {', '.join(list(missing)[:10])}")

def main():
    print("="*50); print("  启动子提取器"); print("="*50)
    gf = get_input("基因列表文件路径", "gene_list.txt")
    ff = get_input("参考基因组FASTA路径", "genome.fa")
    gtf = get_input("GTF注释路径", "annotation.gtf")
    up = get_input("上游长度(bp)", 2000, int)
    dn = get_input("下游长度(bp)", 500, int)
    fo = get_input("过滤重叠(yes/no)", "yes")
    extract_promoters(gf, ff, gtf, up, dn, fo.lower() in ('yes','y'))

if __name__ == "__main__": main()