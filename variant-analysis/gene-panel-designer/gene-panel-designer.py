#!/usr/bin/env python3
"""基因Panel设计(靶向测序)"""

# 基因Panel设计器
print("=" * 60)
print("  🧪 基因Panel设计器(靶向测序)")
print("=" * 60)


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

input_genes = get_input("目标基因列表文件路径", "target_genes.txt")
input_gtf = get_input("GTF注释路径", "annotation.gtf")
flank = int(get_input("侧翼区域大小(bp)", "50"))
min_cov = float(get_input("最小覆盖度要求", "0.8"))
output_file = get_input("Panel设计结果路径", "gene_panel.tsv")

genes = [line.strip() for line in open(input_genes) if line.strip()]
print("✅ 目标基因: " + str(len(genes)))

gene_coords = {}
gene_exons = {}

with open(input_gtf, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("#"):
            continue
        parts = line.strip().split("\t")
        feature = parts[2]
        chrom = parts[0]
        start = int(parts[3])
        end = int(parts[4])
        attrs = parts[8]
        
        gene_name = ""
        for attr in attrs.split(";"):
            if "gene_name" in attr or "gene_id" in attr:
                gene_name = attr.split('"')[1]
        
        if feature == "gene" and gene_name in genes:
            if gene_name not in gene_coords:
                gene_coords[gene_name] = (chrom, start, end)
        
        if feature == "exon" and gene_name in genes:
            if gene_name not in gene_exons:
                gene_exons[gene_name] = []
            gene_exons[gene_name].append((chrom, start, end))

found = 0
not_found = []
panel_regions = []

for gene in genes:
    if gene in gene_coords:
        found += 1
        chrom, g_start, g_end = gene_coords[gene]
        gene_len = g_end - g_start
        
        if gene in gene_exons:
            exon_total = sum(e - s for c, s, e in gene_exons[gene])
            coverage = exon_total / gene_len if gene_len > 0 else 1.0
            
            if coverage >= min_cov:
                panel_regions.append((gene, chrom, g_start-flank, g_end+flank, g_end-g_start+2*flank, "full_gene", coverage))
            else:
                for c, s, e in gene_exons[gene]:
                    panel_regions.append((gene, c, s-flank, e+flank, e-s+2*flank, "exon", coverage))
        else:
            panel_regions.append((gene, chrom, g_start-flank, g_end+flank, gene_len+2*flank, "full_gene", 1.0))
    else:
        not_found.append(gene)

with open(output_file, "w") as f:
    f.write("gene\tchrom\tstart\tend\tprobe_length\tstrategy\tcoding_coverage\n")
    for r in panel_regions:
        f.write("\t".join(str(x) for x in r) + "\n")

total_length = sum(r[4] for r in panel_regions)
print("\n✅ Panel设计完成:")
print("  找到基因: " + str(found) + ", 未找到: " + str(len(not_found)))
print("  探针总数: " + str(len(panel_regions)))
print("  Panel总长: " + str(total_length) + " bp (" + str(round(total_length/1000, 1)) + " kb)")
if not_found:
    print("  ⚠️ 未找到: " + ", ".join(not_found))
print("📄 结果: " + output_file)
