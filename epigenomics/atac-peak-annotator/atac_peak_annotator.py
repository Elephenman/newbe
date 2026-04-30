#!/usr/bin/env python3
"""ATAC-seq peak最近基因+调控元件注释"""

import os
import sys
import re


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def annotate_peaks(peak_file, gtf_file, output_file, max_distance=50000):
    """Annotate ATAC-seq peaks with nearest genes from GTF."""
    # Parse GTF for gene features
    genes = []
    with open(gtf_file) as f:
        for line in f:
            if line.startswith("#"):
                continue
            fields = line.strip().split("\t")
            if len(fields) < 9 or fields[2] != "gene":
                continue
            chrom = fields[0]
            start = int(fields[3])
            end = int(fields[4])
            strand = fields[6]
            attrs = fields[8]
            name_match = re.search(r'gene_name "([^"]+)"', attrs)
            gene_id_match = re.search(r'gene_id "([^"]+)"', attrs)
            gene_name = name_match.group(1) if name_match else (gene_id_match.group(1) if gene_id_match else ".")
            genes.append((chrom, start, end, gene_name, strand))

    # Sort genes by chrom and start
    genes.sort(key=lambda x: (x[0], x[1]))

    # Parse peaks (BED format: chrom, start, end, name, score, strand)
    peaks = []
    with open(peak_file) as f:
        for line in f:
            if line.startswith("#") or line.startswith("track"):
                continue
            fields = line.strip().split("\t")
            if len(fields) < 3:
                continue
            chrom = fields[0]
            start = int(fields[1])
            end = int(fields[2])
            name = fields[3] if len(fields) > 3 else f"{chrom}:{start}-{end}"
            peaks.append((chrom, start, end, name))

    if not peaks:
        print("[ERROR] No valid peaks found in input file")
        sys.exit(1)

    # Annotate each peak with nearest gene
    results = []
    for p_chrom, p_start, p_end, p_name in peaks:
        best_gene = "None"
        best_dist = float("inf")
        best_strand = "."
        for g_chrom, g_start, g_end, g_name, g_strand in genes:
            if g_chrom != p_chrom:
                continue
            # Calculate distance: 0 if overlapping, otherwise gap
            if g_start < p_end and g_end > p_start:
                dist = 0
            elif g_end <= p_start:
                dist = p_start - g_end
            else:
                dist = g_start - p_end
            if dist < best_dist:
                best_dist = dist
                best_gene = g_name
                best_strand = g_strand

        # Classify regulatory region
        region_type = "Intergenic"
        if best_dist == 0:
            region_type = "Gene Body"
        elif best_dist <= 2000:
            region_type = "Promoter (<=2kb)"
        elif best_dist <= 5000:
            region_type = "Proximal (2-5kb)"

        within_max = "Yes" if best_dist <= max_distance else "No"
        results.append((p_chrom, p_start, p_end, p_name, best_gene, best_dist, region_type, best_strand, within_max))

    # Write output
    with open(output_file, "w") as out:
        out.write("Chrom\tStart\tEnd\tPeak_Name\tNearest_Gene\tDistance\tRegion_Type\tStrand\tWithin_Range\n")
        for r in results:
            out.write("\t".join(str(x) for x in r) + "\n")

    # Summary
    promoter_count = sum(1 for r in results if "Promoter" in r[6])
    gene_body_count = sum(1 for r in results if "Gene Body" in r[6])
    proximal_count = sum(1 for r in results if "Proximal" in r[6])
    intergenic_count = sum(1 for r in results if "Intergenic" in r[6])

    return {
        "total": len(results),
        "promoter": promoter_count,
        "gene_body": gene_body_count,
        "proximal": proximal_count,
        "intergenic": intergenic_count,
    }


def main():
    print("=" * 60)
    print("  ATAC-seq peak nearest gene + regulatory element annotation")
    print("=" * 60)
    print()

    peak_file = get_input("Peak BED file path", "peaks.bed")
    gtf_file = get_input("Gene annotation GTF path", "genes.gtf")
    output_file = get_input("Output annotation path", "atac_annotated.tsv")
    max_distance = get_input("Max annotation distance (bp)", "50000", int)

    if not os.path.exists(peak_file):
        print(f"[ERROR] Peak file not found: {peak_file}")
        sys.exit(1)
    if not os.path.exists(gtf_file):
        print(f"[ERROR] GTF file not found: {gtf_file}")
        sys.exit(1)

    summary = annotate_peaks(peak_file, gtf_file, output_file, max_distance)

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  Total peaks annotated: {summary['total']}")
    print(f"  Promoter (<=2kb):      {summary['promoter']}")
    print(f"  Gene Body:             {summary['gene_body']}")
    print(f"  Proximal (2-5kb):      {summary['proximal']}")
    print(f"  Intergenic:            {summary['intergenic']}")
    print(f"  Output saved to:       {output_file}")
    print("=" * 60)
    print()
    print("[Done] ATAC-seq peak annotation completed successfully!")


if __name__ == "__main__":
    main()
