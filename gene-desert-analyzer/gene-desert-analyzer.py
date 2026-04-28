#!/usr/bin/env python3
"""基因荒漠区分析与注释"""

# 基因荒漠区分析
from collections import defaultdict

print("=" * 60)
print("  🧪 基因荒漠区分析器")
print("=" * 60)

input_gtf = get_input("GTF注释路径", "annotation.gtf")
input_fa = get_input("基因组FASTA路径(NA=无)", "NA")
min_desert = int(get_input("最小荒漠区大小(bp)", "500000"))
output_file = get_input("荒漠区列表路径", "gene_deserts.tsv")

gene_positions = defaultdict(list)
with open(input_gtf, 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        parts = line.strip().split('\t')
        if parts[2] != 'gene':
            continue
        chrom = parts[0]
        start = int(parts[3])
        end = int(parts[4])
        attrs = parts[8]
        gene_name = ''
        for attr in attrs.split(';'):
            if 'gene_name' in attr:
                gene_name = attr.split('"')[1]
        gene_positions[chrom].append((start, end, gene_name))

print(f"✅ 加载基因: {sum(len(v) for v in gene_positions.values())}")

deserts = []
for chrom, genes in sorted(gene_positions.items()):
    sorted_genes = sorted(genes, key=lambda x: x[0])
    
    for i in range(len(sorted_genes) - 1):
        gap_start = sorted_genes[i][1] + 1
        gap_end = sorted_genes[i+1][0] - 1
        gap_size = gap_end - gap_start
        
        if gap_size >= min_desert:
            deserts.append((chrom, gap_start, gap_end, gap_size,
                          sorted_genes[i][2], sorted_genes[i+1][2]))

with open(output_file, 'w') as f:
    f.write("chrom\tstart\tend\tsize\tflanking_gene_left\tflanking_gene_right\n")
    for d in deserts:
        f.write('\t'.join(str(x) for x in d) + '\n')

print(f"\n✅ 分析完成: {len(deserts)} 个基因荒漠区")
if deserts:
    sizes = [d[3] for d in deserts]
    print(f"  最大荒漠: {max(sizes)} bp")
    print(f"  平均大小: {sum(sizes)/len(sizes):.0f} bp")
print(f"📄 结果: {output_file}")
