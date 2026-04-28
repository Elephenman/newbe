#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  spatial-distance-decay-plotter
  空间距离衰减可视化工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def plot_distance_decay(output="distance_decay.png"):
    """绘制空间距离与基因表达/接触的衰减曲线"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        distances = np.arange(0, 100, 5)
        expression_decay = np.exp(-distances / 30) + np.random.randn(len(distances)) * 0.05
        contact_decay = np.exp(-distances / 20) + np.random.randn(len(distances)) * 0.05
        
        ax.plot(distances, expression_decay, 'o-', label='Expression correlation', color='steelblue')
        ax.plot(distances, contact_decay, 's-', label='Cell contact', color='coral')
        
        ax.set_xlabel('Spatial Distance', fontsize=12)
        ax.set_ylabel('Correlation / Contact', fontsize=12)
        ax.set_title('Spatial Distance Decay')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output, dpi=300)
        plt.close()
        print(f"距离衰减图已保存: {output}")
    except ImportError:
        print("matplotlib未安装")

def main():
    print("\n" + "=" * 60)
    print("  空间距离衰减可视化工具")
    print("=" * 60)
    
    output = get_input("\n输出图片", "distance_decay.png", str)
    
    plot_distance_decay(output)
    print("\n完成!")

if __name__ == "__main__":
    main()
