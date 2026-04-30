#!/usr/bin/env python3
"""FASTQ exact duplicate reads removal + statistics"""

import os
import sys
from collections import defaultdict


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def remove_duplicates(input_fastq, output_fastq, dedup_mode="sequence"):
    """Remove duplicate reads from FASTQ file.

    Args:
        input_fastq: Input FASTQ file path
        output_fastq: Output FASTQ file path
        dedup_mode: 'sequence' (dedup by sequence), 'header' (dedup by header),
                    'both' (dedup by sequence+quality)
    """
    seen = set()
    total = 0
    kept = 0
    dup_counts = defaultdict(int)  # track duplication levels

    with open(input_fastq) as fin, open(output_fastq, "w") as fout:
        while True:
            header = fin.readline().strip()
            if not header:
                break
            seq = fin.readline().strip()
            plus = fin.readline().strip()
            qual = fin.readline().strip()
            total += 1

            # Determine dedup key based on mode
            if dedup_mode == "sequence":
                key = seq
            elif dedup_mode == "header":
                key = header
            else:  # both
                key = seq + qual

            if key in seen:
                dup_counts[key] = dup_counts.get(key, 0) + 1
                continue
            seen.add(key)
            kept += 1
            fout.write(f"{header}\n{seq}\n{plus}\n{qual}\n")

    # Calculate stats
    removed = total - kept
    dup_rate = removed / total * 100 if total > 0 else 0

    # Duplication level distribution
    level_counts = defaultdict(int)
    for key, count in dup_counts.items():
        level = min(count + 1, 10)  # cap at 10+
        level_counts[level] += 1

    return {
        "total": total,
        "kept": kept,
        "removed": removed,
        "dup_rate": round(dup_rate, 2),
        "level_counts": dict(level_counts),
    }


def main():
    print("=" * 60)
    print("  FASTQ Exact Duplicate Reads Removal + Statistics")
    print("=" * 60)
    print()

    input_file = get_input("Input FASTQ file path", "input.fastq")
    output_file = get_input("Output FASTQ path", "deduped.fastq")
    dedup_mode = get_input("Dedup mode (sequence/header/both)", "sequence")

    if not os.path.exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)

    stats = remove_duplicates(input_file, output_file, dedup_mode)

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  Total reads:      {stats['total']}")
    print(f"  Kept reads:       {stats['kept']}")
    print(f"  Removed dups:     {stats['removed']}")
    print(f"  Duplication rate: {stats['dup_rate']}%")
    if stats['level_counts']:
        print(f"  Duplication levels:")
        for level in sorted(stats['level_counts'].keys()):
            label = f"{level}+" if level >= 10 else str(level)
            print(f"    {label} copies: {stats['level_counts'][level]} reads")
    print(f"  Output saved to:  {output_file}")
    print("=" * 60)
    print()
    print("[Done] FASTQ deduplication completed successfully!")


if __name__ == "__main__":
    main()
