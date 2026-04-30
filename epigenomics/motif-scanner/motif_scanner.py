#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DNA序列motif扫描"""
import os, sys, re
from collections import defaultdict

def get_input(p, d=None, t=str):
    v = input(f"{p} [默认: {d}]: ").strip()
    if v == "" or v is None: return d
    try: return t(v)
    except: return d

# JASPAR核心motif库(简化版)
JASPAR_MOTIFS = {
    "TF_AP1": ["TGASTCA", "TGAGTCA", "TGACTCA"],  # AP-1
    "TF_SP1": ["GGGCGGR", "CCGCCC"],               # SP1
    "TF_NFkB": ["GGGRNWYYCC"],                      # NF-κB
    "TF_Ebox": ["CACGTG", "CANNTG"],                # E-box
    "TF_TATA": ["TATAAA", "TATATA"],                # TATA box
    "TF_P53": ["RRRCWWGYYY"],                       # p53响应元件
    "TF_MYC": ["CACGTG"],                           # Myc
    "TF_SOX": ["AACAAT", "ATTGTT"],                 # SOX
}

def scan_motifs(filepath, motifs=None, p_threshold=0.05, make_plot=False):
    if motifs is None: motifs = JASPAR_MOTIFS
    
    # 加载FASTA序列
    sequences = {}; current_id = None; current_seq = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('>'):
                if current_id: sequences[current_id] = ''.join(current_seq)
                current_id = line[1:].split()[0]; current_seq = []
            else: current_seq.append(line.strip().upper())
    if current_id: sequences[current_id] = ''.join(current_seq)
    
    hits = defaultdict(list); hit_counts = defaultdict(int)
    
    for seq_id, seq in sequences.items():
        for tf_name, patterns in motifs.items():
            for pattern in patterns:
                # 将IUPAC转换为正则
                iupac = {"R":"[AG]","Y":"[CT]","S":"[GC]","W":"[AT]","K":"[GT]","M":"[AC]",
                         "B":"[CGT]","D":"[AGT]","H":"[ACT]","V":"[ACG]","N":"[ACGT]"}
                regex = pattern
                for code, repl in iupac.items():
                    regex = regex.replace(code, repl)
                
                for match in re.finditer(regex, seq):
                    pos = match.start()
                    matched_seq = match.group()
                    hits[tf_name].append({"seq_id": seq_id, "pos": pos, "matched": matched_seq})
                    hit_counts[tf_name] += 1
    
    # 报告
    total_hits = sum(hit_counts.values())
    print(f"\n{'='*60}")
    print(f"  Motif扫描报告")
    print(f"{'='*60}")
    print(f"  序列数: {len(sequences)}")
    print(f"  总命中: {total_hits}")
    print(f"\n  【Top Motif排名】")
    for tf, cnt in sorted(hit_counts.items(), key=lambda x: -x[1]):
        pct = round(cnt / total_hits * 100, 1) if total_hits else 0
        print(f"    {tf}: {cnt} hits ({pct}%)")
    
    # 保存结果
    with open("motif_hits.csv", 'w') as out:
        out.write("TF,seq_id,position,matched_sequence\n")
        for tf, hit_list in hits.items():
            for h in hit_list:
                out.write(f"{tf},{h['seq_id']},{h['pos']},{h['matched']}\n")
    print(f"  结果CSV: motif_hits.csv")
    
    # 绘图
    if make_plot:
        try:
            import matplotlib; matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            tfs = sorted(hit_counts.keys())
            counts = [hit_counts[t] for t in tfs]
            plt.figure(figsize=(8, 5))
            plt.barh(range(len(tfs)), counts, color='#2196F3')
            plt.yticks(range(len(tfs)), tfs); plt.xlabel('命中数')
            plt.title('Motif命中排名'); plt.tight_layout()
            plt.savefig("motif_density.png", dpi=300); plt.close()
            print(f"  Motif图: motif_density.png")
        except: print("  需要matplotlib")
    print(f"{'='*60}")

def main():
    print("="*50); print("  Motif扫描器"); print("="*50)
    fp = get_input("序列FASTA路径", "sequences.fasta")
    mf = get_input("motif字典(内置JASPAR/自定义文件路径)", "JASPAR")
    pt = get_input("p-value阈值", 0.05, float)
    mp = get_input("是否出图(yes/no)", "no")
    motifs = JASPAR_MOTIFS if mf.upper() == "JASPAR" else None
    if mf != "JASPAR" and os.path.exists(mf):
        motifs = {}
        with open(mf, 'r') as f:
            for line in f: fields=line.strip().split('\t'); motifs[fields[0]]=fields[1:]
    scan_motifs(fp, motifs, pt, mp.lower() in ('yes','y'))

if __name__ == "__main__": main()