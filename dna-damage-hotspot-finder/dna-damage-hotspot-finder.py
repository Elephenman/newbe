#!/usr/bin/env python3
"""DNA损伤修复热点区域识别(DDR相关)"""

def main():
    input_file = input("DNA损伤信号文件BED路径 [damage_peaks.bed]: ") or "damage_peaks.bed"
    gene_file = input("基因注释GTF路径 [genes.gtf]: ") or "genes.gtf"
    output_file = input("输出热点区域路径 [damage_hotspots.tsv]: ") or "damage_hotspots.tsv"
    merge_distance = input("合并距离(bp) [500]: ") or "500"
    merge_dist = int(merge_distance)
    peaks = []
    with open(input_file) as f:
        for line in f:
            if line.startswith("#") or line.startswith("track"): continue
            p = line.strip().split("\t")
            if len(p) >= 3: peaks.append((p[0], int(p[1]), int(p[2])))
    peaks.sort()
    merged = []
    for chrom, start, end in peaks:
        if merged and merged[-1][0] == chrom and start - merged[-1][2] <= merge_dist:
            merged[-1] = (chrom, merged[-1][1], max(merged[-1][2], end))
        else: merged.append((chrom, start, end))
    genes = []
    with open(gene_file) as f:
        for line in f:
            if line.startswith("#"): continue
            p = line.strip().split("\t")
            if len(p) >= 9 and p[2] == "gene":
                attrs = dict(a.strip().split(" ",1) if " " in a.strip() else ("","") for a in p[8].split(";") if a.strip())
                gn = attrs.get("gene_name","").strip('"')
                if gn: genes.append((p[0], int(p[3]), int(p[4]), gn))
    results = []
    for chrom, start, end in merged:
        nearest = ""; min_d = float("inf")
        for gc, gs, ge, gn in genes:
            if gc == chrom:
                d = max(0, max(start, gs) - min(end, ge))
                if d < min_d: min_d = d; nearest = gn
        results.append((chrom, start, end, end-start, nearest, min_d))
    with open(output_file, "w") as out:
        out.write("Chrom\tStart\tEnd\tLength\tNearest_Gene\tDistance\n")
        for r in results: out.write("\t".join(str(x) for x in r)+"\n")
    print(f"热点: {len(merged)} (从 {len(peaks)} peaks合并)")


if __name__ == "__main__":
    main()
