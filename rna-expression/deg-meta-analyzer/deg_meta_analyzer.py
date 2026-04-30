#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  deg-meta-analyzer
  多研究DEG元分析工具 - Fisher/Stouffer统计方法
============================================================
"""

import math

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def fishers_combined_test(p_values):
    """
    Fisher's combined probability test:
    chi2 = -2 * sum(ln(p_i)), df = 2*k
    Returns combined p-value.
    """
    if not p_values or any(p <= 0 or p > 1 for p in p_values):
        return 1.0
    chi2 = -2.0 * sum(math.log(p) for p in p_values)
    k = len(p_values)
    df = 2 * k
    # Chi-square survival function using regularized incomplete gamma
    # P(X > chi2) where X ~ chi2(df)
    try:
        from scipy.stats import chi2
        combined_pval = chi2.sf(chi2, df)
    except ImportError:
        # Manual approximation for chi2 p-value
        # Using the Wilson-Hilferty approximation
        if df > 0:
            z = ((chi2 / df) ** (1.0/3.0) - (1.0 - 2.0/(9.0*df))) / math.sqrt(2.0/(9.0*df))
            combined_pval = 0.5 * math.erfc(z / math.sqrt(2.0))
        else:
            combined_pval = 1.0
    return combined_pval

def stouffers_z_test(p_values, weights=None):
    """
    Stouffer's Z-score method:
    Z = sum(w_i * z_i) / sqrt(sum(w_i^2))
    where z_i = Phi^{-1}(1 - p_i)
    Returns combined p-value.
    """
    if not p_values or any(p <= 0 or p >= 1 for p in p_values):
        return 1.0

    # Inverse normal CDF: z = Phi^{-1}(1 - p) = -Phi^{-1}(p)
    # Using rational approximation (Abramowitz and Stegun)
    def norm_ppf(p):
        """Inverse of standard normal CDF (probit function)"""
        if p <= 0:
            return -float('inf')
        if p >= 1:
            return float('inf')
        # Rational approximation
        a = [-3.969683028665376e+01, 2.209460984245205e+02,
             -2.759285104469687e+02, 1.383577518672690e+02,
             -3.066479806614716e+01, 2.506628277459239e+00]
        b = [-5.447609879822406e+01, 1.615858368580409e+02,
             -1.556989798598866e+02, 6.680131188771972e+01,
             -1.328068155288572e+01]
        c = [-7.784894002430293e-03, -3.223964580411365e-01,
             -2.400758277161838e+00, -2.549732539343734e+00,
              4.374664141464968e+00, 2.938163982698783e+00]
        d = [7.784695709041462e-03, 3.224671290700398e-01,
             2.445134137142996e+00, 3.754408661907416e+00]

        p_low = 0.02425
        p_high = 1 - p_low

        if p < p_low:
            q = math.sqrt(-2 * math.log(p))
            x = (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
        elif p <= p_high:
            q = p - 0.5
            r = q * q
            x = (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
                (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
        else:
            q = math.sqrt(-2 * math.log(1 - p))
            x = -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                 ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
        return x

    # Convert p-values to z-scores
    z_scores = [norm_ppf(1 - p) for p in p_values]

    if weights is None:
        weights = [1.0] * len(p_values)

    # Combined Z
    sum_wz = sum(w * z for w, z in zip(weights, z_scores))
    sum_w2 = sum(w ** 2 for w in weights)
    combined_z = sum_wz / math.sqrt(sum_w2)

    # Convert back to p-value using standard normal CDF
    # P(Z > combined_z) = 0.5 * erfc(z / sqrt(2))
    combined_pval = 0.5 * math.erfc(combined_z / math.sqrt(2.0))
    return combined_pval

def meta_analyze_deg(deg_files, output="meta_deg.txt", pval_col=4, fc_col=3, method="fisher"):
    """
    对多研究DEG进行元分析
    method: 'fisher' (Fisher's combined test) or 'stouffer' (Stouffer's Z-score method)
    """
    from collections import defaultdict

    # Collect p-values and fold changes per gene across studies
    gene_pvals = defaultdict(list)    # gene -> [(study, pval)]
    gene_fcs = defaultdict(list)      # gene -> [(study, fc)]

    study_names = []
    for deg_file in deg_files:
        study_name = deg_file.replace('.txt', '').replace('.tsv', '').replace('.csv', '')
        study_names.append(study_name)

        try:
            with open(deg_file, 'r') as f:
                header = f.readline()
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) > max(pval_col, fc_col):
                        gene = parts[0]
                        try:
                            fc = float(parts[fc_col])
                            pval = float(parts[pval_col])
                        except (ValueError, IndexError):
                            continue

                        # Skip invalid p-values
                        if pval <= 0 or pval > 1:
                            continue

                        gene_pvals[gene].append((study_name, pval))
                        gene_fcs[gene].append((study_name, fc))
        except FileNotFoundError:
            print(f"警告: 文件未找到 {deg_file}")

    # Perform meta-analysis for each gene
    results = []
    for gene in gene_pvals:
        pvals = [p for _, p in gene_pvals[gene]]
        fcs = [fc for _, fc in gene_fcs[gene]]
        n_studies = len(pvals)

        if n_studies < 1:
            continue

        # Compute combined p-value
        if method == "fisher":
            combined_pval = fishers_combined_test(pvals)
        elif method == "stouffer":
            combined_pval = stouffers_z_test(pvals)
        else:
            combined_pval = fishers_combined_test(pvals)

        # Determine consensus direction from fold changes
        mean_fc = sum(fcs) / len(fcs) if fcs else 0
        direction = "Up" if mean_fc > 0 else "Down"

        # Count consistent direction
        consistent = sum(1 for fc in fcs if (fc > 0 and direction == "Up") or (fc < 0 and direction == "Down"))
        consistency = consistent / len(fcs) if fcs else 0

        results.append((gene, n_studies, combined_pval, mean_fc, direction, consistency))

    # Sort by combined p-value
    results.sort(key=lambda x: x[2])

    with open(output, 'w') as f:
        f.write("Gene\tN_Studies\tCombined_Pval\tMean_FC\tDirection\tDirection_Consistency\n")
        for gene, n_studies, combined_pval, mean_fc, direction, consistency in results:
            f.write(f"{gene}\t{n_studies}\t{combined_pval:.6e}\t{mean_fc:.4f}\t{direction}\t{consistency:.2f}\n")

    return len(results)

def main():
    print("\n" + "=" * 60)
    print("  DEG元分析工具 (Fisher/Stouffer方法)")
    print("=" * 60)

    deg_input = get_input("\nDEG文件列表(逗号分隔)", "deg1.txt,deg2.txt,deg3.txt", str)
    output = get_input("输出文件", "meta_deg.txt", str)
    pval_col = get_input("P-value列号(1-based)", "4", int)
    fc_col = get_input("Fold Change列号(1-based)", "3", int)
    method = get_input("元分析方法(fisher/stouffer)", "fisher", str)

    deg_files = [f.strip() for f in deg_input.split(',') if f.strip()]
    count = meta_analyze_deg(deg_files, output, pval_col, fc_col, method)

    print(f"\n分析完成: {count} 个基因通过元分析")
    print(f"方法: {method}")
    print(f"结果已保存到: {output}")

if __name__ == "__main__":
    main()
