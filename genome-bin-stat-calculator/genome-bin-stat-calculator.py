#!/usr/bin/env python3
"""基因组窗口bin统计(GC/基因密度/SNP密度) - 使用正确的GTF列解析"""

import gzip

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

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

def read_gtf_coords(path):
    """Read gene coordinates from GTF file using correct column indices.
    GTF columns: 0=chrom, 1=source, 2=feature, 3=start, 4=end, 5=score, 6=strand, 7=frame, 8=attributes
    We filter for feature type 'gene' (column 2), and use start (column 3) and end (column 4).
    Gene positions span from start to end; we store both for overlap calculation.
    """
    coords = {}
    opener = gzip.open if path.endswith('.gz') else open
    mode = 'rt' if path.endswith('.gz') else 'r'
    with opener(path, mode) as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 9:
                continue
            # Column 2 (index 2) = feature type; only count 'gene' features
            feature_type = parts[2]
            if feature_type != 'gene':
                continue
            chrom = parts[0]
            start = int(parts[3])  # Column 3 (index 3) = start position
            end = int(parts[4])    # Column 4 (index 4) = end position
            if chrom not in coords:
                coords[chrom] = []
            # Store (start, end) tuples for proper gene overlap calculation
            coords[chrom].append((start, end))
    return coords

def read_vcf_coords(path):
    """Read variant positions from VCF file."""
    coords = {}
    opener = gzip.open if path.endswith('.gz') else open
    mode = 'rt' if path.endswith('.gz') else 'r'
    with opener(path, mode) as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            chrom = parts[0]
            pos = int(parts[1])
            if chrom not in coords:
                coords[chrom] = []
            coords[chrom].append(pos)
    return coords

def read_bed_coords(path):
    """Read coordinates from BED file."""
    coords = {}
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('\t')
            chrom = parts[0]
            pos = int(parts[2])
            if chrom not in coords:
                coords[chrom] = []
            coords[chrom].append(pos)
    return coords

def main():
    print("=" * 60)
    print("  基因组Bin统计计算器")
    print("=" * 60)

    input_fa = get_input("基因组FASTA路径", "genome.fa", str)
    input_gtf = get_input("GTF注释路径(NA=无)", "NA", str)
    input_vcf = get_input("VCF变异文件路径(NA=无)", "NA", str)
    bin_size = get_input("bin窗口大小(bp)", "100000", int)
    output_file = get_input("统计结果路径", "genome_bin_stats.tsv", str)

    seqs = read_fasta(input_fa)
    print(f"加载 {len(seqs)} 染色体")

    gene_coords = {}
    if input_gtf != 'NA':
        gene_coords = read_gtf_coords(input_gtf)
        total_genes = sum(len(v) for v in gene_coords.values())
        print(f"  基因注释: {total_genes} 基因")

    snp_coords = {}
    if input_vcf != 'NA':
        snp_coords = read_vcf_coords(input_vcf)
        total_snps = sum(len(v) for v in snp_coords.values())
        print(f"  变异位点: {total_snps} SNPs")

    with open(output_file, 'w') as f:
        f.write("chrom\tbin_start\tbin_end\tgc_pct\tgene_density\tsnp_density\n")
        for chrom, seq in sorted(seqs.items()):
            for i in range(0, len(seq), bin_size):
                end = min(i + bin_size, len(seq))
                subseq = seq[i:end]
                gc = (subseq.count('G') + subseq.count('C')) / len(subseq) * 100 if len(subseq) > 0 else 0

                # Gene density: count genes that overlap this bin
                gene_d = 0
                if chrom in gene_coords:
                    for gene_start, gene_end in gene_coords[chrom]:
                        # Gene overlaps bin if gene_start < bin_end AND gene_end > bin_start
                        if gene_start < end and gene_end > i:
                            gene_d += 1

                # SNP density: count SNPs within this bin
                snp_d = 0
                if chrom in snp_coords:
                    for pos in snp_coords[chrom]:
                        if i < pos <= end:
                            snp_d += 1

                f.write(f"{chrom}\t{i}\t{end}\t{gc:.2f}\t{gene_d}\t{snp_d}\n")

    print(f"\n统计完成")
    print(f"结果: {output_file}")

if __name__ == "__main__":
    main()
