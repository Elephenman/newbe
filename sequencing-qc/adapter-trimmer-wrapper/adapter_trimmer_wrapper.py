#!/usr/bin/env python3
"""FASTQ adapter sequence detection + trimming report"""

import os
import sys


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


# Common adapter sequences
ADAPTER_SEQUENCES = {
    "Illumina TruSeq Read 1": "AGATCGGAAGAGCACACGTCTGAACTCCAGTCA",
    "Illumina TruSeq Read 2": "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT",
    "Illumina Small RNA 3": "TGGAATTCTCGGGTGCCAAGG",
    "Illumina Small RNA 5": "GTTCAGAGTTCTACAGTCCGACGATC",
    "Nextera Transposase Read 1": "CTGTCTCTTATACACATCT",
    "Nextera Transposase Read 2": "CTGTCTCTTATACACATCTCCGAGCCCACGAGAC",
}


def detect_adapter(sequence, min_overlap=10):
    """Detect which adapter is present in a sequence."""
    for adapter_name, adapter_seq in ADAPTER_SEQUENCES.items():
        # Check for adapter anywhere in sequence (3' end contamination)
        for start_pos in range(len(sequence) - min_overlap + 1):
            match_len = 0
            for i in range(min(len(adapter_seq), len(sequence) - start_pos)):
                if sequence[start_pos + i] == adapter_seq[i]:
                    match_len += 1
                else:
                    break
            if match_len >= min_overlap:
                return adapter_name, start_pos, match_len
    return None, -1, 0


def trim_adapter(sequence, quality, adapter_seq, min_overlap=10):
    """Trim adapter from sequence if present."""
    for start_pos in range(len(sequence) - min_overlap + 1):
        match_len = 0
        for i in range(min(len(adapter_seq), len(sequence) - start_pos)):
            if sequence[start_pos + i] == adapter_seq[i]:
                match_len += 1
            else:
                break
        if match_len >= min_overlap:
            return sequence[:start_pos], quality[:start_pos], True
    return sequence, quality, False


def main():
    print("=" * 60)
    print("  FASTQ Adapter Detection + Trimming Report")
    print("=" * 60)
    print()

    input_file = get_input("Input FASTQ file path", "input.fastq")
    output_file = get_input("Output trimmed FASTQ path", "trimmed.fastq")
    report_file = get_input("Output report path", "adapter_report.txt")
    min_overlap = get_input("Minimum adapter overlap (bp)", "10", int)

    if not os.path.exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)

    # Detect and trim adapters
    adapter_counts = {}
    total_reads = 0
    trimmed_reads = 0
    total_bases_trimmed = 0

    with open(input_file) as fin, open(output_file, "w") as fout, open(report_file, "w") as frep:
        while True:
            header = fin.readline().strip()
            if not header:
                break
            seq = fin.readline().strip()
            plus = fin.readline().strip()
            qual = fin.readline().strip()
            total_reads += 1

            # Detect adapter
            adapter_name, start_pos, match_len = detect_adapter(seq.upper(), min_overlap)

            if adapter_name:
                adapter_counts[adapter_name] = adapter_counts.get(adapter_name, 0) + 1
                # Trim using the specific adapter sequence
                adapter_seq = ADAPTER_SEQUENCES[adapter_name]
                trimmed_seq, trimmed_qual, was_trimmed = trim_adapter(
                    seq, qual, adapter_seq, min_overlap
                )
                if was_trimmed:
                    total_bases_trimmed += len(seq) - len(trimmed_seq)
                    trimmed_reads += 1
                    fout.write(f"{header}\n{trimmed_seq}\n{plus}\n{trimmed_qual}\n")
                else:
                    fout.write(f"{header}\n{seq}\n{plus}\n{qual}\n")
            else:
                fout.write(f"{header}\n{seq}\n{plus}\n{qual}\n")

        # Write report
        frep.write("=== Adapter Detection & Trimming Report ===\n\n")
        frep.write(f"Input file: {input_file}\n")
        frep.write(f"Total reads: {total_reads}\n")
        frep.write(f"Reads with adapter: {sum(adapter_counts.values())}\n")
        frep.write(f"Reads trimmed: {trimmed_reads}\n")
        frep.write(f"Adapter detection rate: {sum(adapter_counts.values())/total_reads*100:.2f}%\n")
        frep.write(f"Total bases trimmed: {total_bases_trimmed}\n\n")
        frep.write("Adapter breakdown:\n")
        for name, count in sorted(adapter_counts.items(), key=lambda x: -x[1]):
            pct = count / total_reads * 100
            frep.write(f"  {name}: {count} reads ({pct:.2f}%)\n")

    # Summary
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  Total reads:        {total_reads}")
    print(f"  Adapter detected:   {sum(adapter_counts.values())}")
    print(f"  Reads trimmed:      {trimmed_reads}")
    print(f"  Bases trimmed:      {total_bases_trimmed}")
    print(f"  Adapter rate:       {sum(adapter_counts.values())/total_reads*100:.2f}%")
    for name, count in sorted(adapter_counts.items(), key=lambda x: -x[1]):
        print(f"    {name}: {count}")
    print(f"  Output FASTQ:       {output_file}")
    print(f"  Report:             {report_file}")
    print("=" * 60)
    print()
    print("[Done] Adapter trimming completed successfully!")


if __name__ == "__main__":
    main()
