#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Jupyter notebook指定cell提取+导出"""
import os, sys, json

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def extract_notebook_cells(nb_path, cell_range=None, cell_type=None, output_file=None, output_format="py"):
    """从Jupyter Notebook提取指定cell并导出

    Args:
        nb_path: .ipynb文件路径
        cell_range: 如 "1-5" 或 "3,5,7"
        cell_type: "code", "markdown", or None(所有)
        output_format: "py", "md", "ipynb"
    """
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb.get('cells', [])
    if not cells:
        print("[ERROR] No cells found in notebook")
        return

    # 解析cell范围
    selected_indices = None
    if cell_range:
        selected_indices = set()
        for part in cell_range.split(','):
            if '-' in part:
                start, end = part.split('-')
                selected_indices.update(range(int(start) - 1, int(end)))
            else:
                selected_indices.add(int(part) - 1)

    # 过滤cells
    filtered = []
    for i, cell in enumerate(cells):
        if selected_indices is not None and i not in selected_indices:
            continue
        if cell_type and cell.get('cell_type') != cell_type:
            continue
        filtered.append((i + 1, cell))

    if not filtered:
        print("[ERROR] No cells matched the selection criteria")
        return

    # 导出
    out_path = output_file or os.path.splitext(nb_path)[0] + f"_extracted.{output_format}"

    if output_format == "py":
        with open(out_path, 'w', encoding='utf-8') as f:
            for idx, cell in filtered:
                if cell.get('cell_type') == 'code':
                    source = ''.join(cell.get('source', []))
                    f.write(f"# Cell {idx} [code]\n")
                    f.write(source + '\n\n')
                elif cell.get('cell_type') == 'markdown':
                    source = ''.join(cell.get('source', []))
                    f.write(f"# Cell {idx} [markdown]\n")
                    for line in source.split('\n'):
                        f.write(f"# {line}\n")
                    f.write('\n')

    elif output_format == "md":
        with open(out_path, 'w', encoding='utf-8') as f:
            for idx, cell in filtered:
                if cell.get('cell_type') == 'markdown':
                    source = ''.join(cell.get('source', []))
                    f.write(source + '\n\n')
                elif cell.get('cell_type') == 'code':
                    source = ''.join(cell.get('source', []))
                    f.write(f'```python\n{source}\n```\n\n')

    elif output_format == "ipynb":
        new_nb = {
            "nbformat": nb.get("nbformat", 4),
            "nbformat_minor": nb.get("nbformat_minor", 0),
            "metadata": nb.get("metadata", {}),
            "cells": [cell for _, cell in filtered]
        }
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(new_nb, f, indent=1, ensure_ascii=False)

    print(f"Notebook cell extraction complete")
    print(f"  Notebook: {nb_path}")
    print(f"  Total cells: {len(cells)}")
    print(f"  Extracted: {len(filtered)}")
    if cell_range:
        print(f"  Range: {cell_range}")
    if cell_type:
        print(f"  Type filter: {cell_type}")
    print(f"  Output: {out_path}")

def main():
    print("=" * 60)
    print("  Jupyter notebook指定cell提取+导出")
    print("=" * 60)
    nb_path = get_input("Notebook文件路径(.ipynb)", "notebook.ipynb")
    cell_range = get_input("Cell范围(如1-5或3,5,7，留空=全部)", "")
    cell_type = get_input("Cell类型(code/markdown/空=全部)", "")
    output = get_input("输出文件路径", "")
    fmt = get_input("输出格式(py/md/ipynb)", "py")
    extract_notebook_cells(nb_path, cell_range or None, cell_type or None,
                          output or None, fmt)

if __name__ == "__main__":
    main()
