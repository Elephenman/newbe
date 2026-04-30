#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""蛋白质结构域注释+可视化分布"""
import os, sys, re

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def map_protein_domains(protein_file, output_file=None, make_plot=True):
    """从蛋白质序列FASTA和/或InterProScan结果中注释结构域

    输入格式1 (InterProScan TSV): protein_id\tsuperfamily\tstart\tend\tdomain_name
    输入格式2 (FASTA): 仅蛋白质序列，需InterProScan结果文件
    """
    domains = {}  # protein_id -> list of (start, end, domain_name, superfamily)

    with open(protein_file, 'r') as f:
        first_line = f.readline().strip()
        f.seek(0)

        if first_line.startswith('>'):
            # FASTA格式 - 读取序列信息
            current_id = None
            sequences = {}
            for line in f:
                line = line.strip()
                if line.startswith('>'):
                    current_id = line[1:].split()[0]
                    sequences[current_id] = ""
                else:
                    sequences[current_id] += line

            print(f"Loaded {len(sequences)} protein sequences")
            print("Note: Domain annotation requires InterProScan results.")
            print("      Use InterProScan TSV as input for domain mapping.")

            # 输出序列长度信息
            out_path = output_file or os.path.splitext(protein_file)[0] + "_protein_info.tsv"
            with open(out_path, 'w') as out:
                out.write("protein_id\tlength\tsequence\n")
                for pid, seq in sequences.items():
                    out.write(f"{pid}\t{len(seq)}\t{seq[:50]}...\n")

            print(f"  Protein info: {out_path}")
            return

        else:
            # InterProScan TSV格式
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                fields = line.split('\t')
                if len(fields) >= 4:
                    protein_id = fields[0]
                    try:
                        start = int(fields[2]) if fields[2].isdigit() else int(fields[4]) if len(fields) > 4 and fields[4].isdigit() else 0
                        end = int(fields[3]) if fields[3].isdigit() else int(fields[5]) if len(fields) > 5 and fields[5].isdigit() else 0
                    except (ValueError, IndexError):
                        start, end = 0, 0

                    domain_name = fields[1] if len(fields) > 1 else "Unknown"
                    superfamily = fields[6] if len(fields) > 6 else ""

                    # Try to get better names
                    if len(fields) > 8 and fields[8]:
                        domain_name = fields[8]
                    elif len(fields) > 7 and fields[7]:
                        domain_name = fields[7]

                    domains.setdefault(protein_id, []).append((start, end, domain_name, superfamily))

    if not domains:
        print("[ERROR] No domain data found. Expected InterProScan TSV format.")
        return

    # 输出
    out_path = output_file or os.path.splitext(protein_file)[0] + "_domains.tsv"
    with open(out_path, 'w') as out:
        out.write("protein_id\tstart\tend\tdomain_name\tsuperfamily\n")
        for pid, domain_list in sorted(domains.items()):
            for start, end, name, sf in sorted(domain_list, key=lambda x: x[0]):
                out.write(f"{pid}\t{start}\t{end}\t{name}\t{sf}\n")

    # 绘图
    if make_plot:
        try:
            import matplotlib; matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            import matplotlib.patches as patches

            protein_ids = sorted(domains.keys())
            n_proteins = len(protein_ids)

            fig, ax = plt.subplots(figsize=(14, max(3, n_proteins * 0.8)))

            colors = plt.cm.Set2(range(20))
            domain_colors = {}
            color_idx = 0

            for i, pid in enumerate(protein_ids):
                y = n_proteins - i
                # 画蛋白质全长线
                max_end = max(d[1] for d in domains[pid])
                ax.plot([0, max_end], [y, y], 'k-', linewidth=2)

                for start, end, name, sf in domains[pid]:
                    if name not in domain_colors:
                        domain_colors[name] = colors[color_idx % len(colors)]
                        color_idx += 1

                    rect = patches.FancyBboxPatch(
                        (start, y - 0.3), end - start, 0.6,
                        boxstyle="round,pad=0.05",
                        facecolor=domain_colors[name], edgecolor='black', linewidth=0.5
                    )
                    ax.add_patch(rect)
                    if end - start > 50:
                        ax.text((start + end) / 2, y, name[:15], ha='center', va='center', fontsize=6)

                ax.text(-10, y, pid[:20], ha='right', va='center', fontsize=8)

            ax.set_xlim(-50, max(max(d[1] for d in domains[pid]) for pid in protein_ids) * 1.05)
            ax.set_ylim(0.5, n_proteins + 0.5)
            ax.set_xlabel('Amino acid position')
            ax.set_title('Protein Domain Architecture')
            ax.set_yticks([])
            plt.tight_layout()

            plot_path = os.path.splitext(protein_file)[0] + "_domains.png"
            plt.savefig(plot_path, dpi=200)
            plt.close()
            print(f"  Domain plot: {plot_path}")

        except ImportError:
            print("  [INFO] matplotlib required for domain plot")

    total_domains = sum(len(v) for v in domains.values())
    print(f"Protein domain mapping complete")
    print(f"  Proteins: {len(domains)}")
    print(f"  Domains: {total_domains}")
    unique_domains = set()
    for dl in domains.values():
        for _, _, name, _ in dl:
            unique_domains.add(name)
    print(f"  Unique domain types: {len(unique_domains)}")
    print(f"  Output: {out_path}")

def main():
    print("=" * 60)
    print("  蛋白质结构域注释+可视化分布")
    print("=" * 60)
    protein_file = get_input("InterProScan TSV或蛋白质FASTA路径", "interproscan.tsv")
    output = get_input("输出文件路径", "")
    plot = get_input("是否出图(yes/no)", "yes")
    map_protein_domains(protein_file, output or None, plot.lower() in ('yes', 'y'))

if __name__ == "__main__":
    main()
