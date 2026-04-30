#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  spatial-domain-correlator
  空间领域相关性分析工具
  Computes Pearson correlation between spatial domain
  membership (binary) and gene expression across spots,
   reporting top correlated genes per domain.
============================================================
"""

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)


def correlate_spatial_domains(domain_file, expression_file, output="domain_correlation.tsv", top_n=20):
    """Compute correlations between spatial domain assignments and gene expression.

    For each domain, compute Pearson correlation between a binary vector
    (1 = spot belongs to this domain, 0 = does not) and each gene's
    expression across all spots. Report top correlated genes per domain.

    Parameters
    ----------
    domain_file : str
        Path to domain assignment file (TSV: spot_id, domain_label).
    expression_file : str
        Path to spatial expression matrix (genes x spots, TSV).
    output : str
        Output file path.
    top_n : int
        Number of top correlated genes to report per domain.
    """
    import numpy as np

    # ------------------------------------------------------------------
    # Load domain assignments
    # ------------------------------------------------------------------
    try:
        import pandas as pd
        domain_df = pd.read_csv(domain_file, sep='\t')
        # Expect columns: spot_id, domain (or similar)
        if 'spot_id' in domain_df.columns and 'domain' in domain_df.columns:
            spot_ids_domain = domain_df['spot_id'].astype(str).values
            domain_labels = domain_df['domain'].astype(str).values
        else:
            # Use first two columns
            spot_ids_domain = domain_df.iloc[:, 0].astype(str).values
            domain_labels = domain_df.iloc[:, 1].astype(str).values
    except Exception:
        print("[INFO] Could not read domain file – generating demo data.")
        np.random.seed(42)
        n_spots = 2000
        n_domains = 8
        domain_labels = np.array([f"Domain_{i+1}" for i in np.random.randint(0, n_domains, n_spots)])
        spot_ids_domain = np.array([f"Spot_{i+1}" for i in range(n_spots)])

    # ------------------------------------------------------------------
    # Load expression matrix
    # ------------------------------------------------------------------
    try:
        import pandas as pd
        expr_df = pd.read_csv(expression_file, sep='\t', index_col=0)
        gene_names = list(expr_df.index)
        spot_ids_expr = [str(c) for c in expr_df.columns]
        matrix = expr_df.values.astype(float)
    except Exception:
        print("[INFO] Could not read expression file – generating demo data.")
        np.random.seed(123)
        n_spots_expr = len(spot_ids_domain) if 'spot_ids_domain' in dir() else 2000
        n_genes = 1000
        matrix = np.random.negative_binomial(n=5, p=0.05, size=(n_genes, n_spots_expr)).astype(float)
        # Add domain-specific expression signal
        unique_domains = sorted(set(domain_labels))
        for d_idx, d in enumerate(unique_domains):
            d_mask = domain_labels == d
            signal_genes = np.random.choice(n_genes, size=30, replace=False)
            for sg in signal_genes:
                matrix[sg, d_mask] += np.random.poisson(lam=20, size=d_mask.sum())
        gene_names = [f"Gene_{i+1}" for i in range(n_genes)]
        spot_ids_expr = list(spot_ids_domain)

    # ------------------------------------------------------------------
    # Align spots between domain and expression data
    # ------------------------------------------------------------------
    n_genes, n_spots = matrix.shape
    if len(domain_labels) != n_spots:
        # Try to align by spot IDs
        try:
            common_spots = sorted(set(spot_ids_domain) & set(spot_ids_expr))
            if len(common_spots) == 0:
                print(f"[WARN] Cannot align spots ({len(domain_labels)} domain vs {n_spots} expr). Using min length.")
                min_spots = min(len(domain_labels), n_spots)
                domain_labels = domain_labels[:min_spots]
                matrix = matrix[:, :min_spots]
            else:
                # Subset to common spots
                domain_idx = [i for i, s in enumerate(spot_ids_domain) if s in set(common_spots)]
                expr_idx = [i for i, s in enumerate(spot_ids_expr) if s in set(common_spots)]
                domain_labels = domain_labels[domain_idx]
                matrix = matrix[:, expr_idx]
                n_spots = len(domain_labels)
        except Exception:
            min_spots = min(len(domain_labels), n_spots)
            domain_labels = domain_labels[:min_spots]
            matrix = matrix[:, :min_spots]
            n_spots = min_spots

    unique_domains = sorted(set(domain_labels))
    n_domains = len(unique_domains)

    # ------------------------------------------------------------------
    # Compute Pearson correlation for each domain vs each gene
    # ------------------------------------------------------------------
    # For each domain, create binary membership vector (1 = in domain, 0 = not)
    correlations = {}
    p_values = {}

    for d in unique_domains:
        # Binary membership vector
        membership = (domain_labels == d).astype(float)
        n_in = membership.sum()
        if n_in < 2 or n_in > n_spots - 2:
            print(f"[WARN] Domain {d}: {int(n_in)} spots (skipping, insufficient for correlation)")
            continue

        correlations[d] = {}
        p_values[d] = {}

        for g_idx, gene in enumerate(gene_names):
            expr_vec = matrix[g_idx, :]
            # Pearson correlation
            r, p = _pearson_correlation(membership, expr_vec)
            correlations[d][gene] = round(r, 4)
            p_values[d][gene] = round(p, 6)

    # ------------------------------------------------------------------
    # Report top correlated genes per domain
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("  Top Domain-Gene Correlations")
    print("=" * 60)

    for d in unique_domains:
        if d not in correlations:
            continue
        sorted_genes = sorted(correlations[d].items(), key=lambda x: -abs(x[1]))
        print(f"\n  {d} (n_spots={int((domain_labels == d).sum())}):")
        print(f"  {'Gene':<20} {'Correlation':<12} {'P-value'}")
        for gene, corr in sorted_genes[:min(top_n, 5)]:
            p = p_values[d].get(gene, float('nan'))
            print(f"  {gene:<20} {corr:>10.4f}   {p:.2e}")

    # ------------------------------------------------------------------
    # Correlation heatmap
    # ------------------------------------------------------------------
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        # Build top-gene matrix for heatmap
        all_top_genes = set()
        for d in unique_domains:
            if d not in correlations:
                continue
            sorted_genes = sorted(correlations[d].items(), key=lambda x: -abs(x[1]))
            for gene, _ in sorted_genes[:top_n]:
                all_top_genes.add(gene)

        all_top_genes = sorted(all_top_genes)
        if len(all_top_genes) > 0:
            heatmap_matrix = np.zeros((len(unique_domains), len(all_top_genes)))
            for i, d in enumerate(unique_domains):
                for j, gene in enumerate(all_top_genes):
                    heatmap_matrix[i, j] = correlations.get(d, {}).get(gene, 0)

            fig, ax = plt.subplots(figsize=(max(10, len(all_top_genes) * 0.3), max(4, n_domains * 0.6)))
            im = ax.imshow(heatmap_matrix, aspect='auto', cmap='RdBu_r', vmin=-1, vmax=1)
            ax.set_yticks(range(n_domains))
            ax.set_yticklabels(unique_domains)
            ax.set_xticks(range(len(all_top_genes)))
            ax.set_xticklabels(all_top_genes, rotation=90, fontsize=6)
            ax.set_title('Domain-Gene Correlation Heatmap')
            plt.colorbar(im, ax=ax, label='Pearson r')
            plt.tight_layout()
            plot_file = output.replace('.tsv', '_heatmap.png')
            plt.savefig(plot_file, dpi=150)
            plt.close()
            print(f"\n  Heatmap saved to: {plot_file}")
    except ImportError:
        pass

    # ------------------------------------------------------------------
    # Write results
    # ------------------------------------------------------------------
    with open(output, 'w') as f:
        f.write("Domain\tGene\tCorrelation\tPValue\n")
        for d in unique_domains:
            if d not in correlations:
                continue
            sorted_genes = sorted(correlations[d].items(), key=lambda x: -abs(x[1]))
            for gene, corr in sorted_genes[:top_n]:
                p = p_values[d].get(gene, float('nan'))
                f.write(f"{d}\t{gene}\t{corr}\t{p}\n")

    return correlations


def _pearson_correlation(x, y):
    """Compute Pearson correlation and approximate p-value."""
    import numpy as np
    n = len(x)
    if n < 3:
        return 0.0, 1.0

    x_mean = x.mean()
    y_mean = y.mean()
    xm = x - x_mean
    ym = y - y_mean

    num = (xm * ym).sum()
    denom = np.sqrt((xm ** 2).sum() * (ym ** 2).sum())

    if denom == 0:
        return 0.0, 1.0

    r = num / denom
    r = np.clip(r, -1, 1)  # numerical safety

    # t-statistic and p-value (two-tailed)
    t = r * np.sqrt((n - 2) / (1 - r ** 2 + 1e-16))
    # Approximate p-value using the t distribution
    try:
        from scipy.stats import t as t_dist
        p = 2 * t_dist.sf(np.abs(t), df=n - 2)
    except ImportError:
        # Rough approximation for large n
        p = 2 * np.exp(-0.5 * t ** 2) / (np.sqrt(2 * np.pi) * np.maximum(np.abs(t), 1e-10))
        p = min(p, 1.0)

    return float(r), float(p)


def main():
    print("\n" + "=" * 60)
    print("  空间领域相关性分析工具 (Pearson Correlation)")
    print("=" * 60)

    domain_file = get_input("\n空间领域文件 (spot_id, domain TSV)", "spatial_domains.tsv", str)
    expression_file = get_input("表达矩阵文件 (genes x spots TSV)", "expression.tsv", str)
    output = get_input("输出文件", "domain_correlation.tsv", str)
    top_n = get_input("每领域报告基因数", 20, int)

    results = correlate_spatial_domains(domain_file, expression_file, output, top_n=top_n)

    print(f"\n相关性分析完成!")
    print(f"结果已保存到: {output}")


if __name__ == "__main__":
    main()
