#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""科研绘图配色方案生成器"""
import os, sys
def get_input(p,d=None,t=str):
    v=input(f"{p} [默认: {d}]: ").strip()
    if v=="" or v is None: return d
    try: return t(v)
    except: return d

# 预置顶级期刊配色库
JOURNAL_PALETTES = {
    "Nature": ["#3C5488","#E64B35","#4DBBD5","#00A087","#F39B7F","#8491B4","#91D1C2","#DC0000","#7E6148","#B09E85"],
    "Science": ["#0C5B3F","#E3120B","#1A7A00","#FF9505","#5A005A","#0073B7","#E29200","#5B255B","#A1C7ED","#D4E6F1"],
    "Cell": ["#333333","#CC0000","#0066CC","#009933","#FF6600","#990066","#CC6600","#336600","#660033","#996600"],
    "NEJM": ["#1B4F72","#A93226","#27AE60","#E67E22","#8E44AD","#2C3E50","#D35400","#16A085","#C0392B","#7D3C98"],
}

CB_FRIENDLY = {
    "Okabe-Ito": ["#E69F00","#56B4E9","#009E73","#F0E442","#0072B2","#D55E00","#CC79A7","#000000"],
    "Wong": ["#000000","#E69F00","#56B4E9","#009E73","#F0E442","#0072B2","#D55E00","#CC79A7"],
}

def generate_palette(n_colors=8, purpose="discrete", journal="Nature", cb_friendly=True, show=True):
    try: import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; import matplotlib.colors as mcolors
    except: print("需要matplotlib"); return
    
    # 选择配色来源
    if journal in JOURNAL_PALETTES:
        base = JOURNAL_PALETTES[journal]
    elif cb_friendly and purpose=="discrete":
        base = CB_FRIENDLY["Okabe-Ito"]
    else:
        base = JOURNAL_PALETTES["Nature"]
    
    # 扩展到需要的颜色数
    if n_colors <= len(base):
        colors = base[:n_colors]
    else:
        cmap = mcolors.LinearSegmentedColormap.from_list("custom", base)
        colors = [mcolors.to_hex(cmap(i/n_colors)) for i in range(n_colors)]
    
    # 输出
    print(f"配色方案 ({n_colors}色, {purpose}, {journal}风格):")
    for i, c in enumerate(colors):
        rgb = mcolors.to_rgb(c)
        print(f"  {i+1}. HEX: {c}  RGB: ({int(rgb[0]*255)},{int(rgb[1]*255)},{int(rgb[2]*255)})")
    
    # Python代码片段
    print(f"\nPython代码:")
    print(f"colors = {colors}")
    print(f"\nR代码:")
    r_colors = ", ".join(["'" + c + "'" for c in colors])
    print(f"colors <- c({r_colors})")
    
    # 展示图
    if show:
        plt.figure(figsize=(max(8,n_colors*0.8), 2))
        for i, c in enumerate(colors):
            plt.barh(0, 1, left=i, color=c, edgecolor='white')
        plt.xlim(0, n_colors); plt.ylim(-0.5, 0.5)
        plt.yticks([]); plt.xticks(range(n_colors), colors, fontsize=8)
        plt.title(f"{journal} Style Palette ({n_colors} colors)")
        plt.tight_layout(); plt.savefig("color_palette.png", dpi=300); plt.close()
        print("配色展示图: color_palette.png")
    
    # 保存JSON
    import json
    with open("color_palette.json", 'w') as f:
        json.dump({"colors":colors, "journal":journal, "purpose":purpose, "n":n_colors}, f, indent=2)

def main():
    print("="*50); print("  🎨 科研配色生成器"); print("="*50)
    nc=get_input("颜色数量",8,int)
    pu=get_input("用途(连续/离散/heatmap)","discrete")
    jo=get_input("参考期刊(Nature/Science/Cell/NEJM)","Nature")
    cb=get_input("色盲友好(yes/no)","yes")
    sh=get_input("展示图(yes/no)","yes")
    generate_palette(nc, pu, jo, cb.lower() in ('yes','y'), sh.lower() in ('yes','y'))
if __name__=="__main__": main()