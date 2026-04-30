#!/usr/bin/env python3
"""SAM/BAM转FASTQ+可选拆分paired-end
解析SAM格式文件，提取序列和质量信息，输出FASTQ格式
支持paired-end拆分为R1/R2
"""

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


def parse_cigar(cigar):
    """解析CIGAR字符串，返回参考序列和read的消耗长度"""
    ref_len = 0
    read_len = 0
    num = ''
    for c in cigar:
        if c.isdigit():
            num += c
        else:
            n = int(num) if num else 0
            num = ''
            if c in 'MND=X':
                ref_len += n
            if c in 'MIS=X':
                read_len += n
    return ref_len, read_len


def reverse_complement(seq):
    """反向互补"""
    comp = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N',
            'a': 't', 't': 'a', 'g': 'c', 'c': 'g', 'n': 'n'}
    return ''.join(comp.get(c, 'N') for c in reversed(seq))


def main():
    print("=" * 60)
    print("  SAM/BAM转FASTQ+可选拆分paired-end")
    print("=" * 60)
    print()

    input_file = get_input("输入SAM文件路径", "input.sam")
    output_prefix = get_input("输出FASTQ前缀", "output")
    paired = get_input("是否paired-end(yes/no)", "no")
    filter_mapped = get_input("仅输出mapped reads(yes/no)", "no")

    print()
    print(f"输入:      {input_file}")
    print(f"输出前缀:  {output_prefix}")
    print(f"Paired:    {paired}")
    print()

    if not os.path.exists(input_file):
        print(f"[ERROR] 输入文件不存在: {input_file}")
        sys.exit(1)

    is_paired = paired.lower() in ('yes', 'y')
    filter_map = filter_mapped.lower() in ('yes', 'y')

    # Open output files
    if is_paired:
        r1_file = output_prefix + "_R1.fastq"
        r2_file = output_prefix + "_R2.fastq"
        out_r1 = open(r1_file, 'w')
        out_r2 = open(r2_file, 'w')
    else:
        fq_file = output_prefix + ".fastq"
        out_r1 = open(fq_file, 'w')
        out_r2 = None

    # Process SAM
    print("[Processing] 解析SAM文件...")
    total_reads = 0
    written_reads = 0
    r1_reads = 0
    r2_reads = 0

    opener = gzip.open if input_file.endswith('.gz') else open
    mode = 'rt' if input_file.endswith('.gz') else 'r'

    with opener(input_file, mode) as f:
        for line in f:
            if line.startswith('@'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 11:
                continue

            total_reads += 1
            qname = parts[0]
            flag = int(parts[1])
            seq = parts[9]
            qual = parts[10]

            # Skip unmapped if filter
            if filter_map and (flag & 4):
                continue

            # Skip if sequence is *
            if seq == '*' or qual == '*':
                continue

            # Handle reverse strand
            is_reverse = bool(flag & 16)
            if is_reverse:
                seq = reverse_complement(seq)
                qual = qual[::-1]

            # Determine read number for paired-end
            is_read1 = bool(flag & 64)
            is_read2 = bool(flag & 128)

            fastq_entry = f"@{qname}\n{seq}\n+\n{qual}\n"

            if is_paired:
                if is_read1:
                    out_r1.write(fastq_entry)
                    r1_reads += 1
                elif is_read2:
                    out_r2.write(fastq_entry)
                    r2_reads += 1
                else:
                    # Unpaired read in paired mode - write to R1
                    out_r1.write(fastq_entry)
                    r1_reads += 1
            else:
                out_r1.write(fastq_entry)

            written_reads += 1

    out_r1.close()
    if out_r2:
        out_r2.close()

    # Summary
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  总读取数:       {total_reads}")
    print(f"  写入reads:      {written_reads}")
    if is_paired:
        print(f"  R1 reads:       {r1_reads}")
        print(f"  R2 reads:       {r2_reads}")
        print(f"  R1输出:         {r1_file}")
        print(f"  R2输出:         {r2_file}")
    else:
        print(f"  FASTQ输出:      {fq_file}")
    print("=" * 60)
    print()
    print("[Done] sam_to_fastq_converter completed successfully!")


if __name__ == "__main__":
    main()
