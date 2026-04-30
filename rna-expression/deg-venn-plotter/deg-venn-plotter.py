#!/usr/bin/env python3
"""对多组DEG结果绘制韦恩图，展示共有/特有基因"""

def main():
    deg_files = input("DEG基因列表文件(逗号分隔) [deg1.txt,deg2.txt,deg3.txt]: ") or "deg1.txt,deg2.txt,deg3.txt"
    output_plot = input("输出图片路径 [deg_venn.png]: ") or "deg_venn.png"
    labels = input("组标签(逗号分隔) [G1,G2,G3]: ") or "G1,G2,G3"
    try:
        import matplotlib.pyplot as plt
        from matplotlib_venn import venn2, venn3
    except ImportError:
        print("[ERROR] matplotlib-venn is required: pip install matplotlib-venn")
        return
    files = [f.strip() for f in deg_files.split(",")]
    labs = [l.strip() for l in labels.split(",")]
    sets = []
    for fp in files:
        with open(fp) as f: sets.append(set(l.strip() for l in f if l.strip()))
    fig, ax = plt.subplots(figsize=(8, 6))
    if len(sets) == 2: venn2(sets, labs, ax=ax)
    elif len(sets) == 3: venn3(sets, labs, ax=ax)
    else: print("仅支持2-3组"); return
    plt.title("DEG Venn"); plt.tight_layout(); plt.savefig(output_plot, dpi=150)
    print(f"韦恩图: {output_plot}")


if __name__ == "__main__":
    main()
