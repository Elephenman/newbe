#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""论文图表标题批量提取+编号校验"""
import os, sys, re

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def extract_captions(filepath, check_numbering=True, output_file=None):
    """从文本/Markdown/LaTeX文件中提取图表标题并校验编号连续性"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 匹配Figure/Table标题的多种格式
    # LaTeX: \caption{...}, \begin{figure}... 或 Figure N: / Table N:
    # Markdown: **Figure N:** 或 **Table N:**
    patterns = [
        # LaTeX
        r'\\caption\{([^}]+)\}',
        r'\\caption\[(.*?)\]\{([^}]+)\}',
        # Markdown/plain text
        r'(?:\*\*)?[Ff]igur[e]?\s*(\d+)(?:\.\d+)?[:\.\s]*((?:\*\*)?.*?)(?:\n|$)',
        r'(?:\*\*)?[Tt]abl[e]?\s*(\d+)(?:\.\d+)?[:\.\s]*((?:\*\*)?.*?)(?:\n|$)',
        # Numbered format
        r'^[Ff]ig\.?\s*(\d+)[.:]\s*(.+)$',
        r'^[Tt]ab\.?\s*(\d+)[.:]\s*(.+)$',
    ]

    figures = []  # (type, number, caption, line_number)
    lines = content.split('\n')

    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped:
            continue

        # Figure captions
        fig_match = re.match(r'(?:\*\*)?[Ff]igur[e]?\s*(\d+)(?:\.\d+)?[:\.\s–-]*\s*(.*)', line_stripped)
        if fig_match:
            num = int(fig_match.group(1))
            caption = fig_match.group(2).strip().rstrip('*').strip()
            figures.append(("Figure", num, caption, i + 1))
            continue

        # Table captions
        tab_match = re.match(r'(?:\*\*)?[Tt]abl[e]?\s*(\d+)(?:\.\d+)?[:\.\s–-]*\s*(.*)', line_stripped)
        if tab_match:
            num = int(tab_match.group(1))
            caption = tab_match.group(2).strip().rstrip('*').strip()
            figures.append(("Table", num, caption, i + 1))
            continue

        # LaTeX
        latex_match = re.search(r'\\caption\{([^}]+)\}', line_stripped)
        if latex_match:
            caption = latex_match.group(1).strip()
            # Try to determine type from context
            ftype = "Figure"  # default
            for prev_line in lines[max(0, i-5):i]:
                if re.search(r'\\begin\{table', prev_line):
                    ftype = "Table"
                    break
                if re.search(r'\\begin\{figure', prev_line):
                    ftype = "Figure"
                    break
            num_match = re.search(r'\\label\{(?:fig|tab|table|figure):?(\d+)', line_stripped)
            num = int(num_match.group(1)) if num_match else len(figures) + 1
            figures.append((ftype, num, caption, i + 1))

    # 编号校验
    fig_nums = sorted([f[1] for f in figures if f[0] == "Figure"])
    tab_nums = sorted([t[1] for t in figures if t[0] == "Table"])

    fig_issues = []
    tab_issues = []

    if check_numbering:
        # Check for gaps or duplicates
        if fig_nums:
            for n in range(1, max(fig_nums) + 1):
                if n not in fig_nums:
                    fig_issues.append(f"Figure {n} missing (gap in numbering)")
            for n in fig_nums:
                if fig_nums.count(n) > 1:
                    fig_issues.append(f"Figure {n} appears {fig_nums.count(n)} times (duplicate)")
        if tab_nums:
            for n in range(1, max(tab_nums) + 1):
                if n not in tab_nums:
                    tab_issues.append(f"Table {n} missing (gap in numbering)")
            for n in tab_nums:
                if tab_nums.count(n) > 1:
                    tab_issues.append(f"Table {n} appears {tab_nums.count(n)} times (duplicate)")

    # 输出
    out_path = output_file or os.path.splitext(filepath)[0] + "_captions.txt"
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write(f"# Caption extraction from {filepath}\n")
        out.write(f"# Total: {len(figures)} captions ({len(fig_nums)} Figures, {len(tab_nums)} Tables)\n\n")

        for ftype, num, caption, line_no in sorted(figures, key=lambda x: (x[0], x[1])):
            out.write(f"{ftype} {num} (line {line_no}): {caption}\n")

        if fig_issues:
            out.write(f"\n## Figure Numbering Issues\n")
            for issue in fig_issues:
                out.write(f"  WARNING: {issue}\n")
        if tab_issues:
            out.write(f"\n## Table Numbering Issues\n")
            for issue in tab_issues:
                out.write(f"  WARNING: {issue}\n")

    print(f"Caption extraction: {len(figures)} captions found")
    print(f"  Figures: {len(fig_nums)}, Tables: {len(tab_nums)}")
    if fig_issues:
        print(f"  Figure issues: {len(fig_issues)}")
        for i in fig_issues[:5]:
            print(f"    - {i}")
    if tab_issues:
        print(f"  Table issues: {len(tab_issues)}")
        for i in tab_issues[:5]:
            print(f"    - {i}")
    print(f"  Output: {out_path}")

def main():
    print("=" * 60)
    print("  论文图表标题批量提取+编号校验")
    print("=" * 60)
    input_file = get_input("输入文件路径(Markdown/LaTeX/TXT)", "manuscript.md")
    check = get_input("校验编号连续性(yes/no)", "yes")
    output = get_input("输出文件路径", "")
    extract_captions(input_file, check.lower() in ('yes', 'y'), output or None)

if __name__ == "__main__":
    main()
