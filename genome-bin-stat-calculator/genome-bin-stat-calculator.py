#!/usr/bin/env python3
"""基因组窗口bin统计(GC/基因密度/SNP密度)"""

# 基因组窗口bin统计
import gzip

print("=" * 60)
print("  🧪 基因组Bin统计计算器")
print("=" * 60)

input_fa = get_input("基因组FASTA路径", "genome.fa")
input_gtf = get_input("GTF注释路径(NA=无)", "NA")
input_vcf = get_input("VCF变异文件路径(NA=无)", "NA")
bin_size = int(get_input("bin窗口大小(bp)", "100000"))
output_file = get_input("统计结果路径", "genome_bin_stats.tsv")

def read_fasta(path):
    seqs = {}
    current = None
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('>'):
                current = line.strip()[1:].split()[0]
                seqs[current] = ''
            elif current:
                seqs[current] += line.strip().upper()
    return seqs

def read_bed_coords(path):
    coords = {}
    opener = gzip.open if path.endswith('.gz') else open
    mode = 'rt' if path.endswith('.gz') else 'r'
    with opener(path, mode) as f:
        for line in f:
            if path.endswith('.vcf') or path.endswith('.vcf.gz'):
                if line.startswith('#'):
                    continue
                parts = line.strip().split('\t')
                chrom = parts[0]
                pos = int(parts[1])
            elif path.endswith('.gtf') or path.endswith('.gtf.gz'):
                if line.startswith('#'):
                    continue
                parts = line.strip().split('\t')
                if parts[2] != 'gene':
                    continue
                chrom = parts[0]
                pos = int(parts[4])
            else:
                parts = line.strip().split('\t')
                chrom = parts[0]
                pos = int(parts[2])
            if chrom not in coords:
                coords[chrom] = []
            coords[chrom].append(pos)
    return coords

seqs = read_fasta(input_fa)
print(f"✅ 加载 {len(seqs)} 染色体")

gene_coords = {}
if input_gtf != 'NA':
    gene_coords = read_bed_coords(input_gtf)
    print(f"  基因注释: {sum(len(v) for v in gene_coords.values())} 基因")

snp_coords = {}
if input_vcf != 'NA':
    snp_coords = read_bed_coords(input_vcf)
    print(f"  变异位点: {sum(len(v) for v in snp_coords.values())} SNPs")

with open(output_file, 'w') as f:
    f.write("chrom\tbin_start\tbin_end\tgc_pct\tgene_density\tsnp_density\n")
    for chrom, seq in sorted(seqs.items()):
        for i in range(0, len(seq), bin_size):
            end = min(i + bin_size, len(seq))
            subseq = seq[i:end]
            gc = (subseq.count('G') + subseq.count('C')) / len(subseq) * 100 if len(subseq) > 0 else 0
            gene_d = 0
            if chrom in gene_coords:
                gene_d = sum(1 for p in gene_coords[chrom] if i <= p <= end)
            snp_d = 0
            if chrom in snp_coords:
                snp_d = sum(1 for p in snp_coords[chrom] if i <= p <= end)
            f.write(f"{chrom}\t{i}\t{end}\t{gc:.2f}\t{gene_d}\t{snp_d}\n")

print(f"\n✅ 统计完成")
print(f"📄 结果: {output_file}")
