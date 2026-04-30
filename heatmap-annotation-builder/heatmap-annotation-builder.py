#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""热图行列注释文件构建器"""
import os, sys, csv
from collections import defaultdict

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def build_heatmap_annotation(sample_file, output_file=None, color_scheme="set1"):
    """从样本信息CSV构建热图注释文件，支持R pheatmap/ComplexHeatmap格式

    输入CSV格式: sample_id,group,batch,condition,... (任意列)
    """
    out_path = output_file or "heatmap_annotation.tsv"

    # 读取样本信息
    samples = []
    with open(sample_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        for row in reader:
            samples.append(row)

    if not samples:
        print("[ERROR] No sample data found in input file")
        return

    # Build annotation data frame (sample as row, columns as annotation)
    # Output in TSV format compatible with R pheatmap annotation_row/annotation_col
    with open(out_path, 'w', encoding='utf-8') as out:
        # Header
        out.write("\t".join(columns) + "\n")
        for row in samples:
            values = [str(row.get(col, "")) for col in columns]
            out.write("\t".join(values) + "\n")

    # Generate R color code
    r_code_path = os.path.splitext(out_path)[0] + "_colors.R"
    with open(r_code_path, 'w', encoding='utf-8') as out:
        out.write("# Auto-generated annotation colors for pheatmap/ComplexHeatmap\n")
        out.write(f"# Input: {sample_file}\n\n")
        out.write(f"library(RColorBrewer)\n\n")
        out.write(f"# Read annotation file\n")
        out.write(f"anno <- read.delim('{os.path.basename(out_path)}', row.names=1, sep='\\t')\n\n")

        for col in columns[1:]:  # skip sample_id column
            unique_vals = list(set(str(row.get(col, "")) for row in samples))
            n_vals = len(unique_vals)
            out.write(f"# Colors for {col} ({n_vals} groups)\n")
            if n_vals <= 8:
                out.write(f"anno_colors${col} <- brewer.pal({max(3, n_vals)}, '{color_scheme}')[1:{n_vals}]\n")
                out.write(f"names(anno_colors${col}) <- c({','.join(repr(v) for v in unique_vals)})\n")
            else:
                out.write(f"anno_colors${col} <- rainbow({n_vals})\n")
                out.write(f"names(anno_colors${col}) <- c({','.join(repr(v) for v in unique_vals)})\n")
            out.write("\n")

    n_cols = len(columns)
    n_groups = defaultdict(int)
    for col in columns[1:]:
        n_groups[col] = len(set(str(row.get(col, "")) for row in samples))

    print(f"Heatmap annotation built")
    print(f"  Samples: {len(samples)}")
    print(f"  Annotation columns: {n_cols - 1}")
    for col, ng in n_groups.items():
        print(f"    {col}: {ng} groups")
    print(f"  Color scheme: {color_scheme}")
    print(f"  Annotation TSV: {out_path}")
    print(f"  R color code: {r_code_path}")

def main():
    sample_file = get_input("样本信息CSV路径", "samples.csv")
    output = get_input("输出注释文件路径", "heatmap_anno.tsv")
    color = get_input("配色方案(set1/set2/dark2/Paired)", "set1")
    build_heatmap_annotation(sample_file, output, color)

if __name__ == "__main__":
    main()
