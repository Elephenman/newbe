#!/usr/bin/env python3
"""基因共出现频率分析+网络构建"""

# 基因共出现频率分析
from collections import defaultdict
from itertools import combinations

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


print("=" * 60)
print("  📊 基因共出现频率分析")
print("=" * 60)

input_file = get_input("基因列表文件(每行一组基因)", "gene_groups.txt")
min_co = int(get_input("最小共出现次数", "2"))
output_file = get_input("网络输出路径", "co_occurrence_network.tsv")
plot_file = get_input("网络图路径", "co_occurrence_network.png")

gene_groups = []
with open(input_file, 'r') as f:
    for line in f:
        genes = [g.strip() for g in line.strip().split(',') if g.strip()]
        if genes:
            gene_groups.append(set(genes))

print(f"✅ 加载 {len(gene_groups)} 组基因")

co_occurrence = defaultdict(int)
for group in gene_groups:
    for pair in combinations(group, 2):
        co_occurrence[tuple(sorted(pair))] += 1

filtered = {k: v for k, v in co_occurrence.items() if v >= min_co}
print(f"  共出现对: {len(filtered)} (阈值>={min_co})")

gene_freq = defaultdict(int)
for group in gene_groups:
    for gene in group:
        gene_freq[gene] += 1

with open(output_file, 'w') as f:
    f.write("gene_A\tgene_B\tco_occurrence\tfreq_A\tfreq_B\n")
    for (a, b), count in sorted(filtered.items(), key=lambda x: -x[1]):
        f.write(f"{a}\t{b}\t{count}\t{gene_freq[a]}\t{gene_freq[b]}\n")

print(f"\n📄 网络数据: {output_file}")

top_pairs = sorted(filtered.items(), key=lambda x: -x[1])[:20]
print(f"  Top 5共出现对:")
for (a, b), c in top_pairs[:5]:
    print(f"    {a}-{b}: {c}次")
