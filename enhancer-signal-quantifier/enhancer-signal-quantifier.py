#!/usr/bin/env python3
"""增强子信号定量(ATAC/H3K27ac)"""

# 增强子信号定量
print("=" * 60)
print("  🧪 增强子信号定量器")
print("=" * 60)

enhancer_bed = get_input("增强子BED文件路径", "enhancers.bed")
signal_file = get_input("信号文件路径(BEDGRAPH)", "signal.bedgraph")
output_file = get_input("定量结果路径", "enhancer_signal.tsv")
normalize = get_input("是否标准化(RPKM)(yes/no)", "yes")

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
            name = parts[3] if len(parts) > 3 else f"region_{len(regions)}"
            regions.append((chrom, start, end, name))
    return regions

def read_bedgraph(path):
    signals = {}
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('\t')
            chrom = parts[0]
            start = int(parts[1])
            end = int(parts[2])
            value = float(parts[3])
            if chrom not in signals:
                signals[chrom] = []
            signals[chrom].append((start, end, value))
    return signals

enhancers = read_bed(enhancer_bed)
signals = read_bedgraph(signal_file)
print(f"✅ 加载: {len(enhancers)} 增强子, {sum(len(v) for v in signals.values())} 信号区间")

results = []
total_signal = 0

for enh in enhancers:
    echrom, estart, eend, ename = enh
    enh_signal = 0
    overlap_count = 0
    
    if echrom in signals:
        for sstart, send, svalue in signals[echrom]:
            ov_start = max(estart, sstart)
            ov_end = min(eend, send)
            if ov_start < ov_end:
                enh_signal += svalue * (ov_end - ov_start)
                overlap_count += 1
    
    enh_len = eend - estart
    if normalize == "yes" and enh_len > 0:
        rpkm = enh_signal / enh_len / 1000
        results.append((ename, echrom, estart, eend, enh_len, enh_signal, rpkm, overlap_count))
    else:
        results.append((ename, echrom, estart, eend, enh_len, enh_signal, enh_signal, overlap_count))
    total_signal += enh_signal

with open(output_file, 'w') as f:
    header = "name\tchrom\tstart\tend\tlength\tsignal\tnormalized\toverlap_count\n"
    f.write(header)
    for r in results:
        f.write('\t'.join(str(x) for x in r) + '\n')

print(f"\n✅ 定量完成: {len(results)} 增强子")
print(f"  总信号量: {total_signal:.2f}")
print(f"📄 结果: {output_file}")
