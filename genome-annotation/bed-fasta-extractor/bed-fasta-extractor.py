#!/usr/bin/env python3
"""根据BED坐标从基因组FASTA中提取对应序列"""

def main():
    bed_file = input("输入BED文件路径 [regions.bed]: ") or "regions.bed"
    fasta_file = input("基因组FASTA路径 [genome.fa]: ") or "genome.fa"
    output_file = input("输出FASTA路径 [extracted.fa]: ") or "extracted.fa"
    flank = input("两侧扩展碱基数 [0]: ") or "0"
    flk = int(flank)
    genome = {}; cur = None; seq = []
    with open(fasta_file) as f:
        for line in f:
            if line.startswith(">"):
                if cur: genome[cur] = "".join(seq)
                cur = line[1:].strip().split()[0]; seq = []
            else: seq.append(line.strip())
    if cur: genome[cur] = "".join(seq)
    n = 0
    with open(bed_file) as bf, open(output_file, "w") as out:
        for line in bf:
            if line.startswith("#") or line.startswith("track"): continue
            p = line.strip().split("\t")
            if len(p) < 3: continue
            c, s, e = p[0], int(p[1]), int(p[2])
            nm = p[3] if len(p)>3 else f"{c}:{s}-{e}"
            s2, e2 = max(0, s-flk), min(len(genome.get(c,"")), e+flk)
            out.write(f">{nm}\n{genome.get(c,'')[s2:e2]}\n"); n += 1
    print(f"提取完成: {n} 个区域")


if __name__ == "__main__":
    main()
