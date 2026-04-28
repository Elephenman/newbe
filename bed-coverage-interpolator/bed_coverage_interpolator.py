#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  bed-coverage-interpolator
  BED区域覆盖深度插值工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def interpolate_coverage(bed_file, depth_file, output="interpolated.bed", window=10):
    """对BED区域进行覆盖深度插值"""
    try:
        import pysam
    except ImportError:
        print("需要安装pysam")
        return
    
    regions = []
    with open(bed_file, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                regions.append((parts[0], int(parts[1]), int(parts[2])))
    
    bam = pysam.AlignmentFile(depth_file, "rb")
    results = []
    
    for chrom, start, end in regions:
        depths = []
        try:
            for pileup in bam.pileup(chrom, start, end):
                if start <= pileup.reference_pos <= end:
                    depths.append(pileup.n)
        except:
            pass
        
        if depths:
            avg_depth = sum(depths) / len(depths)
        else:
            avg_depth = 0
        
        results.append((chrom, start, end, avg_depth))
    
    bam.close()
    
    with open(output, 'w') as f:
        for chrom, start, end, depth in results:
            f.write(f"{chrom}\t{start}\t{end}\t{depth:.2f}\n")
    
    return len(results)

def main():
    print("\n" + "=" * 60)
    print("  BED覆盖深度插值工具")
    print("=" * 60)
    
    bed_file = get_input("\nBED文件路径", "regions.bed", str)
    depth_file = get_input("BAM文件路径", "sample.bam", str)
    output = get_input("输出文件", "interpolated.bed", str)
    
    count = interpolate_coverage(bed_file, depth_file, output)
    print(f"\n处理了 {count} 个区域")
    print(f"结果已保存到: {output}")

if __name__ == "__main__":
    main()
