#!/usr/bin/env python3
"""拷贝数变异片段基因注释"""

def main():
    cnv_file = input("CNV片段文件(TSV: chr,start,end,cn) [cnv_segments.tsv]: ") or "cnv_segments.tsv"
    gene_file = input("基因注释GTF路径 [genes.gtf]: ") or "genes.gtf"
    output_file = input("输出注释路径 [cnv_annotated.tsv]: ") or "cnv_annotated.tsv"
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
    with open(cnv_file) as f:
        for line in f:
            if line.startswith("#"): continue
            p = line.strip().split("\t")
            if len(p) < 4: continue
            chrom, start, end, cn = p[0], int(p[1]), int(p[2]), p[3]
            ov = [gn for gc, gs, ge, gn in genes if gc==chrom and gs<end and ge>start]
            results.append((chrom, start, end, cn, len(ov), ",".join(ov[:20])))
    with open(output_file, "w") as out:
        out.write("Chrom\tStart\tEnd\tCN\tGene_Count\tGenes\n")
        for r in results: out.write("\t".join(str(x) for x in r)+"\n")
    print(f"CNV注释: {len(results)} 片段")


if __name__ == "__main__":
    main()
