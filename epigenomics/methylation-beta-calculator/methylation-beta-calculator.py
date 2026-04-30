#!/usr/bin/env python3
"""从bedGraph计算甲基化beta值并做基本统计"""

def main():
    input_file = input("甲基化信号文件(chr,pos,methylated,unmethylated 或 chr,pos,methylated,total) [methylation.bedgraph]: ") or "methylation.bedgraph"
    output_file = input("输出beta值路径 [beta_values.tsv]: ") or "beta_values.tsv"
    min_coverage = input("最低覆盖度 [5]: ") or "5"
    input_format = input("输入格式(methylated_total/methylated_unmethylated) [methylated_total]: ") or "methylated_total"
    alpha = 100  # Beta value offset to stabilize at low coverage
    min_cov = int(min_coverage); results = []
    with open(input_file) as f:
        for line in f:
            if line.startswith("#"): continue
            p = line.strip().split("\t")
            if len(p) < 4: continue
            chrom, pos = p[0], p[1]
            try:
                m = float(p[2])
                v = float(p[3])
            except ValueError:
                continue

            if input_format == "methylated_unmethylated":
                u = v
                t = m + u
            else:
                # methylated_total format
                t = v
                u = t - m

            if t < min_cov: continue

            # Beta value = M / (M + U + alpha), alpha=100 (standard)
            beta = m / (m + u + alpha) if (m + u + alpha) > 0 else 0
            results.append((chrom, pos, m, u, t, f"{beta:.4f}"))
    with open(output_file, "w") as out:
        out.write("Chrom\tPos\tMethylated\tUnmethylated\tTotal\tBeta\n")
        for r in results: out.write("\t".join(str(x) for x in r)+"\n")
    betas = [float(r[5]) for r in results]
    if betas:
        avg_beta = sum(betas) / len(betas)
        # M-value = log2(beta / (1 - beta)) for statistical analysis
        print(f"甲基化: {len(results)} sites, avg_beta={avg_beta:.3f}")


if __name__ == "__main__":
    main()
