#!/usr/bin/env python3
"""火山图标签编辑器(添加/修改/删除基因标签)"""

def main():
    input_file = input("DEG结果CSV(基因,log2FC,padj) [deg_results.csv]: ") or "deg_results.csv"
    output_plot = input("输出火山图路径 [volcano_labeled.png]: ") or "volcano_labeled.png"
    label_genes = input("标注基因(逗号分隔) [TP53,BRCA1,MYC]: ") or "TP53,BRCA1,MYC"
    log2fc_threshold = input("log2FC阈值 [1]: ") or "1"
    padj_threshold = input("padj阈值 [0.05]: ") or "0.05"
    import pandas as pd, matplotlib.pyplot as plt, numpy as np
    df = pd.read_csv(input_file)
    l2fc = float(log2fc_threshold); pt = float(padj_threshold)
    df["neg_log10p"] = -np.log10(df["padj"].clip(lower=1e-300))
    df["sig"] = "NS"
    df.loc[(df["log2FC"] > l2fc) & (df["padj"] < pt), "sig"] = "Up"
    df.loc[(df["log2FC"] < -l2fc) & (df["padj"] < pt), "sig"] = "Down"
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = {"Up": "red", "Down": "blue", "NS": "gray"}
    for s, sub in df.groupby("sig"):
        ax.scatter(sub["log2FC"], sub["neg_log10p"], c=colors[s], s=5, alpha=0.5, label=s)
    lg = [g.strip() for g in label_genes.split(",")]
    for gene in lg:
        row = df[df.iloc[:, 0] == gene]
        if not row.empty:
            r = row.iloc[0]
            ax.annotate(gene, (r["log2FC"], r["neg_log10p"]),
                       xytext=(5, 5), textcoords="offset points", fontsize=8, fontweight="bold")
    ax.axhline(-np.log10(pt), linestyle="--", color="black", alpha=0.3)
    ax.axvline(l2fc, linestyle="--", color="black", alpha=0.3)
    ax.axvline(-l2fc, linestyle="--", color="black", alpha=0.3)
    ax.set_xlabel("log2FC"); ax.set_ylabel("-log10(padj)"); ax.set_title("Volcano Plot")
    ax.legend(); plt.tight_layout(); plt.savefig(output_plot, dpi=150)
    print(f"火山图: {output_plot}")


if __name__ == "__main__":
    main()
