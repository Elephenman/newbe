#!/usr/bin/env python3
"""VCF样本祖源推断"""

# VCF样本祖源推断
import gzip
import numpy as np

print("=" * 60)
print("  🧪 VCF祖源推断器")
print("=" * 60)

input_vcf = get_input("VCF文件路径", "variants.vcf")
ref_pca_file = get_input("参考PCA坐标文件路径", "reference_pca.tsv")
output_file = get_input("祖源推断结果路径", "ancestry_results.tsv")
n_pcs = int(get_input("使用的主成分数", "10"))

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

print("✅ 加载 " + str(len(sample_names)) + " 样本")

genotype_matrix = np.array([sample_genotypes[s] for s in sample_names])
mean = np.mean(genotype_matrix, axis=0)
centered = genotype_matrix - mean
cov = np.cov(centered.T)
eigenvalues, eigenvectors = np.linalg.eigh(cov)
idx = np.argsort(eigenvalues)[::-1]
eigenvectors = eigenvectors[:, idx][:, :n_pcs]

pcs = centered @ eigenvectors

ancestry_assignments = []
try:
    ref_pcs = np.loadtxt(ref_pca_file, skiprows=1)
    for i in range(len(sample_names)):
        sample_pc = pcs[i]
        distances = np.sqrt(np.sum((ref_pcs[:, :n_pcs] - sample_pc)**2, axis=1))
        nearest = np.argmin(distances)
        ancestry_assignments.append("Cluster_" + str(nearest))
except FileNotFoundError:
    ancestry_assignments = ["Unknown"] * len(sample_names)

with open(output_file, "w") as f:
    f.write("sample\tPC1\tPC2\tPC3\tancestry_assignment\n")
    for i, s in enumerate(sample_names):
        f.write(s + "\t" + str(round(pcs[i,0], 4)) + "\t" + str(round(pcs[i,1], 4)) + "\t" + str(round(pcs[i,2], 4)) + "\t" + ancestry_assignments[i] + "\n")

print("\n✅ 祖源推断完成: " + str(len(sample_names)) + " 样本")
print("📄 结果: " + output_file)
