#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SNP/InDel变异统计一键报告"""
import os, sys
from collections import defaultdict

def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

def analyze_vcf(filepath, group_by_chr=True, calc_maf=True, make_plot=False):
    stats = {"total": 0, "snp": 0, "indel": 0, "chr_dist": defaultdict(int),
             "qual_dist": defaultdict(int), "maf_dist": defaultdict(int)}
    alleles_per_site = defaultdict(list)
    
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#'): continue
            fields = line.strip().split('\t')
            if len(fields) < 5: continue
            chrom, pos, id_, ref, alt = fields[:5]
            qual = fields[5]
            
            stats["total"] += 1
            # SNP vs INDEL
            if len(ref) == 1 and len(alt) == 1 and alt != '.':
                stats["snp"] += 1
            else:
                stats["indel"] += 1
            
            if group_by_chr: stats["chr_dist"][chrom] += 1
            
            # QUAL分布(按10分桶)
            q = float(qual) if qual != '.' else 0
            stats["qual_dist"][int(q // 10) * 10] += 1
            
            # MAF计算
            if calc_maf and len(fields) >= 10:
                ref_count = 0; alt_count = 0
                for sample in fields[9:]:
                    if sample == '.' or sample.startswith('./.'): continue
                    gt = sample.split(':')[0]
                    if '/' in gt:
                        for allele in gt.split('/'):
                            if allele == '0': ref_count += 1
                            elif allele == '1': alt_count += 1
                    elif '|' in gt:
                        for allele in gt.split('|'):
                            if allele == '0': ref_count += 1
                            elif allele == '1': alt_count += 1
                total_alleles = ref_count + alt_count
                if total_alleles > 0:
                    maf = min(ref_count, alt_count) / total_alleles
                    maf_bin = round(maf * 10, 1)
                    stats["maf_dist"][maf_bin] += 1
    
    # 报告
    snp_pct = round(stats["snp"] / stats["total"] * 100, 1) if stats["total"] else 0
    indel_pct = round(stats["indel"] / stats["total"] * 100, 1) if stats["total"] else 0
    
    print(f"\n{'='*60}")
    print(f"  SNP/InDel变异统计报告")
    print(f"{'='*60}")
    print(f"  文件: {os.path.basename(filepath)}")
    print(f"  总变异数: {stats['total']}")
    print(f"  SNP: {stats['snp']} ({snp_pct}%)")
    print(f"  INDEL: {stats['indel']} ({indel_pct}%)")
    
    if group_by_chr:
        print(f"\n  【染色体分布】")
        for chrom in sorted(stats["chr_dist"].keys()):
            cnt = stats["chr_dist"][chrom]
            bar = "#" * min(int(cnt / stats["total"] * 100), 50)
            print(f"    {chrom}: {cnt} ({round(cnt/stats['total']*100,1)}%) {bar}")
    
    if calc_maf and stats["maf_dist"]:
        print(f"\n  【MAF分布】")
        for maf_bin in sorted(stats["maf_dist"].keys()):
            cnt = stats["maf_dist"][maf_bin]
            print(f"    MAF {maf_bin:.1f}-{(maf_bin+0.1):.1f}: {cnt}")
        # LD50
        sorted_maf = sorted(stats["maf_dist"].keys())
        cumulative = 0
        for m in sorted_maf:
            cumulative += stats["maf_dist"][m]
            if cumulative >= stats["total"] * 0.5:
                print(f"    MAF50 ≈ {m:.1f}")
                break
    
    # QUAL分布
    print(f"\n  【QUAL分布】")
    for q_bin in sorted(stats["qual_dist"].keys()):
        cnt = stats["qual_dist"][q_bin]
        print(f"    QUAL {q_bin}-{q_bin+9}: {cnt}")
    
    # 绘图
    if make_plot:
        try:
            import matplotlib; matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            
            # 染色体分布图
            if group_by_chr:
                chrs = sorted(stats["chr_dist"].keys())
                counts = [stats["chr_dist"][c] for c in chrs]
                plt.figure(figsize=(12, 5))
                plt.bar(range(len(chrs)), counts, color='#2196F3')
                plt.xticks(range(len(chrs)), chrs, rotation=45)
                plt.ylabel('变异数'); plt.title('染色体变异分布')
                plt.tight_layout()
                plt.savefig("snp_chr_distribution.png", dpi=300); plt.close()
                print(f"  染色体分布图: snp_chr_distribution.png")
            
            # SNP/INDEL比例饼图
            plt.figure(figsize=(6, 6))
            plt.pie([stats["snp"], stats["indel"]], labels=["SNP", "INDEL"],
                    colors=["#E64B35", "#4DBBD5"], autopct='%1.1f%%')
            plt.title("SNP vs INDEL"); plt.savefig("snp_type_pie.png", dpi=300); plt.close()
            print(f"  类型饼图: snp_type_pie.png")
        except: print("  需要matplotlib出图")
    
    # 保存CSV
    with open("snp_stats_report.csv", 'w') as out:
        out.write("指标,值\n")
        out.write(f"总变异数,{stats['total']}\n")
        out.write(f"SNP,{stats['snp']} ({snp_pct}%)\n")
        out.write(f"INDEL,{stats['indel']} ({indel_pct}%)\n")
        for chrom, cnt in sorted(stats["chr_dist"].items()):
            out.write(f"{chrom},{cnt}\n")
    print(f"\n  统计CSV: snp_stats_report.csv")
    print(f"{'='*60}")

def main():
    print("="*50); print("  SNP/InDel变异统计报告"); print("="*50)
    fp = get_input("VCF文件路径", "variants.vcf")
    gc = get_input("是否按染色体分组(yes/no)", "yes")
    mf = get_input("是否计算MAF(yes/no)", "yes")
    mp = get_input("是否出图(yes/no)", "no")
    analyze_vcf(fp, gc.lower() in ('yes','y'), mf.lower() in ('yes','y'), mp.lower() in ('yes','y'))

if __name__ == "__main__": main()