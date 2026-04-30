#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  deconvolution-estimator
  表达数据去卷积估计工具
  Uses Non-Negative Least Squares (NNLS) deconvolution
  to estimate cell type proportions from bulk expression.
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def estimate_deconvolution(expr_file, signature_file, output="deconvolution_results.tsv"):
    """Estimate cell type proportions using NNLS deconvolution.

    Solves: bulk = signature * proportions, with proportions >= 0,
    then normalizes proportions to sum to 1 per sample.
    """
    import numpy as np
    from scipy.optimize import nnls

    # ------------------------------------------------------------------
    # Load or generate bulk expression matrix
    # ------------------------------------------------------------------
    try:
        import pandas as pd
        expr_df = pd.read_csv(expr_file, sep='\t', index_col=0)
        gene_names = list(expr_df.index)
        sample_names = list(expr_df.columns)
        bulk_matrix = expr_df.values  # genes x samples
    except Exception:
        print("[INFO] Could not read expression file – generating demo data.")
        np.random.seed(42)
        cell_types = ["T_cells", "B_cells", "Macrophages", "NK_cells", "Fibroblasts"]
        n_genes = 500
        n_samples = 5
        # True mixing proportions
        true_props = np.random.dirichlet(np.ones(len(cell_types)), size=n_samples).T  # C x S
        # Signature: distinct expression profiles per cell type
        sig_matrix = np.abs(np.random.randn(n_genes, len(cell_types))) + 1.0
        for c in range(len(cell_types)):
            # Give each cell type a signature boost on a subset of genes
            boost_genes = np.random.choice(n_genes, size=n_genes // 5, replace=False)
            sig_matrix[boost_genes, c] += np.random.uniform(3, 8, size=len(boost_genes))
        # Bulk = sig * props + noise
        bulk_matrix = sig_matrix @ true_props + 0.1 * np.abs(np.random.randn(n_genes, n_samples))
        sample_names = [f"Sample{i+1}" for i in range(n_samples)]
        gene_names = [f"Gene_{i+1}" for i in range(n_genes)]
        # Also use this as the signature matrix
        signature_df = None

    # ------------------------------------------------------------------
    # Load or generate signature matrix
    # ------------------------------------------------------------------
    if signature_df is not None:
        pass  # already set from the except branch failure path – handled below
    try:
        if 'signature_df' in dir() and signature_df is not None:
            pass
        else:
            raise RuntimeError("need to load")
    except Exception:
        pass

    try:
        import pandas as pd
        sig_df = pd.read_csv(signature_file, sep='\t', index_col=0)
        sig_gene_names = list(sig_df.index)
        cell_types = list(sig_df.columns)
        sig_matrix = sig_df.values  # genes x cell_types
    except Exception:
        if 'sig_matrix' not in dir() or sig_matrix is None:
            print("[INFO] Could not read signature file – generating demo signature.")
            np.random.seed(123)
            cell_types = ["T_cells", "B_cells", "Macrophages", "NK_cells", "Fibroblasts"]
            n_sig_genes = bulk_matrix.shape[0]
            sig_matrix = np.abs(np.random.randn(n_sig_genes, len(cell_types))) + 1.0
            for c in range(len(cell_types)):
                boost_genes = np.random.choice(n_sig_genes, size=n_sig_genes // 5, replace=False)
                sig_matrix[boost_genes, c] += np.random.uniform(3, 8, size=len(boost_genes))
            sig_gene_names = gene_names

    # ------------------------------------------------------------------
    # Align genes between bulk and signature (intersection)
    # ------------------------------------------------------------------
    try:
        import pandas as pd
        common_genes = sorted(set(gene_names) & set(sig_gene_names))
        if len(common_genes) == 0:
            raise ValueError("No common genes between bulk and signature matrices.")
        if len(common_genes) < len(gene_names):
            print(f"[INFO] Using {len(common_genes)} common genes out of "
                  f"{len(gene_names)} bulk genes and {len(sig_gene_names)} signature genes.")
        bulk_idx = [gene_names.index(g) for g in common_genes]
        sig_idx = [sig_gene_names.index(g) for g in common_genes]
        bulk_aligned = bulk_matrix[bulk_idx, :]
        sig_aligned = sig_matrix[sig_idx, :]
    except Exception:
        # If alignment fails (e.g. demo data), just use as-is
        bulk_aligned = bulk_matrix
        sig_aligned = sig_matrix
        # Ensure dimensions match: use min rows
        min_genes = min(bulk_aligned.shape[0], sig_aligned.shape[0])
        bulk_aligned = bulk_aligned[:min_genes, :]
        sig_aligned = sig_aligned[:min_genes, :]

    # ------------------------------------------------------------------
    # NNLS deconvolution per sample
    # ------------------------------------------------------------------
    n_samples = bulk_aligned.shape[1]
    n_celltypes = sig_aligned.shape[1]
    proportions = np.zeros((n_samples, n_celltypes))

    for s in range(n_samples):
        bulk_vec = bulk_aligned[:, s]
        # Solve: minimize || sig * p - bulk ||^2 s.t. p >= 0
        p, residual = nnls(sig_aligned, bulk_vec)
        # Normalize to sum to 1
        total = p.sum()
        if total > 0:
            p = p / total
        proportions[s, :] = p

    # ------------------------------------------------------------------
    # Write results
    # ------------------------------------------------------------------
    with open(output, 'w') as f:
        f.write("Sample\t" + "\t".join(cell_types) + "\n")
        for i, sample in enumerate(sample_names):
            vals = "\t".join(f"{proportions[i, c]:.4f}" for c in range(n_celltypes))
            f.write(f"{sample}\t{vals}\n")

    # Build results dict for return
    results = {}
    for i, sample in enumerate(sample_names):
        results[sample] = {ct: round(proportions[i, c], 4) for c, ct in enumerate(cell_types)}

    return results


def main():
    print("\n" + "=" * 60)
    print("  表达数据去卷积估计工具 (NNLS Deconvolution)")
    print("=" * 60)

    expr_file = get_input("\n表达矩阵文件 (genes x samples)", "expression.tsv", str)
    signature_file = get_input("签名矩阵文件 (genes x cell_types)", "signature.tsv", str)
    output = get_input("输出文件", "deconvolution_results.tsv", str)

    results = estimate_deconvolution(expr_file, signature_file, output=output)

    print("\n估算的细胞类型比例 (NNLS):")
    for sample, proportions in list(results.items())[:5]:
        print(f"\n{sample}:")
        for ct, prop in proportions.items():
            print(f"  {ct}: {prop:.1%}")
    print(f"\n结果已保存到: {output}")


if __name__ == "__main__":
    main()
