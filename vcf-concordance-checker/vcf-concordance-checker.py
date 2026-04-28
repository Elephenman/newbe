#!/usr/bin/env python3
"""比较两个VCF文件的变异一致性，输出concordance统计"""

def main():
    vcf1 = input("第一个VCF文件路径 [sample1.vcf]: ") or "sample1.vcf"
    vcf2 = input("第二个VCF文件路径 [sample2.vcf]: ") or "sample2.vcf"
    output_file = input("输出报告路径 [concordance.txt]: ") or "concordance.txt"
    def parse_vcf(path):
        v = set()
        with open(path) as f:
            for line in f:
                if line.startswith("#"): continue
                p = line.strip().split("\t")
                if len(p) >= 5: v.add((p[0], p[1], p[3], p[4]))
        return v
    s1, s2 = parse_vcf(vcf1), parse_vcf(vcf2)
    shared = s1 & s2
    with open(output_file, "w") as out:
        out.write(f"VCF1: {len(s1)}\nVCF2: {len(s2)}\nShared: {len(shared)}\n")
        out.write(f"Only1: {len(s1-s2)}\nOnly2: {len(s2-s1)}\n")
        if s1 and s2: out.write(f"Jaccard: {len(shared)/len(s1|s2):.4f}\n")
    print(f"一致性报告: {output_file}")


if __name__ == "__main__":
    main()
