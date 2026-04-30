#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  bam-readcount-summarizer
  批量汇总BAM文件中基因组位置reads覆盖信息
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def summarize_readcounts(bam_file, bed_file=None, output="readcount_summary.txt"):
    """汇总readcount结果"""
    try:
        import pysam
    except ImportError:
        print("错误: 需要安装pysam库")
        return
    
    result = {
        "total_reads": 0,
        "mapped_reads": 0,
        "unmapped_reads": 0,
        "proper_pairs": 0,
        "duplicate_reads": 0,
        "avg_depth": 0.0
    }
    
    try:
        bam = pysam.AlignmentFile(bam_file, "rb")
        result["total_reads"] = bam.mapped + bam.unmapped
        result["mapped_reads"] = bam.mapped
        result["unmapped_reads"] = bam.unmapped
        
        depth_sum = 0
        depth_count = 0
        for pileup in bam.pileup(until_eof=True):
            depth_sum += pileup.n
            depth_count += 1
        
        if depth_count > 0:
            result["avg_depth"] = depth_sum / depth_count
        
        bam.close()
    except Exception as e:
        print(f"警告: {e}")
    
    return result

def main():
    print("\n" + "=" * 60)
    print("  BAM ReadCount 汇总工具")
    print("=" * 60)
    print("\n汇总BAM文件中reads覆盖信息并输出统计报告")
    
    bam_file = get_input("\nBAM文件路径", "sample.bam", str)
    output = get_input("输出文件", "readcount_summary.txt", str)
    
    results = summarize_readcounts(bam_file, output=output)
    
    print("\n" + "-" * 40)
    print("BAM 统计摘要:")
    print("-" * 40)
    print(f"  总reads数: {results['total_reads']:,}")
    print(f"  Mapped reads: {results['mapped_reads']:,}")
    print(f"  Unmapped reads: {results['unmapped_reads']:,}")
    print(f"  平均深度: {results['avg_depth']:.2f}x")
    
    with open(output, "w") as f:
        f.write("BAM ReadCount Summary\n")
        f.write("=" * 40 + "\n")
        for k, v in results.items():
            f.write(f"{k}: {v}\n")
    
    print(f"\n结果已保存到: {output}")

if __name__ == "__main__":
    main()
