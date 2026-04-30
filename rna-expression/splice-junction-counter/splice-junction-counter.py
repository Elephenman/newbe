#!/usr/bin/env python3
"""从STAR SJ.out.tab统计剪接junction并注释已知/新颖"""

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


def main():
    print("=" * 60)
    print("  STAR剪接Junction统计")
    print("=" * 60)
    print()

    input_file = get_input("STAR SJ.out.tab路径", "SJ.out.tab")
    output_file = get_input("输出统计路径", "junction_counts.tsv")
    min_count = get_input("最低junction read数", "5", int)

    print()
    print(f"输入:    {input_file}")
    print(f"输出:    {output_file}")
    print(f"最低数:  {min_count}")
    print()

    if not os.path.exists(input_file):
        print(f"[ERROR] 文件不存在: {input_file}")
        sys.exit(1)

    min_cnt = int(min_count)
    juncs = []
    total_juncs = 0

    with open(input_file) as f:
        for line in f:
            total_juncs += 1
            p = line.strip().split("\t")
            if len(p) < 7:
                continue

            # STAR SJ.out.tab format:
            # chrom  start  end  strand  intron_motif  annotated  unique_reads
            # Strand: 0=unknown, 1=+, 2=-
            strand_map = {"0": ".", "1": "+", "2": "-"}
            strand = strand_map.get(p[3], p[3]) if p[3].isdigit() else p[3]

            # Intron motif: 0=non-canonical, 1=GT/AG, 2=CT/AC, 3=GC/AG, 4=CT/GC, 5=AT/AC, 6=AT-AA
            motif_map = {"0": "NonCanonical", "1": "GT-AG", "2": "CT-AC",
                        "3": "GC-AG", "4": "CT-GC", "5": "AT-AC", "6": "AT-AA"}
            motif = motif_map.get(p[4], p[4]) if p[4].isdigit() else p[4]

            # Annotated: 0=novel, 1=known (or sum of known annotations)
            ann = "Known" if p[5] != "0" else "Novel"

            # Read count: column 6 (unique) + column 7 (multi) if present
            try:
                cnt_unique = int(p[6])
            except ValueError:
                cnt_unique = 0

            try:
                cnt_multi = int(p[7]) if len(p) > 7 else 0
            except (ValueError, IndexError):
                cnt_multi = 0

            cnt_total = cnt_unique + cnt_multi

            if cnt_total >= min_cnt:
                juncs.append([p[0], p[1], p[2], strand, motif, ann, cnt_total,
                              cnt_unique, cnt_multi])

    # Sort by count
    juncs.sort(key=lambda x: x[6], reverse=True)

    # Write output
    try:
        with open(output_file, "w") as out:
            out.write("Chrom\tStart\tEnd\tStrand\tMotif\tType\tTotalCount\tUniqueCount\tMultiCount\n")
            for r in juncs:
                out.write("\t".join(str(x) for x in r) + "\n")
    except Exception as e:
        print(f"[ERROR] 写入失败: {e}")
        sys.exit(1)

    # Statistics
    known = sum(1 for j in juncs if j[5] == "Known")
    novel = sum(1 for j in juncs if j[5] == "Novel")
    canonical = sum(1 for j in juncs if j[4] in ("GT-AG", "CT-AC"))

    # Motif distribution
    motif_counts = {}
    for j in juncs:
        m = j[4]
        motif_counts[m] = motif_counts.get(m, 0) + 1

    # Summary
    print()
    print("=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    print(f"  总junction行:  {total_juncs}")
    print(f"  过滤后:        {len(juncs)} (count >= {min_cnt})")
    print(f"  Known:         {known}")
    print(f"  Novel:         {novel}")
    print(f"  Canonical:     {canonical}")
    print(f"  Motif分布:")
    for m, c in sorted(motif_counts.items(), key=lambda x: -x[1]):
        print(f"    {m}: {c}")
    print(f"  输出:          {output_file}")
    print("=" * 60)
    print()
    print("[Done] splice-junction-counter completed successfully!")


if __name__ == "__main__":
    main()
