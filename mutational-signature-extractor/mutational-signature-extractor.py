#!/usr/bin/env python3
"""从VCF提取突变特征(SBS96谱)并可视化"""

def main():
    input_vcf = input("输入VCF文件路径 [somatic.vcf]: ") or "somatic.vcf"
    output_plot = input("输出SBS96谱图片路径 [sbs96.png]: ") or "sbs96.png"
    output_file = input("输出SBS96计数CSV [sbs96_counts.csv]: ") or "sbs96_counts.csv"
    import matplotlib.pyplot as plt, numpy as np
    bases = ["A","C","G","T"]
    sbs96 = {}
    for s in ["CA","CG","CT","TA","TC","TG"]:
        for b5 in bases:
            for b3 in bases: sbs96[f"{b5}[{s}]{b3}"] = 0
    with open(input_vcf) as f:
        for line in f:
            if line.startswith("#"): continue
            p = line.strip().split("\t")
            if len(p) < 5: continue
            ref, alt = p[3].upper(), p[4].upper()
            if len(ref) != 1 or len(alt) != 1: continue
            r, a = ref, alt
            if (r, a) in [("A","C"),("A","G"),("A","T"),("G","A"),("G","C"),("G","T")]:
                comp = {"A":"T","T":"A","C":"G","G":"C"}; r, a = comp[a], comp[r]
            ctx = f"N[{r}{a}]N"
            sbs96[ctx] = sbs96.get(ctx, 0) + 1
    cats = list(sbs96.keys()); vals = [sbs96[c] for c in cats]
    fig, ax = plt.subplots(figsize=(15, 4))
    colors = ["#1a9850" if "[C" in c else "#e41a1c" if "[T" in c else "#999" for c in cats]
    ax.bar(range(len(cats)), vals, color=colors)
    ax.set_xlabel("SBS96 Context"); ax.set_ylabel("Count"); ax.set_title("SBS96 Spectrum")
    plt.tight_layout(); plt.savefig(output_plot, dpi=150)
    import csv
    with open(output_file, "w", newline="") as out:
        w = csv.writer(out); w.writerow(["Context","Count"])
        for c, v in zip(cats, vals): w.writerow([c, v])
    print(f"SBS96谱: {output_plot}")


if __name__ == "__main__":
    main()
