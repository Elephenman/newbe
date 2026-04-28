#!/usr/bin/env python3
"""复制起始点预测与注释"""

# 复制起始点预测
print("=" * 60)
print("  🧪 复制起始点预测器")
print("=" * 60)

input_fa = get_input("基因组FASTA路径", "genome.fa")
data_file = get_input("Repli-seq/ori数据路径(NA=纯序列预测)", "NA")
window = int(get_input("搜索窗口大小(bp)", "1000"))
output_file = get_input("预测结果路径", "replication_origins.tsv")

def read_fasta(path):
    seqs = {}
    current = None
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('>'):
                current = line.strip()[1:].split()[0]
                seqs[current] = ''
            elif current:
                seqs[current] += line.strip().upper()
    return seqs

seqs = read_fasta(input_fa)
print(f"✅ 加载 {len(seqs)} 染色体")

origins = []

for chrom, seq in seqs.items():
    for i in range(0, len(seq) - window + 1, window // 2):
        subseq = seq[i:i+window]
        at_pct = (subseq.count('A') + subseq.count('T')) / len(subseq) * 100
        gc_pct = (subseq.count('G') + subseq.count('C')) / len(subseq) * 100
        
        # AT-richness score (ori regions tend to be AT-rich)
        at_score = at_pct / 100
        
        # Check for ORC-like motifs (simplified)
        has_watson_crick = False
        for motif in ['ATATAT', 'TTATTT', 'AATATA', 'ATAAAT']:
            if motif in subseq:
                has_watson_crick = True
                break
        
        # Directionality (asymmetry score)
        g_skew = 0
        c_skew = 0
        for j in range(len(subseq)):
            if subseq[j] == 'G':
                g_skew += 1
            elif subseq[j] == 'C':
                c_skew += 1
        skew = (g_skew - c_skew) / (g_skew + c_skew + 1)
        
        combined_score = at_score * 0.6 + (0.4 if has_watson_crick else 0) + abs(skew) * 0.2
        
        if combined_score >= 0.7:
            origins.append((chrom, i, i+window, combined_score, at_pct, has_watson_crick, skew))

origins = sorted(origins, key=lambda x: -x[3])

with open(output_file, 'w') as f:
    f.write("chrom\tstart\tend\tscore\tat_pct\thas_motif\tg_c_skew\n")
    for o in origins:
        f.write('\t'.join(str(x) for x in o) + '\n')

print(f"\n✅ 预测完成: {len(origins)} 个候选复制起始点")
top5 = origins[:5]
for o in top5:
    print(f"  {o[0]}:{o[1]}-{o[2]} 评分={o[3]:.2f}")
print(f"📄 结果: {output_file}")
