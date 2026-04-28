#!/usr/bin/env python3
"""从STAR SJ.out.tab统计剪接junction并注释已知/新颖"""

def main():
    input_file = input("STAR SJ.out.tab路径 [SJ.out.tab]: ") or "SJ.out.tab"
    output_file = input("输出统计路径 [junction_counts.tsv]: ") or "junction_counts.tsv"
    min_count = input("最低junction read数 [5]: ") or "5"
    min_cnt = int(min_count); juncs = []
    with open(input_file) as f:
        for line in f:
            p = line.strip().split("\t")
            if len(p) < 7: continue
            strand = ["-", "+", "."][int(p[3])] if p[3].isdigit() else p[3]
            ann = "Known" if p[5] != "0" else "Novel"
            cnt = int(p[6])
            if cnt >= min_cnt: juncs.append([p[0],p[1],p[2],strand,p[4],ann,cnt])
    juncs.sort(key=lambda x: x[6], reverse=True)
    with open(output_file, "w") as out:
        out.write("Chrom\tStart\tEnd\tStrand\tMotif\tType\tCount\n")
        for r in juncs: out.write("\t".join(str(x) for x in r)+"\n")
    known = sum(1 for j in juncs if j[5] == "Known")
    print(f"Junction: {len(juncs)} ({known} known, {len(juncs)-known} novel)")


if __name__ == "__main__":
    main()
