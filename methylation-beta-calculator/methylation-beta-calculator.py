#!/usr/bin/env python3
"""从bedGraph计算甲基化beta值并做基本统计"""

def main():
    input_file = input("甲基化信号文件(chr,pos,methylated,total) [methylation.bedgraph]: ") or "methylation.bedgraph"
    output_file = input("输出beta值路径 [beta_values.tsv]: ") or "beta_values.tsv"
    min_coverage = input("最低覆盖度 [5]: ") or "5"
    min_cov = int(min_coverage); results = []
    with open(input_file) as f:
        for line in f:
            if line.startswith("#"): continue
            p = line.strip().split("\t")
            if len(p) < 4: continue
            chrom, pos = p[0], p[1]
            try: m, t = float(p[2]), float(p[3])
            except: continue
            if t < min_cov: continue
            beta = m / t if t > 0 else 0
            results.append((chrom, pos, m, t, f"{beta:.4f}"))
    with open(output_file, "w") as out:
        out.write("Chrom\tPos\tMethylated\tTotal\tBeta\n")
        for r in results: out.write("\t".join(str(x) for x in r)+"\n")
    betas = [float(r[4]) for r in results]
    if betas:
        print(f"甲基化: {len(results)} sites, avg={sum(betas)/len(betas):.3f}")


if __name__ == "__main__":
    main()
