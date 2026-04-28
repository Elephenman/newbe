#!/usr/bin/env python3
"""色盲友好科研配色方案生成器"""

def main():
    n_colors = input("颜色数量 [8]: ") or "8"
    palette_type = input("类型(qualitative/sequential/diverging) [qualitative]: ") or "qualitative"
    output_file = input("输出配色文件路径(CSV) [palette.csv]: ") or "palette.csv"
    output_plot = input("输出预览图路径 [palette_preview.png]: ") or "palette_preview.png"
    import matplotlib.pyplot as plt, matplotlib.colors as mcolors
    n = int(n_colors)
    palettes = {
        "qualitative": ["#E69F00","#56B4E9","#009E73","#F0E442","#0072B2","#D55E00","#CC79A7","#000000"],
        "sequential": plt.cm.viridis if n <= 256 else plt.cm.plasma,
        "diverging": plt.cm.RdBu if n <= 256 else plt.cm.coolwarm,
    }
    if palette_type == "qualitative":
        colors = palettes["qualitative"][:n]
        if n > len(colors): colors = colors * (n // len(colors) + 1); colors = colors[:n]
    else:
        cmap = palettes.get(palette_type, plt.cm.viridis)
        colors = [mcolors.to_hex(cmap(i / max(1, n-1))) for i in range(n)]
    with open(output_file, "w") as out:
        out.write("index,hex_color\n")
        for i, c in enumerate(colors): out.write(f"{i},{c}\n")
    fig, ax = plt.subplots(figsize=(10, 2))
    for i, c in enumerate(colors):
        ax.barh(0, 1, left=i, color=c, edgecolor="white")
    ax.set_xlim(0, n); ax.set_yticks([]); ax.set_xticks(range(n))
    ax.set_xticklabels([f"C{i+1}" for i in range(n)], fontsize=8)
    ax.set_title(f"Colorblind-Safe Palette ({palette_type}, n={n})")
    plt.tight_layout(); plt.savefig(output_plot, dpi=150)
    print(f"配色方案: {output_file}")


if __name__ == "__main__":
    main()
