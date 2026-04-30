#!/usr/bin/env python3
"""基因组重复序列标注+mask文件生成
从RepeatMasker输出或BED文件读取重复区域，对FASTA序列进行soft/hard mask
"""

import os
import sys


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    try:
        return dtype(val)
    except (ValueError, TypeError):
        return default


def parse_repeatmasker(filepath):
    """解析RepeatMasker .out格式"""
    regions = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('SW') or line.startswith('score') or line.startswith('-'):
                continue
            parts = line.split()
            if len(parts) < 9:
                continue
            try:
                chrom = parts[4]
                start = int(parts[5])
                end = int(parts[6])
                rtype = parts[8]
                regions.append((chrom, start, end, rtype))
            except (ValueError, IndexError):
                continue
    return regions


def parse_bed(filepath):
    """解析BED格式的重复区域"""
    regions = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#') or line.startswith('track') or line.startswith('browser'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 3:
                continue
            try:
                chrom = parts[0]
                start = int(parts[1])
                end = int(parts[2])
                rtype = parts[3] if len(parts) > 3 else "repeat"
                regions.append((chrom, start, end, rtype))
            except (ValueError, IndexError):
                continue
    return regions


def parse_fasta(filepath):
    """解析FASTA文件"""
    sequences = {}
    current_id = None
    current_seq = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_id:
                    sequences[current_id] = ''.join(current_seq)
                current_id = line[1:].split()[0]
                current_seq = []
            elif line and current_id:
                current_seq.append(line)
    if current_id:
        sequences[current_id] = ''.join(current_seq)
    return sequences


def mask_sequence(seq, regions, mask_type='soft'):
    """对序列进行mask"""
    seq_list = list(seq)
    for chrom, start, end, rtype in regions:
        # BED is 0-based half-open, RepeatMasker is 1-based inclusive
        # Convert to 0-based for Python indexing
        s = max(0, start - 1)  # 1-based to 0-based
        e = min(len(seq_list), end)
        if mask_type == 'soft':
            for i in range(s, e):
                seq_list[i] = seq_list[i].lower()
        else:  # hard mask
            for i in range(s, e):
                seq_list[i] = 'N'
    return ''.join(seq_list)


def main():
    print("=" * 60)
    print("  基因组重复序列标注+mask文件生成")
    print("=" * 60)
    print()

    repeat_file = get_input("重复区域文件(BED/RepeatMasker .out)", "repeats.bed")
    fasta_file = get_input("基因组FASTA路径", "genome.fa")
    output_file = get_input("Masked FASTA输出路径", "genome_masked.fa")
    mask_type = get_input("Mask类型(soft/hard)", "soft")
    format_type = get_input("重复区域文件格式(bed/rm)", "bed")

    print()
    print(f"重复区域:  {repeat_file}")
    print(f"FASTA:     {fasta_file}")
    print(f"输出:      {output_file}")
    print(f"Mask类型:  {mask_type}")
    print()

    # Validate inputs
    if not os.path.exists(repeat_file):
        print(f"[ERROR] 重复区域文件不存在: {repeat_file}")
        sys.exit(1)
    if not os.path.exists(fasta_file):
        print(f"[ERROR] FASTA文件不存在: {fasta_file}")
        sys.exit(1)

    # Parse repeat regions
    print("[Processing] 读取重复区域...")
    if format_type == 'rm':
        regions = parse_repeatmasker(repeat_file)
    else:
        regions = parse_bed(repeat_file)
    print(f"[Processing] 找到 {len(regions)} 个重复区域")

    # Group by chromosome
    regions_by_chr = {}
    for chrom, start, end, rtype in regions:
        regions_by_chr.setdefault(chrom, []).append((chrom, start, end, rtype))

    # Parse and mask FASTA
    print("[Processing] 读取FASTA并mask...")
    total_masked = 0
    with open(fasta_file, 'r') as fin, open(output_file, 'w') as fout:
        current_id = None
        current_seq = []
        for line in fin:
            if line.startswith('>'):
                # Process previous sequence
                if current_id:
                    seq = ''.join(current_seq)
                    chr_regions = regions_by_chr.get(current_id, [])
                    masked_seq = mask_sequence(seq, chr_regions, mask_type)
                    masked_bases = sum(1 for a, b in zip(seq, masked_seq) if a != b)
                    total_masked += masked_bases
                    # Write in 80-char lines
                    for i in range(0, len(masked_seq), 80):
                        fout.write(masked_seq[i:i+80] + '\n')
                current_id = line[1:].split()[0]
                current_seq = []
                fout.write(line)
            else:
                current_seq.append(line.strip())

        # Process last sequence
        if current_id:
            seq = ''.join(current_seq)
            chr_regions = regions_by_chr.get(current_id, [])
            masked_seq = mask_sequence(seq, chr_regions, mask_type)
            masked_bases = sum(1 for a, b in zip(seq, masked_seq) if a != b)
            total_masked += masked_bases
            for i in range(0, len(masked_seq), 80):
                fout.write(masked_seq[i:i+80] + '\n')

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  重复区域数:      {len(regions)}")
    print(f"  Masked碱基数:    {total_masked}")
    print(f"  Mask类型:        {mask_type}")
    print(f"  输出文件:        {output_file}")
    print("=" * 60)
    print()
    print("[Done] repeat_region_masker completed successfully!")


if __name__ == "__main__":
    main()
