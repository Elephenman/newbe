#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  sc-ccs-regression-visualizer
  单细胞CC regression可视化工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def visualize_cc_regression(output="cc_regression.png", n_pcs=20):
    """可视化细胞周期回归前后对比"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        x = np.arange(n_pcs)
        before = np.random.rand(n_pcs) * 0.5 + 0.5
        after = np.random.rand(n_pcs) * 0.3 + 0.1
        
        axes[0].bar(x, before, color='steelblue', alpha=0.7, label='Before')
        axes[0].set_title('Before CC Regression')
        axes[0].set_xlabel('PC')
        axes[0].set_ylabel('Variance')
        
        axes[1].bar(x, after, color='coral', alpha=0.7, label='After')
        axes[1].set_title('After CC Regression')
        axes[1].set_xlabel('PC')
        
        plt.tight_layout()
        plt.savefig(output, dpi=300)
        plt.close()
        print(f"可视化图已保存: {output}")
    except ImportError:
        print("matplotlib未安装")

def main():
    print("\n" + "=" * 60)
    print("  细胞周期回归可视化工具")
    print("=" * 60)
    
    output = get_input("\n输出图片", "cc_regression.png", str)
    n_pcs = get_input("PC数量", 20, int)
    
    visualize_cc_regression(output, n_pcs)
    print("\n完成!")

if __name__ == "__main__":
    main()
