#!/usr/bin/env python3
"""从RNA-seq VCF中筛选候选RNA编辑位点(A>I/G等)"""

def main():
    input_vcf = input("RNA-seq变异VCF路径 [rna_variants.vcf]: ") or "rna_variants.vcf"
    output_file = input("候选编辑位点输出 [rna_editing.tsv]: ") or "rna_editing.tsv"
    min_alt_freq = input("最低变异频率 [0.1]: ") or "0.1"
    min_depth = input("最低测序深度 [10]: ") or "10"
    min_af, min_dp = float(min_alt_freq), int(min_depth)
    etypes = {("A","G"), ("T","C")}
    res = []
    with open(input_vcf) as f:
        for line in f:
            if line.startswith("#"): continue
            p = line.strip().split("\t")
            if len(p) < 8: continue
            ref, alt = p[3].upper(), p[4].upper()
            if len(ref) > 1 or len(alt) > 1 or (ref, alt) not in etypes: continue
            info = dict(it.split("=", 1) if "=" in it else (it, "T") for it in p[7].split(";"))
            dp = int(info.get("DP", "0")); af = float(info.get("AF", "0"))
            if dp >= min_dp and af >= min_af: res.append([p[0],p[1],p[2],ref,alt,dp,f"{af:.4f}"])
    with open(output_file, "w") as out:
        out.write("CHROM\tPOS\tID\tREF\tALT\tDepth\tAF\n")
        for r in res: out.write("\t".join(str(x) for x in r)+"\n")
    print(f"RNA编辑: {len(res)} 个候选位点")


if __name__ == "__main__":
    main()
