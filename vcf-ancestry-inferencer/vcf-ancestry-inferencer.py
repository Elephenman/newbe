#!/usr/bin/env python3
"""VCF样本祖源推断 - 使用参考面板进行有监督分类"""

import gzip
import numpy as np

def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    return dtype(val)

def main():
    print("=" * 60)
    print("  VCF祖源推断器")
    print("=" * 60)

    input_vcf = get_input("VCF文件路径", "variants.vcf", str)
    ref_pca_file = get_input("参考PCA坐标文件路径(包含祖源标签列)", "reference_pca.tsv", str)
    output_file = get_input("祖源推断结果路径", "ancestry_results.tsv", str)
    n_pcs = get_input("使用的主成分数", "10", int)

    opener = gzip.open if input_vcf.endswith(".gz") else open
    mode = "rt" if input_vcf.endswith(".gz") else "r"

    sample_names = []
    sample_genotypes = {}

    with opener(input_vcf, mode) as f:
        for line in f:
            if line.startswith("#CHROM"):
                parts = line.strip().split("\t")
                sample_names = parts[9:]
                for s in sample_names:
                    sample_genotypes[s] = []
            elif not line.startswith("#"):
                parts = line.strip().split("\t")
                for i, gt in enumerate(parts[9:]):
                    s = sample_names[i]
                    alleles = gt.split(":")[0].replace("|", "/").split("/")
                    a1 = alleles[0] if alleles[0] != "." else "0"
                    a2 = alleles[1] if len(alleles) > 1 and alleles[1] != "." else "0"
                    numeric = int(a1) + int(a2)
                    sample_genotypes[s].append(numeric)

    print(f"加载 {len(sample_names)} 样本")

    genotype_matrix = np.array([sample_genotypes[s] for s in sample_names])
    mean = np.mean(genotype_matrix, axis=0)
    centered = genotype_matrix - mean

    # Handle NaN/missing values
    centered = np.nan_to_num(centered, nan=0.0)

    cov = np.cov(centered.T)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    idx = np.argsort(eigenvalues)[::-1]
    eigenvectors = eigenvectors[:, idx][:, :n_pcs]

    pcs = centered @ eigenvectors

    # Load reference panel with population labels
    # Expected format: TSV with columns: sample  population  PC1  PC2  ...  PCn
    ancestry_assignments = []
    ref_populations = []

    try:
        # Read reference PCA file with population labels
        ref_header = None
        ref_data = []
        with open(ref_pca_file, 'r') as f:
            ref_header = f.readline().strip().split('\t')
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    ref_data.append(parts)

        # Identify population label column and PC columns
        pop_col_idx = None
        pc_col_indices = []
        for i, col in enumerate(ref_header):
            col_lower = col.lower()
            if col_lower in ('population', 'pop', 'ancestry', 'super_population', 'group', 'label'):
                pop_col_idx = i
            elif col_lower.startswith('pc') or col_lower.startswith('pca'):
                pc_col_indices.append(i)

        # If no PC columns found, assume numeric columns after first 2
        if not pc_col_indices:
            # Try columns that look like numeric (PC values)
            pc_col_indices = [i for i in range(2, len(ref_header)) if i != pop_col_idx]
            pc_col_indices = pc_col_indices[:n_pcs]

        if pop_col_idx is None:
            # Try second column as population if first is sample name
            if len(ref_header) >= 2:
                pop_col_idx = 1
            else:
                raise ValueError("Cannot find population column in reference file")

        # Build reference panel
        ref_pcs = []
        ref_labels = []
        for parts in ref_data:
            pop = parts[pop_col_idx]
            pc_vals = []
            for ci in pc_col_indices[:n_pcs]:
                try:
                    pc_vals.append(float(parts[ci]))
                except (ValueError, IndexError):
                    pc_vals.append(0.0)
            ref_pcs.append(pc_vals)
            ref_labels.append(pop)

        ref_pcs = np.array(ref_pcs)
        ref_labels = np.array(ref_labels)

        # Compute population centroids for nearest-centroid classification
        unique_pops = np.unique(ref_labels)
        pop_centroids = {}
        for pop in unique_pops:
            mask = ref_labels == pop
            centroid = np.mean(ref_pcs[mask, :n_pcs], axis=0)
            pop_centroids[pop] = centroid

        print(f"参考面板: {len(unique_pops)} 个群体, {len(ref_labels)} 个参考样本")
        print(f"  群体: {', '.join(unique_pops)}")

        # Classify each sample using nearest-centroid matching
        for i in range(len(sample_names)):
            sample_pc = pcs[i, :n_pcs]
            min_dist = float('inf')
            best_pop = "Unknown"

            # Try nearest-centroid first
            for pop, centroid in pop_centroids.items():
                dist = np.sqrt(np.sum((centroid - sample_pc) ** 2))
                if dist < min_dist:
                    min_dist = dist
                    best_pop = pop

            # Also check nearest individual reference sample as backup
            # This handles cases where centroids overlap
            if len(ref_pcs) > 0:
                individual_dists = np.sqrt(np.sum((ref_pcs[:, :n_pcs] - sample_pc) ** 2, axis=1))
                nearest_idx = np.argmin(individual_dists)
                nearest_individual_pop = ref_labels[nearest_idx]
                # Use individual neighbor if centroid and neighbor agree, or if neighbor is much closer
                centroid_of_nearest = pop_centroids.get(nearest_individual_pop, None)
                if centroid_of_nearest is not None:
                    centroid_dist = np.sqrt(np.sum((centroid_of_nearest - sample_pc) ** 2))
                    if individual_dists[nearest_idx] < centroid_dist * 0.5:
                        best_pop = nearest_individual_pop

            ancestry_assignments.append(best_pop)

    except FileNotFoundError:
        print(f"参考面板文件未找到: {ref_pca_file}")
        ancestry_assignments = ["Unknown"] * len(sample_names)
    except Exception as e:
        print(f"参考面板加载失败: {e}")
        ancestry_assignments = ["Unknown"] * len(sample_names)

    with open(output_file, "w") as f:
        f.write("sample\tPC1\tPC2\tPC3\tancestry_assignment\n")
        for i, s in enumerate(sample_names):
            f.write(s + "\t" + str(round(pcs[i,0], 4)) + "\t" + str(round(pcs[i,1], 4)) + "\t" + str(round(pcs[i,2], 4)) + "\t" + ancestry_assignments[i] + "\n")

    # Print summary
    from collections import Counter
    pop_counts = Counter(ancestry_assignments)
    print(f"\n祖源推断完成: {len(sample_names)} 样本")
    print("群体分布:")
    for pop, count in pop_counts.most_common():
        print(f"  {pop}: {count}")
    print(f"结果: {output_file}")

if __name__ == "__main__":
    main()
