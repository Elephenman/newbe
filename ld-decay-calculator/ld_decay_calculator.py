#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LD衰减曲线计算与绘图"""
import os, sys
from collections import defaultdict

def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

def calc_ld_decay(filepath, max_distance_kb=500, r2_threshold=0.2, make_plot=True):
    try:
        import matplotlib; matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
    except: print("需要matplotlib+numpy"); return
    
    # 解析VCF获取SNP位置和allele
    snps = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#'): continue
            fields = line.strip().split('\t')
            if len(fields) < 10: continue
            ref = fields[3]; alt = fields[4]
            if len(ref) > 1 or len(alt) > 1: continue  # 只取SNP
            # 提取样本allele
            alleles = []
            for sample in fields[9:]:
                if sample == '.' or sample.startswith('./.'): continue
                gt = sample.split(':')[0].replace('|','/')
                for a in gt.split('/'):
                    alleles.append(int(a) if a != '.' else 0)
            snps.append({"chr": fields[0], "pos": int(fields[2] if fields[2] != '.' else fields[1]),
                         "ref": ref, "alt": alt, "alleles": alleles})
    
    if len(snps) < 10:
        print("SNP数量太少，无法计算LD"); return
    
    # 按染色体分组计算LD
    chr_groups = defaultdict(list)
    for s in snps: chr_groups[s["chr"]].append(s)
    
    ld_values = defaultdict(list)  # distance -> list of r2
    
    for chrom, group in chr_groups.items():
        group.sort(key=lambda x: x["pos"])
        # 计算pairwise LD
        for i in range(min(len(group), 200)):  # 限制计算量
            for j in range(i+1, min(len(group), i+50)):
                dist = abs(group[j]["pos"] - group[i]["pos"])
                if dist > max_distance_kb * 1000: continue
                
                a1 = group[i]["alleles"]; a2 = group[j]["alleles"]
                if len(a1) != len(a2) or len(a1) < 2: continue

                # Proper r^2 calculation from genotype dosages
                # Using dosage (0,1,2) representation for correlation
                # Each allele list contains 0/1 for each haplotype
                # Convert to dosage per individual
                n_hap = len(a1)
                n_ind = n_hap // 2
                if n_ind < 2: continue

                # Compute allele frequencies
                n = len(a1)
                pA = sum(a1) / n if n > 0 else 0
                pB = sum(a2) / n if n > 0 else 0

                if pA == 0 or pA == 1 or pB == 0 or pB == 1:
                    continue  # Monomorphic site

                # Compute haplotype frequencies
                n_AB = n_aB = n_Ab = n_ab = 0
                for k in range(n):
                    if a1[k] == 1 and a2[k] == 1: n_AB += 1
                    elif a1[k] == 0 and a2[k] == 1: n_aB += 1
                    elif a1[k] == 1 and a2[k] == 0: n_Ab += 1
                    else: n_ab += 1

                pAB = n_AB / n
                D = pAB - pA * pB
                denom = pA * (1-pA) * pB * (1-pB)
                r2 = D*D / denom if denom > 0 else 0
                r2 = min(max(r2, 0), 1)
                
                dist_kb = dist / 1000
                ld_values[dist_kb].append(r2)
    
    # 平均LD
    avg_ld = {}
    for dist, vals in ld_values.items():
        avg_ld[dist] = np.mean(vals)
    
    # 找LD50
    sorted_distances = sorted(avg_ld.keys())
    ld50 = None
    for d in sorted_distances:
        if avg_ld[d] < r2_threshold:
            ld50 = d; break
    
    # 绘图
    if make_plot and avg_ld:
        dists = sorted(avg_ld.keys())
        r2s = [avg_ld[d] for d in dists]
        
        plt.figure(figsize=(10, 6))
        plt.plot(dists, r2s, 'b-', linewidth=2, alpha=0.7)
        plt.axhline(y=r2_threshold, color='r', linestyle='--', label=f'r²={r2_threshold}')
        if ld50: plt.axvline(x=ld50, color='g', linestyle='--', label=f'LD50={ld50:.0f}kb')
        plt.xlabel('距离 (kb)', fontsize=12)
        plt.ylabel('r²', fontsize=12)
        plt.title('LD衰减曲线', fontsize=14)
        plt.legend(); plt.tight_layout()
        plt.savefig("ld_decay_curve.png", dpi=300); plt.close()
        print("LD衰减图: ld_decay_curve.png")
    
    # 报告
    print(f"LD衰减计算完成")
    print(f"  SNP数: {len(snps)}")
    print(f"  最大距离: {max_distance_kb}kb")
    print(f"  LD50距离: {ld50:.0f}kb (r²衰减到{r2_threshold}的距离)" if ld50 else "  LD50: 未检测到")
    
    # 保存
    with open("ld_decay_values.csv", 'w') as out:
        out.write("distance_kb,mean_r2\n")
        for d in sorted(avg_ld.keys()):
            out.write(f"{d},{avg_ld[d]:.4f}\n")
    print("LD值CSV: ld_decay_values.csv")

def main():
    print("="*50); print("  LD衰减曲线"); print("="*50)
    fp = get_input("VCF文件路径", "variants.vcf")
    md = get_input("最大距离(kb)", 500, int)
    rt = get_input("r2阈值", 0.2, float)
    mp = get_input("是否出图(yes/no)", "yes")
    calc_ld_decay(fp, md, rt, mp.lower() in ('yes','y'))

if __name__ == "__main__": main()