#!/usr/bin/env python3
"""CTCF绝缘子边界识别"""

# CTCF绝缘子边界识别
print("=" * 60)
print("  🧪 CTCF绝缘子边界识别器")
print("=" * 60)

ctcf_bed = get_input("CTCF peak BED文件路径", "ctcf_peaks.bed")
hic_file = get_input("Hi-C接触矩阵路径(NA=无)", "NA")
min_score = float(get_input("最小边界评分", "0.5"))
output_file = get_input("绝缘子边界路径", "insulator_boundaries.tsv")

ctcf_peaks = []
with open(ctcf_bed, 'r') as f:
    for line in f:
        if line.startswith('#') or not line.strip():
            continue
        parts = line.strip().split('\t')
        chrom = parts[0]
        start = int(parts[1])
        end = int(parts[2])
        score = float(parts[4]) if len(parts) > 4 else 1.0
        strand = parts[5] if len(parts) > 5 else '+'
        ctcf_peaks.append((chrom, start, end, score, strand))

print(f"✅ 加载CTCF peaks: {len(ctcf_peaks)}")

boundaries = []
prev = None

for peak in ctcf_peaks:
    chrom, start, end, score, strand = peak
    boundary_score = score
    
    if prev and prev[0] == chrom:
        distance = start - prev[2]
        if 100 < distance < 2000:
            orientation_match = (prev[4] == '+' and strand == '-') or (prev[4] == '-' and strand == '+')
            if orientation_match:
                boundary_score = score * 1.5
    
    if boundary_score >= min_score:
        center = (start + end) // 2
        boundaries.append((chrom, center-500, center+500, boundary_score, strand, peak))

with open(output_file, 'w') as f:
    f.write("chrom\tstart\tend\tboundary_score\torientation\tctcf_peak\n")
    for b in boundaries:
        peak_str = f"{b[5][0]}:{b[5][1]}-{b[5][2]}"
        f.write(f"{b[0]}\t{b[1]}\t{b[2]}\t{b[3]:.2f}\t{b[4]}\t{peak_str}\n")

print(f"\n✅ 识别完成: {len(boundaries)} 个绝缘子边界")
print(f"  CTCF peaks输入: {len(ctcf_peaks)}")
print(f"  边界评分阈值: {min_score}")
print(f"📄 结果: {output_file}")
