#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  manhattan-genome-plotter
  基因组Manhattan图绘制工具 - 读取真实GWAS数据，添加5e-8阈值线
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def plot_manhattan(gwas_file, output="manhattan_plot.png", pval_col=6, chrom_col=1, pos_col=2):
    """读取GWAS结果文件绘制Manhattan图"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np

        # Read GWAS data from file
        data = []
        with open(gwas_file, 'r') as f:
            header = f.readline().strip().split('\t')
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) < max(chrom_col, pos_col, pval_col):
                    continue
                try:
                    chrom = parts[chrom_col - 1]
                    pos = int(parts[pos_col - 1])
                    pval = float(parts[pval_col - 1])
                    # Skip invalid p-values
                    if pval <= 0 or pval > 1:
                        continue
                    data.append((chrom, pos, pval))
                except (ValueError, IndexError):
                    continue

        if not data:
            print("未读取到有效GWAS数据")
            return

        # Organize by chromosome and compute cumulative bp positions
        chrom_data = {}
        for chrom, pos, pval in data:
            # Normalize chromosome names
            c = chrom.replace('chr', '')
            if c not in chrom_data:
                chrom_data[c] = []
            chrom_data[c].append((pos, pval))

        # Sort chromosomes naturally
        def chrom_sort_key(c):
            try:
                return (0, int(c))
            except ValueError:
                return (1, c)
        sorted_chroms = sorted(chrom_data.keys(), key=chrom_sort_key)

        # Compute cumulative positions (using bp, not Mb)
        chrom_offsets = {}
        cumulative_pos = 0
        chrom_labels = []
        for c in sorted_chroms:
            chrom_offsets[c] = cumulative_pos
            max_pos = max(p for p, _ in chrom_data[c])
            cumulative_pos += max_pos
            chrom_labels.append((c, chrom_offsets[c] + max_pos / 2))

        # Plot
        fig, ax = plt.subplots(figsize=(16, 6))

        genome_wide_threshold = 5e-8
        threshold_y = -np.log10(genome_wide_threshold)

        for i, c in enumerate(sorted_chroms):
            offset = chrom_offsets[c]
            positions = [offset + p for p, _ in chrom_data[c]]
            log_pvals = [-np.log10(pv) for _, pv in chrom_data[c]]
            color = 'steelblue' if i % 2 == 0 else 'coral'
            ax.scatter(positions, log_pvals, c=color, s=5, alpha=0.6)

        # Add genome-wide significance threshold line at -log10(5e-8)
        ax.axhline(y=threshold_y, color='red', linestyle='--', linewidth=1.5,
                   label=f'Genome-wide threshold (5e-8)')

        # Add suggestive threshold line
        suggestive_y = -np.log10(1e-5)
        ax.axhline(y=suggestive_y, color='blue', linestyle=':', linewidth=1, alpha=0.5,
                   label='Suggestive threshold (1e-5)')

        # Chromosome labels
        for c, x_pos in chrom_labels:
            ax.text(x_pos, -0.5, c, ha='center', fontsize=8)

        # Separator lines between chromosomes
        cumulative_pos = 0
        for c in sorted_chroms:
            max_pos = max(p for p, _ in chrom_data[c])
            cumulative_pos += max_pos
            if c != sorted_chroms[-1]:
                ax.axvline(x=cumulative_pos, color='gray', linestyle='-', alpha=0.2)

        ax.set_xlabel('Chromosome')
        ax.set_ylabel('-log10(P-value)')
        ax.set_title('Manhattan Plot')
        ax.legend(loc='upper right', fontsize=8)
        ax.set_xlim(0, cumulative_pos)
        max_y = max(-np.log10(pv) for _, _, pv in data)
        ax.set_ylim(0, max(max_y * 1.1, threshold_y * 1.2))

        plt.tight_layout()
        plt.savefig(output, dpi=300)
        plt.close()
        print(f"Manhattan图已保存: {output}")
        print(f"基因组显著阈值线: -log10(5e-8) = {threshold_y:.2f}")
    except FileNotFoundError:
        print(f"文件不存在: {gwas_file}")
    except ImportError:
        print("matplotlib未安装")

def main():
    print("\n" + "=" * 60)
    print("  基因组Manhattan图绘制工具")
    print("=" * 60)

    gwas_file = get_input("\nGWAS结果文件路径(TSV)", "gwas_results.tsv", str)
    output = get_input("输出图片", "manhattan_plot.png", str)
    pval_col = get_input("P-value列号", 6, int)
    chrom_col = get_input("染色体列号", 1, int)
    pos_col = get_input("位置列号(bp)", 2, int)

    plot_manhattan(gwas_file, output, pval_col, chrom_col, pos_col)
    print("\n完成!")

if __name__ == "__main__":
    main()
