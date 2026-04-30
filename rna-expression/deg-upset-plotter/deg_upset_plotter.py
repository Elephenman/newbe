#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  deg-upset-plotter
  多组DEG交集UpSet图绘制工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def plot_upset(deg_files, output="upset_plot.png", min_size=1):
    """绘制UpSet图展示多组DEG交集"""
    import collections
    
    deg_sets = {}
    all_genes = set()
    
    for deg_file in deg_files:
        name = deg_file.replace('.txt', '').replace('.tsv', '').replace('.csv', '')
        genes = set()
        try:
            with open(deg_file, 'r') as f:
                header = f.readline()
                for line in f:
                    parts = line.strip().split('\t')
                    if parts:
                        genes.add(parts[0])
            deg_sets[name] = genes
            all_genes.update(genes)
        except:
            deg_sets[name] = set()
    
    if not deg_sets:
        deg_sets = {"Group_A": {"gene1", "gene2", "gene3"}, 
                   "Group_B": {"gene2", "gene3", "gene4"},
                   "Group_C": {"gene3", "gene4", "gene5"}}
        all_genes = set()
        for s in deg_sets.values():
            all_genes.update(s)
    
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        
        n_groups = len(deg_sets)
        fig, axes = plt.subplots(2, 1, figsize=(12, 6), 
                                  gridspec_kw={'height_ratios': [3, 1]})
        
        bar_positions = []
        bar_heights = []
        labels = []
        
        intersection_counts = {}
        for i, (name1, set1) in enumerate(deg_sets.items()):
            for name2, set2 in deg_sets.items():
                if name1 < name2:
                    intersection = len(set1 & set2)
                    if intersection >= min_size:
                        key = f"{name1} ∩ {name2}"
                        intersection_counts[key] = intersection
        
        keys = sorted(intersection_counts.keys(), key=lambda x: intersection_counts[x], reverse=True)[:10]
        heights = [intersection_counts[k] for k in keys]
        
        axes[0].bar(range(len(keys)), heights, color='steelblue', edgecolor='black')
        axes[0].set_xticks(range(len(keys)))
        axes[0].set_xticklabels(keys, rotation=45, ha='right')
        axes[0].set_ylabel('Intersection Size')
        axes[0].set_title('DEG UpSet Plot')
        axes[0].grid(True, alpha=0.3)
        
        for i, h in enumerate(heights):
            axes[0].text(i, h, str(h), ha='center', va='bottom', fontsize=10)
        
        group_names = list(deg_sets.keys())
        axes[1].bar(range(len(group_names)), [len(s) for s in deg_sets.values()], 
                    color=['#1f77b4', '#ff7f0e', '#2ca02c'][:n_groups], edgecolor='black')
        axes[1].set_xticks(range(len(group_names)))
        axes[1].set_xticklabels(group_names, rotation=45, ha='right')
        axes[1].set_ylabel('Total DEGs')
        
        plt.tight_layout()
        plt.savefig(output, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"UpSet图已保存: {output}")
    except ImportError:
        print("matplotlib未安装，仅输出交集统计")
        print("\n交集统计:")
        for i, (name1, set1) in enumerate(deg_sets.items()):
            for name2, set2 in enumerate(deg_sets.values()):
                if name1 < name2:
                    inter = len(set1 & set2)
                    print(f"  {name1} ∩ {name2}: {inter}")

def main():
    print("\n" + "=" * 60)
    print("  DEG交集UpSet图绘制工具")
    print("=" * 60)
    
    deg_input = get_input("\nDEG文件列表(逗号分隔)", "deg1.txt,deg2.txt,deg3.txt", str)
    output = get_input("输出图片", "upset_plot.png", str)
    
    deg_files = [f.strip() for f in deg_input.split(',')]
    plot_upset(deg_files, output)
    print("\n完成!")

if __name__ == "__main__":
    main()
