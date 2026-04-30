#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  bam-mate-pair-resolver
  BAM Mate-Pair解析与修复工具
============================================================
"""

import pysam
from collections import defaultdict


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def resolve_mate_pairs(input_bam, output_bam, report_file="mate_pair_report.txt"):
    """Read BAM, identify orphan reads, resolve mate pairs by query name, write resolved BAM."""
    stats = {
        "total_reads": 0,
        "paired_reads": 0,
        "proper_pairs": 0,
        "orphan_reads": 0,
        "mate_unmapped": 0,
        "mate_wrong_chr": 0,
        "resolved_pairs": 0,
        "unpaired_reads": 0,
    }

    # First pass: index reads by query name to find orphan mates
    bamfile = pysam.AlignmentFile(input_bam, "rb")
    query_index = defaultdict(list)
    for read in bamfile:
        stats["total_reads"] += 1
        query_index[read.query_name].append(read)
    bamfile.close()

    # Identify orphan reads (mate unmapped or on different chromosome)
    orphan_queries = set()
    for qname, reads in query_index.items():
        for read in reads:
            if read.is_paired:
                stats["paired_reads"] += 1
                if read.is_proper_pair:
                    stats["proper_pairs"] += 1
                if read.mate_is_unmapped:
                    stats["mate_unmapped"] += 1
                    orphan_queries.add(qname)
                elif read.reference_name != read.next_reference_name:
                    stats["mate_wrong_chr"] += 1
                    orphan_queries.add(qname)
            else:
                stats["unpaired_reads"] += 1

    stats["orphan_reads"] = len(orphan_queries)

    # Second pass: resolve mate pairs for orphan reads
    # For reads whose mate is unmapped: check if mate exists in file by query name
    # For reads whose mate is on different chr: attempt to re-pair by query name
    resolved_qnames = set()
    for qname in orphan_queries:
        reads = query_index[qname]
        paired_reads_in_file = [r for r in reads if r.is_paired]
        # If we have both R1 and R2 in the file, we can resolve
        r1_reads = [r for r in paired_reads_in_file if r.is_read1]
        r2_reads = [r for r in paired_reads_in_file if r.is_read2]

        if r1_reads and r2_reads:
            resolved_qnames.add(qname)

    stats["resolved_pairs"] = len(resolved_qnames)

    # Write output BAM, updating mate information for resolved pairs
    bamfile = pysam.AlignmentFile(input_bam, "rb")
    out = pysam.AlignmentFile(output_bam, "wb", template=bamfile)

    for read in bamfile:
        if read.query_name in resolved_qnames:
            # Fix mate information for resolved orphan pairs
            reads = query_index[read.query_name]
            r1_reads = [r for r in reads if r.is_read1]
            r2_reads = [r for r in reads if r.is_read2]

            if r1_reads and r2_reads:
                mate = r2_reads[0] if read.is_read1 else r1_reads[0]
                read.next_reference_name = mate.reference_name
                read.next_reference_start = mate.reference_start
                read.mate_is_unmapped = mate.is_unmapped
                read.mate_is_reverse = mate.is_reverse
        out.write(read)

    bamfile.close()
    out.close()

    # Sort and index the output
    try:
        sorted_bam = output_bam.replace(".bam", ".sorted.bam")
        pysam.sort("-o", sorted_bam, output_bam)
        pysam.index(sorted_bam)
    except Exception:
        pass  # Sorting is best-effort

    # Write report
    with open(report_file, "w") as f:
        f.write("Mate-Pair Resolution Report\n")
        f.write("=" * 50 + "\n")
        f.write(f"Total reads: {stats['total_reads']}\n")
        f.write(f"Paired reads: {stats['paired_reads']}\n")
        f.write(f"Proper pairs: {stats['proper_pairs']}\n")
        f.write(f"Unpaired reads: {stats['unpaired_reads']}\n")
        f.write(f"Orphan reads (mate unmapped/diff chr): {stats['orphan_reads']}\n")
        f.write(f"  Mate unmapped: {stats['mate_unmapped']}\n")
        f.write(f"  Mate wrong chromosome: {stats['mate_wrong_chr']}\n")
        f.write(f"Resolved pairs: {stats['resolved_pairs']}\n")

    return stats


def main():
    print("\n" + "=" * 60)
    print("  BAM Mate-Pair Resolver")
    print("=" * 60)

    input_bam = get_input("\nInput BAM file", "sample.bam", str)
    output_bam = get_input("Output BAM file", "resolved.bam", str)
    report_file = get_input("Report file", "mate_pair_report.txt", str)

    try:
        stats = resolve_mate_pairs(input_bam, output_bam, report_file)
    except Exception as e:
        print(f"\nError: {e}")
        return

    total = stats["total_reads"]
    paired = stats["paired_reads"]
    proper = stats["proper_pairs"]

    print(f"\nResolution complete:")
    print(f"  Total reads: {total}")
    print(f"  Paired reads: {paired}")
    if paired > 0:
        print(f"  Proper pairs: {proper} ({proper / paired * 100:.1f}%)")
    print(f"  Unpaired reads: {stats['unpaired_reads']}")
    print(f"  Orphan reads: {stats['orphan_reads']}")
    print(f"    Mate unmapped: {stats['mate_unmapped']}")
    print(f"    Mate wrong chr: {stats['mate_wrong_chr']}")
    print(f"  Resolved pairs: {stats['resolved_pairs']}")
    print(f"\nReport saved to: {report_file}")


if __name__ == "__main__":
    main()
