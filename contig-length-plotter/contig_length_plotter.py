#!/usr/bin/env python3
"""Assembly contig/N50 statistics + length distribution plot"""

import os
import sys


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def calculate_n50(lengths):
    """Calculate N50 from a list of contig lengths."""
    sorted_lengths = sorted(lengths, reverse=True)
    total = sum(sorted_lengths)
    cumsum = 0
    for length in sorted_lengths:
        cumsum += length
        if cumsum >= total / 2:
            return length
    return 0


def analyze_contigs(fasta_file, output_file, output_plot=None):
    """Analyze contig lengths from FASTA assembly file."""
    # Parse FASTA
    lengths = []
    cur_id = None
    cur_len = 0

    with open(fasta_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if cur_id is not None:
                    lengths.append(cur_len)
                cur_id = line[1:].split()[0]
                cur_len = 0
            else:
                cur_len += len(line)
    if cur_id is not None:
        lengths.append(cur_len)

    if not lengths:
        print("[ERROR] No sequences found in FASTA file")
        sys.exit(1)

    # Calculate statistics
    total_length = sum(lengths)
    n50 = calculate_n50(lengths)
    l50 = sum(1 for l in sorted(lengths, reverse=True)
              if sum(sorted(lengths, reverse=True)[:sum(1 for _ in filter(lambda x: x >= l, sorted(lengths, reverse=True)))]) >= total_length / 2)
    # Simpler L50 calculation
    sorted_lengths = sorted(lengths, reverse=True)
    cumsum = 0
    l50 = 0
    for length in sorted_lengths:
        cumsum += length
        l50 += 1
        if cumsum >= total_length / 2:
            break

    max_len = max(lengths)
    min_len = min(lengths)
    avg_len = total_length / len(lengths)
    gc_content = 0  # Not applicable from length alone

    # Generate plot if matplotlib available
    if output_plot:
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            import numpy as np

            fig, axes = plt.subplots(1, 2, figsize=(14, 6))

            # Histogram
            axes[0].hist(lengths, bins=50, color='#4DBBD5', alpha=0.7, edgecolor='white')
            axes[0].axvline(x=n50, color='#E64B35', linestyle='--', linewidth=2, label=f'N50={n50:,}')
            axes[0].axvline(x=avg_len, color='#3C5488', linestyle=':', linewidth=2, label=f'Mean={avg_len:,.0f}')
            axes[0].set_xlabel('Contig Length (bp)')
            axes[0].set_ylabel('Count')
            axes[0].set_title('Contig Length Distribution')
            axes[0].legend()

            # Log-scale histogram
            log_lengths = [np.log10(l) for l in lengths if l > 0]
            axes[1].hist(log_lengths, bins=50, color='#E64B35', alpha=0.7, edgecolor='white')
            axes[1].axvline(x=np.log10(n50), color='#3C5488', linestyle='--', linewidth=2,
                          label=f'N50={n50:,}')
            axes[1].set_xlabel('log10(Contig Length)')
            axes[1].set_ylabel('Count')
            axes[1].set_title('Contig Length Distribution (log scale)')
            axes[1].legend()

            plt.tight_layout()
            plt.savefig(output_plot, dpi=150)
            plt.close()
        except ImportError:
            print("[WARN] matplotlib not available, skipping plot")

    # Write output
    with open(output_file, "w") as out:
        out.write("=== Assembly Statistics ===\n")
        out.write(f"Total contigs: {len(lengths)}\n")
        out.write(f"Total length: {total_length:,} bp\n")
        out.write(f"N50: {n50:,} bp\n")
        out.write(f"L50: {l50}\n")
        out.write(f"Max contig: {max_len:,} bp\n")
        out.write(f"Min contig: {min_len:,} bp\n")
        out.write(f"Average length: {avg_len:,.1f} bp\n")
        out.write(f"\nLength percentiles:\n")
        for p in [10, 25, 50, 75, 90]:
            idx = int(len(sorted_lengths) * p / 100)
            val = sorted_lengths[min(idx, len(sorted_lengths)-1)]
            out.write(f"  {p}th: {val:,} bp\n")

    return {
        "total_contigs": len(lengths),
        "total_length": total_length,
        "n50": n50,
        "l50": l50,
        "max_len": max_len,
        "avg_len": round(avg_len, 1),
    }


def main():
    print("=" * 60)
    print("  Assembly Contig/N50 Statistics + Length Distribution")
    print("=" * 60)
    print()

    input_file = get_input("Input FASTA assembly path", "assembly.fasta")
    output_file = get_input("Output report path", "contig_stats.txt")
    output_plot = get_input("Output plot path (empty=skip)", "contig_length.png")

    if not os.path.exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)

    stats = analyze_contigs(input_file, output_file, output_plot or None)

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  Total contigs:    {stats['total_contigs']}")
    print(f"  Total length:     {stats['total_length']:,} bp")
    print(f"  N50:              {stats['n50']:,} bp")
    print(f"  L50:              {stats['l50']}")
    print(f"  Max contig:       {stats['max_len']:,} bp")
    print(f"  Average length:   {stats['avg_len']:,.1f} bp")
    print(f"  Output saved to:  {output_file}")
    print("=" * 60)
    print()
    print("[Done] Contig analysis completed successfully!")


if __name__ == "__main__":
    main()
