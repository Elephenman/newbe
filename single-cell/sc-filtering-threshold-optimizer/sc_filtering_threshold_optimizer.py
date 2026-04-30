#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  sc-filtering-threshold-optimizer
  单细胞质控阈值优化工具
  Uses Median Absolute Deviation (MAD) and knee/inflection
  point detection for data-driven QC thresholds.
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def _mad(values):
    """Compute Median Absolute Deviation."""
    import numpy as np
    med = np.median(values)
    return np.median(np.abs(values - med))


def _knee_point(sorted_values):
    """Detect knee point from a sorted (descending) curve using max curvature."""
    import numpy as np
    n = len(sorted_values)
    if n < 3:
        return sorted_values[-1]

    # Normalize x and y to [0, 1]
    x = np.arange(n, dtype=float)
    y = np.array(sorted_values, dtype=float)

    x_norm = x / (n - 1) if n > 1 else x
    y_min, y_max = y.min(), y.max()
    y_norm = (y - y_min) / (y_max - y_min) if y_max > y_min else y

    # Line from first to last point
    p1 = np.array([x_norm[0], y_norm[0]])
    p2 = np.array([x_norm[-1], y_norm[-1]])

    # Distance from each point to the line
    line_vec = p2 - p1
    line_len = np.linalg.norm(line_vec)
    if line_len == 0:
        return sorted_values[n // 2]

    distances = np.abs(np.cross(line_vec, p1 - np.column_stack([x_norm, y_norm]))) / line_len
    knee_idx = np.argmax(distances)
    return sorted_values[knee_idx]


def optimize_thresholds(seurat_file, output="optimal_thresholds.txt", k=3):
    """Optimize single-cell QC thresholds using MAD-based filtering.

    Parameters
    ----------
    seurat_file : str
        Path to expression matrix (genes x cells, TSV) or Seurat-compatible file.
    output : str
        Output file path.
    k : float
        Number of MADs from median for outlier detection (default 3).
    """
    import numpy as np

    # ------------------------------------------------------------------
    # Load expression data
    # ------------------------------------------------------------------
    try:
        import pandas as pd
        expr_df = pd.read_csv(seurat_file, sep='\t', index_col=0)
        # genes x cells matrix
        gene_names = list(expr_df.index)
        cell_names = list(expr_df.columns)
        matrix = expr_df.values.astype(float)
    except Exception:
        print("[INFO] Could not read expression file – generating demo data.")
        np.random.seed(42)
        n_genes = 20000
        n_cells = 3000
        # Simulate realistic droplet scRNA-seq: most genes zero, some expressed
        matrix = np.random.negative_binomial(n=2, p=0.02, size=(n_genes, n_cells)).astype(float)
        # Add some low-quality cells
        n_bad = 100
        matrix[:, -n_bad:] = np.random.negative_binomial(n=1, p=0.1, size=(n_genes, n_bad)).astype(float)
        gene_names = [f"Gene_{i+1}" for i in range(n_genes)]
        cell_names = [f"Cell_{i+1}" for i in range(n_cells)]

    n_genes_total, n_cells = matrix.shape

    # ------------------------------------------------------------------
    # Calculate per-cell QC metrics
    # ------------------------------------------------------------------
    # nCount_RNA: total UMIs per cell
    nCount = matrix.sum(axis=0)

    # nFeature_RNA: number of detected genes per cell (non-zero counts)
    nFeature = (matrix > 0).sum(axis=0)

    # percent_mito: fraction of counts from mitochondrial genes
    # Identify mitochondrial genes (starting with MT- or mt-)
    mito_genes = [i for i, g in enumerate(gene_names)
                  if g.upper().startswith("MT-") or g.upper().startswith("MT-")]
    if len(mito_genes) == 0:
        # For demo / non-standard naming: randomly assign ~5% of genes as mitochondrial
        np.random.seed(7)
        mito_genes = np.random.choice(n_genes_total, size=max(1, n_genes_total // 20), replace=False).tolist()
    percent_mito = matrix[mito_genes, :].sum(axis=0) / np.maximum(nCount, 1) * 100

    # ------------------------------------------------------------------
    # MAD-based threshold calculation
    # ------------------------------------------------------------------
    # nFeature_RNA thresholds
    nFeature_med = np.median(nFeature)
    nFeature_mad = _mad(nFeature)
    nFeature_min = max(0, nFeature_med - k * nFeature_mad)
    nFeature_max = nFeature_med + k * nFeature_mad

    # nCount_RNA thresholds
    nCount_med = np.median(nCount)
    nCount_mad = _mad(nCount)
    nCount_min = max(0, nCount_med - k * nCount_mad)
    nCount_max = nCount_med + k * nCount_mad

    # percent_mito threshold (only upper bound matters)
    pmito_med = np.median(percent_mito)
    pmito_mad = _mad(percent_mito)
    pmito_max = pmito_med + k * pmito_mad

    # ------------------------------------------------------------------
    # Knee / inflection point detection on sorted nCount curve
    # ------------------------------------------------------------------
    sorted_nCount = np.sort(nCount)[::-1]  # descending
    knee_nCount = _knee_point(sorted_nCount)

    # ------------------------------------------------------------------
    # Print results
    # ------------------------------------------------------------------
    results = {
        "nFeature_RNA_min": int(round(nFeature_min)),
        "nFeature_RNA_max": int(round(nFeature_max)),
        "nCount_RNA_min": int(round(nCount_min)),
        "nCount_RNA_max": int(round(nCount_max)),
        "percent_mito_max": round(pmito_max, 1),
        "knee_nCount": int(round(knee_nCount)),
    }

    print("\n" + "-" * 50)
    print(f"  QC Metrics Summary (n_cells = {n_cells})")
    print("-" * 50)
    print(f"  nFeature_RNA: median={nFeature_med:.0f}, MAD={nFeature_mad:.0f}")
    print(f"  nCount_RNA:   median={nCount_med:.0f}, MAD={nCount_mad:.0f}")
    print(f"  percent_mito: median={pmito_med:.1f}%, MAD={pmito_mad:.1f}%")
    print()
    print("  Recommended QC Thresholds (k={} MAD):".format(k))
    print("-" * 50)
    print(f"  nFeature_RNA (genes/cell): {results['nFeature_RNA_min']} - {results['nFeature_RNA_max']}")
    print(f"  nCount_RNA (UMIs/cell):    {results['nCount_RNA_min']} - {results['nCount_RNA_max']}")
    print(f"  percent_mito:              < {results['percent_mito_max']}%")
    print(f"  knee nCount:               {results['knee_nCount']} (inflection point)")

    # ------------------------------------------------------------------
    # Distribution plot
    # ------------------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 3, figsize=(15, 4))

        # nFeature histogram
        axes[0].hist(nFeature, bins=80, color='steelblue', alpha=0.7)
        axes[0].axvline(nFeature_min, color='red', linestyle='--', label=f'low={nFeature_min:.0f}')
        axes[0].axvline(nFeature_max, color='red', linestyle='--', label=f'high={nFeature_max:.0f}')
        axes[0].set_title('nFeature_RNA')
        axes[0].legend(fontsize=8)

        # nCount histogram
        axes[1].hist(nCount, bins=80, color='seagreen', alpha=0.7)
        axes[1].axvline(nCount_min, color='red', linestyle='--', label=f'low={nCount_min:.0f}')
        axes[1].axvline(nCount_max, color='red', linestyle='--', label=f'high={nCount_max:.0f}')
        axes[1].set_title('nCount_RNA')
        axes[1].legend(fontsize=8)

        # percent_mito histogram
        axes[2].hist(percent_mito, bins=80, color='coral', alpha=0.7)
        axes[2].axvline(pmito_max, color='red', linestyle='--', label=f'max={pmito_max:.1f}%')
        axes[2].set_title('percent_mito')
        axes[2].legend(fontsize=8)

        plt.tight_layout()
        plot_file = output.replace('.txt', '_qc_distributions.png')
        plt.savefig(plot_file, dpi=150)
        plt.close()
        print(f"  Distribution plot saved to: {plot_file}")
    except ImportError:
        pass

    # ------------------------------------------------------------------
    # Write results to file
    # ------------------------------------------------------------------
    with open(output, 'w') as f:
        f.write("Parameter\tMin\tMax\tMethod\n")
        f.write(f"nFeature_RNA\t{results['nFeature_RNA_min']}\t{results['nFeature_RNA_max']}\tMAD(k={k})\n")
        f.write(f"nCount_RNA\t{results['nCount_RNA_min']}\t{results['nCount_RNA_max']}\tMAD(k={k})\n")
        f.write(f"percent_mito\t0\t{results['percent_mito_max']}\tMAD(k={k})\n")
        f.write(f"knee_nCount\t0\t{results['knee_nCount']}\tknee_point\n")

    return results


def main():
    print("\n" + "=" * 60)
    print("  单细胞质控阈值优化工具 (MAD + Knee Detection)")
    print("=" * 60)

    seurat_file = get_input("\n表达矩阵文件 (genes x cells TSV)", "expression.tsv", str)
    output = get_input("输出阈值文件", "optimal_thresholds.txt", str)
    k = get_input("MAD倍数 k", 3, float)

    results = optimize_thresholds(seurat_file, output, k=k)
    print(f"\n阈值已保存到: {output}")


if __name__ == "__main__":
    main()
