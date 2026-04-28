#!/usr/bin/env python3
"""比较两个条件下的TF结合位点差异"""

def main():
    peak_file1 = input("条件1 peak文件BED路径 [cond1_peaks.bed]: ") or "cond1_peaks.bed"
    peak_file2 = input("条件2 peak文件BED路径 [cond2_peaks.bed]: ") or "cond2_peaks.bed"
    output_file = input("输出差异peak路径 [diff_peaks.tsv]: ") or "diff_peaks.tsv"
    def parse_bed(path):
        peaks = set()
        with open(path) as f:
            for line in f:
                if line.startswith("#") or line.startswith("track"): continue
                p = line.strip().split("\t")
                if len(p) >= 3: peaks.add((p[0], int(p[1]), int(p[2])))
        return peaks
    s1, s2 = parse_bed(peak_file1), parse_bed(peak_file2)
    only1, only2, shared = s1-s2, s2-s1, s1&s2
    with open(output_file, "w") as out:
        out.write("Category\tChrom\tStart\tEnd\n")
        for p in only1: out.write(f"Cond1_only\t{p[0]}\t{p[1]}\t{p[2]}\n")
        for p in only2: out.write(f"Cond2_only\t{p[0]}\t{p[1]}\t{p[2]}\n")
        for p in shared: out.write(f"Shared\t{p[0]}\t{p[1]}\t{p[2]}\n")
    print(f"TF比较: {len(only1)} only1, {len(only2)} only2, {len(shared)} shared")


if __name__ == "__main__":
    main()
