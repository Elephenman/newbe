#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""VCF变异过滤+注释格式化"""
import os, sys, re
from collections import defaultdict

def get_input(prompt, default=None, type=str):
    val = input(f"{prompt} [默认: {default}]: ").strip()
    if val == "" or val is None: return default
    try: return type(val)
    except: return default

def filter_vcf(filepath, min_qual=30, min_dp=10, max_missing=0.5, keep_indel=True, output_format="tsv"):
    stats = {"total":0,"snp":0,"indel":0,"kept":0,"filtered":0,"chr_dist":defaultdict(int)}
    out_path = filepath.replace('.vcf','') + f'_filtered.{output_format}'
    
    with open(filepath, 'r') as f, open(out_path, 'w') as out:
        for line in f:
            if line.startswith('#'):
                if output_format == 'vcf': out.write(line)
                continue
            fields = line.strip().split('\t')
            if len(fields) < 8: continue
            stats["total"] += 1
            chrom, pos, id_, ref, alt, qual, filter_, info = fields[:8]
            
            # 变异类型
            is_indel = len(ref) > 1 or len(alt) > 1 or alt == '.'
            if is_indel: stats["indel"] += 1
            else: stats["snp"] += 1
            
            # 过滤
            q_val = float(qual) if qual != '.' else 0
            dp_val = 0
            dp_match = re.search(r'DP=(\d+)', info)
            if dp_match: dp_val = int(dp_match.group(1))
            
            # 缺失率（从样本列计算）
            missing = 0; total_samples = 0
            for s in fields[9:]:
                total_samples += 1
                if s == '.' or s.startswith('./.') : missing += 1
            miss_rate = missing/total_samples if total_samples > 0 else 0
            
            if q_val < min_qual or dp_val < min_dp or miss_rate > max_missing or (not keep_indel and is_indel):
                stats["filtered"] += 1
                continue
            
            stats["kept"] += 1
            stats["chr_dist"][chrom] += 1
            
            if output_format == 'vcf':
                out.write(line)
            else:
                out.write(f"{chrom}\t{pos}\t{id_}\t{ref}\t{alt}\t{qual}\t{dp_val}\t{'INDEL' if is_indel else 'SNP'}\n")
    
    print(f"✅ VCF过滤完成: {out_path}")
    print(f"   总变异数: {stats['total']}")
    print(f"   保留: {stats['kept']} (SNP:{stats['snp']-stats['filtered']}, INDEL:{stats['indel']})")
    print(f"   丢弃: {stats['filtered']}")

def main():
    print("="*50); print("  🔬 VCF变异过滤器"); print("="*50)
    fp = get_input("输入VCF文件路径", "variants.vcf")
    mq = get_input("最小QUAL阈值", 30, int)
    md = get_input("最小DP阈值", 10, int)
    mm = get_input("最大缺失率", 0.5, float)
    ki = get_input("是否保留INDEL(yes/no)", "yes")
    of = get_input("输出格式(vcf/tsv)", "tsv")
    filter_vcf(fp, mq, md, mm, ki.lower() in ('yes','y'), of)

if __name__ == "__main__": main()