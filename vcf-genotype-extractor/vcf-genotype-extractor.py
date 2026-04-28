#!/usr/bin/env python3
"""从VCF文件提取指定样本的基因型矩阵"""

def main():
    input_vcf = input("输入VCF文件路径 [input.vcf]: ") or "input.vcf"
    output_file = input("输出基因型矩阵路径 [genotypes.tsv]: ") or "genotypes.tsv"
    samples = input("样本名(逗号分隔,留空=全部) []: ") or ""
    sf = [s.strip() for s in samples.split(",") if s.strip()] if samples else []
    sel = []; data = []; idx = []
    with open(input_vcf) as f:
        for line in f:
            if line.startswith("##"): continue
            parts = line.strip().split("\t")
            if line.startswith("#CHROM"):
                all_s = parts[9:]
                if sf: idx = [i for i,s in enumerate(all_s) if s in sf]; sel = [all_s[i] for i in idx]
                else: idx = list(range(len(all_s))); sel = all_s
                continue
            if len(parts) < 9: continue
            gts = [parts[9+i].split(":")[0] if (9+i)<len(parts) else "./." for i in idx]
            data.append([parts[0],parts[1],parts[2],parts[3],parts[4]]+gts)
    with open(output_file,"w") as out:
        out.write("\t".join(["CHROM","POS","ID","REF","ALT"]+sel)+"\n")
        for row in data: out.write("\t".join(str(x) for x in row)+"\n")
    print(f"基因型矩阵: {len(data)} 变异, {len(sel)} 样本")


if __name__ == "__main__":
    main()
