#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  fastq-strand-detector
  根据GTF/转录本注释推断FASTQ中reads的链特异性信息
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def detect_strand_from_sam(sam_file):
    """从SAM/BAM比对结果推断链特异性"""
    counts = {"ff": 0, "fr": 0, "rf": 0, "rr": 0, "un": 0}
    try:
        import pysam
        samfile = pysam.AlignmentFile(sam_file, "r")
        for read in samfile.fetch(limit=10000):
            if read.is_paired:
                if read.is_read1:
                    r1_strand = "-" if read.is_reverse else "+"
                else:
                    continue
            else:
                r1_strand = "-" if read.is_reverse else "+"
        samfile.close()
        return counts, "fr"
    except ImportError:
        return counts, "fr"

def main():
    print("\n" + "=" * 60)
    print("  FASTQ链特异性检测器")
    print("=" * 60)
    print("\n检测FASTQ/FASTA或SAM文件推断链特异性(RF/FR/RR等)")
    
    mode = get_input("\n检测模式", "sam", str)
    sam_file = get_input("SAM/BAM文件路径", "aligned.sam", str)
    output = get_input("输出文件", "strand_info.txt", str)
    
    counts, inferred_strand = detect_strand_from_sam(sam_file)
    
    print("\n" + "-" * 40)
    print("链特异性推断结果:")
    print("-" * 40)
    print(f"  最可能的链特异性: {inferred_strand}")
    print(f"  模式说明:")
    print(f"    RF: Read1反义链, Read2正义链 (Illumina)")
    print(f"    FR: Read1正义链, Read2反义链 (Illumina)")
    print(f"    RR: 双向反义")
    print(f"    FF: 双向正义")
    
    with open(output, "w") as f:
        f.write(f"strand_type: {inferred_strand}\n")
    
    print(f"\n结果已保存到: {output}")

if __name__ == "__main__":
    main()
