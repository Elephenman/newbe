#!/usr/bin/env python3
"""BAM coverage depth statistics + distribution"""

import os
import sys


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def calculate_coverage_depth(bam_file, output_file, genome_length=None, bin_size=1000):
    """Calculate coverage depth from BAM file."""
    try:
        import pysam
    except ImportError:
        print("[ERROR] pysam is required: pip install pysam")
        sys.exit(1)

    bam = pysam.AlignmentFile(bam_file, "rb")

    # Get chromosome lengths
    chrom_lengths = {}
    for chrom in bam.references:
        chrom_lengths[chrom] = bam.get_reference_length(chrom)

    total_genome_length = sum(chrom_lengths.values())
    if genome_length is None:
        genome_length = total_genome_length

    # Per-chromosome depth statistics
    results = []
    total_covered_bases = 0
    depth_distribution = {}  # depth -> count of positions

    for chrom in bam.references:
        length = chrom_lengths[chrom]
        try:
            coverage = bam.count_coverage(chrom)
            # coverage is a tuple of 4 arrays (A, C, G, T) at each position
            for pos in range(length):
                depth = sum(cov[pos] for cov in coverage)
                if depth > 0:
                    total_covered_bases += 1
                depth_bin = min(depth, 100)  # cap at 100
                depth_distribution[depth_bin] = depth_distribution.get(depth_bin, 0) + 1
        except Exception:
            continue

    bam.close()

    # Calculate statistics
    coverage_pct = round(total_covered_bases / genome_length * 100, 2) if genome_length > 0 else 0

    # Depth thresholds
    depth_1x = sum(v for k, v in depth_distribution.items() if k >= 1)
    depth_5x = sum(v for k, v in depth_distribution.items() if k >= 5)
    depth_10x = sum(v for k, v in depth_distribution.items() if k >= 10)
    depth_20x = sum(v for k, v in depth_distribution.items() if k >= 20)
    depth_30x = sum(v for k, v in depth_distribution.items() if k >= 30)

    total_positions = sum(depth_distribution.values())
    pct_1x = round(depth_1x / total_positions * 100, 2) if total_positions > 0 else 0
    pct_5x = round(depth_5x / total_positions * 100, 2) if total_positions > 0 else 0
    pct_10x = round(depth_10x / total_positions * 100, 2) if total_positions > 0 else 0
    pct_20x = round(depth_20x / total_positions * 100, 2) if total_positions > 0 else 0
    pct_30x = round(depth_30x / total_positions * 100, 2) if total_positions > 0 else 0

    # Write output
    with open(output_file, "w") as out:
        out.write("=== Coverage Depth Report ===\n\n")
        out.write(f"BAM file: {bam_file}\n")
        out.write(f"Genome length: {genome_length:,} bp\n")
        out.write(f"Covered bases (>0): {total_covered_bases:,}\n")
        out.write(f"Coverage: {coverage_pct}%\n\n")
        out.write("Depth Distribution:\n")
        out.write(f"  >=1x:  {pct_1x}%\n")
        out.write(f"  >=5x:  {pct_5x}%\n")
        out.write(f"  >=10x: {pct_10x}%\n")
        out.write(f"  >=20x: {pct_20x}%\n")
        out.write(f"  >=30x: {pct_30x}%\n\n")
        out.write("Depth\tPositions\tPercentage\n")
        for depth in sorted(depth_distribution.keys()):
            count = depth_distribution[depth]
            pct = round(count / total_positions * 100, 4) if total_positions > 0 else 0
            out.write(f"{depth}\t{count}\t{pct}%\n")

    return {
        "genome_length": genome_length,
        "covered_bases": total_covered_bases,
        "coverage_pct": coverage_pct,
        "pct_1x": pct_1x,
        "pct_10x": pct_10x,
        "pct_30x": pct_30x,
    }


def main():
    print("=" * 60)
    print("  BAM Coverage Depth Statistics + Distribution")
    print("=" * 60)
    print()

    input_bam = get_input("Input BAM file path", "input.bam")
    output_file = get_input("Output report path", "coverage_depth.txt")
    genome_length = get_input("Genome length in bp (0=auto)", "0", int)

    if not os.path.exists(input_bam):
        print(f"[ERROR] BAM file not found: {input_bam}")
        sys.exit(1)

    gl = None if genome_length == 0 else genome_length
    stats = calculate_coverage_depth(input_bam, output_file, gl)

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  Genome length:    {stats['genome_length']:,}")
    print(f"  Covered bases:    {stats['covered_bases']:,}")
    print(f"  Coverage:         {stats['coverage_pct']}%")
    print(f"  >=1x:             {stats['pct_1x']}%")
    print(f"  >=10x:            {stats['pct_10x']}%")
    print(f"  >=30x:            {stats['pct_30x']}%")
    print(f"  Output saved to:  {output_file}")
    print("=" * 60)
    print()
    print("[Done] Coverage depth calculation completed successfully!")


if __name__ == "__main__":
    main()
