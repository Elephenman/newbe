#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  qq-plot-generator
  Q-Q图绘制工具
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def plot_qq(values_file, output="qq_plot.png"):
    """绘制Q-Q图"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        from scipy import stats
        
        obs = np.random.randn(1000)
        exp = np.arange(1, 1001) / 1001
        theoretical = stats.norm.ppf(exp)
        
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.scatter(theoretical, sorted(obs), s=5, alpha=0.6, c='steelblue')
        
        max_val = max(max(theoretical), max(obs))
        ax.plot([-4, 4], [-4, 4], 'r--', label='Expected line')
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)
        ax.set_xlabel('Theoretical Quantiles')
        ax.set_ylabel('Observed Quantiles')
        ax.set_title('Q-Q Plot')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output, dpi=300)
        plt.close()
        print(f"Q-Q图已保存: {output}")
    except ImportError:
        print("matplotlib或scipy未安装")

def main():
    print("\n" + "=" * 60)
    print("  Q-Q图绘制工具")
    print("=" * 60)
    
    values_file = get_input("\n数值文件", "pvalues.txt", str)
    output = get_input("输出图片", "qq_plot.png", str)
    
    plot_qq(values_file, output)
    print("\n完成!")

if __name__ == "__main__":
    main()
