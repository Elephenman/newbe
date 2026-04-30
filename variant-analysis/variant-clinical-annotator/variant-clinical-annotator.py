#!/usr/bin/env python3
"""变异临床注释(ClinVar/COSMIC信息整合)"""

# 变异临床注释
import gzip

print("=" * 60)
print("  🧪 变异临床注释器")
print("=" * 60)

input_vcf = get_input("VCF文件路径", "variants.vcf")
clinvar_file = get_input("ClinVar注释文件路径", "clinvar.tsv")
output_file = get_input("注释结果路径", "clinically_annotated.tsv")
pathogenic_only = get_input("仅保留致病性变异(yes/no)", "no")

# Load ClinVar annotations
clinvar = {}
with open(clinvar_file, 'r') as f:
    header = f.readline()
    for line in f:
        parts = line.strip().split('\t')
        key = f"{parts[0]}_{parts[1]}_{parts[2]}_{parts[3]}"
        clinvar[key] = {
            'significance': parts[4] if len(parts) > 4 else 'NA',
            'disease': parts[5] if len(parts) > 5 else 'NA',
            'review_status': parts[6] if len(parts) > 6 else 'NA',
            'rs_id': parts[7] if len(parts) > 7 else 'NA'
        }

print(f"✅ 加载ClinVar: {len(clinvar)} 条注释")

opener = gzip.open if input_vcf.endswith('.gz') else open
mode = 'rt' if input_vcf.endswith('.gz') else 'r'

annotated = 0
pathogenic = 0
total = 0

with opener(input_vcf, mode) as fin, open(output_file, 'w') as fout:
    fout.write("chrom\tpos\tref\talt\tclinical_significance\tdisease\treview_status\trs_id\n")
    for line in fin:
        if line.startswith('#'):
            continue
        parts = line.strip().split('\t')
        total += 1
        key = f"{parts[0]}_{parts[1]}_{parts[3]}_{parts[4]}"
        
        if key in clinvar:
            annotated += 1
            cv = clinvar[key]
            if pathogenic_only == "yes":
                if 'Pathogenic' in cv['significance'] or 'Likely_pathogenic' in cv['significance']:
                    pathogenic += 1
                    fout.write(f"{parts[0]}\t{parts[1]}\t{parts[3]}\t{parts[4]}\t{cv['significance']}\t{cv['disease']}\t{cv['review_status']}\t{cv['rs_id']}\n")
            else:
                fout.write(f"{parts[0]}\t{parts[1]}\t{parts[3]}\t{parts[4]}\t{cv['significance']}\t{cv['disease']}\t{cv['review_status']}\t{cv['rs_id']}\n")

print(f"\n✅ 注释完成:")
print(f"  总变异: {total}")
print(f"  已注释: {annotated} ({annotated/total*100:.1f}%)")
if pathogenic_only == "yes":
    print(f"  致病性: {pathogenic}")
print(f"📄 结果: {output_file}")
