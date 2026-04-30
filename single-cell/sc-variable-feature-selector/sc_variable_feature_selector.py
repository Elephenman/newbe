#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  sc-variable-feature-selector
  单细胞可变特征选择工具
  Computes mean-variance relationship and selects highly
  variable genes using dispersion (variance/mean) relative
  to a loess-fitted trend, following the Seurat method.
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def select_variable_features(expr_file, output="variable_genes.txt", n_features=2000):
    """Select highly variable features using mean-variance dispersion.

    Algorithm (Seurat-style):
    1. Calculate mean and variance of each gene across cells.
    2. Compute dispersion = log(variance / mean).
    3. Fit a loess curve of log(variance) vs log(mean).
    4. Compute standardized dispersion residuals = (observed - fitted) / MSE.
    5. Select genes with highest positive residuals (most variable above trend).
    """
    import numpy as np

    # ------------------------------------------------------------------
    # Load expression data
    # ------------------------------------------------------------------
    try:
        import pandas as pd
        expr_df = pd.read_csv(expr_file, sep='\t', index_col=0)
        gene_names = list(expr_df.index)
        matrix = expr_df.values.astype(float)
    except Exception:
        print("[INFO] Could not read expression file – generating demo data.")
        np.random.seed(42)
        n_genes = 5000
        n_cells = 1000
        # Simulate realistic scRNA-seq: most genes lowly expressed, some highly variable
        base_mean = np.exp(np.random.uniform(-2, 5, n_genes))
        matrix = np.zeros((n_genes, n_cells), dtype=float)
        for i in range(n_genes):
            n_param = max(base_mean[i], 1.0)
            p_param = np.clip(base_mean[i] / (base_mean[i] + 10), 0.01, 0.99)
            matrix[i, :] = np.random.negative_binomial(n=n_param, p=p_param, size=n_cells)
        # Add some highly variable genes
        hv_idx = np.random.choice(n_genes, size=500, replace=False)
        matrix[hv_idx, :] += np.random.negative_binomial(n=20, p=0.1, size=(500, n_cells))
        gene_names = [f"Gene_{i+1}" for i in range(n_genes)]

    n_genes_total, n_cells = matrix.shape

    # ------------------------------------------------------------------
    # Calculate mean, variance, and dispersion per gene
    # ------------------------------------------------------------------
    gene_means = matrix.mean(axis=1)
    gene_vars = matrix.var(axis=1)

    # Filter out genes with zero mean
    valid_mask = gene_means > 0
    valid_genes = [g for g, v in zip(gene_names, valid_mask) if v]
    valid_means = gene_means[valid_mask]
    valid_vars = gene_vars[valid_mask]

    # Dispersion: log(variance / mean)
    log_means = np.log10(valid_means)
    log_vars = np.log10(valid_vars)
    dispersion = np.log10(valid_vars / valid_means)  # log(var/mean)

    # ------------------------------------------------------------------
    # Fit loess curve: log(variance) ~ log(mean)
    # ------------------------------------------------------------------
    try:
        from statsmodels.nonparametric.smoothers_lowess import lowess
        # Sort by log_means for LOWESS
        sort_idx = np.argsort(log_means)
        log_means_sorted = log_means[sort_idx]
        log_vars_sorted = log_vars[sort_idx]

        # LOWESS fit
        frac = min(0.3, max(0.05, 5000 / len(log_means_sorted)))  # adaptive span
        lowess_result = lowess(log_vars_sorted, log_means_sorted, frac=frac, return_sorted=True)
        fitted_log_vars = np.interp(log_means, lowess_result[:, 0], lowess_result[:, 1])
    except ImportError:
        # Fallback: polynomial fit if statsmodels not available
        print("[INFO] statsmodels not available, using polynomial fit instead of LOWESS.")
        coeffs = np.polyfit(log_means, log_vars, deg=3)
        fitted_log_vars = np.polyval(coeffs, log_means)

    # ------------------------------------------------------------------
    # Compute standardized dispersion residuals
    # ------------------------------------------------------------------
    residuals = log_vars - fitted_log_vars
    # Standardize by the spread of residuals (robust: use MAD)
    residual_mad = np.median(np.abs(residuals - np.median(residuals)))
    if residual_mad == 0:
        residual_mad = 1.0
    # Scale factor: 1 / (MAD * 1.4826) approximates 1/sd for normal data
    standardized_dispersion = residuals / (residual_mad * 1.4826)

    # ------------------------------------------------------------------
    # Select top variable features
    # ------------------------------------------------------------------
    n_select = min(n_features, len(valid_genes))
    # Sort by standardized dispersion (descending) – highest = most variable
    rank_idx = np.argsort(-standardized_dispersion)
    selected_idx = rank_idx[:n_select]

    selected_genes = [valid_genes[i] for i in selected_idx]
    selected_means = valid_means[selected_idx]
    selected_vars = valid_vars[selected_idx]
    selected_disp = standardized_dispersion[selected_idx]

    # ------------------------------------------------------------------
    # Print results
    # ------------------------------------------------------------------
    print(f"\n  Total genes analyzed: {len(valid_genes)}")
    print(f"  Selected variable features: {n_select}")
    print(f"  Top 10 variable genes:")
    for i in range(min(10, n_select)):
        print(f"    {selected_genes[i]}: mean={selected_means[i]:.2f}, "
              f"var={selected_vars[i]:.2f}, std_disp={selected_disp[i]:.2f}")

    # ------------------------------------------------------------------
    # Mean-variance plot
    # ------------------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 6))

        # All genes
        ax.scatter(log_means, log_vars, c='lightgray', s=3, alpha=0.5, label='All genes')
        # Fitted curve
        sort_idx_plot = np.argsort(log_means)
        ax.plot(log_means[sort_idx_plot], fitted_log_vars[sort_idx_plot],
                'r-', linewidth=2, label='Fitted trend')
        # Selected variable genes
        ax.scatter(log_means[selected_idx], log_vars[selected_idx],
                   c='blue', s=8, alpha=0.7, label=f'Top {n_select} variable')

        ax.set_xlabel('log10(Mean Expression)')
        ax.set_ylabel('log10(Variance)')
        ax.set_title('Mean-Variance Plot (Highly Variable Genes)')
        ax.legend()

        plt.tight_layout()
        plot_file = output.replace('.txt', '_mean_variance.png')
        plt.savefig(plot_file, dpi=150)
        plt.close()
        print(f"  Mean-variance plot saved to: {plot_file}")
    except ImportError:
        pass

    # ------------------------------------------------------------------
    # Write results
    # ------------------------------------------------------------------
    with open(output, 'w') as f:
        f.write("Gene\tMean\tVariance\tDispersion\tSelected\n")
        # Write all genes (sorted by standardized dispersion descending)
        all_sorted_idx = np.argsort(-standardized_dispersion)
        for rank, idx in enumerate(all_sorted_idx):
            sel = "Yes" if rank < n_select else "No"
            f.write(f"{valid_genes[idx]}\t{valid_means[idx]:.4f}\t"
                    f"{valid_vars[idx]:.4f}\t{standardized_dispersion[idx]:.4f}\t{sel}\n")

    return n_select


def main():
    print("\n" + "=" * 60)
    print("  单细胞可变特征选择工具 (Mean-Variance Dispersion)")
    print("=" * 60)

    expr_file = get_input("\n表达矩阵文件 (genes x cells TSV)", "expression.tsv", str)
    output = get_input("输出基因列表", "variable_genes.txt", str)
    n_features = get_input("选择基因数", 2000, int)

    count = select_variable_features(expr_file, output, n_features)

    print(f"\n选择了 {count} 个可变特征基因")
    print(f"结果已保存到: {output}")


if __name__ == "__main__":
    main()
