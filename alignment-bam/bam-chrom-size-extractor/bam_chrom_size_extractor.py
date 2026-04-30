#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  bam-chrom-size-extractor
  从BAM文件提取染色体长度信息
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def extract_chrom_sizes(bam_file, output="chrom.sizes"):
    """从BAM头信息提取染色体长度"""
    try:
        import pysam
    except ImportError:
        print("需要安装pysam")
        return []
    
    chroms = []
    try:
        bam = pysam.AlignmentFile(bam_file, "rb")
        header = bam.header.to_dict()
        
        if "SQ" in header:
            for sq in header["SQ"]:
                chroms.append((sq["SN"], sq["LN"]))
        
        bam.close()
    except Exception as e:
        print(f"错误: {e}")
    
    with open(output, 'w') as f:
        for chrom, length in chroms:
            f.write(f"{chrom}\t{length}\n")
    
    return chroms

def main():
    print("\n" + "=" * 60)
    print("  BAM染色体长度提取工具")
    print("=" * 60)
    
    bam_file = get_input("\nBAM文件路径", "sample.bam", str)
    output = get_input("输出染色体文件", "chrom.sizes", str)
    
    chroms = extract_chrom_sizes(bam_file, output)
    
    print(f"\n提取了 {len(chroms)} 条染色体")
    print("\n前10条染色体:")
    for chrom, length in chroms[:10]:
        print(f"  {chrom}: {length:,} bp")
    print(f"\n结果已保存到: {output}")

if __name__ == "__main__":
    main()
