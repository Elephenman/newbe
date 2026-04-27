#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从GTF/GFF提取指定特征到表格"""
import os, sys, re
from collections import defaultdict

def get_input(prompt, default=None, type=str):
    val = input(f"{prompt} [默认: {default}]: ").strip()
    if val == "" or val is None: return default
    try: return type(val)
    except: return default

def extract_gtf(filepath, feature_type="gene", filter_chr=False, output_format="csv"):
    features = []; chr_counts = defaultdict(int)
    sep = "," if output_format == "csv" else "\t"
    ext = output_format
    out_path = filepath.replace('.gtf','').replace('.gff','') + f'_features.{ext}'
    
    with open(filepath, 'r') as f, open(out_path, 'w') as out:
        out.write(sep.join(["gene_id","chr","start","end","strand","biotype","feature_type"]) + "\n")
        for line in f:
            if line.startswith('#'): continue
            fields = line.strip().split('\t')
            if len(fields) < 9: continue
            chr_, source, ftype, start, end, score, strand, phase, attributes = fields
            if ftype != feature_type: continue
            # 解析属性
            gene_id = re.search(r'gene_id "([^"]+)"', attributes)
            biotype = re.search(r'gene_biotype "([^"]+)"|gene_type "([^"]+)"', attributes)
            gid = gene_id.group(1) if gene_id else "NA"
            bio = (biotype.group(1) or biotype.group(2)) if biotype else "NA"
            
            if filter_chr and not chr_.startswith('chr'): continue
            if filter_chr and chr_ in ['chrM','chrMT']: continue
            
            features.append([gid, chr_, start, end, strand, bio, ftype])
            chr_counts[chr_] += 1
            out.write(sep.join([gid, chr_, start, end, strand, bio, ftype]) + "\n")
    
    print(f"✅ GTF特征提取完成: {out_path}")
    print(f"   提取类型: {feature_type}")
    print(f"   特征数: {len(features)}")
    for c, n in sorted(chr_counts.items())[:10]:
        print(f"   {c}: {n}")

def main():
    print("="*50); print("  🧬 GTF特征提取器"); print("="*50)
    fp = get_input("输入GTF/GFF文件路径", "annotation.gtf")
    ft = get_input("提取类型(gene/exon/CDS/transcript)", "gene")
    fc = get_input("是否过滤非标准染色体(yes/no)", "yes")
    of = get_input("输出格式(csv/tsv)", "csv")
    extract_gtf(fp, ft, fc.lower() in ('yes','y'), of)

if __name__ == "__main__": main()