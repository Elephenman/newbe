#!/usr/bin/env python3
"""根据FASTQ和基因组大小计算测序深度"""

import os
import sys
import gzip


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    try:
        return dtype(val)
    except (ValueError, TypeError):
        return default


def main():
    print("=" * 60)
    print("  测序深度计算器")
    print("=" * 60)
    print()

    input_file = get_input("输入FASTQ文件路径", "input.fastq")
    genome_size = get_input("基因组大小(bp)", "3000000000", int)
    output_file = get_input("输出报告路径", "depth_report.txt")

    print()
    print(f"FASTQ:     {input_file}")
    print(f"基因组:    {genome_size:,} bp")
    print()

    if not os.path.exists(input_file):
        print(f"[ERROR] FASTQ文件不存在: {input_file}")
        sys.exit(1)

    # Count total bases and reads
    print("[Processing] 读取FASTQ文件...")
    total_bases = 0
    read_count = 0
    read_lengths = []

    opener = gzip.open if input_file.endswith('.gz') else open
    mode = 'rt' if input_file.endswith('.gz') else 'r'

    with opener(input_file, mode) as f:
        line_num = 0
        for line in f:
            line_num += 1
            if line_num % 4 == 2:  # Sequence line in FASTQ
                seq_len = len(line.strip())
                total_bases += seq_len
                read_count += 1
                if read_count <= 1000:
                    read_lengths.append(seq_len)

    if read_count == 0:
        print("[ERROR] 未读取到任何read")
        sys.exit(1)

    # Calculate depth and statistics
    depth = total_bases / genome_size if genome_size > 0 else 0
    avg_read_len = total_bases / read_count if read_count > 0 else 0

    # Estimate from first 1000 reads if available
    if read_lengths:
        median_read_len = sorted(read_lengths)[len(read_lengths)//2]
    else:
        median_read_len = avg_read_len

    # Write report
    try:
        with open(output_file, "w") as out:
            out.write("Sequencing Depth Report\n")
            out.write("=" * 40 + "\n")
            out.write(f"Input file:      {input_file}\n")
            out.write(f"Genome size:     {genome_size:,} bp\n")
            out.write(f"Total reads:     {read_count:,}\n")
            out.write(f"Total bases:     {total_bases:,}\n")
            out.write(f"Avg read length: {avg_read_len:.1f} bp\n")
            out.write(f"Median read len: {median_read_len:.1f} bp\n")
            out.write(f"Sequencing depth: {depth:.2f}X\n")
            out.write(f"Coverage:        {total_bases / genome_size * 100:.2f}%\n")
    except Exception as e:
        print(f"[ERROR] 写入报告失败: {e}")
        sys.exit(1)

    # Summary
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  总reads:          {read_count:,}")
    print(f"  总碱基:           {total_bases:,}")
    print(f"  平均read长度:     {avg_read_len:.1f} bp")
    print(f"  测序深度:         {depth:.2f}X")
    print(f"  报告文件:         {output_file}")
    print("=" * 60)
    print()
    print(f"[Done] 测序深度: {depth:.2f}X")


if __name__ == "__main__":
    main()
