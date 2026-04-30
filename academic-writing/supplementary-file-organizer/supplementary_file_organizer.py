#!/usr/bin/env python3
"""附件材料整理+编号重排+目录生成
扫描论文附图/附表目录，自动重编号并生成目录文件
"""

import os
import sys
import re
import shutil


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    try:
        return dtype(val)
    except (ValueError, TypeError):
        return default


def main():
    print("=" * 60)
    print("  附件材料整理+编号重排+目录生成")
    print("=" * 60)
    print()

    input_dir = get_input("附件目录路径", "supplementary/")
    output_dir = get_input("整理后输出目录", "supplementary_organized/")
    prefix = get_input("文件名前缀(如 SupplementaryFigure)", "SupplementaryFigure")
    start_num = get_input("起始编号", "1", int)
    generate_catalog = get_input("生成目录文件(yes/no)", "yes")
    copy_mode = get_input("复制/移动(copy/move)", "copy")

    print()
    print(f"输入目录:  {input_dir}")
    print(f"输出目录:  {output_dir}")
    print(f"前缀:      {prefix}")
    print()

    if not os.path.isdir(input_dir):
        print(f"[ERROR] 目录不存在: {input_dir}")
        sys.exit(1)

    # Scan for supplementary files
    supp_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.tif',
                       '.svg', '.eps', '.csv', '.tsv', '.xlsx', '.docx'}

    files = []
    for fname in sorted(os.listdir(input_dir)):
        fpath = os.path.join(input_dir, fname)
        if os.path.isfile(fpath):
            ext = os.path.splitext(fname)[1].lower()
            if ext in supp_extensions:
                files.append({
                    'original_name': fname,
                    'original_path': fpath,
                    'ext': ext,
                    'size': os.path.getsize(fpath)
                })

    if not files:
        print("[ERROR] 未找到附件文件")
        sys.exit(1)

    print(f"[Processing] 找到 {len(files)} 个附件文件")

    # Organize and rename
    os.makedirs(output_dir, exist_ok=True)
    catalog_entries = []

    for i, f in enumerate(files):
        new_num = start_num + i
        new_name = f"{prefix}{new_num}{f['ext']}"
        new_path = os.path.join(output_dir, new_name)

        if copy_mode == 'move':
            shutil.move(f['original_path'], new_path)
        else:
            shutil.copy2(f['original_path'], new_path)

        catalog_entries.append({
            'number': new_num,
            'original_name': f['original_name'],
            'new_name': new_name,
            'size': f['size'],
            'type': 'Figure' if f['ext'] in ('.png', '.jpg', '.pdf', '.svg', '.tiff', '.eps') else 'Table'
        })
        print(f"  {f['original_name']} -> {new_name}")

    # Generate catalog
    if generate_catalog.lower() in ('yes', 'y'):
        catalog_path = os.path.join(output_dir, "catalog.md")
        with open(catalog_path, 'w', encoding='utf-8') as cat:
            cat.write("# Supplementary Materials Catalog\n\n")
            cat.write("| # | Type | New Name | Original Name | Size |\n")
            cat.write("|---|------|----------|---------------|------|\n")
            for entry in catalog_entries:
                size_str = f"{entry['size']/1024:.1f} KB" if entry['size'] < 1024*1024 else f"{entry['size']/1024/1024:.1f} MB"
                cat.write(f"| {entry['number']} | {entry['type']} | {entry['new_name']} | {entry['original_name']} | {size_str} |\n")

        # Also generate LaTeX snippet
        latex_path = os.path.join(output_dir, "supplementary_latex.tex")
        with open(latex_path, 'w', encoding='utf-8') as tex:
            for entry in catalog_entries:
                if entry['type'] == 'Figure':
                    tex.write(f"\\begin{{figure}}[htbp]\n")
                    tex.write(f"  \\centering\n")
                    tex.write(f"  \\includegraphics[width=0.8\\textwidth]{{{entry['new_name']}}}\n")
                    tex.write(f"  \\caption{{Supplementary Figure {entry['number']}}}\n")
                    tex.write(f"  \\label{{fig:supp{entry['number']}}}\n")
                    tex.write(f"\\end{{figure}}\n\n")
                else:
                    tex.write(f"% Supplementary Table {entry['number']}: {entry['new_name']}\n\n")

        print(f"  目录文件: {catalog_path}")
        print(f"  LaTeX片段: {latex_path}")

    # Summary
    n_figures = sum(1 for e in catalog_entries if e['type'] == 'Figure')
    n_tables = sum(1 for e in catalog_entries if e['type'] == 'Table')

    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  总文件数:     {len(files)}")
    print(f"  附图:         {n_figures}")
    print(f"  附表:         {n_tables}")
    print(f"  输出目录:     {output_dir}")
    print("=" * 60)
    print()
    print("[Done] supplementary_file_organizer completed successfully!")


if __name__ == "__main__":
    main()
