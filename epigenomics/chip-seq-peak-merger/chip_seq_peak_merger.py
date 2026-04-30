#!/usr/bin/env python3
"""ChIP-seq peak merge + shared peak extraction across samples"""

import os
import sys


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def merge_peaks(bed_files, merge_distance=0, output_file="merged_peaks.bed"):
    """Merge peaks from multiple BED files and identify shared/shared-by-all peaks."""
    # Collect all intervals with source tracking
    all_intervals = []
    file_names = []
    for fp in bed_files:
        name = os.path.splitext(os.path.basename(fp))[0]
        file_names.append(name)
        with open(fp) as f:
            for line in f:
                if line.startswith("#") or line.startswith("track") or not line.strip():
                    continue
                fields = line.strip().split("\t")
                if len(fields) < 3:
                    continue
                chrom = fields[0]
                start = int(fields[1])
                end = int(fields[2])
                name_field = fields[3] if len(fields) > 3 else "."
                score = fields[4] if len(fields) > 4 else "."
                all_intervals.append((chrom, start, end, name_field, score, name))

    if not all_intervals:
        print("[ERROR] No valid peaks found in input files")
        sys.exit(1)

    # Sort by chromosome and start position
    all_intervals.sort(key=lambda x: (x[0], x[1]))

    # Greedy merge: track which samples contribute to each merged region
    merged = []
    current = None
    current_sources = set()

    for iv in all_intervals:
        if current is None:
            current = iv
            current_sources = {iv[5]}
            continue
        if iv[0] == current[0] and iv[1] <= current[2] + merge_distance:
            # Overlapping or within merge distance - merge
            current = (current[0], current[1], max(current[2], iv[2]), current[3], current[4], current[5])
            current_sources.add(iv[5])
        else:
            merged.append((current[0], current[1], current[2], current[3], current[4], frozenset(current_sources)))
            current = iv
            current_sources = {iv[5]}

    if current:
        merged.append((current[0], current[1], current[2], current[3], current[4], frozenset(current_sources)))

    # Count shared peaks
    shared_all = sum(1 for m in merged if len(m[5]) == len(file_names))
    unique_to = {}
    for name in file_names:
        unique_to[name] = sum(1 for m in merged if m[5] == {name})

    # Write output
    with open(output_file, "w") as out:
        out.write("Chrom\tStart\tEnd\tName\tScore\tSample_Count\tSamples\n")
        for m in merged:
            samples_str = ",".join(sorted(m[5]))
            out.write(f"{m[0]}\t{m[1]}\t{m[2]}\t{m[3]}\t{m[4]}\t{len(m[5])}\t{samples_str}\n")

    # Write shared-by-all peaks
    if shared_all > 0:
        shared_file = output_file.replace(".bed", "_shared_all.bed")
        with open(shared_file, "w") as out:
            for m in merged:
                if len(m[5]) == len(file_names):
                    out.write(f"{m[0]}\t{m[1]}\t{m[2]}\t{m[3]}\t{m[4]}\n")

    return {
        "total_input": len(all_intervals),
        "total_merged": len(merged),
        "shared_all": shared_all,
        "unique_to": unique_to,
    }


def main():
    print("=" * 60)
    print("  ChIP-seq Peak Merge + Shared Peak Extraction")
    print("=" * 60)
    print()

    bed_input = get_input("Peak BED files (comma-separated)", "sample1.bed,sample2.bed")
    output_file = get_input("Output merged BED path", "merged_peaks.bed")
    merge_distance = get_input("Merge distance (bp)", "0", int)

    bed_files = [f.strip() for f in bed_input.split(",") if f.strip()]

    for fp in bed_files:
        if not os.path.exists(fp):
            print(f"[ERROR] File not found: {fp}")
            sys.exit(1)

    if len(bed_files) < 1:
        print("[ERROR] At least one BED file is required")
        sys.exit(1)

    stats = merge_peaks(bed_files, merge_distance, output_file)

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  Input files:          {len(bed_files)}")
    print(f"  Total input peaks:    {stats['total_input']}")
    print(f"  Merged peaks:         {stats['total_merged']}")
    print(f"  Shared by all:        {stats['shared_all']}")
    for name, count in stats['unique_to'].items():
        print(f"  Unique to {name}:    {count}")
    print(f"  Output saved to:      {output_file}")
    print("=" * 60)
    print()
    print("[Done] ChIP-seq peak merge completed successfully!")


if __name__ == "__main__":
    main()
