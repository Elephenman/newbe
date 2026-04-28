#!/usr/bin/env python3
"""基于Hi-C/ChIA-PET数据关联增强子与靶基因"""

def main():
    interaction_file = input("交互文件BEDPE路径 [interactions.bedpe]: ") or "interactions.bedpe"
    gene_file = input("基因注释GTF路径 [genes.gtf]: ") or "genes.gtf"
    output_file = input("输出增强子-基因关联路径 [enhancer_gene.tsv]: ") or "enhancer_gene.tsv"
    max_distance = input("最大关联距离(bp) [1000000]: ") or "1000000"
    max_dist = int(max_distance)
    genes = []
    with open(gene_file) as f:
        for line in f:
            if line.startswith("#"): continue
            p = line.strip().split("\t")
            if len(p) < 9 or p[2] != "gene": continue
            attrs = dict(a.strip().split(" ",1) if " " in a.strip() else ("","") for a in p[8].split(";") if a.strip())
            name = attrs.get("gene_name", attrs.get("gene_id","")).strip('"')
            if name: genes.append((p[0], int(p[3]), int(p[4]), name))
    links = []
    with open(interaction_file) as f:
        for line in f:
            if line.startswith("#"): continue
            p = line.strip().split("\t")
            if len(p) < 7: continue
            c1, s1, e1 = p[0], int(p[1]), int(p[2])
            c2, s2, e2 = p[3], int(p[4]), int(p[5])
            links.append((c1, (s1+e1)//2, c2, (s2+e2)//2))
    results = []
    for c1, mid1, c2, mid2 in links:
        for gc, gs, ge, gn in genes:
            if gc == c2 and abs(mid2-(gs+ge)//2) < max_dist:
                results.append((c1, mid1, gc, gs, ge, gn))
    with open(output_file, "w") as out:
        out.write("Enh_chr\tEnh_pos\tGene_chr\tGene_start\tGene_end\tGene_name\n")
        for r in results: out.write("\t".join(str(x) for x in r)+"\n")
    print(f"增强子-基因: {len(results)} 对")


if __name__ == "__main__":
    main()
