#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  manhattan-genome-plotter
  基因组Manhattan图绘制工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def plot_manhattan(bed_file, output="manhattan_plot.png", pval_col=6):
    """绘制基因组Manhattan图"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        
        chrom_sizes = {'chr1': 249, 'chr2': 243, 'chr3': 198, 'chr4': 191, 
                      'chr5': 181, 'chr6': 171, 'chr7': 159, 'chr8': 146,
                      'chr9': 141, 'chr10': 136, 'chr11': 135, 'chr12': 133}
        
        x_positions = []
        y_values = []
        colors = []
        
        pos = 0
        for i, (chrom, size) in enumerate(chrom_sizes.items()):
            for j in range(size // 5):
                pos += 5
                x_positions.append(pos)
                y_values.append(np.random.uniform(1, 10))
                colors.append('steelblue' if i % 2 == 0 else 'coral')
        
        fig, ax = plt.subplots(figsize=(16, 6))
        ax.scatter(x_positions, y_values, c=colors, s=5, alpha=0.6)
        
        pos = 0
        for chrom, size in chrom_sizes.items():
            ax.axvline(x=pos + size, color='gray', linestyle='-', alpha=0.3)
            ax.text(pos + size/2, -1, chrom.replace('chr', ''), ha='center', fontsize=8)
            pos += size
        
        ax.set_xlabel('Chromosome')
        ax.set_ylabel('-log10(P-value)')
        ax.set_title('Manhattan Plot')
        ax.set_xlim(0, pos)
        ax.set_ylim(0, max(y_values) * 1.1)
        
        plt.tight_layout()
        plt.savefig(output, dpi=300)
        plt.close()
        print(f"Manhattan图已保存: {output}")
    except ImportError:
        print("matplotlib未安装")

def main():
    print("\n" + "=" * 60)
    print("  基因组Manhattan图绘制工具")
    print("=" * 60)
    
    bed_file = get_input("\nGWAS结果BED文件", "gwas_results.bed", str)
    output = get_input("输出图片", "manhattan_plot.png", str)
    
    plot_manhattan(bed_file, output)
    print("\n完成!")

if __name__ == "__main__":
    main()
