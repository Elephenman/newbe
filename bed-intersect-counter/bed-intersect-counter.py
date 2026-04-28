#!/usr/bin/env python3
"""BED文件交集计数+重叠统计"""

# BED文件交集计数
print("=" * 60)
print("  🧬 BED文件交集计数器")
print("=" * 60)

bed_a = get_input("BED文件A路径", "file_a.bed")
bed_b = get_input("BED文件B路径", "file_b.bed")
min_overlap = float(get_input("最小重叠比例", "0.5"))
output_file = get_input("输出结果路径", "intersect_results.tsv")
report_file = get_input("统计报告路径", "intersect_report.txt")

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

try:
    regions_a = read_bed(bed_a)
    regions_b = read_bed(bed_b)
except FileNotFoundError as e:
    print(f"❌ {e}")
    exit(1)

intersects = []
a_count = 0
b_count = 0

for ra in regions_a:
    for rb in regions_b:
        if ra[0] != rb[0]:
            continue
        overlap_start = max(ra[1], rb[1])
        overlap_end = min(ra[2], rb[2])
        if overlap_start < overlap_end:
            overlap_len = overlap_end - overlap_start
            a_len = ra[2] - ra[1]
            b_len = rb[2] - rb[1]
            overlap_ratio = overlap_len / min(a_len, b_len)
            if overlap_ratio >= min_overlap:
                intersects.append((ra[0], overlap_start, overlap_end, ra[3], rb[3], overlap_ratio))
                a_count += 1
                b_count += 1

with open(output_file, 'w') as f:
    f.write("chrom\tstart\tend\tname_A\tname_B\toverlap_ratio\n")
    for item in intersects:
        f.write('\t'.join(str(x) for x in item) + '\n')

with open(report_file, 'w') as f:
    f.write(f"BED Intersect Report\n")
    f.write(f"Regions in A: {len(regions_a)}\n")
    f.write(f"Regions in B: {len(regions_b)}\n")
    f.write(f"Overlapping pairs: {len(intersects)}\n")
    f.write(f"Min overlap threshold: {min_overlap}\n")

print(f"\n✅ 计算完成:")
print(f"  A文件区间数: {len(regions_a)}")
print(f"  B文件区间数: {len(regions_b)}")
print(f"  有效交集数: {len(intersects)}")
print(f"📄 结果: {output_file}")
