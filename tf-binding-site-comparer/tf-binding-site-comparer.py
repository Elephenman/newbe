#!/usr/bin/env python3
"""比较两个条件下的TF结合位点差异"""

import os
import sys


def get_input(prompt, default="", dtype=str):
    val = input(prompt + (" [" + str(default) + "]" if default else "") + ": ")
    if not val.strip():
        return default
    try:
        return dtype(val)
    except (ValueError, TypeError):
        return default


def parse_bed(path):
    """解析BED格式peak文件"""
    peaks = set()
    peak_list = []
    with open(path) as f:
        for line in f:
            if line.startswith("#") or line.startswith("track") or line.startswith("browser"):
                continue
            p = line.strip().split("\t")
            if len(p) >= 3:
                try:
                    chrom, start, end = p[0], int(p[1]), int(p[2])
                    peaks.add((chrom, start, end))
                    peak_list.append((chrom, start, end))
                except ValueError:
                    continue
    return peaks, peak_list


def main():
    print("=" * 60)
    print("  TF结合位点差异比较")
    print("=" * 60)
    print()

    peak_file1 = get_input("条件1 peak文件BED路径", "cond1_peaks.bed")
    peak_file2 = get_input("条件2 peak文件BED路径", "cond2_peaks.bed")
    output_file = get_input("输出差异peak路径", "diff_peaks.tsv")
    overlap_mode = get_input("重叠模式(exact/reciprocal)", "reciprocal")

    print()
    print(f"条件1:    {peak_file1}")
    print(f"条件2:    {peak_file2}")
    print(f"输出:     {output_file}")
    print(f"模式:     {overlap_mode}")
    print()

    if not os.path.exists(peak_file1):
        print(f"[ERROR] 条件1文件不存在: {peak_file1}")
        sys.exit(1)
    if not os.path.exists(peak_file2):
        print(f"[ERROR] 条件2文件不存在: {peak_file2}")
        sys.exit(1)

    s1, l1 = parse_bed(peak_file1)
    s2, l2 = parse_bed(peak_file2)

    if not s1:
        print(f"[ERROR] 条件1无有效peak")
        sys.exit(1)
    if not s2:
        print(f"[ERROR] 条件2无有效peak")
        sys.exit(1)

    print(f"[Processing] 条件1: {len(s1)} peaks")
    print(f"[Processing] 条件2: {len(s2)} peaks")

    if overlap_mode == "exact":
        # Exact coordinate match
        only1 = s1 - s2
        only2 = s2 - s1
        shared = s1 & s2
    else:
        # Reciprocal overlap: peaks overlap if they share any region
        # For large peak sets, use interval-based approach
        shared = set()
        only1 = set()
        only2 = set()

        # Simple reciprocal overlap check
        for p1 in s1:
            found = False
            for p2 in s2:
                if p1[0] == p2[0]:  # same chromosome
                    overlap_start = max(p1[1], p2[1])
                    overlap_end = min(p1[2], p2[2])
                    if overlap_start < overlap_end:
                        # Check reciprocal overlap
                        overlap_len = overlap_end - overlap_start
                        len1 = p1[2] - p1[1]
                        len2 = p2[2] - p2[1]
                        if overlap_len / len1 > 0.5 and overlap_len / len2 > 0.5:
                            found = True
                            break
            if found:
                shared.add(p1)
            else:
                only1.add(p1)

        for p2 in s2:
            found = False
            for p1 in s1:
                if p1[0] == p2[0]:
                    overlap_start = max(p1[1], p2[1])
                    overlap_end = min(p1[2], p2[2])
                    if overlap_start < overlap_end:
                        overlap_len = overlap_end - overlap_start
                        len1 = p1[2] - p1[1]
                        len2 = p2[2] - p2[1]
                        if overlap_len / len1 > 0.5 and overlap_len / len2 > 0.5:
                            found = True
                            break
            if not found:
                only2.add(p2)

    # Write output
    try:
        with open(output_file, "w") as out:
            out.write("Category\tChrom\tStart\tEnd\n")
            for p in sorted(only1):
                out.write(f"Cond1_only\t{p[0]}\t{p[1]}\t{p[2]}\n")
            for p in sorted(only2):
                out.write(f"Cond2_only\t{p[0]}\t{p[1]}\t{p[2]}\n")
            for p in sorted(shared):
                out.write(f"Shared\t{p[0]}\t{p[1]}\t{p[2]}\n")
    except Exception as e:
        print(f"[ERROR] 写入失败: {e}")
        sys.exit(1)

    # Summary
    total1 = len(s1)
    total2 = len(s2)
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  条件1 peaks:     {total1}")
    print(f"  条件2 peaks:     {total2}")
    print(f"  条件1特异:       {len(only1)} ({len(only1)/total1*100:.1f}% of cond1)")
    print(f"  条件2特异:       {len(only2)} ({len(only2)/total2*100:.1f}% of cond2)")
    print(f"  共享peaks:       {len(shared)}")
    print(f"  Jaccard index:   {len(shared)/len(s1|s2):.4f}")
    print(f"  输出:            {output_file}")
    print("=" * 60)
    print()
    print("[Done] tf-binding-site-comparer completed successfully!")


if __name__ == "__main__":
    main()
