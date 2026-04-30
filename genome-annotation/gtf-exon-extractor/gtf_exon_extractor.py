#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  gtf-exon-extractor
  从GTF文件提取外显子坐标和长度信息
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def extract_exons(gtf_file, output="exons.bed", gene_id=None):
    """提取GTF中的外显子信息，转换为BED坐标(GTF 1-based -> BED 0-based start, 1-based end)"""
    exons = []

    try:
        with open(gtf_file, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                parts = line.strip().split('\t')
                if len(parts) < 9:
                    continue
                feature_type = parts[2]
                if feature_type != 'exon':
                    continue

                chrom = parts[0]
                start_gtf = int(parts[3])  # GTF: 1-based
                end_gtf = int(parts[4])    # GTF: 1-based, inclusive
                strand = parts[6]
                attrs = parts[8]

                gene_name = ""
                transcript_id = ""
                current_gene_id = ""

                for attr in attrs.split(';'):
                    attr = attr.strip()
                    if attr.startswith('gene_name'):
                        gene_name = attr.split('"')[1] if '"' in attr else attr.replace('gene_name ', '')
                    elif attr.startswith('gene_id'):
                        current_gene_id = attr.split('"')[1] if '"' in attr else attr.replace('gene_id ', '')
                    elif attr.startswith('transcript_id'):
                        transcript_id = attr.split('"')[1] if '"' in attr else attr.replace('transcript_id ', '')

                # Filter by gene_id if specified
                if gene_id and current_gene_id != gene_id:
                    continue

                # Convert GTF 1-based coordinates to BED 0-based coordinates
                # BED: start = GTF_start - 1, end = GTF_end (stays same)
                start_bed = start_gtf - 1
                end_bed = end_gtf

                exons.append((chrom, start_bed, end_bed, gene_name, transcript_id, strand))

        with open(output, 'w') as f:
            for exon in exons:
                f.write(f"{exon[0]}\t{exon[1]}\t{exon[2]}\t{exon[3]}\t{exon[4]}\t{exon[5]}\n")

        return len(exons)
    except FileNotFoundError:
        print(f"错误: 文件不存在 {gtf_file}")
        return 0

def main():
    print("\n" + "=" * 60)
    print("  GTF外显子提取工具")
    print("=" * 60)
    print("\n从GTF文件中提取外显子坐标信息")

    gtf_file = get_input("\nGTF文件路径", "annotation.gtf", str)
    output = get_input("输出BED文件", "exons.bed", str)
    gene_id = get_input("指定基因ID(留空提取全部)", "", str)

    gene_id = gene_id if gene_id else None
    count = extract_exons(gtf_file, output, gene_id)

    print(f"\n已提取 {count} 个外显子")
    print(f"结果已保存到: {output}")

if __name__ == "__main__":
    main()
