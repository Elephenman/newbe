#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  sc-jackstraw-wrapper
  单细胞JackStraw显著性检验包装器
  Implements permutation-based PCA significance testing:
  permute each gene's expression, recompute PCA, and
  compare observed PC variance to the permuted null.
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def run_jackstraw(expr_file, output="jackstraw_results.txt", n_pcs=30, n_reps=100, significance=0.05):
    """Run permutation-based JackStraw PCA significance testing.

    For each PC, compare the observed variance explained to a null
    distribution obtained by permuting each gene independently and
    re-running PCA. The p-value is the fraction of permutations where
    the permuted variance >= the observed variance.

    Parameters
    ----------
    expr_file : str
        Path to expression matrix (genes x cells, TSV).
    output : str
        Output file path.
    n_pcs : int
        Number of principal components to test.
    n_reps : int
        Number of permutation replicates.
    significance : float
        P-value threshold for significance.
    """
    import numpy as np
    from sklearn.decomposition import PCA

    # ------------------------------------------------------------------
    # Load expression data
    # ------------------------------------------------------------------
    try:
        import pandas as pd
        expr_df = pd.read_csv(expr_file, sep='\t', index_col=0)
        gene_names = list(expr_df.index)
        cell_names = list(expr_df.columns)
        matrix = expr_df.values.astype(float)
    except Exception:
        print("[INFO] Could not read expression file – generating demo data.")
        np.random.seed(42)
        n_genes = 3000
        n_cells = 500
        # Create data with a few real PCs + noise
        latent = np.random.randn(n_cells, 5)
        loadings = np.random.randn(n_genes, 5)
        # matrix is genes x cells, so: loadings @ latent.T + noise
        matrix = loadings @ latent.T + 3 * np.random.randn(n_genes, n_cells)
        matrix = np.abs(matrix)  # counts are non-negative
        gene_names = [f"Gene_{i+1}" for i in range(n_genes)]
        cell_names = [f"Cell_{i+1}" for i in range(n_cells)]

    n_genes, n_cells = matrix.shape
    n_pcs = min(n_pcs, min(n_genes, n_cells) - 1)

    # ------------------------------------------------------------------
    # Center and scale the expression matrix (genes as features, cells as observations)
    # Standard: cells are rows, genes are columns for PCA
    # ------------------------------------------------------------------
    # Transpose so cells are rows
    X = matrix.T.copy()  # cells x genes
    # Center each gene (column)
    gene_means = X.mean(axis=0)
    X_centered = X - gene_means
    # Scale by standard deviation
    gene_stds = X_centered.std(axis=0)
    gene_stds[gene_stds == 0] = 1.0
    X_scaled = X_centered / gene_stds

    # ------------------------------------------------------------------
    # Observed PCA
    # ------------------------------------------------------------------
    pca = PCA(n_components=n_pcs)
    pca.fit(X_scaled)
    observed_variance = pca.explained_variance_ratio_

    # ------------------------------------------------------------------
    # Permutation-based null distribution
    # ------------------------------------------------------------------
    print(f"[INFO] Running {n_reps} permutations for {n_pcs} PCs ...")
    null_variance = np.zeros((n_reps, n_pcs))

    for r in range(n_reps):
        # Permute each gene (column) independently
        X_perm = X_scaled.copy()
        for g in range(X_perm.shape[1]):
            np.random.shuffle(X_perm[:, g])

        pca_perm = PCA(n_components=n_pcs)
        pca_perm.fit(X_perm)
        # Pad if fewer components (shouldn't happen but safety)
        pv = pca_perm.explained_variance_ratio_
        null_variance[r, :len(pv)] = pv

    # ------------------------------------------------------------------
    # Compute p-values: fraction of null >= observed
    # ------------------------------------------------------------------
    p_values = np.zeros(n_pcs)
    for pc in range(n_pcs):
        p_values[pc] = np.mean(null_variance[:, pc] >= observed_variance[pc])

    significant_pcs = [i + 1 for i in range(n_pcs) if p_values[i] < significance]

    # ------------------------------------------------------------------
    # Print results
    # ------------------------------------------------------------------
    print("\n" + "-" * 50)
    print("  JackStraw PCA Significance Test Results")
    print("-" * 50)
    print(f"  {'PC':<8} {'Variance%':<12} {'P-value':<10} {'Significant'}")
    print("-" * 50)
    for pc in range(n_pcs):
        sig = "Yes" if p_values[pc] < significance else "No"
        print(f"  PC{pc+1:<5} {observed_variance[pc]*100:>8.2f}%    {p_values[pc]:.4f}     {sig}")
    print("-" * 50)
    print(f"  Significant PCs (p < {significance}): {significant_pcs}")

    # ------------------------------------------------------------------
    # Plot JackStraw p-value distribution
    # ------------------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # P-value bar plot
        pc_labels = [f"PC{i+1}" for i in range(n_pcs)]
        colors = ['coral' if p_values[i] < significance else 'steelblue' for i in range(n_pcs)]
        axes[0].bar(range(n_pcs), p_values, color=colors)
        axes[0].axhline(y=significance, color='red', linestyle='--', label=f'p={significance}')
        axes[0].set_xlabel('Principal Component')
        axes[0].set_ylabel('P-value')
        axes[0].set_title('JackStraw P-values per PC')
        axes[0].legend()

        # Scree plot with observed vs null
        axes[1].plot(range(1, n_pcs + 1), observed_variance * 100, 'o-', label='Observed', color='steelblue')
        null_mean = null_variance.mean(axis=0) * 100
        axes[1].plot(range(1, n_pcs + 1), null_mean, 's--', label='Null (permuted)', color='coral')
        axes[1].set_xlabel('Principal Component')
        axes[1].set_ylabel('Variance Explained (%)')
        axes[1].set_title('Scree Plot: Observed vs Null')
        axes[1].legend()

        plt.tight_layout()
        plot_file = output.replace('.txt', '_jackstraw_plot.png')
        plt.savefig(plot_file, dpi=150)
        plt.close()
        print(f"  Plot saved to: {plot_file}")
    except ImportError:
        pass

    # ------------------------------------------------------------------
    # Write results
    # ------------------------------------------------------------------
    results = {"significant_pcs": significant_pcs, "p_values": {}}

    with open(output, 'w') as f:
        f.write("PC\tVariancePercent\tPValue\tSignificant\n")
        for pc in range(n_pcs):
            sig = "Yes" if p_values[pc] < significance else "No"
            f.write(f"PC{pc+1}\t{observed_variance[pc]*100:.4f}\t{p_values[pc]:.4f}\t{sig}\n")
            results["p_values"][f"PC{pc+1}"] = round(p_values[pc], 4)

    return results


def main():
    print("\n" + "=" * 60)
    print("  JackStraw显著性检验工具 (Permutation-based)")
    print("=" * 60)

    expr_file = get_input("\n表达矩阵文件 (genes x cells TSV)", "expression.tsv", str)
    output = get_input("输出文件", "jackstraw_results.txt", str)
    n_pcs = get_input("PC数量", 30, int)
    n_reps = get_input("置换重复次数", 100, int)

    results = run_jackstraw(expr_file, output, n_pcs=n_pcs, n_reps=n_reps)

    print(f"\n显著PC数: {len(results['significant_pcs'])}")
    print(f"显著PC: {['PC'+str(p) for p in results['significant_pcs']]}")
    print(f"结果已保存到: {output}")


if __name__ == "__main__":
    main()
