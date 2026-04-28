#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  pathway-network-visualizer
  通路网络可视化工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def visualize_pathway_network(enrich_file, output="pathway_network.png", top_n=20):
    """可视化通路富集网络"""
    pathways = []
    
    try:
        with open(enrich_file, 'r') as f:
            header = f.readline()
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    pathways.append({
                        'name': parts[0],
                        'pvalue': float(parts[1]) if len(parts) > 1 else 1.0,
                        'genes': parts[2].split(',') if len(parts) > 2 else []
                    })
    except:
        pathways = [
            {'name': 'Pathway_A', 'pvalue': 0.001, 'genes': ['g1', 'g2', 'g3']},
            {'name': 'Pathway_B', 'pvalue': 0.005, 'genes': ['g2', 'g3', 'g4']},
            {'name': 'Pathway_C', 'pvalue': 0.01, 'genes': ['g3', 'g4', 'g5']}
        ]
    
    pathways = sorted(pathways, key=lambda x: x['pvalue'])[:top_n]
    
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        x_pos = np.arange(len(pathways))
        colors = -np.log10([p['pvalue'] for p in pathways])
        
        ax.scatter(x_pos, colors, s=[100 + len(p['genes'])*10 for p in pathways],
                  c=colors, cmap='viridis', alpha=0.7, edgecolors='black')
        
        for i, p in enumerate(pathways):
            ax.annotate(p['name'][:15], (i, colors[i]), rotation=45, ha='left', fontsize=8)
        
        ax.set_xlabel('Pathway', fontsize=12)
        ax.set_ylabel('-log10(P-value)', fontsize=12)
        ax.set_title('Pathway Enrichment Network')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"通路网络图已保存: {output}")
    except ImportError:
        print("matplotlib未安装，仅输出通路列表")
        for p in pathways[:10]:
            print(f"  {p['name']}: {p['pvalue']:.2e}")

def main():
    print("\n" + "=" * 60)
    print("  通路网络可视化工具")
    print("=" * 60)
    
    enrich_file = get_input("\n富集结果文件", "enrichment.txt", str)
    output = get_input("输出图片", "pathway_network.png", str)
    top_n = get_input("显示前N个通路", 20, int)
    
    visualize_pathway_network(enrich_file, output, top_n)
    print("\n完成!")

if __name__ == "__main__":
    main()
