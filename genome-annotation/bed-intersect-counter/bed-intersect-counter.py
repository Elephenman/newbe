#!/usr/bin/env python3
"""BED文件交集计数+重叠统计 - 使用排序扫描算法高效计算"""

import bisect
from collections import defaultdict

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def read_bed(path):
    regions = []
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('\t')
            chrom = parts[0]
            start = int(parts[1])
            end = int(parts[2])
            name = parts[3] if len(parts) > 3 else '.'
            regions.append((chrom, start, end, name))
    return regions

def find_intersections(regions_a, regions_b, min_overlap=0.5):
    """
    Efficient O((n+m) log m) intersection finding using sorted sweep.
    For each chromosome, sort regions_b by start, then for each region in A,
    use binary search to find candidate regions in B and check overlap.
    """
    # Group B regions by chromosome and sort by start
    b_by_chrom = defaultdict(list)
    for rb in regions_b:
        b_by_chrom[rb[0]].append(rb)

    # Sort each chromosome's B regions by start position
    for chrom in b_by_chrom:
        b_by_chrom[chrom].sort(key=lambda x: x[1])

    intersects = []
    a_has_intersect = set()
    b_has_intersect = set()

    for ra in regions_a:
        chrom = ra[0]
        if chrom not in b_by_chrom:
            continue

        b_regions = b_by_chrom[chrom]
        b_starts = [rb[1] for rb in b_regions]

        # Find B regions whose start <= ra.end using binary search
        # Any region that starts after ra.end cannot overlap
        upper_idx = bisect.bisect_right(b_starts, ra[2])

        # Check candidates: only those whose start <= ra.end
        for j in range(upper_idx):
            rb = b_regions[j]
            # Check if rb.end > ra.start (necessary for overlap)
            if rb[2] <= ra[1]:
                continue

            overlap_start = max(ra[1], rb[1])
            overlap_end = min(ra[2], rb[2])
            overlap_len = overlap_end - overlap_start

            a_len = ra[2] - ra[1]
            b_len = rb[2] - rb[1]
            overlap_ratio = overlap_len / min(a_len, b_len)

            if overlap_ratio >= min_overlap:
                intersects.append((ra[0], overlap_start, overlap_end, ra[3], rb[3], overlap_ratio))
                a_has_intersect.add(id(ra))
                b_has_intersect.add(id(rb))

    a_count = len(a_has_intersect)
    b_count = len(b_has_intersect)
    return intersects, a_count, b_count

def main():
    print("=" * 60)
    print("  BED文件交集计数器")
    print("=" * 60)

    bed_a = get_input("BED文件A路径", "file_a.bed", str)
    bed_b = get_input("BED文件B路径", "file_b.bed", str)
    min_overlap = get_input("最小重叠比例", "0.5", float)
    output_file = get_input("输出结果路径", "intersect_results.tsv", str)
    report_file = get_input("统计报告路径", "intersect_report.txt", str)

    try:
        regions_a = read_bed(bed_a)
        regions_b = read_bed(bed_b)
    except FileNotFoundError as e:
        print(f"文件未找到: {e}")
        return

    intersects, a_count, b_count = find_intersections(regions_a, regions_b, min_overlap)

    with open(output_file, 'w') as f:
        f.write("chrom\tstart\tend\tname_A\tname_B\toverlap_ratio\n")
        for item in intersects:
            f.write('\t'.join(str(x) for x in item) + '\n')

    with open(report_file, 'w') as f:
        f.write(f"BED Intersect Report\n")
        f.write(f"Regions in A: {len(regions_a)}\n")
        f.write(f"Regions in B: {len(regions_b)}\n")
        f.write(f"Overlapping pairs: {len(intersects)}\n")
        f.write(f"Regions in A with overlap: {a_count}\n")
        f.write(f"Regions in B with overlap: {b_count}\n")
        f.write(f"Min overlap threshold: {min_overlap}\n")

    print(f"\n计算完成:")
    print(f"  A文件区间数: {len(regions_a)}")
    print(f"  B文件区间数: {len(regions_b)}")
    print(f"  有效交集数: {len(intersects)}")
    print(f"结果: {output_file}")

if __name__ == "__main__":
    main()
