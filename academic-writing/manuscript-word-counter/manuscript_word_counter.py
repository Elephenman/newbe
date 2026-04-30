#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""论文逐章节字数统计+合规检查"""
import os, sys, re

def get_input(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

# 期刊字数限制参考
JOURNAL_LIMITS = {
    "Nature": {"abstract": 200, "main": 3000, "methods": 1500},
    "Science": {"abstract": 125, "main": 4500, "methods": 2000},
    "Cell": {"abstract": 150, "main": 6000, "methods": 3000},
    "PNAS": {"abstract": 250, "main": 6000, "methods": 2000},
    "custom": {"abstract": 300, "main": 8000, "methods": 3000},
}

def count_manuscript_words(filepath, journal="custom", output_file=None):
    """统计论文字数，按章节分组"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 识别章节
    sections = {}
    current_section = "Title"
    current_text = []

    for line in content.split('\n'):
        # Markdown标题
        header_match = re.match(r'^#{1,3}\s+(.+)', line)
        # LaTeX section
        latex_match = re.match(r'\\(section|subsection|subsubsection)\{([^}]+)\}', line)

        new_section = None
        if header_match:
            new_section = header_match.group(1).strip()
        elif latex_match:
            new_section = latex_match.group(2).strip()

        if new_section:
            if current_text:
                sections[current_section] = '\n'.join(current_text)
            current_section = new_section
            current_text = []
        else:
            current_text.append(line)

    if current_text:
        sections[current_section] = '\n'.join(current_text)

    # 统计各章节字数
    results = {}
    total_words = 0

    for section, text in sections.items():
        # 去除引用、代码块等
        clean_text = re.sub(r'\[[\d,]+\]', '', text)  # 去引用编号
        clean_text = re.sub(r'```.*?```', '', clean_text, flags=re.DOTALL)  # 去代码块
        clean_text = re.sub(r'[#*`\[\]()]', ' ', clean_text)  # 去Markdown标记

        words = [w for w in clean_text.split() if w.strip()]
        word_count = len(words)
        results[section] = word_count
        total_words += word_count

    # 分类统计
    section_map = {"abstract": 0, "main": 0, "methods": 0, "other": 0}
    for section, count in results.items():
        sec_lower = section.lower()
        if 'abstract' in sec_lower:
            section_map["abstract"] += count
        elif 'method' in sec_lower or 'material' in sec_lower:
            section_map["methods"] += count
        elif any(kw in sec_lower for kw in ['introduction', 'result', 'discussion', 'conclusion']):
            section_map["main"] += count
        else:
            section_map["other"] += count

    # 检查合规性
    limits = JOURNAL_LIMITS.get(journal, JOURNAL_LIMITS["custom"])
    warnings = []
    for category, limit in limits.items():
        if section_map.get(category, 0) > limit:
            warnings.append(f"{category}: {section_map[category]} words (limit: {limit})")

    # 输出
    out_path = output_file or os.path.splitext(filepath)[0] + "_wordcount.tsv"
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write("Section\tWordCount\n")
        for section, count in results.items():
            out.write(f"{section}\t{count}\n")
        out.write(f"\n# Category summary\n")
        for cat, count in section_map.items():
            limit = limits.get(cat, "N/A")
            out.write(f"{cat}\t{count}\t(limit: {limit})\n")
        out.write(f"\nTotal\t{total_words}\n")
        if warnings:
            out.write(f"\n# Warnings\n")
            for w in warnings:
                out.write(f"OVER LIMIT: {w}\n")

    print(f"Manuscript word count complete")
    print(f"  Total words: {total_words}")
    for section, count in results.items():
        print(f"    {section}: {count}")
    print(f"  Journal: {journal}")
    for cat, count in section_map.items():
        limit = limits.get(cat, "N/A")
        status = "OVER" if isinstance(limit, int) and count > limit else "OK"
        print(f"    {cat}: {count} (limit: {limit}) [{status}]")
    if warnings:
        print(f"  Warnings: {len(warnings)} sections over limit")
    print(f"  Output: {out_path}")

def main():
    print("=" * 60)
    print("  论文逐章节字数统计+合规检查")
    print("=" * 60)
    input_file = get_input("论文文件路径(Markdown/LaTeX/TXT)", "manuscript.md")
    journal = get_input("目标期刊(Nature/Science/Cell/PNAS/custom)", "custom")
    output = get_input("输出文件路径", "")
    count_manuscript_words(input_file, journal, output or None)

if __name__ == "__main__":
    main()
