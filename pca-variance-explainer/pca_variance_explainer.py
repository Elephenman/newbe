#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  pca-variance-explainer
  PCA方差解释比例可视化工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def plot_pca_variance(output="pca_variance.png", n_components=20):
    """可视化PCA方差解释比例"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        
        variances = np.random.dirichlet(np.ones(n_components) * 2) * 100
        cumulative = np.cumsum(variances)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        ax1.bar(range(1, n_components+1), variances, color='steelblue', edgecolor='black')
        ax1.set_xlabel('Principal Component')
        ax1.set_ylabel('Variance Explained (%)')
        ax1.set_title('Scree Plot')
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(range(1, n_components+1), cumulative, 'o-', color='coral')
        ax2.axhline(y=80, color='green', linestyle='--', label='80% threshold')
        ax2.set_xlabel('Number of Components')
        ax2.set_ylabel('Cumulative Variance (%)')
        ax2.set_title('Cumulative Variance')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output, dpi=300)
        plt.close()
        print(f"PCA方差图已保存: {output}")
    except ImportError:
        print("matplotlib未安装")

def main():
    print("\n" + "=" * 60)
    print("  PCA方差解释比例可视化工具")
    print("=" * 60)
    
    output = get_input("\n输出图片", "pca_variance.png", str)
    n_components = get_input("PC数量", 20, int)
    
    plot_pca_variance(output, n_components)
    print("\n完成!")

if __name__ == "__main__":
    main()
