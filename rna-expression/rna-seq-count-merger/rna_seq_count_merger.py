#!/usr/bin/env python3
"""RNA-seq count矩阵合并+一致性检查
读取多个样本的count文件，合并为矩阵，检查基因一致性
"""

import os
import sys
import glob


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    try:
        return dtype(val)
    except (ValueError, TypeError):
        return default


def read_count_file(filepath):
    """读取单个count文件，返回基因->计数字典"""
    counts = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('__'):
                continue
            parts = line.split('\t') if '\t' in line else line.split(',')
            if len(parts) >= 2:
                gene_id = parts[0].strip()
                try:
                    count = float(parts[1].strip())
                    counts[gene_id] = count
                except ValueError:
                    continue
    return counts


def main():
    print("=" * 60)
    print("  多样本count矩阵合并+一致性检查")
    print("=" * 60)
    print()

    input_dir = get_input("Count文件目录", "counts/")
    file_pattern = get_input("文件匹配模式(如 *.txt)", "*.txt")
    output_file = get_input("合并矩阵输出路径", "merged_counts.csv")
    fill_missing = get_input("缺失基因填充值", "0")

    print()
    print(f"目录:    {input_dir}")
    print(f"模式:    {file_pattern}")
    print(f"输出:    {output_file}")
    print()

    if not os.path.isdir(input_dir):
        print(f"[ERROR] 目录不存在: {input_dir}")
        sys.exit(1)

    # Find count files
    pattern = os.path.join(input_dir, file_pattern)
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"[ERROR] 未找到匹配文件: {pattern}")
        sys.exit(1)

    print(f"[Processing] 找到 {len(files)} 个count文件")

    # Read all count files
    all_counts = {}
    sample_names = []
    all_genes = set()

    for fpath in files:
        sample_name = os.path.splitext(os.path.basename(fpath))[0]
        sample_names.append(sample_name)
        counts = read_count_file(fpath)
        all_counts[sample_name] = counts
        all_genes.update(counts.keys())
        print(f"  {sample_name}: {len(counts)} genes")

    all_genes = sorted(all_genes)
    print(f"[Processing] 共 {len(all_genes)} 个唯一基因")

    # Consistency check
    print("[Processing] 一致性检查...")
    missing_report = {}
    for sample, counts in all_counts.items():
        missing = all_genes - set(counts.keys())
        if missing:
            missing_report[sample] = missing
            print(f"  {sample}: 缺少 {len(missing)} 个基因")

    if not missing_report:
        print("  所有样本基因一致")

    # Merge into matrix
    print("[Processing] 合并矩阵...")
    fill_val = float(fill_missing)
    try:
        with open(output_file, 'w') as out:
            # Header
            out.write("Gene," + ",".join(sample_names) + "\n")
            # Data
            for gene in all_genes:
                values = []
                for sample in sample_names:
                    val = all_counts[sample].get(gene, fill_val)
                    values.append(str(int(val) if val == int(val) else val))
                out.write(gene + "," + ",".join(values) + "\n")
    except Exception as e:
        print(f"[ERROR] 写入失败: {e}")
        sys.exit(1)

    # Summary
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  样本数:       {len(sample_names)}")
    print(f"  基因数:       {len(all_genes)}")
    print(f"  基因不一致:   {len(missing_report)} 个样本有缺失基因")
    print(f"  输出文件:     {output_file}")
    print("=" * 60)
    print()
    print("[Done] rna_seq_count_merger completed successfully!")


if __name__ == "__main__":
    main()
