#!/usr/bin/env python3
"""FASTA多序列比对可视化"""

# FASTA多序列比对可视化
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

print("=" * 60)
print("  🎨 FASTA多序列比对可视化")
print("=" * 60)

input_file = get_input("FASTA比对文件路径", "alignment.fasta")
plot_out = get_input("可视化图路径", "alignment_view.png")
color_scheme = get_input("配色方案(clustal/blast)", "clustal")
max_seqs = int(get_input("最大显示序列数", "50"))

def read_fasta(path):
    seqs = {}
    current = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith(">"):
                current = line.strip()[1:].split()[0]
                seqs[current] = ""
            elif current:
                seqs[current] += line.strip().upper()
    return seqs

seqs = read_fasta(input_file)
seq_names = list(seqs.keys())[:max_seqs]
seq_len = max(len(seqs[s]) for s in seq_names)
print("✅ 加载: " + str(len(seqs)) + " 序列, 长度: " + str(seq_len))

clustal_colors = {
    "A": "#80D080", "V": "#80D080", "I": "#80D080", "L": "#80D080", "M": "#80D080", "F": "#80D080", "W": "#80D080", "Y": "#80D080",
    "C": "#FFFF00", "G": "#FF8080", "P": "#FF8080", "S": "#FF8080", "T": "#FF8080",
    "N": "#8080FF", "Q": "#8080FF", "H": "#8080FF", "D": "#8080FF", "E": "#8080FF",
    "K": "#FF0000", "R": "#FF0000",
    "-": "#FFFFFF"
}
blast_colors = {"A": "#33FF33", "T": "#FF3333", "G": "#3333FF", "C": "#FFFF33", "-": "#FFFFFF"}

colors = clustal_colors if color_scheme == "clustal" else blast_colors

fig, ax = plt.subplots(figsize=(max(12, seq_len*0.1), max(6, len(seq_names)*0.3)))
for j, seq_name in enumerate(seq_names):
    seq = seqs[seq_name]
    for i in range(len(seq)):
        c = seq[i]
        color = colors.get(c, "#FFFFFF")
        ax.add_patch(plt.Rectangle((i, j), 1, 1, facecolor=color, edgecolor="gray", linewidth=0.3))
        if len(seq_names) <= 20:
            ax.text(i+0.5, j+0.5, c, ha="center", va="center", fontsize=6)

ax.set_xlim(0, seq_len)
ax.set_ylim(0, len(seq_names))
ax.set_yticks([i+0.5 for i in range(len(seq_names))])
ax.set_yticklabels(seq_names, fontsize=8)
ax.set_xlabel("Position")
ax.set_title("Sequence Alignment View")
plt.tight_layout()
plt.savefig(plot_out, dpi=150)
print("\n✅ 可视化完成: " + plot_out)
