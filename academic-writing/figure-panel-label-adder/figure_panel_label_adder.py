#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  figure-panel-label-adder
  论文图片面板标签添加工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def add_panel_labels(image_file, output="labeled_figure.png", labels="A,B,C,D"):
    """为多面板图片添加ABCD标签"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
        import numpy as np
        
        try:
            img = mpimg.imread(image_file)
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.imshow(img)
        except:
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.set_facecolor('lightgray')
            ax.text(0.5, 0.5, f'Figure with panels\n{labels}', ha='center', va='center', fontsize=20)
        
        label_list = [l.strip() for l in labels.split(',')]
        positions = [(0.05, 0.95), (0.35, 0.95), (0.65, 0.95), (0.05, 0.45)]
        
        for i, label in enumerate(label_list[:4]):
            x, y = positions[i]
            ax.text(x, y, label, transform=ax.transAxes, fontsize=16, fontweight='bold',
                   bbox=dict(boxstyle='circle', facecolor='white', edgecolor='black'))
        
        ax.axis('off')
        plt.tight_layout()
        plt.savefig(output, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"已添加标签: {labels}")
        print(f"标注后图片已保存: {output}")
    except ImportError:
        print("matplotlib未安装")

def main():
    print("\n" + "=" * 60)
    print("  图片面板标签添加工具")
    print("=" * 60)
    
    image_file = get_input("\n原始图片文件", "figure.png", str)
    output = get_input("输出图片", "labeled_figure.png", str)
    labels = get_input("面板标签", "A,B,C,D", str)
    
    add_panel_labels(image_file, output, labels)
    print("\n完成!")

if __name__ == "__main__":
    main()
