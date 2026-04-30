#!/usr/bin/env python3
"""从BAM文件计算并绘制基因组覆盖度分布图"""

def main():
    input_bam = input("输入BAM文件路径 [input.bam]: ") or "input.bam"
    output_plot = input("输出图片路径 [coverage.png]: ") or "coverage.png"
    bin_size = input("窗口大小(bp) [1000]: ") or "1000"
    chrom = input("指定染色体(留空=全部) []: ") or ""
    import pysam, matplotlib.pyplot as plt
    bin_size = int(bin_size)
    bam = pysam.AlignmentFile(input_bam, "rb")
    chroms = [chrom] if chrom else list(bam.references)[:24]
    fig, ax = plt.subplots(figsize=(12, 5))
    for c in chroms:
        try:
            length = bam.get_reference_length(c)
            cov = [bam.count(c, s, min(s+bin_size, length)) for s in range(0, length, bin_size)]
            ax.plot(range(len(cov)), cov, alpha=0.7, label=c)
        except Exception: continue
    bam.close()
    ax.set_xlabel(f"Bin ({bin_size}bp)"); ax.set_ylabel("Read count")
    ax.set_title("BAM Coverage Profile"); ax.legend(fontsize=7, ncol=4)
    plt.tight_layout(); plt.savefig(output_plot, dpi=150)
    print(f"覆盖度图已保存: {output_plot}")


if __name__ == "__main__":
    main()
