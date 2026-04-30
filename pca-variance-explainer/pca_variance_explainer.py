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

def plot_pca_variance(input_file=None, output="pca_variance.png", n_components=20):
    """读取输入矩阵，执行PCA，可视化方差解释比例"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np

        # Read input matrix and perform PCA
        if input_file:
            import pandas as pd
            data = pd.read_csv(input_file, sep='\t', index_col=0)
            # Center the data
            data_centered = data - data.mean(axis=0)
            matrix = data_centered.values
        else:
            print("未提供输入文件，使用随机示例数据")
            np.random.seed(42)
            matrix = np.random.randn(100, n_components)

        # Perform PCA using sklearn if available, otherwise manual
        try:
            from sklearn.decomposition import PCA
            n_comp = min(n_components, min(matrix.shape) - 1)
            pca = PCA(n_components=n_comp)
            pca.fit(matrix)
            variances = pca.explained_variance_ratio_ * 100
        except ImportError:
            # Manual PCA via SVD
            n_comp = min(n_components, min(matrix.shape) - 1)
            U, S, Vt = np.linalg.svd(matrix, full_matrices=False)
            total_var = np.sum(S ** 2)
            variances = (S[:n_comp] ** 2 / total_var) * 100

        cumulative = np.cumsum(variances)
        n_comp = len(variances)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        ax1.bar(range(1, n_comp+1), variances, color='steelblue', edgecolor='black')
        ax1.set_xlabel('Principal Component')
        ax1.set_ylabel('Variance Explained (%)')
        ax1.set_title('Scree Plot')
        ax1.grid(True, alpha=0.3)

        ax2.plot(range(1, n_comp+1), cumulative, 'o-', color='coral')
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
        print(f"前2个PC解释方差: PC1={variances[0]:.2f}%, PC2={variances[1]:.2f}%")
        print(f"达到80%方差需要 {np.searchsorted(cumulative, 80) + 1} 个主成分")
    except ImportError:
        print("matplotlib未安装")

def main():
    print("\n" + "=" * 60)
    print("  PCA方差解释比例可视化工具")
    print("=" * 60)

    input_file = get_input("\n输入矩阵文件(TSV, 行=样本, 列=特征, 留空用示例)", "", str)
    output = get_input("输出图片", "pca_variance.png", str)
    n_components = get_input("PC数量", 20, int)

    input_file = input_file if input_file else None
    plot_pca_variance(input_file, output, n_components)
    print("\n完成!")

if __name__ == "__main__":
    main()
