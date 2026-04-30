#!/usr/bin/env python3
"""从GTF提取内含子坐标+长度统计"""

# GTF内含子提取器
import matplotlib.pyplot as plt
from collections import defaultdict

print("=" * 60)
print("  🧬 GTF内含子提取器")
print("=" * 60)

input_gtf = get_input("GTF文件路径", "annotation.gtf")
output_file = get_input("输出内含子列表路径", "introns.tsv")
stats_file = get_input("统计报告路径", "intron_stats.txt")
plot_out = get_input("长度分布图路径", "intron_length_dist.png")

exons_by_gene = defaultdict(list)

with open(input_gtf, 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        parts = line.strip().split('\t')
        if len(parts) < 9:
            continue
        if parts[2] != 'exon':
            continue
        chrom = parts[0]
        start = int(parts[3])
        end = int(parts[4])
        attrs = parts[8]
        gene_id = ''
        for attr in attrs.split(';'):
            attr = attr.strip()
            if attr.startswith('gene_id'):
                gene_id = attr.split('"')[1]
        if gene_id:
            exons_by_gene[gene_id].append((chrom, start, end))

introns = []
intron_lengths = []

for gene_id, exons in exons_by_gene.items():
    sorted_exons = sorted(exons, key=lambda x: x[1])
    for i in range(len(sorted_exons) - 1):
        chrom = sorted_exons[i][0]
        intron_start = sorted_exons[i][2] + 1
        intron_end = sorted_exons[i+1][1] - 1
        if intron_start < intron_end:
            length = intron_end - intron_start + 1
            introns.append((chrom, intron_start, intron_end, gene_id, length))
            intron_lengths.append(length)

with open(output_file, 'w') as f:
    f.write("chrom\tstart\tend\tgene_id\tlength\n")
    for intron in introns:
        f.write('\t'.join(str(x) for x in intron) + '\n')

print(f"\n✅ 提取完成: {len(introns)} 个内含子")
print(f"  涉及基因: {len(exons_by_gene)}")

if intron_lengths:
    avg_len = sum(intron_lengths) / len(intron_lengths)
    print(f"  平均长度: {avg_len:.0f} bp")
    print(f"  中位长度: {sorted(intron_lengths)[len(intron_lengths)//2]} bp")

    plt.figure(figsize=(10, 5))
    plt.hist([l for l in intron_lengths if l < 50000], bins=50, edgecolor='black', alpha=0.7)
    plt.xlabel("Intron Length (bp)")
    plt.ylabel("Count")
    plt.title("Intron Length Distribution")
    plt.tight_layout()
    plt.savefig(plot_out, dpi=150)
    print(f"📊 分布图: {plot_out}")

with open(stats_file, 'w') as f:
    f.write(f"Intron Statistics\nTotal introns: {len(introns)}\n")
    f.write(f"Genes: {len(exons_by_gene)}\n")
    if intron_lengths:
        f.write(f"Mean length: {avg_len:.0f}\n")
print(f"📄 统计: {stats_file}")
