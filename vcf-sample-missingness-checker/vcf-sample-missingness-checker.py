#!/usr/bin/env python3
"""VCF样本缺失率检查+过滤"""

# VCF样本缺失率检查
import gzip

print("=" * 60)
print("  🧪 VCF样本缺失率检查器")
print("=" * 60)

input_vcf = get_input("VCF文件路径", "variants.vcf")
max_missing = float(get_input("最大缺失率阈值", "0.1"))
output_file = get_input("过滤结果路径", "filtered_variants.vcf")
report_file = get_input("缺失率报告路径", "missingness_report.txt")

opener = gzip.open if input_vcf.endswith('.gz') else open
mode = 'rt' if input_vcf.endswith('.gz') else 'r'

sample_names = []
header_lines = []
total_variants = 0
kept = 0

with opener(input_vcf, mode) as fin, open(output_file, 'w') as fout:
    for line in fin:
        if line.startswith('##'):
            fout.write(line)
            header_lines.append(line)
        elif line.startswith('#CHROM'):
            parts = line.strip().split('\t')
            sample_names = parts[9:]
            fout.write(line)
        else:
            total_variants += 1
            parts = line.strip().split('\t')
            genotypes = parts[9:]
            missing_count = sum(1 for gt in genotypes if gt.startswith('.') or gt == '.')
            missing_rate = missing_count / len(genotypes) if genotypes else 0
            
            if missing_rate <= max_missing:
                fout.write(line)
                kept += 1

print(f"\n✅ 检查完成:")
print(f"  总变异: {total_variants}")
print(f"  保留变异: {kept} ({kept/total_variants*100:.1f}%)")
print(f"  过滤变异: {total_variants-kept}")
print(f"  缺失率阈值: {max_missing}")

with open(report_file, 'w') as f:
    f.write(f"VCF Missingness Report\n")
    f.write(f"Total variants: {total_variants}\n")
    f.write(f"Kept variants: {kept}\n")
    f.write(f"Missing rate threshold: {max_missing}\n")
    f.write(f"Samples: {len(sample_names)}\n")
print(f"📄 报告: {report_file}")
