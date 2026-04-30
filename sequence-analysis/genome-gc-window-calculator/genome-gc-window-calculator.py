#!/usr/bin/env python3
"""基因组GC含量滑动窗口计算"""

# 基因组GC含量滑动窗口计算
import matplotlib.pyplot as plt

print("=" * 60)
print("  🧬 基因组GC含量滑动窗口计算")
print("=" * 60)

input_fa = get_input("基因组FASTA路径", "genome.fa")
window = int(get_input("滑动窗口大小(bp)", "1000"))
step = int(get_input("滑动步长(bp)", "500"))
output_file = get_input("输出文件路径", "gc_windows.tsv")
plot_out = get_input("GC分布图路径", "gc_distribution.png")

def read_fasta(path):
    sequences = {}
    current = None
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('>'):
                current = line.strip()[1:].split()[0]
                sequences[current] = ''
            elif current:
                sequences[current] += line.strip().upper()
    return sequences

try:
    seqs = read_fasta(input_fa)
except FileNotFoundError:
    print(f"❌ 文件不存在: {input_fa}")
    exit(1)

results = []
all_gc = []

with open(output_file, 'w') as f:
    f.write("chrom\tstart\tend\tgc_content\tlength\n")
    for chrom, seq in seqs.items():
        for i in range(0, len(seq) - window + 1, step):
            subseq = seq[i:i+window]
            gc = (subseq.count('G') + subseq.count('C')) / len(subseq) * 100 if len(subseq) > 0 else 0
            f.write(f"{chrom}\t{i}\t{i+window}\t{gc:.2f}\t{len(subseq)}\n")
            results.append((chrom, i, gc))
            all_gc.append(gc)

print(f"\n✅ 计算完成: {len(results)} 个窗口")
print(f"  总染色体数: {len(seqs)}")
print(f"  平均GC: {sum(all_gc)/len(all_gc):.2f}%")

plt.figure(figsize=(12, 5))
plt.hist(all_gc, bins=50, edgecolor='black', alpha=0.7, color='#4C72B0')
plt.xlabel("GC Content (%)")
plt.ylabel("Window Count")
plt.title("GC Content Distribution (window={window}bp, step={step}bp)")
plt.tight_layout()
plt.savefig(plot_out, dpi=150)
print(f"📊 GC分布图: {plot_out}")
