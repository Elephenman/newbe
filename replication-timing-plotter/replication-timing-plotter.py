#!/usr/bin/env python3
"""复制时序(Repli-seq)数据可视化"""

def main():
    input_file = input("Repli-seq信号文件(CSV: chr,start,end,early,late) [repliseq.csv]: ") or "repliseq.csv"
    output_plot = input("输出图片路径 [replication_timing.png]: ") or "replication_timing.png"
    chrom = input("指定染色体 [chr1]: ") or "chr1"
    import pandas as pd, matplotlib.pyplot as plt
    df = pd.read_csv(input_file)
    df["ratio"] = (df["early"]+1) / (df["late"]+1)
    sub = df[df["chr"] == chrom] if chrom in df["chr"].values else df
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(sub["start"], sub["ratio"], alpha=0.7, linewidth=0.5)
    ax.axhline(y=1, color="red", linestyle="--", alpha=0.5)
    ax.set_xlabel("Position"); ax.set_ylabel("Early/Late Ratio")
    ax.set_title(f"Replication Timing - {chrom}")
    plt.tight_layout(); plt.savefig(output_plot, dpi=150)
    print(f"复制时序图: {output_plot}")


if __name__ == "__main__":
    main()
