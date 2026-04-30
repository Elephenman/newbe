#!/usr/bin/env python3
"""FASTQ按read长度范围精确过滤"""

# FASTQ按read长度过滤
import gzip
import matplotlib.pyplot as plt

print("=" * 60)
print("  🧬 FASTQ Read长度过滤器")
print("=" * 60)

input_fq = get_input("输入FASTQ路径", "sample.fastq.gz")
min_len = int(get_input("最小read长度", "50"))
max_len = int(get_input("最大read长度", "300"))
output_fq = get_input("输出FASTQ路径", "filtered.fastq")
stats_file = get_input("统计文件路径", "length_filter_stats.txt")

kept = 0
removed = 0
all_lengths = []

is_gz = input_fq.endswith('.gz')
opener = gzip.open if is_gz else open
mode_in = 'rt' if is_gz else 'r'
mode_out = 'wt' if output_fq.endswith('.gz') else 'w'
out_opener = gzip.open if output_fq.endswith('.gz') else open

with opener(input_fq, mode_in) as fin, out_opener(output_fq, mode_out) as fout:
    while True:
        header = fin.readline()
        if not header:
            break
        seq = fin.readline()
        plus = fin.readline()
        qual = fin.readline()
        
        read_len = len(seq.strip())
        all_lengths.append(read_len)
        
        if min_len <= read_len <= max_len:
            fout.write(header + seq + plus + qual)
            kept += 1
        else:
            removed += 1

total = kept + removed
print(f"\n✅ 过滤完成:")
print(f"  保留: {kept} reads ({kept/total*100:.1f}%)")
print(f"  移除: {removed} reads ({removed/total*100:.1f}%)")
print(f"  长度范围: {min_len}-{max_len} bp")

if all_lengths:
    plt.figure(figsize=(10, 5))
    plt.hist(all_lengths, bins=50, edgecolor='black', alpha=0.7, color='#55A868')
    plt.axvline(min_len, color='red', linestyle='--', label=f'Min={min_len}')
    plt.axvline(max_len, color='red', linestyle='--', label=f'Max={max_len}')
    plt.xlabel("Read Length (bp)")
    plt.ylabel("Count")
    plt.title("Read Length Distribution")
    plt.legend()
    plt.tight_layout()
    plt.savefig("read_length_hist.png", dpi=150)

with open(stats_file, 'w') as f:
    f.write(f"Read Length Filter Stats\n")
    f.write(f"Total: {total}\nKept: {kept}\nRemoved: {removed}\n")
    f.write(f"Min length: {min_len}\nMax length: {max_len}\n")
print(f"📄 统计: {stats_file}")
