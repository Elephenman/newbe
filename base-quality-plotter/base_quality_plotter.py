#!/usr/bin/env python3
"""Base quality per-position distribution plot"""

import os
import sys


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def plot_base_quality(fastq_file, output_plot, max_reads=100000):
    """Parse FASTQ and generate per-position base quality box plot."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("[ERROR] matplotlib is required: pip install matplotlib")
        sys.exit(1)

    # Parse FASTQ quality scores per position
    position_quals = {}
    total_reads = 0

    with open(fastq_file) as f:
        line_count = 0
        for line in f:
            line_count += 1
            if line_count % 4 == 0:  # Quality line
                qual_str = line.strip()
                for pos, char in enumerate(qual_str):
                    qval = ord(char) - 33  # Phred+33
                    if pos not in position_quals:
                        position_quals[pos] = []
                    position_quals[pos].append(qval)
                total_reads += 1
                if total_reads >= max_reads:
                    break

    if not position_quals:
        print("[ERROR] No quality data parsed from FASTQ file")
        sys.exit(1)

    # Compute statistics per position
    positions = sorted(position_quals.keys())
    max_pos = positions[-1] + 1

    means = []
    q25s = []
    q50s = []
    q75s = []

    for pos in range(max_pos):
        quals = position_quals.get(pos, [])
        if quals:
            sorted_q = sorted(quals)
            n = len(sorted_q)
            means.append(sum(sorted_q) / n)
            q25s.append(sorted_q[int(n * 0.25)])
            q50s.append(sorted_q[int(n * 0.50)])
            q75s.append(sorted_q[int(n * 0.75)])
        else:
            means.append(0)
            q25s.append(0)
            q50s.append(0)
            q75s.append(0)

    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    x = list(range(max_pos))

    # IQR band
    ax.fill_between(x, q25s, q75s, alpha=0.3, color='#4DBBD5', label='IQR (Q25-Q75)')
    # Median line
    ax.plot(x, q50s, color='#E64B35', linewidth=2, label='Median')
    # Mean line
    ax.plot(x, means, color='#3C5488', linewidth=1.5, linestyle='--', label='Mean')

    ax.axhline(y=20, color='grey', linestyle=':', alpha=0.7, label='Q20')
    ax.axhline(y=30, color='green', linestyle=':', alpha=0.7, label='Q30')

    ax.set_xlabel('Position in Read')
    ax.set_ylabel('Quality Score (Phred+33)')
    ax.set_title(f'Per-Position Base Quality Distribution ({total_reads} reads)')
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_plot, dpi=150)
    plt.close()

    # Compute overall stats
    all_quals = []
    for quals in position_quals.values():
        all_quals.extend(quals)
    avg_q = sum(all_quals) / len(all_quals) if all_quals else 0
    q20_pct = sum(1 for q in all_quals if q >= 20) / len(all_quals) * 100 if all_quals else 0
    q30_pct = sum(1 for q in all_quals if q >= 30) / len(all_quals) * 100 if all_quals else 0

    return {
        "total_reads": total_reads,
        "read_length": max_pos,
        "avg_quality": round(avg_q, 1),
        "q20_pct": round(q20_pct, 1),
        "q30_pct": round(q30_pct, 1),
    }


def main():
    print("=" * 60)
    print("  Base Quality Per-Position Distribution Plot")
    print("=" * 60)
    print()

    input_file = get_input("Input FASTQ file path", "input.fastq")
    output_plot = get_input("Output plot path", "base_quality.png")
    max_reads = get_input("Max reads to sample", "100000", int)

    if not os.path.exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)

    stats = plot_base_quality(input_file, output_plot, max_reads)

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  Total reads sampled: {stats['total_reads']}")
    print(f"  Max read length:     {stats['read_length']}")
    print(f"  Average quality:     {stats['avg_quality']}")
    print(f"  Q20%:                {stats['q20_pct']}%")
    print(f"  Q30%:                {stats['q30_pct']}%")
    print(f"  Output saved to:     {output_plot}")
    print("=" * 60)
    print()
    print("[Done] Base quality plot completed successfully!")


if __name__ == "__main__":
    main()
